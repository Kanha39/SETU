import pandas as pd

from chatbot.config import CONTEXT_FIELDS


def format_project_row(row) -> str:
    parts = [f"{f}: {row[f]}" for f in CONTEXT_FIELDS if f in row.index and pd.notna(row[f])]
    return " | ".join(parts)


def build_context_block(matches: pd.DataFrame, total_matches: int) -> str:
    if matches.empty:
        return "No matching projects were found in the dataset for this query."
    lines = [format_project_row(row) for _, row in matches.iterrows()]
    header = f"Showing {len(matches)} of {total_matches} matching project(s):"
    return header + "\n" + "\n".join(lines)


SIMILAR_PROJECT_FIELDS = [
    "project_code", "project_name", "sector", "state", "status",
    "original_cost_cr", "revised_cost_cr", "cost_overrun_pct",
    "target_doc", "actual_doc", "delay_actual_days",
]


def format_similar_project_row(row) -> str:
    parts = [f"{f}: {row[f]}" for f in SIMILAR_PROJECT_FIELDS if f in row.index and pd.notna(row[f])]
    return " | ".join(parts)


def build_similar_projects_block(similar: pd.DataFrame) -> str:
    if similar.empty:
        return "PAST COMPARABLE PROJECTS: none found in the dataset."
    lines = [format_similar_project_row(row) for _, row in similar.iterrows()]
    return "PAST COMPARABLE PROJECTS (for root-cause examples):\n" + "\n".join(lines)
