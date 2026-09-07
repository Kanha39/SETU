"""
Turns a query (or its extracted entities) into matching rows from the
dataset -- either a direct name/code/agency match, or a filtered set for
aggregate/analytical queries.
"""

import re

import pandas as pd

from chatbot.config import COST_OVERRUN_PRED_COL
from chatbot.data_loader import df
from chatbot.risk import compute_risk_tier, compute_cost_risk_tier, compute_time_risk_tier


def add_risk_columns(rows: pd.DataFrame) -> pd.DataFrame:
    """Attach _cost_risk_tier, _time_risk_tier, and the combined _risk_tier
    so callers (and eventually the graphs) can see which dimension is
    driving the overall risk, not just the final combined label."""
    return rows.assign(
        _cost_risk_tier=rows.apply(compute_cost_risk_tier, axis=1),
        _time_risk_tier=rows.apply(compute_time_risk_tier, axis=1),
        _risk_tier=rows.apply(compute_risk_tier, axis=1),
    )


def find_direct_match(query: str, top_n: int = 3) -> pd.DataFrame:
    """Crude substring match against project_code/project_name/agency.
    Placeholder until ChromaDB fuzzy matching is added -- this only catches
    queries whose wording is already close to the actual dataset text."""
    q = query.lower().strip()
    if len(q) < 4:
        return pd.DataFrame()

    escaped = re.escape(q)
    name_match = df[df["project_name"].str.lower().str.contains(escaped, na=False, regex=True)]
    code_match = df[df["project_code"].astype(str).str.lower() == q]
    agency_match = df[df["agency"].str.lower().str.contains(escaped, na=False, regex=True)]

    matches = pd.concat([code_match, name_match, agency_match]).drop_duplicates()
    return matches.head(top_n)


def filter_projects(entities: dict, top_n: int = 10):
    """Returns (top_n_matches, total_match_count) so the response can say
    'showing top N of TOTAL matching projects'."""
    filtered = df.copy()

    if entities.get("sector"):
        filtered = filtered[filtered["sector"].str.lower() == entities["sector"].lower()]
    if entities.get("state"):
        filtered = filtered[filtered["state"].str.lower() == entities["state"].lower()]
    if entities.get("ministry"):
        filtered = filtered[filtered["ministry"].str.lower() == entities["ministry"].lower()]
    if entities.get("status"):
        filtered = filtered[filtered["status"].str.lower().str.contains(entities["status"], na=False)]
    if entities.get("year"):
        year = entities["year"]
        year_mask = (
            filtered["target_doc"].dt.year.eq(year)
            | filtered["revised_doc"].dt.year.eq(year)
        )
        filtered = filtered[year_mask.fillna(False)]

    filtered = add_risk_columns(filtered)
    if entities.get("high_risk"):
        filtered = filtered[filtered["_risk_tier"] == "High"]

    if entities.get("delayed") and "delay_actual_days" in filtered.columns:
        filtered = filtered[filtered["delay_actual_days"].notna()]

    total_matches = len(filtered)

    sort_col = COST_OVERRUN_PRED_COL if COST_OVERRUN_PRED_COL in filtered.columns else (
        "cost_overrun_pct" if "cost_overrun_pct" in filtered.columns else None
    )
    if sort_col:
        filtered = filtered.sort_values(sort_col, ascending=False, na_position="last")

    return filtered.head(top_n), total_matches
