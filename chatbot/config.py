"""
Central configuration for the PAIMANA chatbot.
Nothing else in this package should hardcode paths, model names, or the
system prompt -- read them from here so changes only need to happen once.
"""

from pathlib import Path

from dotenv import load_dotenv

# Assumes this file lives at <repo_root>/chatbot/config.py.
BASE_DIR = Path(__file__).resolve().parent.parent
CHATBOT_DIR = Path(__file__).resolve().parent

# Loads chatbot/.env automatically (GEMINI_API_KEY, etc.) so you don't need
# to `export` it manually every terminal session. Does nothing if the file
# doesn't exist -- safe to leave in even before you've created .env.
load_dotenv(dotenv_path=CHATBOT_DIR / ".env")

DATA_PATH = BASE_DIR/ "ml-pipeline" / "data" / "processed" / "merged_projects.csv"

# Trained model files (.pkl) from Person 2 (XGBoost, cost) and Person 3
# (LightGBM, time). Place the actual files at these paths -- see
# model_inference.py for how they're loaded and used.
MODEL_DIR = BASE_DIR/ "ml-pipeline" / "data" / "models"
COST_MODEL_PATH = MODEL_DIR / "cost_model.pkl"
TIME_MODEL_PATH = MODEL_DIR / "time_model.pkl"

MODEL_NAME = "gemini-3.6-flash"  # verify against your working RAG project's model name

# Real ML model output columns, confirmed with Person 2 (cost) and Person 3 (time).
# Note: DELAY_PRED_COL keeps its original casing/spacing as merged in -- it does
# not follow the all-lowercase convention used by the rest of this dataset.
COST_OVERRUN_PRED_COL = "predicted_overrun"     # percentage, e.g. 20 means 20%
DELAY_PRED_COL = "Predicted Delay (days)"       # number of days

# Thresholds for turning each model's raw number into a Low/Medium/High tier.
# These are first-pass guesses -- revisit once you've looked at the actual
# distribution of predictions in your dataset, and mention to judges that
# they're configurable.
COST_RISK_HIGH_THRESHOLD = 20    # percent
COST_RISK_MEDIUM_THRESHOLD = 5   # percent
DELAY_RISK_HIGH_THRESHOLD = 180  # days
DELAY_RISK_MEDIUM_THRESHOLD = 30 # days

# Used to pick the "worse" of the cost-risk and time-risk tiers as the
# overall risk tier.
RISK_TIER_ORDER = {"Low": 0, "Medium": 1, "High": 2, "Unknown": -1}

RISK_KEYWORDS = ["high risk", "high-risk", "risky", "at risk"]
DELAY_KEYWORDS = ["delayed", "delay", "late", "behind schedule"]
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
