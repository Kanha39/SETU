import pandas as pd

from chatbot.data_loader import df
from chatbot.retrieval import add_risk_columns


_RISK_SORT_ORDER = {
    "High": 0,
    "Medium": 1,
    "Low": 2,
    "Unknown": 3,
}


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

    scored["_sort_key"] = scored["_risk_tier"].map(
        _RISK_SORT_ORDER
    )

    return (
        scored
        .sort_values("_sort_key")
        .drop(columns=["_sort_key"])
        .head(top_n)
    )


def get_mega_projects() -> pd.DataFrame:
    """
    Return unique mega-project rows where
    original_cost_cr >= 10,000 crore.

    Duplicate project_code values are removed
    while keeping the first occurrence.
    """

    scored = get_scored_projects().copy()

    # Check that original cost column exists
    if "original_cost_cr" not in scored.columns:
        return pd.DataFrame()

    # Make original cost numeric
    scored["original_cost_cr"] = pd.to_numeric(
        scored["original_cost_cr"],
        errors="coerce"
    ).fillna(0)

    # Filter mega projects
    mega = scored[
        scored["original_cost_cr"] >= 10000
    ].copy()

    # Remove duplicate projects
    # Keep the FIRST occurrence
    if "project_code" in mega.columns:
        mega = mega.drop_duplicates(
            subset=["project_code"],
            keep="first"
        )

    # Make sure revised cost exists
    if "revised_cost_cr" not in mega.columns:
        mega["revised_cost_cr"] = (
            mega["original_cost_cr"]
        )

    # Convert revised cost to numeric
    mega["revised_cost_cr"] = pd.to_numeric(
        mega["revised_cost_cr"],
        errors="coerce"
    ).fillna(0)

    # Original cumulative expenditure column
    cumulative_col = "cumulative expenditure in rs. crore"

    # Create column if it doesn't exist
    if cumulative_col not in mega.columns:
        mega[cumulative_col] = 0.0

    # Convert cumulative expenditure to numeric
    mega[cumulative_col] = pd.to_numeric(
        mega[cumulative_col],
        errors="coerce"
    ).fillna(0)

    # Convert physical progress to numeric if available
    physical_col = "physical progress (in percentage)"

    if physical_col in mega.columns:
        mega[physical_col] = pd.to_numeric(
            mega[physical_col],
            errors="coerce"
        )

    return mega


def get_mega_project_summary() -> dict:
    """
    Provide dashboard-ready mega-project metrics.
    """

    mega = get_mega_projects()

    # Handle empty dataset
    if mega.empty:
        return {
            "total_mega_projects": 0,
            "top_10_mega_projects": [],
            "top_mega_projects": [],
            "totals": {
                "original_cost_cr": 0.0,
                "revised_cost_cr": 0.0,
                "cumulative expenditure in rs. crore": 0.0,
                "physical progress (in percentage)": 0.0,
            },
        }

    # --------------------------------------------------
    # Calculate totals
    # --------------------------------------------------

    original_cost_total = float(
        mega["original_cost_cr"]
        .fillna(0)
        .sum()
    )

    revised_cost_total = float(
        mega["revised_cost_cr"]
        .fillna(0)
        .sum()
    )

    cumulative_expenditure_total = float(
        mega["cumulative expenditure in rs. crore"]
        .fillna(0)
        .sum()
    )

    # Physical progress is a percentage,
    # so calculate the average.
    physical_col = "physical progress (in percentage)"

    if physical_col in mega.columns:
        physical_progress_avg = float(
            mega[physical_col]
            .fillna(0)
            .mean()
        )
    else:
        physical_progress_avg = 0.0

    totals = {
        "original_cost_cr": original_cost_total,
        "revised_cost_cr": revised_cost_total,
        "cumulative expenditure in rs. crore":
            cumulative_expenditure_total,
        "physical progress (in percentage)":
            physical_progress_avg,
    }

    # --------------------------------------------------
    # Select top 10 mega projects
    # --------------------------------------------------

    columns_to_return = [
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
    ]

    # Only select columns that actually exist
    columns_to_return = [
        column
        for column in columns_to_return
        if column in mega.columns
    ]

    top_projects_df = (
        mega
        .sort_values(
            "original_cost_cr",
            ascending=False
        )
        .head(10)
        .loc[:, columns_to_return]
        .copy()
    )

    # --------------------------------------------------
    # Make DataFrame JSON-safe
    # --------------------------------------------------

    # Replace +inf and -inf
    top_projects_df = top_projects_df.replace(
        [float("inf"), float("-inf")],
        pd.NA
    )

    # Replace NaN / NA with None
    top_projects_df = (
        top_projects_df
        .astype(object)
        .where(
            pd.notna(top_projects_df),
            None
        )
    )

    # Convert DataFrame to JSON-compatible dictionaries
    top_projects = top_projects_df.to_dict(
        orient="records"
    )

    # --------------------------------------------------
    # Final response
    # --------------------------------------------------

    return {
        "total_mega_projects": int(len(mega)),

        "top_10_mega_projects": top_projects,

        "top_mega_projects": top_projects,

        "totals": totals,
    }