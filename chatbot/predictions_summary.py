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


def get_home_summary() -> dict:
    total_projects = len(df)
    total_orig_cost = float(df["original_cost_cr"].sum()) if "original_cost_cr" in df.columns else 0.0
    total_cum_exp = float(df["cumulative expenditure in rs. crore"].sum()) if "cumulative expenditure in rs. crore" in df.columns else 0.0
    total_rev_cost = float(df["revised_cost_cr"].sum()) if "revised_cost_cr" in df.columns else 0.0
    ministries_count = int(df["ministry"].nunique()) if "ministry" in df.columns else 0

    top_high_val = df.sort_values("original_cost_cr", ascending=False).drop_duplicates(subset=["project_name"]).head(8)
    high_val_list = []
    for _, row in top_high_val.iterrows():
        completion_str = "N/A"
        if pd.notna(row.get("target_doc")):
            completion_str = str(row.get("target_doc")).split(" ")[0].split("T")[0]

        high_val_list.append({
            "name": str(row.get("project_name", "N/A")),
            "ministry": str(row.get("ministry") or row.get("agency") or "N/A"),
            "sector": str(row.get("sector", "N/A")),
            "cost": f"Rs. {row.get('original_cost_cr', 0):,.2f} Cr",
            "progress": f"{row.get('physical progress (in percentage)', 0):.0f}%",
            "completion": completion_str
        })

    return {
        "total_projects": f"{total_projects:,}",
        "total_original_cost_formatted": f"Rs. {total_orig_cost / 100000:.2f} Lakh Cr",
        "total_expenditure_formatted": f"Rs. {total_cum_exp / 100000:.2f} Lakh Cr",
        "total_revised_cost_formatted": f"Rs. {total_rev_cost / 100000:.2f} Lakh Cr",
        "tracked_ministries": ministries_count,
        "high_value_projects": high_val_list
    }

