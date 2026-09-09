import json
from sqlalchemy import create_engine, text
from chatbot.config import DB_URL, DB_POOL_SIZE, DB_MAX_OVERFLOW

# Kept deliberately small: this MySQL instance is shared with the Spring Boot
# backend's own connection pool. See the integration notes for how to check
# your host's max_connections before demo day.
engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=280,
    pool_size=DB_POOL_SIZE,
    max_overflow=DB_MAX_OVERFLOW,
)


def save_chat_message(user_id: int, session_id: str, project_code: str, user_message: str, bot_response: str):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO chat_messages (user_id, session_id, project_code, user_message, bot_response, created_at)
                VALUES (:user_id, :session_id, :project_code, :user_message, :bot_response, NOW())
            """),
            {
                "user_id": user_id,
                "session_id": session_id,
                "project_code": project_code,
                "user_message": user_message,
                "bot_response": bot_response,
            },
        )


def get_chat_history(session_id: str, limit: int = 20) -> list:
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                SELECT user_message, bot_response FROM chat_messages
                WHERE session_id = :session_id
                ORDER BY created_at ASC
                LIMIT :limit
            """),
            {"session_id": session_id, "limit": limit},
        ).fetchall()

    history = []
    for user_message, bot_response in rows:
        history.append({"role": "user", "text": user_message})
        history.append({"role": "model", "text": bot_response})
    return history


def save_user_project(session_id: str, user_id: int, project_data: dict, predictions: dict):
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO user_submitted_projects
                    (session_id, user_id, project_data, predicted_overrun, predicted_delay_days,
                     cost_risk_tier, time_risk_tier, overall_risk_tier, created_at)
                VALUES
                    (:session_id, :user_id, :project_data, :predicted_overrun, :predicted_delay_days,
                     :cost_risk_tier, :time_risk_tier, :overall_risk_tier, NOW())
            """),
            {
                "session_id": session_id,
                "user_id": user_id,
                "project_data": json.dumps(project_data, default=str),  # default=str handles Timestamps/NaN-safe types
                "predicted_overrun": predictions["predicted_overrun_pct"],
                "predicted_delay_days": predictions["predicted_delay_days"],
                "cost_risk_tier": predictions["cost_risk_tier"],
                "time_risk_tier": predictions["time_risk_tier"],
                "overall_risk_tier": predictions["overall_risk_tier"],
            },
        )


def get_user_project(session_id: str) -> dict | None:
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT project_data FROM user_submitted_projects WHERE session_id = :session_id"),
            {"session_id": session_id},
        ).fetchone()
    if row is None:
        return None
    return json.loads(row[0])