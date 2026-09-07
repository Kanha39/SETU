# PAIMANA Cost Overrun Prediction Model

## Overview

This module develops a machine-learning model to predict **cost overrun percentage** for infrastructure projects.

The baseline model uses **XGBoost Regression** and is intended to support early identification of potential cost escalation.

## Cost Overrun Calculation

Historical cost overrun is calculated from original and revised project cost:

    Cost Overrun (₹ crore) = Revised Cost - Original Cost

    Cost Overrun (%) =
        ((Revised Cost - Original Cost) / Original Cost) × 100

Example:

- Original Cost = ₹500 crore
- Revised Cost = ₹600 crore
- Absolute Cost Overrun = ₹100 crore
- Percentage Cost Overrun = 20%

The ML target is:

    cost_overrun_pct

**Important:** `revised_cost_cr` is not used as a model input because it directly determines the target and would cause target leakage.

## Dataset

Input file:

    merged_projects.csv

Initial dataset:

- 18,601 rows
- 34 columns
- 2,369 unique projects
- 3,225 exact duplicate rows
- 218 rows with missing `cost_overrun_pct`

Exact duplicates were removed. Rows with a missing target were excluded from supervised training.

## Features

The model uses relevant project, expenditure, progress, categorical, and date-derived information.

### Numerical/project features

Examples:

- `original_cost_cr`
- `cumulative expenditure in rs. crore`
- `physical progress (in percentage)`
- `expenditure_to_original_cost_ratio`
- `expenditure_progress_mismatch`
- `high_spend_low_progress_flag`
- `negative_expenditure_flag`

### Categorical features

- `agency`
- `state`
- `ministry`
- `sector`

### Date-derived features

- `approval_year`
- `approval_month`
- `start_year`
- `start_month`
- `target_year`
- `target_month`
- `planned_duration_days`

### Excluded leakage/identifier fields

- `cost_overrun_pct` — target
- `revised_cost_cr` — directly determines target
- `cost_overrun_abs_cr` — directly represents the target
- `project_code` — identifier, used only for grouping the train/test split

## Train/Test Strategy

The dataset contains repeated observations for some projects. A random row-level split could put the same project into both training and testing data.

To prevent this, a **project-level GroupShuffleSplit** was used:

- 80% training
- 20% testing
- `project_code` used as the grouping variable
- `random_state = 42`

The split was verified with:

    Overlapping projects: 0

Thus, no project was present in both training and testing groups.

## Preprocessing

A Scikit-learn pipeline combines preprocessing and the model.

### Numerical variables

Missing values are handled using:

    SimpleImputer(strategy="median")

### Categorical variables

Missing values are handled using:

    SimpleImputer(strategy="most_frequent")

Then categorical variables are converted using:

    OneHotEncoder(handle_unknown="ignore")

The preprocessing and XGBoost model are saved together as one reusable pipeline.

## Baseline XGBoost Model

The baseline configuration is:

    XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1
    )

### Parameter meanings

| Parameter | Value | Purpose |
|---|---:|---|
| `n_estimators` | 500 | Number of boosting trees |
| `learning_rate` | 0.05 | Controls each tree's contribution |
| `max_depth` | 6 | Maximum tree depth |
| `subsample` | 0.8 | Fraction of training rows used per tree |
| `colsample_bytree` | 0.8 | Fraction of features used per tree |
| `objective` | `reg:squarederror` | Regression objective |
| `random_state` | 42 | Reproducible results |
| `n_jobs` | -1 | Uses available CPU cores |

## Evaluation

This is a regression problem, so conventional classification accuracy is not used.

Three metrics are calculated:

### R²

Measures how much variation in cost overrun is explained by the model. Higher is better.

Project target:

    R² > 0.65

### MAE

Mean Absolute Error. It measures the average absolute prediction error. Lower is better.

### RMSE

Root Mean Squared Error. It gives more weight to larger errors. Lower is better.

## Baseline Results

The current baseline XGBoost model achieved:

| Metric | Result |
|---|---:|
| R² | 0.5051 |
| MAE | 0.1772 |
| RMSE | 0.6305 |

The baseline is functional, but its R² is below the desired project target of 0.65. Therefore, it should currently be treated as a **baseline**, not the final production model.

## Diagnostics

The notebook includes:

- **Actual vs Predicted plot** — checks how closely predictions follow actual outcomes.
- **Feature importance** — helps identify variables that contribute strongly to model predictions.

## Saved Files

The trained pipeline is saved as:

    data/models/cost_model.pkl

Evaluation metrics are saved as:

    data/models/cost_model_metrics.json

The `.pkl` file contains the preprocessing and XGBoost model together, allowing the backend/website to load the complete prediction pipeline.

## Website Integration

The intended workflow is:

    New Project Data
            ↓
    Saved preprocessing pipeline
            ↓
          XGBoost
            ↓
    Predicted Cost Overrun %
            ↓
    Website / Dashboard
            ↓
    Early Warning / Risk Information

The website should load the trained `cost_model.pkl` rather than retrain the model for each prediction.

The input data supplied to the website model must match the feature structure used during training.

## Important Limitation

The dataset contains repeated observations for projects, but does not provide a clearly defined snapshot/update date for every observation.

Therefore, the model should not automatically be described as a fully time-aware forecasting model. The project-level split prevents the same project from appearing in both train and test sets, but the exact point in a project's lifecycle at which a prediction is made should be defined before production deployment.

## Current Status

Completed:

- Data loading and cleaning
- Duplicate removal
- Missing-target handling
- Target analysis
- Feature selection
- Leakage checks
- Date feature engineering
- Project-level train/test split
- Zero project-overlap verification
- Numerical/categorical preprocessing
- XGBoost baseline training
- Prediction
- R², MAE and RMSE evaluation
- Actual vs predicted analysis
- Feature importance analysis
- Model and metrics saving

Next:

- Tune XGBoost
- Test alternative models in a separate experiment folder if desired
- Compare models using the same leakage-safe project-level split
- Select the best validated model for website integration
