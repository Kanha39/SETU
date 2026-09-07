import re
from datetime import datetime

from chatbot.config import RISK_KEYWORDS, DELAY_KEYWORDS, THIS_YEAR_KEYWORDS, STATUS_KEYWORDS
from chatbot.data_loader import SECTORS, STATES, MINISTRIES


def extract_entities(query: str) -> dict:
    q = query.lower()
    entities = {
        "sector": None,
        "state": None,
        "ministry": None,
        "high_risk": False,
        "delayed": False,
        "year": None,
        "status": None,
    }

    for val in SECTORS:
        if val.lower() in q:
            entities["sector"] = val
            break

    for val in STATES:
        if val.lower() in q:
            entities["state"] = val
            break

    for val in MINISTRIES:
        if val.lower() in q:
            entities["ministry"] = val
            break

    if any(kw in q for kw in RISK_KEYWORDS):
        entities["high_risk"] = True

    if any(kw in q for kw in DELAY_KEYWORDS):
        entities["delayed"] = True

    if any(kw in q for kw in THIS_YEAR_KEYWORDS):
        entities["year"] = datetime.now().year
    else:
        year_match = re.search(r"\b(20\d{2})\b", q)
        if year_match:
            entities["year"] = int(year_match.group(1))

    for status_val in STATUS_KEYWORDS:
        if status_val in q:
            entities["status"] = status_val
            break

    return entities
