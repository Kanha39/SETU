import difflib
import re
 
import pandas as pd
 
from chatbot.config import COST_OVERRUN_PRED_COL
from chatbot.data_loader import df
from chatbot.risk import compute_risk_tier, compute_cost_risk_tier, compute_time_risk_tier
 

_STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "at", "for", "to", "and", "or", "is", "are",
    "tell", "me", "about", "what", "give", "details", "detail", "project", "projects",
    "explain", "show", "please", "can", "you", "info", "information", "regarding",
    "related", "why", "how", "does", "did", "has", "have", "this", "that",
    "more", "it", "them", "these", "those", "any", "further"
}
 
 
def add_risk_columns(rows: pd.DataFrame) -> pd.DataFrame:
    """Attach _cost_risk_tier, _time_risk_tier, and the combined _risk_tier
    so callers (and eventually the graphs) can see which dimension is
    driving the overall risk, not just the final combined label."""
    return rows.assign(
        _cost_risk_tier=rows.apply(compute_cost_risk_tier, axis=1),
        _time_risk_tier=rows.apply(compute_time_risk_tier, axis=1),
        _risk_tier=rows.apply(compute_risk_tier, axis=1),
    )
 
 
def _clean_for_matching(text: str) -> str:
    words = re.findall(r"[a-z0-9]+", str(text).lower())
    significant = [w for w in words if w not in _STOPWORDS and len(w) > 2]
    return " ".join(significant)
 
 
def _fuzzy_score(query_clean: str, candidate_text: str) -> float:
    candidate_clean = _clean_for_matching(candidate_text)
    if not query_clean or not candidate_clean:
        return 0.0
 
    
    ratio = difflib.SequenceMatcher(None, query_clean, candidate_clean).ratio()
 
    
    query_words = set(query_clean.split())
    candidate_words = set(candidate_clean.split())
    overlap = len(query_words & candidate_words) / max(len(query_words), 1)
 
    return max(ratio, overlap)
 
 
def find_direct_match(query: str, top_n: int = 3, min_score: float = 0.35) -> pd.DataFrame:
    q_stripped = query.lower().strip()
    code_match = df[df["project_code"].astype(str).str.lower() == q_stripped]
    if not code_match.empty:
        return code_match.head(top_n)
 
    query_clean = _clean_for_matching(query)
    if not query_clean:
        return pd.DataFrame()
 
    scores = df.apply(
        lambda row: max(
            _fuzzy_score(query_clean, row.get("project_name", "")),
            _fuzzy_score(query_clean, row.get("agency", "")) * 0.8,
        ),
        axis=1,
    )
 
    matched = df[scores >= min_score].copy()
    if matched.empty:
        return matched
    matched["_match_score"] = scores[scores >= min_score]
    matched = matched.sort_values("_match_score", ascending=False)
    return matched.head(top_n).drop(columns=["_match_score"])
 
 
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