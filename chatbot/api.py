import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Import your existing ML and Chatbot modules
from chatbot.model_inference import predict_cost_overrun, predict_delay_days
from chatbot.risk import compute_cost_risk_tier, compute_time_risk_tier, compute_risk_tier
from chatbot.chatbot import answer_query
from chatbot.config import COST_OVERRUN_PRED_COL, DELAY_PRED_COL
import chatbot.predictions_summary as summary_api
from chatbot.questionnaire_mitigation import generate_mitigation_strategies


app = FastAPI(title="PAIMANA MVP Backend")

# Allow Spring Boot (and anything else) to call this service
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- No in-memory storage here anymore. ---
# Spring Boot + MySQL is the single source of truth for sessions,
# submitted projects, and chat history. This service is stateless:
# every request must carry whatever context it needs (project data,
# chat history), and every response hands back whatever needs saving.


# --- PYDANTIC MODELS (Data Validation) ---
class ProjectForm(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    project_name: str
    agency: str
    state: str
    ministry: str
    sector: str
    status: str
    original_cost_cr: float
    cumulative_expenditure: float
    physical_progress: float
    date_of_approval: str
    start_date: str
    target_doc: str


class ChatRequest(BaseModel):
    message: str
    # The full project_data dict Spring Boot got back from /api/predict
    # and stored against this session. Omit/null for general/database
    # questions not tied to a specific submitted project.
    user_project: Optional[Dict[str, Any]] = None
    # Prior turns for this session, oldest first. Each item:
    # {"role": "user" | "model", "text": "..."}
    # NOTE: role must be "user" or "model" (Gemini's naming), not "assistant".
    history: Optional[List[Dict[str, str]]] = None


class QuestionnaireRequest(BaseModel):
    session_id: str
    project_name: str
    land_acquisition: str
    financial_result: str
    approval_clearance: str
    procurement_result: str
    scope_design: str
    execution_pace: str
    interagency_coordination: str
    created_at: Optional[str] = None


# --- ENDPOINTS ---

@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/predict")
def predict_project(form: ProjectForm):
    """Takes form data, runs ML models, calculates risk, and returns
    everything as JSON. Does NOT store anything -- Spring Boot is
    responsible for saving the returned `project_data` object (e.g. as a
    JSON column) against a session_id it creates, and sending that same
    object back unchanged as `user_project` on later /api/chat calls."""

    project_data = form.model_dump()

    # ML Models expect specific column names
    project_data["cumulative expenditure in rs. crore"] = project_data.pop("cumulative_expenditure")
    project_data["physical progress (in percentage)"] = project_data.pop("physical_progress")

    original_cost = project_data["original_cost_cr"]
    cumulative = project_data["cumulative expenditure in rs. crore"]
    progress = project_data["physical progress (in percentage)"]

    # New project from a form -> hasn't been revised yet, so assume
    # revised cost equals original cost.
    project_data["revised_cost_cr"] = original_cost
    project_data["cost_overrun_pct"] = 0.0
    

    if original_cost > 0:
        ratio = cumulative / original_cost
    else:
        ratio = 0

    project_data["expenditure_to_original_cost_ratio"] = ratio
    project_data["expenditure_progress_mismatch"] = ratio - (progress / 100.0)
    project_data["high_spend_low_progress_flag"] = 1 if (ratio > 0.80 and progress < 50) else 0
    project_data["negative_expenditure_flag"] = 1 if cumulative < 0 else 0

    project_data["expenditure_to_revised_cost_ratio"] = ratio
    project_data["expenditure_exceeds_revised_cost"] = 1 if cumulative > original_cost else 0
    project_data["negative_cost_overrun_flag"] = 0

    project_data["actual_doc_is_missing"] = 1
    project_data["revised_doc_is_missing"] = 1
    project_data["revised_cost_cr_is_missing"] = 1
    project_data["ministry_is_missing"] = 0 if project_data["ministry"] else 1
    project_data["date_of_approval_is_missing"] = 0
    project_data["start_date_is_missing"] = 0
    project_data["target_doc_is_missing"] = 0
    project_data["project_code"] = "NEW-USER-PROJECT"

    try:
        df = pd.DataFrame([project_data])
        predicted_cost = predict_cost_overrun(df)[0]
        predicted_delay = predict_delay_days(df)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

    project_data[COST_OVERRUN_PRED_COL] = float(predicted_cost)
    project_data[DELAY_PRED_COL] = float(predicted_delay)

    row = pd.Series(project_data)
    cost_tier = compute_cost_risk_tier(row)
    time_tier = compute_time_risk_tier(row)
    overall_tier = compute_risk_tier(row)

    project_data["_cost_risk_tier"] = cost_tier
    project_data["_time_risk_tier"] = time_tier
    project_data["_risk_tier"] = overall_tier

    return {
        "predictions": {
            "predicted_overrun_pct": round(float(predicted_cost), 2),
            "predicted_delay_days": round(float(predicted_delay), 2),
            "cost_risk_tier": cost_tier,
            "time_risk_tier": time_tier,
            "overall_risk_tier": overall_tier,
        },
        # Save this whole object as-is (e.g. as a JSON/TEXT column keyed by
        # your session_id) and send it back unchanged as `user_project` on
        # every later /api/chat call for this session.
        "project_data": project_data,
    }


@app.post("/api/chat")
def chat(req: ChatRequest):
    """Stateless: Spring Boot supplies the saved project (if any) and the
    prior chat history (if any) on every call. This service holds nothing
    between requests -- after getting the answer back, Spring Boot should
    insert both the user's message and this answer into its own
    chat_messages table."""
    try:
        answer = answer_query(
            req.message,
            user_project_row=req.user_project,
            history=req.history or [],
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- DASHBOARD ENDPOINTS (read from the historical CSV dataset directly --
# no session/state, so these need no changes for the new architecture) ---

@app.get("/api/dashboard/risk-summary")
def get_risk_summary():
    return summary_api.get_risk_distribution()


@app.get("/api/dashboard/sector-risk")
def get_sector_risk():
    df_sector = summary_api.get_sector_wise_risk_summary()
    return df_sector.to_dict(orient="records")


@app.get("/api/dashboard/mega-projects")
def get_mega_projects():
    """Return mega-project totals and the top 10 projects by original cost.

    Threshold: original_cost_cr >= 10000 crore.
    This currently reads from the historical CSV and can later be switched
    to MySQL using the same filter logic when the data source changes.
    """
    return summary_api.get_mega_project_summary()


@app.post("/api/project/mitigation")
def project_mitigation(req: QuestionnaireRequest):
    try:
        answers = {
            "land_acquisition": req.land_acquisition,
            "financial_result": req.financial_result,
            "approval_clearance": req.approval_clearance,
            "procurement_result": req.procurement_result,
            "scope_design": req.scope_design,
            "execution_pace": req.execution_pace,
            "interagency_coordination": req.interagency_coordination,
        }

        result = generate_mitigation_strategies(answers)

        return {
            "session_id": req.session_id,
            "project_name": req.project_name,
            "created_at": req.created_at,
            "mitigation_stratergies": result["strategies"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Mitigation generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)