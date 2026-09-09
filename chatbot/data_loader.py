import pandas as pd

from chatbot.config import PROJECTS_TABLE
from chatbot.db import engine

DATE_COLUMNS = ["date_of_approval", "start_date", "actual_doc", "target_doc", "revised_doc"]


def load_data() -> pd.DataFrame:
    """Loads the projects dataset from MySQL (populated once via
    migrate_csv_to_mysql.py) instead of reading the CSV directly, so the
    Spring Boot backend and this chatbot service share one source of truth."""
    df = pd.read_sql_table(PROJECTS_TABLE, con=engine)

    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


df = load_data()

SECTORS = df["sector"].dropna().astype(str).unique().tolist() if "sector" in df.columns else []
STATES = df["state"].dropna().astype(str).unique().tolist() if "state" in df.columns else []
MINISTRIES = df["ministry"].dropna().astype(str).unique().tolist() if "ministry" in df.columns else []