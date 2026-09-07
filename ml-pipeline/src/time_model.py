#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 


# In[5]:


import pandas as pd 

df = pd.read_csv(r"C:\Users\manas\Downloads\ALONE\New folder\new\PAIMANA\ml-pipeline\data\processed\merged_projects.csv")

df.head()


# In[6]:


df.shape


# In[7]:


df.info()
df.columns
df.describe(include="all")
df.isnull().sum()


# In[9]:


df.duplicated().sum()


# In[10]:


df[df.duplicated(keep=False)].head(20)


# In[11]:


df[df.duplicated(keep=False)][["project_code" ,"project_name" ,"status"]].head(10)


# In[12]:


df[df.duplicated()].head(10)


# In[13]:


df[df.duplicated()].shape


# In[15]:


df[df.duplicated()].status.value_counts()


# In[16]:


df[df.duplicated()][["project_code","project_name","date_of_approval" ,"start_date" ,"target_doc","status"]].head(20)


# In[17]:


df.duplicated().sum()


# In[18]:


df.shape


# In[19]:


date_columns = [
    "date_of_approval",
    "start_date",
    "target_doc",
    "revised_doc",
    "actual_doc"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")


# In[20]:


df[date_columns].dtypes


# In[22]:


missing_values = df.isnull().sum()
missing_values[missing_values > 0].sort_values(ascending=False)


# In[23]:


df.groupby("status")[[
    "date_of_approval",
    "start_date",
    "target_doc",
    "revised_doc",
    "actual_doc",
    "revised_cost_cr",
    "ministry"
]].apply(lambda x: x.isnull().sum())


# In[24]:


df[df["state"].isnull()][
    ["project_code", "project_name", "agency", "state"]
]


# In[25]:


df[df["cumulative expenditure in rs. crore"] < 0][
    ["project_code", "project_name",
     "cumulative expenditure in rs. crore", "status"]
]


# In[ ]:


# Data quality issue:
# 2 Ongoing projects have negative cumulative expenditure.
# Values: -4.88 and -0.08 crore.
# As per data dictionary, these are data errors.
# Correction requires source lookup; no automatic imputation applied.


# In[26]:


df[df["revised_cost_cr"] < df["original_cost_cr"]][
    ["project_code", "project_name",
     "original_cost_cr", "revised_cost_cr",
     "cost_overrun_abs_cr", "cost_overrun_pct"]
].head(10)


# In[27]:


# Data quality observation:
# 2,549 projects have revised_cost_cr < original_cost_cr.
# Negative cost overrun is not necessarily an error and may represent
# de-scoping or cost savings. Values are preserved as-is.


# In[28]:


target_columns = [
    "cost_overrun_abs_cr",
    "cost_overrun_pct",
    "delay_actual_days",
    "delay_proxy_days"
]

df[target_columns].info()


# In[29]:


df[target_columns].notnull().sum()


# In[30]:


target_columns = [
    "cost_overrun_abs_cr",
    "cost_overrun_pct",
    "delay_actual_days",
    "delay_proxy_days"
]

df[target_columns].info()


# In[31]:


df[target_columns].notnull().sum()


# In[32]:


leakage_columns = [
    "revised_cost_cr",
    "revised_doc",
    "actual_doc",
    "cumulative expenditure in rs. crore"
]

df[leakage_columns].head()


# In[33]:


df[leakage_columns].isnull().sum()


# In[34]:


leakage_columns = [
    "revised_cost_cr",
    "revised_doc",
    "actual_doc",
    "cumulative expenditure in rs. crore"
]


# In[35]:


df[leakage_columns].isnull().sum()


# In[36]:


df.columns.tolist()


# In[37]:


df.dtypes


# In[38]:


df["delay_actual_days"].value_counts(dropna=False).head(20)


# In[39]:


df["delay_proxy_days"].value_counts(dropna=False).head(20)


# In[40]:


df["delay_actual_days"] = (
    df["delay_actual_days"]
    .str.replace(" days", "", regex=False)
    .astype(float)
)


# In[41]:


df["delay_actual_days"].dtype


# In[42]:


df["delay_proxy_days"] = (
    df["delay_proxy_days"]
    .str.replace(" days", "", regex=False)
    .astype(float)
)


# In[45]:


df[["delay_actual_days","delay_proxy_days"]].dtypes


# In[46]:


numeric_columns = [
    "original_cost_cr",
    "revised_cost_cr",
    "cumulative expenditure in rs. crore",
    "physical progress (in percentage)",
    "cost_overrun_abs_cr",
    "cost_overrun_pct",
    "delay_actual_days",
    "delay_proxy_days"
]

df[numeric_columns].describe().T


# In[47]:


missing_flag_columns = [
    "date_of_approval_is_missing",
    "start_date_is_missing",
    "actual_doc_is_missing",
    "target_doc_is_missing",
    "revised_doc_is_missing",
    "revised_cost_cr_is_missing",
    "ministry_is_missing"
]

df[missing_flag_columns].sum()


# In[48]:


quality_flag_columns = [
    "negative_expenditure_flag",
    "negative_cost_overrun_flag",
    "expenditure_exceeds_revised_cost",
    "high_spend_low_progress_flag"
]

df[quality_flag_columns].sum()


# In[49]:


quality_flag_columns = [
    "negative_expenditure_flag",
    "negative_cost_overrun_flag",
    "expenditure_exceeds_revised_cost",
    "high_spend_low_progress_flag"
]

df[quality_flag_columns].sum()


# In[50]:


quality_flag_columns = [
    "negative_expenditure_flag",
    "negative_cost_overrun_flag",
    "expenditure_exceeds_revised_cost",
    "high_spend_low_progress_flag"
]

df[quality_flag_columns].sum()


# In[51]:


print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("\nData types:")
print(df.dtypes)


# In[52]:


df.head()


# In[54]:


output_path = "../data/processed/merged_projects_cleaned.csv"

df.to_csv(output_path, index=False)

print("Cleaned dataset saved successfully!")
print(output_path)


# In[55]:


import os
print(os.path.exists(output_path))


# In[56]:


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("Scikit-learn imported successfully!")


# In[57]:


# Target
target = "delay_proxy_days"

# Columns that must NOT be used as features
excluded_columns = [
    "delay_proxy_days",
    "delay_actual_days",
    "revised_doc",
    "actual_doc",
    "revised_cost_cr",
    "cumulative expenditure in rs. crore",
    "cost_overrun_abs_cr",
    "cost_overrun_pct",
    "status",
    "project_code",
    "project_name"
]

# Features
X = df.drop(columns=excluded_columns)

# Target
y = df[target]

print("Features shape:", X.shape)
print("Target shape:", y.shape)


# In[58]:


categorical_columns = X.select_dtypes(include=["object"]).columns.tolist()

print("Categorical columns:")
print(categorical_columns)


# In[59]:


from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Numerical columns
numerical_columns = X.select_dtypes(include=["int64", "float64", "bool"]).columns.tolist()

# Preprocessing for categorical columns
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

# Preprocessing for numerical columns
numerical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median"))
])

# Combine preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", numerical_transformer, numerical_columns),
        ("cat", categorical_transformer, categorical_columns)
    ]
)

print("Preprocessing pipeline created successfully!")


# In[60]:


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("X_train:", X_train.shape)
print("X_test:", X_test.shape)
print("y_train:", y_train.shape)
print("y_test:", y_test.shape)


# In[62]:


# Keep only rows where the target is available
model_data = df[df["delay_proxy_days"].notna()].copy()

# Features and target
X = model_data.drop(columns=excluded_columns)
y = model_data["delay_proxy_days"]

print("Model data shape:", model_data.shape)
print("Target missing:", y.isna().sum())


# In[63]:


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("X_train:", X_train.shape)
print("X_test:", X_test.shape)


# In[64]:


rf_model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("model", RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ))
])

rf_model.fit(X_train, y_train)

print("Random Forest model trained successfully!")


# In[65]:


# Make predictions on test data
y_pred = rf_model.predict(X_test)

# Calculate evaluation metrics
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print("Model Performance")
print("------------------")
print("MAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)


# In[66]:


results = pd.DataFrame({
    "Actual Delay (days)": y_test.values,
    "Predicted Delay (days)": y_pred
})

results.head(10)


# In[67]:


# Get feature names after preprocessing
feature_names = rf_model.named_steps["preprocessor"].get_feature_names_out()

# Get feature importance
importances = rf_model.named_steps["model"].feature_importances_

# Create feature importance table
feature_importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importances
}).sort_values("Importance", ascending=False)

feature_importance.head(15)


# In[68]:


model_results = pd.DataFrame({
    "Metric": ["MAE", "RMSE", "R2"],
    "Value": [mae, rmse, r2]
})

model_results


# In[70]:


top_features =feature_importance.head(15)
top_features


# In[71]:


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.4)
plt.xlabel("Actual Delay (days)")
plt.ylabel("Predicted Delay (days)")
plt.title("Actual vs Predicted Delay - Random Forest")
plt.show()


# In[72]:


import joblib

joblib.dump(rf_model, "../data/processed/random_forest_delay_model.pkl")

print("Model saved successfully!")


# In[73]:


import os

print(os.path.exists("../data/processed/merged_projects_cleaned.csv"))
print(os.path.exists("../data/processed/random_forest_delay_model.pkl"))


# In[ ]:




