import pandas as pd

from chatbot.data_loader import df


def find_similar_past_projects(project_row: pd.Series, top_n: int = 3) -> pd.DataFrame:
    finished = df[df["status"].str.lower().isin(["completed", "frozen or deleted"])].copy()
    if finished.empty:
        return finished

    same_sector = finished[finished["sector"] == project_row.get("sector")]
    pool = (same_sector if not same_sector.empty else finished).copy()

    
    pool["_had_overrun"] = pool["cost_overrun_pct"].fillna(0) > 0
    pool["_delay_days"] = pd.to_numeric(
        pool["delay_actual_days"].astype(str).str.extract(r"(-?\d+)")[0], errors="coerce"
    )

    pool = pool.sort_values(
        by=["_had_overrun", "_delay_days", "cost_overrun_pct"],
        ascending=[False, False, False],
        na_position="last",
    )

    return pool.head(top_n).drop(columns=["_had_overrun", "_delay_days"], errors="ignore")
