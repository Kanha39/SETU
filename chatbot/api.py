import uuid
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Import your existing ML and Chatbot modules
from chatbot.model_inference import predict_cost_overrun, predict_delay_days
from chatbot.risk import compute_cost_risk_tier, compute_time_risk_tier, compute_risk_tier
from chatbot.chatbot import answer_query
from chatbot.config import COST_OVERRUN_PRED_COL, DELAY_PRED_COL
import chatbot.predictions_summary as summary_api

app = FastAPI(title="PAIMANA MVP Backend")

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
    session_id: str
    message: str

# --- ENDPOINTS ---

@app.post("/api/predict")
def predict_project(form: ProjectForm):
    """Takes form data, runs ML models, calculates risk, returns session_id."""
    
    # 1. Convert form data into dictionary (using model_dump to fix the warning)
    project_data = form.model_dump()
    
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
    
    # NEW: Add the 3 missing columns the model is crashing over!
    project_data["expenditure_to_revised_cost_ratio"] = ratio  # Same as original since revised==original
    project_data["expenditure_exceeds_revised_cost"] = 1 if cumulative > original_cost else 0
    project_data["negative_cost_overrun_flag"] = 0
    
    # Add structural missingness flags expected by model
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
    predicted_cost = predict_cost_overrun(df)[0]
    predicted_delay = predict_delay_days(df)[0]

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