"""
Aggregate, chart-ready summaries of the model predictions and risk tiers --
deliberately separate from the chatbot's conversational logic, matching the
team's plan for a separate chatbot space vs. a graphical predictions space.

This file only computes numbers/tables; it does not render anything.
Intended to be wrapped in an API endpoint later (by Person 4, or directly
from this service) for the frontend's charts.
"""

import pandas as pd

from chatbot.data_loader import df
from chatbot.retrieval import add_risk_columns

_RISK_SORT_ORDER = {"High": 0, "Medium": 1, "Low": 2, "Unknown": 3}


def get_scored_projects() -> pd.DataFrame:
    """The full dataset with _cost_risk_tier / _time_risk_tier / _risk_tier
    attached. Compute once per request and reuse rather than calling this
    repeatedly for multiple charts in the same page load."""
    return add_risk_columns(df)


def get_risk_distribution() -> dict:
    """e.g. {'High': 42, 'Medium': 130, 'Low': 900, 'Unknown': 15}"""
    scored = get_scored_projects()
    return scored["_risk_tier"].value_counts().to_dict()


def get_cost_risk_distribution() -> dict:
    scored = get_scored_projects()
    return scored["_cost_risk_tier"].value_counts().to_dict()


def get_time_risk_distribution() -> dict:
    scored = get_scored_projects()
    return scored["_time_risk_tier"].value_counts().to_dict()


def get_delayed_project_count() -> int:
    """Count of projects with a real (historical) delay recorded."""
    return int(df["delay_actual_days"].notna().sum())


def get_sector_wise_risk_summary() -> pd.DataFrame:
    """One row per (sector, risk tier) with a count -- feeds a grouped/
    stacked bar chart of risk by sector."""
    scored = get_scored_projects()
    if "sector" not in scored.columns:
        return pd.DataFrame()
    return (
        scored.groupby(["sector", "_risk_tier"])
        .size()
        .reset_index(name="count")
    )


def get_top_risky_projects(top_n: int = 10) -> pd.DataFrame:
    """The N riskiest projects overall (High first), for a leaderboard-
    style chart or table."""
    scored = get_scored_projects().copy()
    scored["_sort_key"] = scored["_risk_tier"].map(_RISK_SORT_ORDER)
    return (
        scored.sort_values("_sort_key")
        .drop(columns=["_sort_key"])
        .head(top_n)
    )
