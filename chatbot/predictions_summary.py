import pandas as pd

from chatbot.data_loader import df
from chatbot.retrieval import add_risk_columns

_RISK_SORT_ORDER = {"High": 0, "Medium": 1, "Low": 2, "Unknown": 3}


def get_scored_projects() -> pd.DataFrame:
    return add_risk_columns(df)


def get_risk_distribution() -> dict:
    scored = get_scored_projects()
    return scored["_risk_tier"].value_counts().to_dict()


def get_cost_risk_distribution() -> dict:
    scored = get_scored_projects()
    return scored["_cost_risk_tier"].value_counts().to_dict()


def get_time_risk_distribution() -> dict:
    scored = get_scored_projects()
    return scored["_time_risk_tier"].value_counts().to_dict()


def get_delayed_project_count() -> int:
    return int(df["delay_actual_days"].notna().sum())


def get_sector_wise_risk_summary() -> pd.DataFrame:
    
    scored = get_scored_projects()
    if "sector" not in scored.columns:
        return pd.DataFrame()
    return (
        scored.groupby(["sector", "_risk_tier"])
        .size()
        .reset_index(name="count")
    )


def get_top_risky_projects(top_n: int = 10) -> pd.DataFrame:
    
    scored = get_scored_projects().copy()
    scored["_sort_key"] = scored["_risk_tier"].map(_RISK_SORT_ORDER)
    return (
        scored.sort_values("_sort_key")
        .drop(columns=["_sort_key"])
        .head(top_n)
    )
