from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
CHATBOT_DIR = Path(__file__).resolve().parent

# Load .env FIRST, before reading any environment variables below.
load_dotenv(dotenv_path=CHATBOT_DIR / ".env")

# --- MySQL (shared with Person 4's Spring Boot backend) ---
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME", "paimana")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

DATA_PATH = BASE_DIR / "ml-pipeline" / "data" / "processed" / "merged_projects.csv"

MODEL_DIR = BASE_DIR / "ml-pipeline" / "data" / "models"
COST_MODEL_PATH = MODEL_DIR / "cost_model.pkl"
TIME_MODEL_PATH = MODEL_DIR / "time_model.pkl"

MODEL_NAME = "gemini-3.6-flash"


COST_OVERRUN_PRED_COL = "predicted_overrun"
DELAY_PRED_COL = "Predicted Delay (days)"


COST_RISK_HIGH_THRESHOLD = 20    # percent
COST_RISK_MEDIUM_THRESHOLD = 5   # percent
DELAY_RISK_HIGH_THRESHOLD = 180  # days
DELAY_RISK_MEDIUM_THRESHOLD = 30 # days


RISK_TIER_ORDER = {"Low": 0, "Medium": 1, "High": 2, "Unknown": -1}

RISK_KEYWORDS = ["high risk", "high-risk", "risky", "at risk"]
DELAY_KEYWORDS = ["delayed", "delay", "behind schedule"]
THIS_YEAR_KEYWORDS = ["this year", "current year"]
STATUS_KEYWORDS = ["completed", "ongoing", "frozen", "deleted"]

CONTEXT_FIELDS = [
    "project_code", "project_name", "agency", "state", "sector", "ministry", "status",
    "date_of_approval", "target_doc", "revised_doc", "actual_doc",
    "original_cost_cr", "revised_cost_cr",
    "cumulative expenditure in rs. crore", "physical progress (in percentage)",
    "cost_overrun_pct", "delay_actual_days", "delay_proxy_days",
    COST_OVERRUN_PRED_COL, DELAY_PRED_COL,
    "_cost_risk_tier", "_time_risk_tier", "_risk_tier",
]

SYSTEM_PROMPT = """You are PAIMANA's project analyst assistant for MoSPI infrastructure monitoring.
You explain delay, cost overrun, and risk for government infrastructure projects, citing real past
projects as evidence, and you suggest concrete mitigation strategies.

Strict rules:
- Only use facts from the PROJECT DATA and PAST COMPARABLE PROJECTS blocks given to you. Never invent
  project names, codes, dates, or figures.
- If the data block says no matching projects were found, tell the user that plainly - do not guess.
- When a query matched more projects than are shown, explicitly state the total count and the number shown.
- Always cite the project_code and project_name when referencing a specific project, including past ones.
- If a project's cost risk or time risk tier is "Unknown", say that dimension hasn't been scored yet - never treat "Unknown" as "Low".
- When asked why a project is at risk of cost or time overrun, ground the explanation in the specific
  numbers given (predicted overrun %, predicted delay days) AND reference at least one past comparable
  project from the PAST COMPARABLE PROJECTS block as precedent, if one is provided.
- Always end an overrun/delay explanation with 2-3 concrete, specific mitigation steps (e.g. tied to
  procurement delays, land acquisition, contractor performance, fund release timing) rather than generic
  advice like "monitor closely" - infer likely causes only from patterns visible in the data given, and
  say so plainly if the data doesn't indicate a specific cause.
- Keep answers concise and factual.
"""