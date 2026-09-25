import pickle
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from chatbot.config import COST_MODEL_PATH, TIME_MODEL_PATH, COST_OVERRUN_PRED_COL, DELAY_PRED_COL

_cost_model = None
_time_model = None


def _fallback_cost_pred(row: pd.Series) -> float:
    original_cost = float(row.get("original_cost_cr", 0) or 0)
    cumulative = float(row.get("cumulative expenditure in rs. crore", row.get("cumulative_expenditure", 0)) or 0)
    progress = float(row.get("physical progress (in percentage)", row.get("physical_progress", 0)) or 0)

    ratio = cumulative / original_cost if original_cost > 0 else 0.0
    base = max(0.0, (ratio - 0.75) * 100)
    progress_penalty = max(0.0, (50 - progress) * 0.35)
    return round(float(base + progress_penalty), 2)


def _fallback_delay_pred(row: pd.Series) -> float:
    original_cost = float(row.get("original_cost_cr", 0) or 0)
    cumulative = float(row.get("cumulative expenditure in rs. crore", row.get("cumulative_expenditure", 0)) or 0)
    progress = float(row.get("physical progress (in percentage)", row.get("physical_progress", 0)) or 0)

    ratio = cumulative / original_cost if original_cost > 0 else 0.0
    delay = max(0.0, (1 - progress / 100) * 180)
    delay += max(0.0, (ratio - 0.80) * 220)
    return round(float(delay), 2)


def _load_pickle(path: Path):
    if not path.exists():
        return None
    try:
        return joblib.load(path)
    except Exception:
        return None


def get_cost_model():
    global _cost_model
    if _cost_model is None:
        _cost_model = _load_pickle(COST_MODEL_PATH)
    return _cost_model


def get_time_model():
    global _time_model
    if _time_model is None:
        _time_model = _load_pickle(TIME_MODEL_PATH)
    return _time_model


def get_expected_features(model) -> list:
    if hasattr(model, "feature_names_in_"):            # generic sklearn estimator
        return list(model.feature_names_in_)
    if hasattr(model, "get_booster"):                   # xgboost sklearn wrapper
        names = model.get_booster().feature_names
        if names:
            return list(names)
    if hasattr(model, "feature_name_"):                  # lightgbm sklearn wrapper
        return list(model.feature_name_)
    if hasattr(model, "booster_") and hasattr(model.booster_, "feature_name"):
        return list(model.booster_.feature_name())

    raise RuntimeError(
        "Could not automatically determine this model's expected feature "
        "names from the .pkl file. Get the exact feature list (and order) "
        "from Person 2/3 and pass it in manually instead of relying on "
        "get_expected_features()."
    )

def prepare_cost_features(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    # Convert date columns to datetime
    date_columns = [
        "date_of_approval",
        "start_date",
        "target_doc",
    ]

    for col in date_columns:
        if col in data.columns:
            data[col] = pd.to_datetime(data[col], errors="coerce")

    # Date-derived features
    data["approval_year"] = data["date_of_approval"].dt.year
    data["approval_month"] = data["date_of_approval"].dt.month

    data["start_year"] = data["start_date"].dt.year
    data["start_month"] = data["start_date"].dt.month

    data["target_year"] = data["target_doc"].dt.year
    data["target_month"] = data["target_doc"].dt.month

    # Planned project duration
    data["planned_duration_days"] = (
        data["target_doc"] - data["start_date"]
    ).dt.days

    return data

def build_feature_matrix(data: pd.DataFrame, expected_features: list) -> pd.DataFrame:
    
    missing = [f for f in expected_features if f not in data.columns]
    if missing:
        raise ValueError(
            f"Dataset is missing {len(missing)} feature(s) the model expects: "
            f"{missing}. Check the exact feature list/order with Person 2/3."
        )
    return data[expected_features]


def predict_cost_overrun(data: pd.DataFrame) -> np.ndarray:
    model = get_cost_model()

    if model is None:
        return np.array([_fallback_cost_pred(row) for _, row in data.iterrows()])

    data = prepare_cost_features(data)

    features = build_feature_matrix(
        data,
        get_expected_features(model)
    )

    return model.predict(features)


def _prepare_delay_model_inputs(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    if COST_OVERRUN_PRED_COL not in data.columns:
        data[COST_OVERRUN_PRED_COL] = predict_cost_overrun(data)

    if DELAY_PRED_COL not in data.columns:
        data[DELAY_PRED_COL] = np.array([
            _fallback_delay_pred(row) for _, row in data.iterrows()
        ])

    return data


def predict_delay_days(data: pd.DataFrame) -> np.ndarray:
    model = get_time_model()

    if model is None:
        return np.array([_fallback_delay_pred(row) for _, row in data.iterrows()])

    data = _prepare_delay_model_inputs(data)
    features = build_feature_matrix(data, get_expected_features(model))
    return model.predict(features)


def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    scored = df.copy()
    scored[COST_OVERRUN_PRED_COL] = predict_cost_overrun(scored)
    scored = _prepare_delay_model_inputs(scored)
    scored[DELAY_PRED_COL] = predict_delay_days(scored)
    return scored
