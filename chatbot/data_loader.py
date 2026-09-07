"""
Loads the merged, cleaned project dataset and derives the reference value
lists used for entity matching. This is the only file that touches the raw CSV.
"""

import pandas as pd

from chatbot.config import DATA_PATH


def load_data(path=DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(
        path,
        parse_dates=["date_of_approval", "start_date", "actual_doc", "target_doc", "revised_doc"],
        low_memory=False,
    )


df = load_data()

SECTORS = df["sector"].dropna().astype(str).unique().tolist() if "sector" in df.columns else []
STATES = df["state"].dropna().astype(str).unique().tolist() if "state" in df.columns else []
MINISTRIES = df["ministry"].dropna().astype(str).unique().tolist() if "ministry" in df.columns else []
