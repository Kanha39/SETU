#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv(
    "../data/processed/merged_projects.csv",
    low_memory=False
)

print("Original shape:", df.shape)

# Remove exact duplicate rows
df = df.drop_duplicates().copy()

print("After removing duplicates:", df.shape)

# Show columns
print("\nColumns:")
print(df.columns.tolist())


# In[2]:


# Keep only rows where the target exists
df_model = df.dropna(
    subset=["cost_overrun_pct"]
).copy()

print("Rows used for modelling:", len(df_model))

print("\nTarget summary:")
print(df_model["cost_overrun_pct"].describe())


# In[3]:


features = [
    "original_cost_cr",
    "cumulative expenditure in rs. crore",
    "physical progress (in percentage)",
    "agency",
    "state",
    "ministry",
    "sector",
    "status",
    "date_of_approval",
    "start_date",
    "target_doc",
    "expenditure_to_original_cost_ratio",
    "expenditure_progress_mismatch",
    "high_spend_low_progress_flag",
    "negative_expenditure_flag"
]

X = df_model[features].copy()
y = df_model["cost_overrun_pct"].copy()

print("Number of features:", len(X.columns))
print(X.columns.tolist())


# In[4]:


# Convert dates
date_columns = [
    "date_of_approval",
    "start_date",
    "target_doc"
]

for col in date_columns:
    X[col] = pd.to_datetime(
        X[col],
        errors="coerce"
    )

# Date features
X["approval_year"] = X["date_of_approval"].dt.year
X["approval_month"] = X["date_of_approval"].dt.month

X["start_year"] = X["start_date"].dt.year
X["start_month"] = X["start_date"].dt.month

X["target_year"] = X["target_doc"].dt.year
X["target_month"] = X["target_doc"].dt.month

X["planned_duration_days"] = (
    X["target_doc"] - X["start_date"]
).dt.days

# Additional safe features
X["approval_to_start_days"] = (
    X["start_date"] - X["date_of_approval"]
).dt.days

X["remaining_progress_pct"] = (
    100 - X["physical progress (in percentage)"]
).clip(lower=0)

X["spend_gap_to_progress"] = (
    X["expenditure_to_original_cost_ratio"]
    - X["physical progress (in percentage)"] / 100
)

X["spend_per_progress_point"] = (
    X["cumulative expenditure in rs. crore"]
    /
    X["physical progress (in percentage)"].clip(lower=1)
)

X["log_original_cost"] = np.log1p(
    X["original_cost_cr"].clip(lower=0)
)

X["log_expenditure"] = np.log1p(
    X["cumulative expenditure in rs. crore"].clip(lower=0)
)

# Remove raw date columns
X = X.drop(columns=date_columns)

print("Final number of input features:", len(X.columns))
print(X.columns.tolist())


# In[5]:


categorical_features = [
    "agency",
    "state",
    "ministry",
    "sector",
    "status"
]

for col in categorical_features:
    X[col] = X[col].fillna("Missing").astype(str)

print("Categorical features:")
print(categorical_features)


# In[6]:


from sklearn.model_selection import GroupShuffleSplit

groups = df_model["project_code"].astype(str)

gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_idx, test_idx = next(
    gss.split(
        X,
        y,
        groups=groups
    )
)

X_train = X.iloc[train_idx].copy()
X_test = X.iloc[test_idx].copy()

y_train = y.iloc[train_idx].copy()
y_test = y.iloc[test_idx].copy()

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

print(
    "Training projects:",
    groups.iloc[train_idx].nunique()
)

print(
    "Testing projects:",
    groups.iloc[test_idx].nunique()
)


# In[7]:


get_ipython().run_line_magic('pip', 'install catboost')


# In[8]:


from catboost import CatBoostRegressor


# In[9]:


model = CatBoostRegressor(
    iterations=2000,
    depth=6,
    learning_rate=0.03,
    l2_leaf_reg=5,
    random_strength=1,
    loss_function="RMSE",
    random_seed=42,
    verbose=100,
    thread_count=4
)

model.fit(
    X_train,
    y_train,
    cat_features=categorical_features,
    eval_set=(X_test, y_test),
    early_stopping_rounds=120
)


# In[10]:


from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

print("===================================")
print("       MODEL PERFORMANCE")
print("===================================")

print(f"R²   : {r2:.4f}")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")


# In[12]:


# ============================================================
# CHATBOT-FRIENDLY COST PREDICTION FUNCTION
# ============================================================

def predict_cost_overrun(
    original_cost,
    cumulative_expenditure,
    physical_progress,
    agency,
    state,
    ministry,
    sector,
    status,
    date_of_approval,
    start_date,
    target_doc
):

    # --------------------------------------------------------
    # 1. CREATE INPUT DATAFRAME
    # --------------------------------------------------------

    new_project = pd.DataFrame([{
        "original_cost_cr": original_cost,
        "cumulative expenditure in rs. crore": cumulative_expenditure,
        "physical progress (in percentage)": physical_progress,
        "agency": agency,
        "state": state,
        "ministry": ministry,
        "sector": sector,
        "status": status,
        "date_of_approval": date_of_approval,
        "start_date": start_date,
        "target_doc": target_doc
    }])


    # --------------------------------------------------------
    # 2. DATE CONVERSION
    # --------------------------------------------------------

    new_project["date_of_approval"] = pd.to_datetime(
        new_project["date_of_approval"],
        errors="coerce"
    )

    new_project["start_date"] = pd.to_datetime(
        new_project["start_date"],
        errors="coerce"
    )

    new_project["target_doc"] = pd.to_datetime(
        new_project["target_doc"],
        errors="coerce"
    )


    # --------------------------------------------------------
    # 3. DERIVED FEATURES
    # --------------------------------------------------------

    # Expenditure / original cost
    if original_cost != 0:
        expenditure_ratio = (
            cumulative_expenditure / original_cost
        )
    else:
        expenditure_ratio = 0


    new_project["expenditure_to_original_cost_ratio"] = (
        expenditure_ratio
    )


    # Expenditure-progress mismatch
    new_project["expenditure_progress_mismatch"] = (
        expenditure_ratio
        - physical_progress / 100
    )


    # High-spend / low-progress flag
    new_project["high_spend_low_progress_flag"] = int(
        expenditure_ratio > 0.80
        and physical_progress < 50
    )


    # Negative expenditure flag
    new_project["negative_expenditure_flag"] = int(
        cumulative_expenditure < 0
    )


    # --------------------------------------------------------
    # 4. DATE FEATURES
    # --------------------------------------------------------

    new_project["approval_year"] = (
        new_project["date_of_approval"].dt.year
    )

    new_project["approval_month"] = (
        new_project["date_of_approval"].dt.month
    )

    new_project["start_year"] = (
        new_project["start_date"].dt.year
    )

    new_project["start_month"] = (
        new_project["start_date"].dt.month
    )

    new_project["target_year"] = (
        new_project["target_doc"].dt.year
    )

    new_project["target_month"] = (
        new_project["target_doc"].dt.month
    )

    new_project["planned_duration_days"] = (
        new_project["target_doc"]
        - new_project["start_date"]
    ).dt.days


    # Additional engineered features
    new_project["approval_to_start_days"] = (
        new_project["start_date"]
        - new_project["date_of_approval"]
    ).dt.days

    new_project["remaining_progress_pct"] = (
        100 - new_project["physical progress (in percentage)"]
    ).clip(lower=0)

    new_project["spend_gap_to_progress"] = (
        expenditure_ratio
        - physical_progress / 100
    )

    new_project["spend_per_progress_point"] = (
        cumulative_expenditure
        /
        max(physical_progress, 1)
    )

    new_project["log_original_cost"] = np.log1p(
        max(original_cost, 0)
    )

    new_project["log_expenditure"] = np.log1p(
        max(cumulative_expenditure, 0)
    )


    # --------------------------------------------------------
    # 5. MISSING VALUES / CATEGORICAL VALUES
    # --------------------------------------------------------

    for col in categorical_features:
        new_project[col] = (
            new_project[col]
            .fillna("Missing")
            .astype(str)
        )


    # --------------------------------------------------------
    # 6. REMOVE RAW DATE COLUMNS
    # --------------------------------------------------------

    new_project = new_project.drop(
        columns=[
            "date_of_approval",
            "start_date",
            "target_doc"
        ]
    )


    # --------------------------------------------------------
    # 7. PREDICT
    # --------------------------------------------------------

    predicted_overrun = float(
        model.predict(new_project)[0]
    )


    # --------------------------------------------------------
    # 8. CALCULATE COST IMPACT
    # --------------------------------------------------------

    estimated_additional_cost = (
        original_cost
        * predicted_overrun
        / 100
    )

    estimated_revised_cost = (
        original_cost
        + estimated_additional_cost
    )


    # --------------------------------------------------------
    # 9. RETURN RESULTS
    # --------------------------------------------------------

    return {
        "predicted_cost_overrun_pct": predicted_overrun,
        "estimated_additional_cost_cr": estimated_additional_cost,
        "estimated_revised_cost_cr": estimated_revised_cost
    }


# In[13]:


result = predict_cost_overrun(
    original_cost=300,
    cumulative_expenditure=120,
    physical_progress=40,
    agency="Airport Authority of India",
    state="Andhra Pradesh",
    ministry="Ministry of Civil Aviation",
    sector="Transport",
    status="Ongoing",
    date_of_approval="2023-01-15",
    start_date="2023-06-01",
    target_doc="2027-06-01"
)

print(result)


# In[14]:


# ============================================================
# ENTER PROJECT DETAILS
# ============================================================

original_cost = float(
    input("Original cost (₹ crore): ")
)

cumulative_expenditure = float(
    input("Cumulative expenditure (₹ crore): ")
)

physical_progress = float(
    input("Physical progress (%): ")
)

agency = input("Agency: ")
state = input("State: ")
ministry = input("Ministry: ")
sector = input("Sector: ")
status = input("Status: ")

date_of_approval = input(
    "Date of approval (YYYY-MM-DD): "
)

start_date = input(
    "Start date (YYYY-MM-DD): "
)

target_doc = input(
    "Target completion date (YYYY-MM-DD): "
)


# ============================================================
# SEND USER INPUT TO MODEL
# ============================================================

result = predict_cost_overrun(
    original_cost=original_cost,
    cumulative_expenditure=cumulative_expenditure,
    physical_progress=physical_progress,
    agency=agency,
    state=state,
    ministry=ministry,
    sector=sector,
    status=status,
    date_of_approval=date_of_approval,
    start_date=start_date,
    target_doc=target_doc
)


# ============================================================
# DISPLAY PREDICTION
# ============================================================

print("\n===================================")
print("       COST PREDICTION")
print("===================================")

print(
    f"Original Cost: "
    f"₹{original_cost:.2f} crore"
)

print(
    f"Predicted Cost Overrun: "
    f"{result['predicted_cost_overrun_pct']:.2f}%"
)

print(
    f"Estimated Additional Cost: "
    f"₹{result['estimated_additional_cost_cr']:.2f} crore"
)

print(
    f"Estimated Revised Cost: "
    f"₹{result['estimated_revised_cost_cr']:.2f} crore"
)

print("===================================")


# In[15]:


# ============================================================
# SAVE TRAINED COST MODEL
# ============================================================

import os
import joblib

# Create models folder if it doesn't exist
os.makedirs("../data/models", exist_ok=True)

# Save the trained CatBoost model
joblib.dump(
    model,
    "../data/models/cost_model_v2.pkl"
)

print("Model saved successfully!")
print("../data/models/cost_model_v2.pkl")


# In[16]:


# ============================================================
# SAVE MODEL METRICS
# ============================================================

import json

metrics = {
    "model": "CatBoostRegressor",
    "target": "cost_overrun_pct",
    "r2": float(r2),
    "mae": float(mae),
    "rmse": float(rmse),
    "test_size": 0.20,
    "random_state": 42,
    "split_method": "Project-level GroupShuffleSplit"
}

with open(
    "../data/models/cost_model_v2_metrics.json",
    "w"
) as f:
    json.dump(
        metrics,
        f,
        indent=4
    )

print("Metrics saved successfully!")
print("../data/models/cost_model_v2_metrics.json")


# In[17]:


# ============================================================
# SAVE MODEL SCHEMA
# ============================================================

schema = {
    "model_name": "cost_model_v2",
    "model_type": "CatBoostRegressor",
    "target": "cost_overrun_pct",

    "required_inputs": [
        "original_cost",
        "cumulative_expenditure",
        "physical_progress",
        "agency",
        "state",
        "ministry",
        "sector",
        "status",
        "date_of_approval",
        "start_date",
        "target_doc"
    ],

    "categorical_features": categorical_features,

    "model_features": X.columns.tolist(),

    "outputs": [
        "predicted_cost_overrun_pct",
        "estimated_additional_cost_cr",
        "estimated_revised_cost_cr"
    ],

    "notes": [
        "Predicted cost overrun is a percentage.",
        "Estimated additional cost is calculated from the user's original cost.",
        "Estimated revised cost is original cost plus estimated additional cost.",
        "The model does not use revised_cost_cr as an input feature.",
        "The model does not use cost_overrun_pct as an input feature."
    ]
}

with open(
    "../data/models/cost_model_v2_schema.json",
    "w"
) as f:
    json.dump(
        schema,
        f,
        indent=4
    )

print("Schema saved successfully!")
print("../data/models/cost_model_v2_schema.json")


# In[18]:


# ============================================================
# SAVE PREDICTION RESULT
# ============================================================

import json
import os
from datetime import datetime

prediction_record = {
    "timestamp": datetime.now().isoformat(),

    "inputs": {
        "original_cost_cr": float(original_cost),
        "cumulative_expenditure_cr": float(cumulative_expenditure),
        "physical_progress_pct": float(physical_progress),
        "agency": agency,
        "state": state,
        "ministry": ministry,
        "sector": sector,
        "status": status,
        "date_of_approval": date_of_approval,
        "start_date": start_date,
        "target_doc": target_doc
    },

    "prediction": {
        "predicted_cost_overrun_pct":
            float(result["predicted_cost_overrun_pct"]),

        "estimated_additional_cost_cr":
            float(result["estimated_additional_cost_cr"]),

        "estimated_revised_cost_cr":
            float(result["estimated_revised_cost_cr"])
    }
}

os.makedirs("../data/models", exist_ok=True)

with open(
    "../data/models/cost_predictions.json",
    "w"
) as f:
    json.dump(
        prediction_record,
        f,
        indent=4
    )

print("Prediction saved successfully!")
print("../data/models/cost_predictions.json")


# In[19]:


# ============================================================
# SAVE 20% TEST DATA
# ============================================================

import os

os.makedirs("../data/test", exist_ok=True)

test_data = df_model.iloc[test_idx].copy()

test_data.to_csv(
    "../data/test/test_cost_data.csv",
    index=False
)

print("Test data saved!")
print("Rows:", len(test_data))
print("../data/test/test_cost_data.csv")


# In[ ]:




