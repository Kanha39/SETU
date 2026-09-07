"""
Finds past (completed/frozen) projects similar to a given project, to use
as real historical examples when the chatbot explains why a project is
likely to overrun on cost or schedule.

"Similar" means: same sector first (falling back to the whole finished-
project pool if none match), restricted to projects that actually finished
(status != Ongoing) so their real outcome (actual overrun, actual delay) is
known -- these are the projects worth citing as precedent, not other
still-ongoing projects whose own outcome is still unknown.
"""

import pandas as pd

from chatbot.data_loader import df


def find_similar_past_projects(project_row: pd.Series, top_n: int = 3) -> pd.DataFrame:
    finished = df[df["status"].str.lower().isin(["completed", "frozen", "deleted"])].copy()
    if finished.empty:
        return finished

    same_sector = finished[finished["sector"] == project_row.get("sector")]
    pool = (same_sector if not same_sector.empty else finished).copy()

    # Prefer past projects that actually had a meaningful cost overrun or
    # delay -- these are the ones worth citing as a cautionary example,
    # rather than ones that finished cleanly on time and on budget.
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
