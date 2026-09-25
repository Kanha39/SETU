import os
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
    session_id: Optional[str] = None
    message: Optional[str] = None

class AuthRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

# --- AUTH ENDPOINTS ---
users_db = {
    "admin@paimana.gov.in": {"name": "MoSPI Officer", "email": "admin@paimana.gov.in", "password": "password123", "role": "admin"}
}

@app.post("/api/auth/login")
def auth_login(req: AuthRequest):
    user = users_db.get(req.email)
    if user and user.get("password") == req.password:
        return {
            "token": str(uuid.uuid4()),
            "name": user["name"],
            "email": user["email"],
            "role": user.get("role", "user")
        }
    display_name = req.email.split("@")[0].capitalize()
    return {
        "token": str(uuid.uuid4()),
        "name": display_name,
        "email": req.email,
        "role": "user"
    }

@app.post("/api/auth/register")
def auth_register(req: AuthRequest):
    name = req.name or req.email.split("@")[0].capitalize()
    users_db[req.email] = {
        "name": name,
        "email": req.email,
        "password": req.password,
        "role": "user"
    }
    return {
        "token": str(uuid.uuid4()),
        "name": name,
        "email": req.email,
        "role": "user"
    }

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


def _handle_chat_message(session_id: Optional[str], message: Optional[str]):
    if not message or not message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    normalized_session_id = session_id or str(uuid.uuid4())
    history = chat_history_db.get(normalized_session_id, [])
    user_project = user_projects_db.get(normalized_session_id)

    try:
        answer = answer_query(message.strip(), user_project_row=user_project, history=history)

        if session_id:
            if normalized_session_id not in chat_history_db:
                chat_history_db[normalized_session_id] = []
            history = chat_history_db[normalized_session_id]
            history.append({"role": "user", "text": message.strip()})
            history.append({"role": "model", "text": answer})

        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat")
def chat(req: ChatRequest):
    """Handles chat messages, using memory and user's project context."""
    return _handle_chat_message(session_id=req.session_id, message=req.message)


@app.post("/api/chatbot/query")
def chatbot_query(payload: dict):
    """Frontend-compatible chatbot endpoint used by the React app."""
    session_id = payload.get("session_id") or payload.get("sessionId")
    message = payload.get("question") or payload.get("message") or payload.get("text")
    return _handle_chat_message(session_id=session_id, message=message)


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


# --- QUESTIONNAIRE EVALUATION ENDPOINTS ---

class QuestionnaireSubmit(BaseModel):
    session_id: Optional[str] = None
    project_name: Optional[str] = None
    land_acquisition: str = "No issue"
    financial_result: str = "No issue"
    approval_clearance: str = "No issue"
    procurement_result: str = "No issue"
    scope_design: str = "No change"
    execution_pace: str = "No issue"
    interagency_coordination: str = "No issue"


SEVERITY_MULTIPLIERS = {
    "No issue": 0.0, "No change": 0.0,
    "Minor issue": 0.25, "Minor changes": 0.25,
    "Moderate issue": 0.50, "Moderate changes": 0.50,
    "Major issue": 0.75, "Major changes": 0.75,
    "Critical issue": 1.00, "Severe changes": 1.00,
}

QUESTION_META = [
    {
        "id": "land_acquisition",
        "question": "Q1. Are there delays in land acquisition, site handover, or utility shifting?",
        "weight": 25,
        "why": "This is the strongest operational delay driver seen in infrastructure projects. It aligns with schedule slippage and low progress.",
        "options": ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"],
        "strategies": {
            "Minor issue": "Establish weekly land acquisition milestone tracking with regional district magistrates.",
            "Moderate issue": "Form a dedicated task force with state revenue officials for expedited ROW & utility shifting.",
            "Major issue": "Deploy high-priority escalation to state cabinet secretary and fast-track compensation distribution.",
            "Critical issue": "Implement emergency land acquisition workflow, clear pending litigation clearances, and re-sequence unencumbered work packages immediately."
        }
    },
    {
        "id": "financial_result",
        "question": "Q2. Are funds / budget releases / cash flow delays affecting execution?",
        "weight": 20,
        "why": "The historical dataset strongly supports cost overrun risk when expenditure rises faster than physical progress.",
        "options": ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"],
        "strategies": {
            "Minor issue": "Streamline invoice verification timelines to ensure smooth contractor billing flow.",
            "Moderate issue": "Ring-fence quarterly budget allocations and expedite milestone-based fund dispatches.",
            "Major issue": "Authorize priority letters of credit (LC) and secure supplementary budget sanction from administrative ministry.",
            "Critical issue": "Restructure project payment milestones, initiate direct vendor payments, and apply emergency liquidity support."
        }
    },
    {
        "id": "approval_clearance",
        "question": "Q3. Are approvals, clearances, or administrative decisions pending?",
        "weight": 20,
        "why": "Approval delays often produce schedule revision and target date shifts.",
        "options": ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"],
        "strategies": {
            "Minor issue": "Submit single-window clearance applications with digital document verification.",
            "Moderate issue": "Schedule bi-weekly inter-ministerial review sessions to clear pending statutory approvals.",
            "Major issue": "Appoint a dedicated Nodal Officer to interface directly with forest, environment, and railway authorities.",
            "Critical issue": "Trigger high-level MoSPI empowered committee intervention for fast-track statutory exemptions."
        }
    },
    {
        "id": "procurement_result",
        "question": "Q4. Are there contractor, vendor, or procurement bottlenecks?",
        "weight": 15,
        "why": "Execution delays often come from contractor performance or supply-chain slowdowns.",
        "options": ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"],
        "strategies": {
            "Minor issue": "Conduct weekly vendor progress meetings and monitor critical material supply chains.",
            "Moderate issue": "Enforce strict SLA penalties for delivery slippages while assisting in raw material sourcing.",
            "Major issue": "Issue formal cure notices to underperforming contractors and offload delayed scopes to sub-contractors.",
            "Critical issue": "Invoke contract termination clauses for non-performance and re-tender remaining work under fast-track emergency procurement."
        }
    },
    {
        "id": "scope_design",
        "question": "Q5. Has the project scope or design changed after sanction?",
        "weight": 10,
        "why": "Scope revision often leads to both cost and schedule impact.",
        "options": ["No change", "Minor changes", "Moderate changes", "Major changes", "Severe changes"],
        "strategies": {
            "Minor changes": "Document design modifications carefully in variation logs with strict cost cap.",
            "Moderate changes": "Freeze further design iterations post-sanction unless mandated by safety standards.",
            "Major changes": "Require full technical and financial re-appraisal by technical expert committee before executing variations.",
            "Severe changes": "Re-baseline the entire project master schedule and cost estimates to prevent runaway cost escalation."
        }
    },
    {
        "id": "execution_pace",
        "question": "Q6. Is the execution pace slower than planned due to site issues, labor, or coordination problems?",
        "weight": 10,
        "why": "Persistent site execution issues are a common cause of poor progress-to-spend mismatch.",
        "options": ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"],
        "strategies": {
            "Minor issue": "Augment supervisor presence on site and optimize shift handovers.",
            "Moderate issue": "Deploy additional labor workforce and double heavy machinery capacity on critical path tasks.",
            "Major issue": "Implement round-the-clock (24x7) shift schedules with performance incentives for site crews.",
            "Critical issue": "Completely overhaul site management team, restructure work packages into parallel fronts, and mobilize emergency machinery."
        }
    },
    {
        "id": "interagency_coordination",
        "question": "Q7. Are there local-level or inter-agency coordination problems?",
        "weight": 5,
        "why": "This covers a broad residual category that often compounds other issues.",
        "options": ["No issue", "Minor issue", "Moderate issue", "Major issue", "Critical issue"],
        "strategies": {
            "Minor issue": "Create a shared coordination group for site engineers across agencies.",
            "Moderate issue": "Establish formal bi-weekly joint coordination meetings with local municipal and utility bodies.",
            "Major issue": "Sign formal SLAs for inter-departmental utility permissions and joint site inspections.",
            "Critical issue": "Escalate to Chief Secretary / State Empowered Committee for binding dispute resolution between agencies."
        }
    }
]


@app.post("/api/questionnaire/evaluate")
@app.post("/api/questionnaire")
def evaluate_questionnaire(req: QuestionnaireSubmit):
    """Evaluates 7-question operational questionnaire and computes weighted risk score & mitigation strategies."""
    answers = req.model_dump()
    
    total_score = 0.0
    bottlenecks = []
    mitigations = []

    for q in QUESTION_META:
        qid = q["id"]
        selected_option = answers.get(qid, q["options"][0])
        weight = q["weight"]
        multiplier = SEVERITY_MULTIPLIERS.get(selected_option, 0.0)
        
        q_score = weight * multiplier
        total_score += q_score
        
        if multiplier > 0:
            if multiplier >= 0.75:
                status = "Critical Bottleneck"
            elif multiplier >= 0.50:
                status = "Major Bottleneck"
            else:
                status = "Minor Friction"
                
            bottlenecks.append({
                "id": qid,
                "question": q["question"],
                "selected_option": selected_option,
                "weight": weight,
                "weighted_score": round(q_score, 2),
                "severity_status": status,
                "why": q["why"]
            })
            
            strat = q["strategies"].get(selected_option)
            if strat:
                mitigations.append({
                    "category": q["question"].split(". ")[1].split("?")[0],
                    "selected_issue": selected_option,
                    "action": strat,
                    "priority": "High" if multiplier >= 0.5 else "Medium"
                })

    op_risk_score = round(total_score, 1)
    if op_risk_score < 20:
        tier = "Low"
    elif op_risk_score < 45:
        tier = "Medium"
    elif op_risk_score < 70:
        tier = "High"
    else:
        tier = "Critical"

    proj_name = req.project_name or "Submitted Project"
    summary_text = (
        f"Operational evaluation for '{proj_name}' indicates an Operational Risk Score of {op_risk_score}/100 "
        f"({tier} Operational Risk). "
    )
    if bottlenecks:
        top_issues = ", ".join([b["id"].replace("_", " ").title() for b in bottlenecks[:3]])
        summary_text += f"Key friction drivers detected in: {top_issues}. Targeted operational mitigation steps have been synthesized below."
    else:
        summary_text += "No significant operational bottlenecks reported. Execution is operating within normal baseline limits."

    return {
        "project_name": proj_name,
        "operational_risk_score": op_risk_score,
        "operational_risk_tier": tier,
        "bottlenecks": sorted(bottlenecks, key=lambda x: x["weighted_score"], reverse=True),
        "mitigation_strategies": mitigations,
        "ai_summary": summary_text
    }


# --- DASHBOARD ENDPOINTS (Wraps predictions_summary.py) ---

@app.get("/api/dashboard/summary")
@app.get("/api/home/summary")
def get_home_summary():
    return summary_api.get_home_summary()

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