import uuid
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from chatbot.model_inference import predict_cost_overrun, predict_delay_days
from chatbot.risk import compute_cost_risk_tier, compute_time_risk_tier, compute_risk_tier
from chatbot.chatbot import answer_query
from chatbot.config import COST_OVERRUN_PRED_COL, DELAY_PRED_COL
from chatbot.db import save_chat_message, get_chat_history, save_user_project, get_user_project
import chatbot.predictions_summary as summary_api

app = FastAPI(title="PAIMANA MVP Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProjectForm(BaseModel):
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
    user_id: str


class ChatRequest(BaseModel):
    session_id: str
    message: str
    user_id: str
    project_code: Optional[str] = None


@app.post("/api/predict")
def predict_project(form: ProjectForm):
    project_data = form.model_dump()
    user_id = project_data.pop("user_id")

    project_data["cumulative expenditure in rs. crore"] = project_data.pop("cumulative_expenditure")
    project_data["physical progress (in percentage)"] = project_data.pop("physical_progress")

    original_cost = project_data["original_cost_cr"]
    cumulative = project_data["cumulative expenditure in rs. crore"]
    progress = project_data["physical progress (in percentage)"]

    project_data["revised_cost_cr"] = original_cost
    project_data["cost_overrun_pct"] = 0.0

    ratio = cumulative / original_cost if original_cost > 0 else 0
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

    df = pd.DataFrame([project_data])
    predicted_cost = predict_cost_overrun(df)[0]
    predicted_delay = predict_delay_days(df)[0]

    project_data[COST_OVERRUN_PRED_COL] = predicted_cost
    project_data[DELAY_PRED_COL] = predicted_delay

    row = pd.Series(project_data)
    cost_tier = compute_cost_risk_tier(row)
    time_tier = compute_time_risk_tier(row)
    overall_tier = compute_risk_tier(row)

    project_data["_cost_risk_tier"] = cost_tier
    project_data["_time_risk_tier"] = time_tier
    project_data["_risk_tier"] = overall_tier

    session_id = str(uuid.uuid4())

    predictions = {
        "predicted_overrun_pct": round(float(predicted_cost), 2),
        "predicted_delay_days": round(float(predicted_delay), 2),
        "cost_risk_tier": cost_tier,
        "time_risk_tier": time_tier,
        "overall_risk_tier": overall_tier,
    }

    save_user_project(session_id, user_id, project_data, predictions)

    return {"session_id": session_id, "predictions": predictions}


@app.post("/api/chat")
def chat(req: ChatRequest):
    user_project = get_user_project(req.session_id)
    if user_project is None:
        raise HTTPException(status_code=404, detail="Session not found")

    history = get_chat_history(req.session_id)

    try:
        answer = answer_query(req.message, user_project_row=user_project, history=history)
        save_chat_message(
            user_id=req.user_id,
            session_id=req.session_id,
            project_code=req.project_code or user_project.get("project_code"),
            user_message=req.message,
            bot_response=answer,
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/dashboard/risk-summary")
def get_risk_summary():
    return summary_api.get_risk_distribution()


@app.get("/api/dashboard/sector-risk")
def get_sector_risk():
    df_sector = summary_api.get_sector_wise_risk_summary()
    return df_sector.to_dict(orient="records")


@app.get("/api/dashboard/top-risky")
def get_top_risky():
    df_top = summary_api.get_top_risky_projects(10)
    df_top = df_top.fillna("").to_dict(orient="records")
    return df_top


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)