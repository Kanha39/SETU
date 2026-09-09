"""
One-time migration: loads merged_projects.csv into the MySQL `projects` table.

Run this AFTER schema.sql has been applied and BEFORE starting the chatbot
service, since data_loader.py now reads from MySQL instead of the CSV.

Usage:
    python -m chatbot.migrate_csv_to_mysql
"""
import pandas as pd

from chatbot.config import DATA_PATH, PROJECTS_TABLE
from chatbot.db import engine


def main():
    print(f"Reading {DATA_PATH} ...")
    df = pd.read_csv(DATA_PATH, low_memory=False)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns from CSV.")

    print(f"Writing to MySQL table `{PROJECTS_TABLE}` (replacing if it exists) ...")
    df.to_sql(
        PROJECTS_TABLE,
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
    )
    print(f"Done. `{PROJECTS_TABLE}` now has {len(df)} rows in MySQL.")


if __name__ == "__main__":
    main()