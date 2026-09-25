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


def get_mega_projects() -> pd.DataFrame:
    """Return project rows where the project cost is >= 10000 crore.

    This is intentionally kept separate from the DB-layer logic. Once the
    backend begins serving MySQL data, the same filtering logic can be reused
    there while keeping the historical CSV fallback intact.
    """
    scored = get_scored_projects().copy()

    if "original_cost_cr" not in scored.columns:
        return pd.DataFrame()

    mega = scored[scored["original_cost_cr"].fillna(0) >= 10000].copy()

    if "revised_cost_cr" not in mega.columns:
        mega["revised_cost_cr"] = mega["original_cost_cr"].fillna(0)

    cumulative_col = "cumulative expenditure in rs. crore"
    if cumulative_col not in mega.columns:
        mega[cumulative_col] = 0.0

    mega[cumulative_col] = pd.to_numeric(mega[cumulative_col], errors="coerce").fillna(0)
    return mega


def get_mega_project_summary() -> dict:
    """Provide dashboard-ready mega-project metrics for the historical dataset."""
    mega = get_mega_projects()

    if mega.empty:
        return {
            "total_mega_projects": 0,
            "top_10_mega_projects": [],
            "totals": {
                "original_cost_cr": 0.0,
                "revised_cost_cr": 0.0,
                "cumulative_expenditure_cr": 0.0,
            },
        }

    totals = {
        "original_cost_cr": float(mega["original_cost_cr"].fillna(0).sum()),
        "revised_cost_cr": float(mega["revised_cost_cr"].fillna(0).sum()),
        "cumulative_expenditure_cr": float(mega["cumulative expenditure in rs. crore"].fillna(0).sum()),
        "physical_progress_pct": float(mega["physical progress (in percentage)"].fillna(0).mean()),
    }

    top_projects = (
        mega.sort_values("original_cost_cr", ascending=False)
        .head(10)
        .loc[:, [
            "project_name",
            "project_code",
            "agency",
            "state",
            "sector",
            "status",
            "original_cost_cr",
            "revised_cost_cr",
            "cumulative expenditure in rs. crore",
            "physical progress (in percentage)",
        ]]
        .to_dict(orient="records")
    )

    return {
        "total_mega_projects": int(len(mega)),
        "top_10_mega_projects": top_projects,
        "top_mega_projects": top_projects,
        "totals": totals,
    }
