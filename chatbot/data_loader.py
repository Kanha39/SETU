import pandas as pd

from chatbot.config import DATA_PATH

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