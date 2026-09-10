import json
import uuid
import urllib.request
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from typing import Optional

# Import your existing ML and Chatbot modules
from chatbot.model_inference import predict_cost_overrun, predict_delay_days
from chatbot.risk import compute_cost_risk_tier, compute_time_risk_tier, compute_risk_tier
from chatbot.chatbot import answer_query
from chatbot.config import COST_OVERRUN_PRED_COL, DELAY_PRED_COL
import chatbot.predictions_summary as summary_api

app = FastAPI(title="PAIMANA MVP Backend")

TELEGRAM_BOT_TOKEN = "8891945925:AAEw7HUakcT3cCnOlCwzls8qtW1Bbmhued8"
TELEGRAM_CHAT_ID = "8951589926"

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- IN-MEMORY DATABASE FOR MVP ---
user_projects_db = {}  # session_id -> dict of project data + predictions
chat_history_db = {}   # session_id -> list of {"role": ..., "text": ...}

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
    target_date_of_completion: Optional[str] = None
    target_doc: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str
    message: str

# --- ENDPOINTS ---


def _fallback_project_predictions(project_data: dict):
    original_cost = float(project_data.get("original_cost_cr", 0) or 0)
    cumulative = float(project_data.get("cumulative expenditure in rs. crore", project_data.get("cumulative_expenditure", 0)) or 0)
    progress = float(project_data.get("physical progress (in percentage)", project_data.get("physical_progress", 0)) or 0)

    ratio = cumulative / original_cost if original_cost > 0 else 0.0
    predicted_cost = max(0.0, (ratio - 0.75) * 100) + max(0.0, (50 - progress) * 0.35)
    predicted_delay = max(0.0, (1 - progress / 100) * 180) + max(0.0, (ratio - 0.80) * 220)
    return round(float(predicted_cost), 2), round(float(predicted_delay), 2)


@app.post("/api/predict")
def predict_project(form: ProjectForm):
    """Takes form data, runs ML models, calculates risk, returns session_id."""
    
    # 1. Convert form data into dictionary (using model_dump to fix the warning)
    project_data = form.model_dump(exclude_none=True)
    project_data["target_doc"] = project_data.get("target_date_of_completion") or project_data.get("target_doc") or ""
    project_data.pop("target_date_of_completion", None)

    # ML Models expect specific column names
    project_data["cumulative expenditure in rs. crore"] = project_data.pop("cumulative_expenditure")
    project_data["physical progress (in percentage)"] = project_data.pop("physical_progress")
    
    original_cost = project_data["original_cost_cr"]
    cumulative = project_data["cumulative expenditure in rs. crore"]
    progress = project_data["physical progress (in percentage)"]

    # Since this is a new project from a form, it hasn't been revised yet.
    # So we assume revised cost is the same as original cost.
    project_data["revised_cost_cr"] = original_cost
    project_data["cost_overrun_pct"] = 0.0

    # Calculate derived ML features
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

    # 2. Run Predictions using your existing model_inference.py
    df = pd.DataFrame([project_data])
    try:
        predicted_cost = float(predict_cost_overrun(df)[0])
        predicted_delay = float(predict_delay_days(df)[0])
    except Exception:
        predicted_cost, predicted_delay = _fallback_project_predictions(project_data)

    # Save predictions to the dictionary so risk.py can calculate tiers
    project_data[COST_OVERRUN_PRED_COL] = predicted_cost
    project_data[DELAY_PRED_COL] = predicted_delay

    # 3. Calculate Risk Tiers using your existing risk.py
    row = pd.Series(project_data)
    cost_tier = compute_cost_risk_tier(row)
    time_tier = compute_time_risk_tier(row)
    overall_tier = compute_risk_tier(row)
    
    project_data["_cost_risk_tier"] = cost_tier
    project_data["_time_risk_tier"] = time_tier
    project_data["_risk_tier"] = overall_tier

    # 4. Generate a session ID and save it in memory
    session_id = str(uuid.uuid4())
    user_projects_db[session_id] = project_data
    chat_history_db[session_id] = []

    # 5. Return data to frontend
    return {
        "session_id": session_id,
        "predictions": {
            "predicted_overrun_pct": round(float(predicted_cost), 2),
            "predicted_delay_days": round(float(predicted_delay), 2),
            "cost_risk_tier": cost_tier,
            "time_risk_tier": time_tier,
            "overall_risk_tier": overall_tier
        }
    }


@app.post("/api/chat")
def chat(req: ChatRequest):
    """Handles chat messages, using memory and user's project context."""
    if req.session_id not in chat_history_db:
        raise HTTPException(status_code=404, detail="Session not found")
        
    history = chat_history_db[req.session_id]
    user_project = user_projects_db.get(req.session_id)

    try:
        # Call the updated chatbot function
        answer = answer_query(req.message, user_project_row=user_project, history=history)
        
        # Save to memory
        history.append({"role": "user", "text": req.message})
        history.append({"role": "model", "text": answer})
        
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/telegram/alert")
def send_telegram_alert(payload: dict):
    """Sends a Telegram alert to the configured operational chat ID."""
    project_name = payload.get("project_name") or payload.get("name") or "Unknown Project"
    risk_level = payload.get("risk_level") or payload.get("overall_risk_tier") or "Unknown"
    source = payload.get("source") or "Manual dispatch"
    message = (
        f"🚨 PAIMANA ALERT\n"
        f"Project: {project_name}\n"
        f"Risk: {risk_level}\n"
        f"Source: {source}\n"
        f"Chat ID: {TELEGRAM_CHAT_ID}"
    )

    try:
        data = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
        }).encode("utf-8")

        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=15) as response:
            response_body = response.read().decode("utf-8")
            result = json.loads(response_body)

        if not result.get("ok"):
            raise RuntimeError(result.get("description", "Telegram send failed"))

        return {"success": True, "message": "Telegram alert sent successfully", "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Telegram alert failed: {str(exc)}")


# --- DASHBOARD ENDPOINTS (Wraps predictions_summary.py) ---

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
    # clean NaNs so JSON doesn't crash
    df_top = df_top.fillna("").to_dict(orient="records") 
    return df_top

if __name__ == "__main__":
    import uvicorn
    # Run the app locally for testing
    uvicorn.run(app, host="0.0.0.0", port=8000)