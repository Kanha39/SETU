"""
Loads Person 2's cost-overrun model and Person 3's delay model from their
.pkl files and runs predictions.

Only this file touches the trained model objects. Everything else
(score_dataset.py, risk.py indirectly via the columns it produces) goes
through the functions here.

These files turned out to be full scikit-learn Pipelines (SimpleImputer +
OneHotEncoder + estimator), not bare XGBoost/LightGBM boosters -- so
preprocessing is already bundled in, you don't need a separate encoder from
Person 2/3. Loaded with joblib rather than plain pickle, since that's the
conventional (and in this case necessary) way to persist fitted sklearn
Pipelines with large internal arrays like a fitted OneHotEncoder.
"""

import pickle
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from chatbot.config import COST_MODEL_PATH, TIME_MODEL_PATH, COST_OVERRUN_PRED_COL, DELAY_PRED_COL

_cost_model = None
_time_model = None


def _load_pickle(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"Model file not found at {path}. Copy the .pkl file from "
            f"Person 2/3 into that location, or update the path in config.py."
        )
    try:
        return joblib.load(path)
    except Exception:
        # Fallback for the rare case a model really was saved with plain
        # pickle rather than joblib.
        with open(path, "rb") as f:
            return pickle.load(f)


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
    """Best-effort introspection of the feature names a model was trained
    on, so you don't have to hunt through the training notebook. Tries the
    common attributes across sklearn / XGBoost / LightGBM wrappers and
    fails loudly if none are found, rather than guessing."""
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
    """Create the engineered features used by Person 2's cost model."""
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
    """Align `data`'s columns to exactly what the model expects, in order.
    Raises a clear error listing any missing columns instead of silently
    filling them with 0/NaN, which would produce a wrong prediction with
    no warning."""
    missing = [f for f in expected_features if f not in data.columns]
    if missing:
        raise ValueError(
            f"Dataset is missing {len(missing)} feature(s) the model expects: "
            f"{missing}. Check the exact feature list/order with Person 2/3."
        )
    return data[expected_features]


def predict_cost_overrun(data: pd.DataFrame) -> np.ndarray:
    model = get_cost_model()

    data = prepare_cost_features(data)

    features = build_feature_matrix(
        data,
        get_expected_features(model)
    )

    return model.predict(features)


def predict_delay_days(data: pd.DataFrame) -> np.ndarray:
    model = get_time_model()
    features = build_feature_matrix(data, get_expected_features(model))
    return model.predict(features)


def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Batch-score every row in df and return a copy with the two
    prediction columns added/overwritten. Run this once (see
    score_dataset.py) rather than scoring rows one at a time on every
    chatbot query -- much faster and keeps per-query latency low."""
    scored = df.copy()
    scored[COST_OVERRUN_PRED_COL] = predict_cost_overrun(df)
    scored[DELAY_PRED_COL] = predict_delay_days(df)
    return scored
