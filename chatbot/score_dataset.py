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
