"""
CSIT332 Component C - Week 2 Task 2

Version A uses sample-size-specific truth.
Version B uses asymptotic truth.

Input files:
    data/reference_results.csv
    data/reference_truth.csv

Run:
    python task2_compare_truth.py

Output files:
    task2_per_replicate.csv
    task2_summary.csv

Tie rule:
    If classifiers share the highest mean AUC, choose the
    alphabetically first classifier as the declared winner.
    A tied replicate is counted as incorrect for both versions.
"""

from pathlib import Path
import pandas as pd


# File locations
FOLDER = Path(__file__).resolve().parent.parent

RESULTS_FILE = FOLDER / "data" / "reference_results.csv"
TRUTH_FILE = FOLDER / "data" / "reference_truth.csv"

DETAILS_FILE = FOLDER / "data" / "task2_per_replicate.csv"
SUMMARY_FILE = FOLDER / "data" / "task2_summary.csv"

SAMPLE_SIZES = [50, 100, 200, 500]
EXPECTED_REPLICATES = 100


def main():
    # Read the input files
    results = pd.read_csv(RESULTS_FILE)
    truth = pd.read_csv(TRUTH_FILE)

    # Check that the required columns are present
    results_columns = {
        "n_sub", "replicate_id", "classifier_id", "fold_id", "auc"
    }
    truth_columns = {"classifier_id", "n_sub", "true_auc"}

    if not results_columns.issubset(results.columns):
        missing = results_columns - set(results.columns)
        raise ValueError(f"Missing columns in results file: {missing}")

    if not truth_columns.issubset(truth.columns):
        missing = truth_columns - set(truth.columns)
        raise ValueError(f"Missing columns in truth file: {missing}")

    # Make a lookup table for the true AUC of each classifier
    truth["n_key"] = truth["n_sub"].astype(str).str.strip()
    true_auc = {}

    for _, row in truth.iterrows():
        key = (row["n_key"], row["classifier_id"])
        true_auc[key] = float(row["true_auc"])

    classifiers = sorted(truth["classifier_id"].unique())

    # Find the best classifier using asymptotic truth
    asymptotic_auc = {}
    for classifier in classifiers:
        key = ("asymptotic", classifier)
        if key not in true_auc:
            raise ValueError(f"Missing asymptotic truth for {classifier}")
        asymptotic_auc[classifier] = true_auc[key]

    best_asymptotic = max(
        classifiers, key=lambda classifier: asymptotic_auc[classifier]
    )

    replicate_rows = []

    # Calculate results separately for each sample size
    for n in SAMPLE_SIZES:
        truth_at_n = {}

        for classifier in classifiers:
            key = (str(n), classifier)
            if key not in true_auc:
                raise ValueError(
                    f"Missing truth for classifier {classifier} at n={n}"
                )
            truth_at_n[classifier] = true_auc[key]

        # Find the best classifier at this sample size
        best_at_n = max(
            classifiers, key=lambda classifier: truth_at_n[classifier]
        )

        results_at_n = results[results["n_sub"] == n]
        replicate_ids = sorted(results_at_n["replicate_id"].unique())

        if len(replicate_ids) != EXPECTED_REPLICATES:
            raise ValueError(
                f"Expected {EXPECTED_REPLICATES} replicates at n={n}, "
                f"but found {len(replicate_ids)}"
            )

        for replicate_id in replicate_ids:
            one_replicate = results_at_n[
                results_at_n["replicate_id"] == replicate_id
            ]

            # Calculate the mean AUC across folds for each classifier
            mean_auc = one_replicate.groupby("classifier_id")["auc"].mean().to_dict()

            missing = set(classifiers) - set(mean_auc)
            if missing:
                raise ValueError(
                    f"Missing classifiers {missing} at n={n}, "
                    f"replicate={replicate_id}"
                )

            # Select the classifier with the highest mean AUC
            highest_auc = max(mean_auc[classifier] for classifier in classifiers)
            winners = sorted(
                classifier for classifier in classifiers
                if abs(mean_auc[classifier] - highest_auc) < 1e-12
            )

            winner = winners[0]
            has_tie = len(winners) > 1

            # A tied replicate is counted as incorrect for both versions
            correct_a = not has_tie and winner == best_at_n
            correct_b = not has_tie and winner == best_asymptotic

            row = {
                "n_sub": int(n),
                "replicate_id": int(replicate_id),
                "declared_winner": winner,
                "winner_mean_cv_auc": mean_auc[winner],
                "observed_winner_tie": has_tie,
                "best_classifier_at_n": best_at_n,
                "best_classifier_asymptotic": best_asymptotic,
                "winner_correct_A": int(correct_a),
                "winner_correct_B": int(correct_b),
                "winner_true_auc_at_n": truth_at_n[winner],
                "winner_asymptotic_true_auc": asymptotic_auc[winner],
                "optimism_A": mean_auc[winner] - truth_at_n[winner],
                "optimism_B": mean_auc[winner] - asymptotic_auc[winner],
            }

            # Save each classifier's mean AUC as an extra column
            for classifier in classifiers:
                row[f"mean_auc_{classifier}"] = mean_auc[classifier]

            replicate_rows.append(row)

    # Save one row per replicate
    per_replicate = pd.DataFrame(replicate_rows)

    # Create one summary row for each sample size
    summary_rows = []

    for n, group in per_replicate.groupby("n_sub", sort=True):
        summary_rows.append({
            "n_sub": int(n),
            "replicates": len(group),
            "best_classifier_at_n": group["best_classifier_at_n"].iloc[0],
            "best_classifier_asymptotic":
                group["best_classifier_asymptotic"].iloc[0],
            "winner_correct_rate_A": group["winner_correct_A"].mean(),
            "winner_correct_rate_B": group["winner_correct_B"].mean(),
            "mean_optimism_A": group["optimism_A"].mean(),
            "mean_optimism_B": group["optimism_B"].mean(),
            "observed_tie_replicates":
                int(group["observed_winner_tie"].sum()),
        })

    summary = pd.DataFrame(summary_rows)

    # Write both output files
    per_replicate.to_csv(DETAILS_FILE, index=False, float_format="%.6f")
    summary.to_csv(SUMMARY_FILE, index=False, float_format="%.6f")

    print(f"Saved replicate results to {DETAILS_FILE.name}")
    print(f"Saved summary results to {SUMMARY_FILE.name}")
    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
