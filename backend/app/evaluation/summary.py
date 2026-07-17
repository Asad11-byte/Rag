from pathlib import Path

import pandas as pd

# Directory containing this file
BASE_DIR = Path(__file__).resolve().parent

# Input and output files
RESULTS_FILE = BASE_DIR / "results.csv"
SUMMARY_FILE = BASE_DIR / "summary.csv"


def main():

    if not RESULTS_FILE.exists():
        print(f"Error: {RESULTS_FILE} not found.")
        return

    df = pd.read_csv(RESULTS_FILE)

    summary = {
        "Precision@5": df["precision@5"].mean(),
        "Recall@5": df["recall@5"].mean(),
        "MRR": df["rr"].mean(),
        "nDCG@5": df["ndcg@5"].mean(),
    }

    print("\n========== OVERALL PERFORMANCE ==========\n")

    for metric, value in summary.items():
        print(f"{metric:<15}: {value:.3f}")

    summary_df = pd.DataFrame(
        {
            "Metric": list(summary.keys()),
            "Score": list(summary.values()),
        }
    )

    summary_df.to_csv(
        SUMMARY_FILE,
        index=False,
    )

    print(f"\nSummary saved to:\n{SUMMARY_FILE}")


if __name__ == "__main__":
    main()