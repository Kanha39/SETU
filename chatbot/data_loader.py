import os
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from chatbot.config import DATA_PATH
except ModuleNotFoundError:
    from config import DATA_PATH


def _build_fallback_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "project_code": "PAI-1001",
                "project_name": "State Highway Rehabilitation",
                "agency": "PWD",
                "state": "Maharashtra",
                "ministry": "Road Transport",
                "sector": "Transport",
                "status": "Ongoing",
                "date_of_approval": "2022-01-15",
                "start_date": "2021-04-01",
                "actual_doc": "2024-03-31",
                "target_doc": "2025-03-31",
                "revised_doc": "2025-06-30",
                "original_cost_cr": 1200.0,
                "revised_cost_cr": 1200.0,
                "cumulative expenditure in rs. crore": 540.0,
                "physical progress (in percentage)": 42.0,
                "cost_overrun_pct": 12.5,
                "delay_actual_days": 180.0,
                "delay_proxy_days": 120.0,
                "predicted_overrun": 18.4,
                "Predicted Delay (days)": 210.0,
            },
            {
                "project_code": "PAI-1002",
                "project_name": "Urban Water Supply Upgrade",
                "agency": "Jal Nigam",
                "state": "Gujarat",
                "ministry": "Water Resources",
                "sector": "Water",
                "status": "Ongoing",
                "date_of_approval": "2023-02-10",
                "start_date": "2022-07-01",
                "actual_doc": "2024-12-31",
                "target_doc": "2026-01-15",
                "revised_doc": "2026-03-01",
                "original_cost_cr": 900.0,
                "revised_cost_cr": 980.0,
                "cumulative expenditure in rs. crore": 470.0,
                "physical progress (in percentage)": 55.0,
                "cost_overrun_pct": 8.2,
                "delay_actual_days": 90.0,
                "delay_proxy_days": 75.0,
                "predicted_overrun": 10.6,
                "Predicted Delay (days)": 110.0,
            },
            {
                "project_code": "PAI-1003",
                "project_name": "Power Transmission Line",
                "agency": "NTPC",
                "state": "Tamil Nadu",
                "ministry": "Power",
                "sector": "Energy",
                "status": "Completed",
                "date_of_approval": "2020-11-20",
                "start_date": "2020-01-10",
                "actual_doc": "2023-08-15",
                "target_doc": "2024-01-31",
                "revised_doc": "2024-03-15",
                "original_cost_cr": 1500.0,
                "revised_cost_cr": 1600.0,
                "cumulative expenditure in rs. crore": 1600.0,
                "physical progress (in percentage)": 100.0,
                "cost_overrun_pct": 6.7,
                "delay_actual_days": 45.0,
                "delay_proxy_days": 38.0,
                "predicted_overrun": 7.1,
                "Predicted Delay (days)": 62.0,
            },
        ]
    )

DATE_COLUMNS = ["date_of_approval", "start_date", "actual_doc", "target_doc", "revised_doc"]


def load_data() -> pd.DataFrame:
    """Loads the historical projects dataset from the local merged_projects.csv
    (DATA_PATH in config.py), instead of fetching it over HTTP from the
    db_bridge service / MySQL. User-submitted project data and chat history
    still go through MySQL via db.py -- this only affects the historical
    dataset used for retrieval, filtering, and similarity search."""
    if not DATA_PATH.exists():
        raise RuntimeError(
            f"Historical dataset CSV not found at {DATA_PATH}. Check "
            "DATA_PATH in config.py, or that merged_projects.csv is "
            "actually there."
        )

    df = pd.read_csv(DATA_PATH, low_memory=False)

    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


df = load_data()

SECTORS = df["sector"].dropna().astype(str).unique().tolist() if "sector" in df.columns else []
STATES = df["state"].dropna().astype(str).unique().tolist() if "state" in df.columns else []
MINISTRIES = df["ministry"].dropna().astype(str).unique().tolist() if "ministry" in df.columns else []