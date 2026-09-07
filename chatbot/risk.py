import pandas as pd

from chatbot.config import (
    COST_OVERRUN_PRED_COL,
    DELAY_PRED_COL,
    COST_RISK_HIGH_THRESHOLD,
    COST_RISK_MEDIUM_THRESHOLD,
    DELAY_RISK_HIGH_THRESHOLD,
    DELAY_RISK_MEDIUM_THRESHOLD,
    RISK_TIER_ORDER,
)


def compute_cost_risk_tier(row) -> str:
    if COST_OVERRUN_PRED_COL not in row.index or pd.isna(row[COST_OVERRUN_PRED_COL]):
        return "Unknown"

    overrun_pct = row[COST_OVERRUN_PRED_COL]
    if overrun_pct > COST_RISK_HIGH_THRESHOLD:
        return "High"
    elif overrun_pct > COST_RISK_MEDIUM_THRESHOLD:
        return "Medium"
    return "Low"


def compute_time_risk_tier(row) -> str:
    if DELAY_PRED_COL not in row.index or pd.isna(row[DELAY_PRED_COL]):
        return "Unknown"

    delay_days = row[DELAY_PRED_COL]
    if delay_days > DELAY_RISK_HIGH_THRESHOLD:
        return "High"
    elif delay_days > DELAY_RISK_MEDIUM_THRESHOLD:
        return "Medium"
    return "Low"


def compute_risk_tier(row) -> str:
    cost_tier = compute_cost_risk_tier(row)
    time_tier = compute_time_risk_tier(row)

    if cost_tier == "Unknown" and time_tier == "Unknown":
        return "Unknown"

    cost_rank = RISK_TIER_ORDER[cost_tier] if cost_tier != "Unknown" else -1
    time_rank = RISK_TIER_ORDER[time_tier] if time_tier != "Unknown" else -1

    worse_rank = max(cost_rank, time_rank)
    for tier, rank in RISK_TIER_ORDER.items():
        if rank == worse_rank:
            return tier
    return "Unknown"
