#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv(
    "../data/processed/merged_projects.csv",
    low_memory=False
)

print("Shape:", df.shape)
print(df.head())


# In[2]:


print("Before removing duplicates:", df.shape)

df = df.drop_duplicates().copy()

print("After removing duplicates:", df.shape)


# In[3]:


project_counts = df["project_code"].value_counts()

print("Unique projects:", df["project_code"].nunique())
print("\nProject observation statistics:")
print(project_counts.describe())

print("\nMost frequent projects:")
print(project_counts.head(10))


# In[4]:


target = "cost_overrun_pct"

print(df[target].describe())
print("\nMissing target values:", df[target].isna().sum())


# In[5]:


df = df.dropna(subset=[target]).copy()

print("Shape after removing missing target:", df.shape)


# In[6]:


plt.figure(figsize=(10, 5))

df["cost_overrun_pct"].hist(bins=50)

plt.xlabel("Cost Overrun (%)")
plt.ylabel("Number of Observations")
plt.title("Distribution of Cost Overrun")

plt.show()

print("Negative overrun:", (df["cost_overrun_pct"] < 0).sum())
print("Zero overrun:", (df["cost_overrun_pct"] == 0).sum())
print("Positive overrun:", (df["cost_overrun_pct"] > 0).sum())


# In[7]:


features = [
    "project_code",
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
    "negative_expenditure_flag",
    "cost_overrun_pct"
]

df_model = df[features].copy()

print("df_model shape:", df_model.shape)
print("\nColumns:")
print(df_model.columns.tolist())


# In[8]:


# Target
y = df_model["cost_overrun_pct"].copy()

# Features
X = df_model.drop(columns=["cost_overrun_pct", "project_code"]).copy()

print("X shape:", X.shape)
print("y shape:", y.shape)


# In[9]:


date_columns = [
    "date_of_approval",
    "start_date",
    "target_doc"
]

# Convert dates
for col in date_columns:
    X[col] = pd.to_datetime(X[col], errors="coerce")

# Extract useful date features
X["approval_year"] = X["date_of_approval"].dt.year
X["approval_month"] = X["date_of_approval"].dt.month

X["start_year"] = X["start_date"].dt.year
X["start_month"] = X["start_date"].dt.month

X["target_year"] = X["target_doc"].dt.year
X["target_month"] = X["target_doc"].dt.month

# Planned project duration
X["planned_duration_days"] = (
    X["target_doc"] - X["start_date"]
).dt.days

# Remove original date columns
X = X.drop(columns=date_columns)

print("X shape:", X.shape)
print(X.head())


# In[10]:


categorical_features = X.select_dtypes(
    include=["object"]
).columns.tolist()

numeric_features = X.select_dtypes(
    include=["number", "bool"]
).columns.tolist()

print("Categorical features:")
print(categorical_features)

print("\nNumerical features:")
print(numeric_features)

print("\nNumber of categorical features:", len(categorical_features))
print("Number of numerical features:", len(numeric_features))


# In[11]:


groups = df_model["project_code"].astype(str)

print("Unique projects:", groups.nunique())


# In[12]:


from sklearn.model_selection import GroupShuffleSplit

gss = GroupShuffleSplit(
    n_splits=1,
    test_size=0.20,
    random_state=42
)

train_idx, test_idx = next(
    gss.split(X, y, groups=groups)
)

X_train = X.iloc[train_idx].copy()
X_test = X.iloc[test_idx].copy()

y_train = y.iloc[train_idx].copy()
y_test = y.iloc[test_idx].copy()

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)
print("y_train:", y_train.shape)
print("y_test :", y_test.shape)


# In[13]:


train_projects = set(groups.iloc[train_idx])
test_projects = set(groups.iloc[test_idx])

overlap = train_projects.intersection(test_projects)

print("Training projects:", len(train_projects))
print("Testing projects:", len(test_projects))
print("Overlapping projects:", len(overlap))


# In[14]:


from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

# Numerical preprocessing
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median"))
])

# Categorical preprocessing
categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# Combine preprocessing
preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

print("Preprocessor created successfully.")


# In[15]:


from xgboost import XGBRegressor

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1
)

print("XGBoost model created successfully.")


# In[16]:


pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", model)
])

print("Complete pipeline created successfully.")


# In[17]:


pipeline.fit(X_train, y_train)

print("Model training completed successfully.")


# In[18]:


y_pred = pipeline.predict(X_test)

print("Predictions generated successfully.")
print("Number of predictions:", len(y_pred))


# In[19]:


from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("Model Performance")
print("-----------------")
print("R²   :", r2)
print("MAE  :", mae)
print("RMSE :", rmse)


# In[20]:


plt.figure(figsize=(8, 6))

plt.scatter(y_test, y_pred, alpha=0.5)

plt.xlabel("Actual Cost Overrun (%)")
plt.ylabel("Predicted Cost Overrun (%)")
plt.title("Actual vs Predicted Cost Overrun")

plt.show()


# In[21]:


feature_names = pipeline.named_steps[
    "preprocessor"
].get_feature_names_out()

importances = pipeline.named_steps[
    "model"
].feature_importances_

feature_importance = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(
    "importance",
    ascending=False
)

print(feature_importance.head(20))


# In[22]:


import os

os.makedirs("../data/models", exist_ok=True)


# In[23]:


import joblib

joblib.dump(
    pipeline,
    "../data/models/cost_model.pkl"
)

print("Model saved successfully.")


# In[24]:


import json

metrics = {
    "r2": float(r2),
    "mae": float(mae),
    "rmse": float(rmse)
}

with open(
    "../data/models/cost_model_metrics.json",
    "w"
) as f:
    json.dump(metrics, f, indent=4)

print("Metrics saved successfully.")
print(metrics)


# In[25]:


print("R²:", r2)
print("MAE:", mae)
print("RMSE:", rmse)


# In[26]:


import os

print(os.path.exists("../data/models/cost_model.pkl"))
print(os.path.exists("../data/models/cost_model_metrics.json"))


# In[29]:


# ============================================================
# NEW PROJECT - COST OVERRUN PREDICTION
# ============================================================

import pandas as pd
import numpy as np

print("===================================")
print("   NEW PROJECT COST PREDICTION")
print("===================================")

# ------------------------------------------------------------
# 1. USER INPUTS
# ------------------------------------------------------------

original_cost = float(
    input("Enter original project cost (₹ crore): ")
)

cumulative_expenditure = float(
    input("Enter cumulative expenditure (₹ crore): ")
)

physical_progress = float(
    input("Enter physical progress (%): ")
)

agency = input("Enter agency: ")
state = input("Enter state: ")
ministry = input("Enter ministry: ")
sector = input("Enter sector: ")

status = input(
    "Enter project status (e.g. Ongoing): "
)

date_of_approval = input(
    "Enter date of approval (YYYY-MM-DD): "
)

start_date = input(
    "Enter project start date (YYYY-MM-DD): "
)

target_doc = input(
    "Enter target completion date (YYYY-MM-DD): "
)


# ------------------------------------------------------------
# 2. CALCULATE DERIVED FEATURES
# ------------------------------------------------------------

# Expenditure / original cost ratio
if original_cost != 0:
    expenditure_to_original_cost_ratio = (
        cumulative_expenditure / original_cost
    )
else:
    expenditure_to_original_cost_ratio = 0


# Expenditure-progress mismatch
expenditure_progress_mismatch = (
    expenditure_to_original_cost_ratio
    - (physical_progress / 100)
)


# High-spend / low-progress flag
if (
    expenditure_to_original_cost_ratio > 0.80
    and physical_progress < 50
):
    high_spend_low_progress_flag = 1
else:
    high_spend_low_progress_flag = 0


# Negative expenditure flag
if cumulative_expenditure < 0:
    negative_expenditure_flag = 1
else:
    negative_expenditure_flag = 0


# ------------------------------------------------------------
# 3. CREATE INPUT DATAFRAME
# ------------------------------------------------------------

new_project = pd.DataFrame([{
    "original_cost_cr": original_cost,

    "cumulative expenditure in rs. crore":
        cumulative_expenditure,

    "physical progress (in percentage)":
        physical_progress,

    "agency": agency,
    "state": state,
    "ministry": ministry,
    "sector": sector,
    "status": status,

    "date_of_approval": date_of_approval,
    "start_date": start_date,
    "target_doc": target_doc,

    "expenditure_to_original_cost_ratio":
        expenditure_to_original_cost_ratio,

    "expenditure_progress_mismatch":
        expenditure_progress_mismatch,

    "high_spend_low_progress_flag":
        high_spend_low_progress_flag,

    "negative_expenditure_flag":
        negative_expenditure_flag
}])


# ------------------------------------------------------------
# 4. DATE FEATURES
# ------------------------------------------------------------

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


# Missingness indicators
new_project["date_of_approval_is_missing"] = (
    new_project["date_of_approval"].isna().astype(int)
)

new_project["start_date_is_missing"] = (
    new_project["start_date"].isna().astype(int)
)

new_project["target_doc_is_missing"] = (
    new_project["target_doc"].isna().astype(int)
)

# These were missing in a new project because they are
# post-outcome fields and are not entered by the user.
new_project["actual_doc_is_missing"] = 1
new_project["revised_doc_is_missing"] = 1
new_project["revised_cost_cr_is_missing"] = 1


# Ministry missing indicator
new_project["ministry_is_missing"] = (
    new_project["ministry"].isna().astype(int)
)


# Date-derived features
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


# Remove original date columns
new_project = new_project.drop(
    columns=[
        "date_of_approval",
        "start_date",
        "target_doc"
    ]
)


# ------------------------------------------------------------
# 5. MATCH THE TRAINED MODEL'S FEATURES
# ------------------------------------------------------------

expected_features = pipeline.named_steps[
    "preprocessor"
].feature_names_in_

for column in expected_features:
    if column not in new_project.columns:
        new_project[column] = np.nan

new_project = new_project[
    expected_features
]


# ------------------------------------------------------------
# 6. MAKE XGBOOST PREDICTION
# ------------------------------------------------------------

predicted_overrun = pipeline.predict(
    new_project
)[0]


# ------------------------------------------------------------
# 7. CALCULATE ESTIMATED COST
# ------------------------------------------------------------

# Uses whatever ORIGINAL COST the user entered.
estimated_overrun = (
    original_cost
    * predicted_overrun
    / 100
)

estimated_revised_cost = (
    original_cost
    + estimated_overrun
)


# ------------------------------------------------------------
# 8. DISPLAY RESULTS
# ------------------------------------------------------------

print("\n===================================")
print("       COST OVERRUN PREDICTION")
print("===================================")

print(
    f"Original Cost: ₹{original_cost:.2f} crore"
)

print(
    f"Predicted Cost Overrun: "
    f"{predicted_overrun:.2f}%"
)

print(
    f"Estimated Additional Cost: "
    f"₹{estimated_overrun:.2f} crore"
)

print(
    f"Estimated Revised Cost: "
    f"₹{estimated_revised_cost:.2f} crore"
)

print("===================================")


# In[1]:


import pandas as pd

test_data = [
    {
        "original_cost_cr": 300,
        "cumulative expenditure in rs. crore": 120,
        "physical progress (in percentage)": 40,
        "agency": "Airport Authority of India",
        "state": "Andhra Pradesh",
        "ministry": "Ministry of Civil Aviation",
        "sector": "Transport",
        "status": "Ongoing",
        "date_of_approval": "2023-01-15",
        "start_date": "2023-06-01",
        "target_doc": "2027-06-01"
    },
    {
        "original_cost_cr": 500,
        "cumulative expenditure in rs. crore": 350,
        "physical progress (in percentage)": 60,
        "agency": "NHAI",
        "state": "Maharashtra",
        "ministry": "Ministry of Road Transport and Highways",
        "sector": "Transport",
        "status": "Ongoing",
        "date_of_approval": "2022-04-10",
        "start_date": "2022-10-01",
        "target_doc": "2026-10-01"
    },
    {
        "original_cost_cr": 1000,
        "cumulative expenditure in rs. crore": 700,
        "physical progress (in percentage)": 55,
        "agency": "CPWD",
        "state": "Delhi",
        "ministry": "Ministry of Housing and Urban Affairs",
        "sector": "Urban Development",
        "status": "Ongoing",
        "date_of_approval": "2021-03-20",
        "start_date": "2021-09-01",
        "target_doc": "2027-09-01"
    }
]

test_df = pd.DataFrame(test_data)

# Save as CSV
test_df.to_csv("test_cost_data.csv", index=False)

print("CSV file created successfully!")
print(test_df)


# In[3]:


# ============================================================
# RECREATE TEST SET AND SAVE THE 20% TEST DATA
# ============================================================

import pandas as pd
import os
from sklearn.model_selection import GroupShuffleSplit

# ------------------------------------------------------------
# 1. LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(
    "../data/processed/merged_projects.csv",
    low_memory=False
)

# Remove exact duplicate rows
df = df.drop_duplicates().copy()

print("Dataset shape:", df.shape)


# ------------------------------------------------------------
# 2. CREATE MODEL DATA
# ------------------------------------------------------------

# Keep only rows where target is available
df_model = df.dropna(
    subset=["cost_overrun_pct"]
).copy()

print("Rows available for modelling:", len(df_model))


# ------------------------------------------------------------
# 3. CREATE X AND Y
# ------------------------------------------------------------

features = [
    "project_code",
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
    "negative_expenditure_flag",
    "cost_overrun_pct"
]

X = df_model[
    features
].copy()

y = df_model[
    "cost_overrun_pct"
].copy()


# ------------------------------------------------------------
# 4. REMOVE TARGET FROM X
# ------------------------------------------------------------

X = X.drop(
    columns=["cost_overrun_pct"]
)


# ------------------------------------------------------------
# 5. REMOVE PROJECT CODE FROM MODEL FEATURES
# ------------------------------------------------------------

groups = df_model[
    "project_code"
].astype(str)

X = X.drop(
    columns=["project_code"]
)


# ------------------------------------------------------------
# 6. DATE FEATURE ENGINEERING
# ------------------------------------------------------------

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

X["approval_year"] = (
    X["date_of_approval"].dt.year
)

X["approval_month"] = (
    X["date_of_approval"].dt.month
)

X["start_year"] = (
    X["start_date"].dt.year
)

X["start_month"] = (
    X["start_date"].dt.month
)

X["target_year"] = (
    X["target_doc"].dt.year
)

X["target_month"] = (
    X["target_doc"].dt.month
)

X["planned_duration_days"] = (
    X["target_doc"]
    - X["start_date"]
).dt.days

X = X.drop(
    columns=date_columns
)


# ------------------------------------------------------------
# 7. PROJECT-LEVEL 80/20 SPLIT
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 8. GET ORIGINAL TEST ROWS
# ------------------------------------------------------------

test_data = df_model.iloc[
    test_idx
].copy()


# ------------------------------------------------------------
# 9. CREATE TEST FOLDER
# ------------------------------------------------------------

os.makedirs(
    "../data/test",
    exist_ok=True
)


# ------------------------------------------------------------
# 10. SAVE TEST CSV
# ------------------------------------------------------------

test_data.to_csv(
    "../data/test/test_cost_data.csv",
    index=False
)


# ------------------------------------------------------------
# 11. DISPLAY RESULTS
# ------------------------------------------------------------

print("\n===================================")
print("       TEST DATA SAVED")
print("===================================")

print(
    f"Training rows: {len(X_train)}"
)

print(
    f"Testing rows: {len(X_test)}"
)

print(
    f"Test projects: "
    f"{groups.iloc[test_idx].nunique()}"
)

print(
    "\nSaved to:"
)

print(
    "../data/test/test_cost_data.csv"
)


# In[4]:


# Create the 20% test data from the same project-level split
test_data = df_model.iloc[test_idx].copy()

test_data.to_csv(
    "../data/test/test_cost_data.csv",
    index=False
)

print("New test CSV created successfully!")
print("Rows:", len(test_data))


# In[ ]:




