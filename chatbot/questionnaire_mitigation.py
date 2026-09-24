from typing import Dict, List, Tuple


ANSWER_SCORE = {
    "no_issue": 0,
    "minor": 1,
    "moderate": 2,
    "major": 3,
    "critical": 4,
    "none": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "very_high": 4,
}

QUESTION_WEIGHTS = {
    "land_acquisition": 25,
    "financial_result": 20,
    "approval_clearance": 20,
    "procurement_result": 15,
    "scope_design": 10,
    "execution_pace": 10,
    "interagency_coordination": 5,
}

CATEGORY_LABELS = {
    "land_acquisition": "land_and_site",
    "financial_result": "funding_and_cash_flow",
    "approval_clearance": "approvals_and_clearances",
    "procurement_result": "procurement_and_contractors",
    "scope_design": "scope_and_design",
    "execution_pace": "execution_and_site_performance",
    "interagency_coordination": "coordination_and_governance",
}

CATEGORY_DESCRIPTIONS = {
    "land_and_site": "land acquisition, utility shifting, and site readiness",
    "funding_and_cash_flow": "budget release, financing, and cash-flow constraints",
    "approvals_and_clearances": "administrative approvals and regulatory delays",
    "procurement_and_contractors": "vendor, contractor, and procurement bottlenecks",
    "scope_and_design": "design changes and scope variation",
    "execution_and_site_performance": "execution pace, supervision, and site-level delays",
    "coordination_and_governance": "inter-agency coordination and governance issues",
}


def _normalize_answer(value) -> str:
    if value is None:
        return "no_issue"
    if isinstance(value, str):
        text = value.strip().lower().replace(" ", "_")
        if text in ANSWER_SCORE:
            return text
        aliases = {
            "no": "no_issue",
            "none": "no_issue",
            "minor_issue": "minor",
            "moderate_issue": "moderate",
            "major_issue": "major",
            "critical_issue": "critical",
        }
        return aliases.get(text, text)
    if isinstance(value, (int, float)):
        if value <= 0:
            return "no_issue"
        if value <= 1:
            return "minor"
        if value <= 2:
            return "moderate"
        if value <= 3:
            return "major"
        return "critical"
    return "no_issue"


def score_questionnaire(questionnaire: Dict[str, object]) -> Dict[str, object]:
    """Score the 7-question delay assessment and return the dominant reason."""
    computed_scores = {}
    for question_key, weight in QUESTION_WEIGHTS.items():
        answer_value = questionnaire.get(question_key, "no_issue")
        normalized = _normalize_answer(answer_value)
        score = ANSWER_SCORE.get(normalized, 0)
        computed_scores[question_key] = {
            "answer": normalized,
            "score": score,
            "weight": weight,
            "weighted_score": score * weight,
        }

    dominant_key = max(
        computed_scores,
        key=lambda key: computed_scores[key]["weighted_score"],
    )
    dominant_reason = CATEGORY_LABELS.get(dominant_key, "coordination_and_governance")
    total_score = sum(item["weighted_score"] for item in computed_scores.values())

    return {
        "question_scores": computed_scores,
        "dominant_reason": dominant_reason,
        "dominant_reason_label": CATEGORY_DESCRIPTIONS.get(dominant_reason, dominant_reason),
        "total_score": total_score,
        "max_possible_score": sum(QUESTION_WEIGHTS.values()) * 4,
    }


def _mitigation_for_category(category: str) -> List[str]:
    if category == "land_and_site":
        return [
            "Accelerate land acquisition and utility shifting to remove site-readiness bottlenecks.",
            "Escalate local authority follow-up and fix the possession plan with a strict timeline.",
            "Prepare a weekly site-readiness tracker for land, utilities, and clearances.",
        ]
    if category == "funding_and_cash_flow":
        return [
            "Review the funding release plan and prioritize the next milestone-linked disbursement.",
            "Tighten contractor payment monitoring to avoid payment-driven execution delays.",
            "Create a cash-flow dashboard linked to project milestones and pending approvals.",
        ]
    if category == "approvals_and_clearances":
        return [
            "Escalate pending approvals and maintain a stage-wise clearance tracker.",
            "Create a single coordination cell for regulatory and administrative follow-up.",
            "Set a weekly review with all approving departments to unblock decisions.",
        ]
    if category == "procurement_and_contractors":
        return [
            "Review vendor performance and recover schedule through milestone enforcement.",
            "Resolve procurement bottlenecks and rebalance contractor workload across critical packages.",
            "Introduce weekly contractor performance review and supply-chain risk tracking.",
        ]
    if category == "scope_and_design":
        return [
            "Freeze non-essential scope changes and enforce a strict change-control process.",
            "Revalidate design assumptions and reduce variations before execution accelerates.",
            "Prioritize only the approved critical design changes required to maintain the current schedule.",
        ]
    if category == "execution_and_site_performance":
        return [
            "Strengthen site supervision and create a milestone-based execution review.",
            "Rebalance manpower and equipment deployment to critical work fronts.",
            "Track daily productivity gaps and align field resources to the bottleneck activities.",
        ]
    return [
        "Set up an inter-agency coordination meeting with a clear escalation path for unresolved issues.",
        "Establish a governance dashboard with owners, due dates, and escalation triggers.",
        "Resolve interfaces between agencies and stakeholders through weekly review cycles.",
    ]


def generate_mitigation_strategies(questionnaire: Dict[str, object]) -> Dict[str, object]:
    scored = score_questionnaire(questionnaire)
    category = scored["dominant_reason"]
    strategies = _mitigation_for_category(category)

    return {
        "dominant_reason": category,
        "dominant_reason_label": CATEGORY_DESCRIPTIONS.get(category, category),
        "score_summary": scored,
        "strategies": strategies,
    }


if __name__ == "__main__":
    sample = {
        "land_acquisition": "major",
        "financial_result": "moderate",
        "approval_clearance": "minor",
        "procurement_result": "major",
        "scope_design": "minor",
        "execution_pace": "major",
        "interagency_coordination": "moderate",
    }
    print(score_questionnaire(sample))
    print(generate_mitigation_strategies(sample))
