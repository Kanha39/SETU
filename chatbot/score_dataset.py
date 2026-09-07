"""
One-off batch scoring script: runs Person 2's and Person 3's trained models
against every project in merged_projects.csv and writes the predictions
back into the same file.

Run this once after merged_projects.csv is finalized, and re-run any time
the dataset or the model files change:

    python -m chatbot.score_dataset
"""

from chatbot.config import DATA_PATH, COST_OVERRUN_PRED_COL, DELAY_PRED_COL
from chatbot.data_loader import load_data
from chatbot.model_inference import score_dataframe


def main():
    df = load_data()
    scored = score_dataframe(df)

    cols = [COST_OVERRUN_PRED_COL, DELAY_PRED_COL]
    print(f"Scored {len(scored)} rows.")
    print(scored[cols].describe())

    scored.to_csv(DATA_PATH, index=False)
    print(f"Saved predictions back to {DATA_PATH}")


if __name__ == "__main__":
    main()
