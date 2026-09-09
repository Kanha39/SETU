"""Run this once (and again any time merged_projects.csv changes) to push
the historical, ML-scored project dataset into MySQL so both the Python
chatbot and the Spring Boot backend read from the same table.

Usage:
    python -m chatbot.migrate_csv_to_mysql
"""
from sqlalchemy import create_engine

from chatbot.config import DATA_PATH, DB_URL, PROJECTS_TABLE, COST_OVERRUN_PRED_COL, DELAY_PRED_COL
from chatbot.data_loader import DATE_COLUMNS
import pandas as pd


def main():
    print(f"Reading {DATA_PATH} ...")
    df = pd.read_csv(DATA_PATH, low_memory=False)

    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    if COST_OVERRUN_PRED_COL not in df.columns or DELAY_PRED_COL not in df.columns:
        print(
            "WARNING: the CSV doesn't have prediction columns yet "
            f"({COST_OVERRUN_PRED_COL!r}, {DELAY_PRED_COL!r}). "
            "Run score_dataset.py first so historical projects have "
            "predicted_overrun / predicted delay values, or risk tiers "
            "for them will show as 'Unknown'."
        )

    print(f"Connecting to MySQL and writing table '{PROJECTS_TABLE}' ({len(df)} rows)...")
    engine = create_engine(DB_URL)
    df.to_sql(PROJECTS_TABLE, con=engine, if_exists="replace", index=False)
    print("Done. Table is ready for both the chatbot service and Spring Boot to read.")


if __name__ == "__main__":
    main()