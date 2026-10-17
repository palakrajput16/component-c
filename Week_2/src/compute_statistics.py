"""
Component C - Week 2 statistics code (Tasks 1 and 3 in one file)

Reads reference_truth.csv and reference_results.csv from ../data and works
out, for each sample size (n_sub = 50, 100, 200 and 500):

1. winner_correct_rate - how often the classifier with the highest mean
   AUC is the best classifier according to the truth file
2. mean_kendall_tau - how close the observed ranking of classifiers is to
   the true ranking
3. mean_optimism - how much the winning classifier's cross-validated score
   is higher than its own true value
4. power and sign_error_rate - how often a paired t-test between two
   classifiers picks the truly better one (power) or the wrong one (sign
   error)

The truth file has an n_sub column. For each classifier there is a true AUC
at each sample size, and one row where n_sub is the word "asymptotic" (the
value with abundant data). Task 1 uses the asymptotic value. Task 3 uses the
value at each sample size.

How to run (from any folder):

    python compute_statistics.py            runs Task 1 and Task 3
    python compute_statistics.py task1      Task 1: Week 1 definitions
                                            (asymptotic truth) on the
                                            reference files
    python compute_statistics.py task3      Task 3: power for a close pair
                                            and a wide-gap pair

Everything is read from and saved to the data folder next to this one.
Tie rules, fold cleaning, tau and optimism are the same as Week 1, see
Edge_Cases.pdf.
"""

import sys
from pathlib import Path
import pandas as pd
from scipy.stats import kendalltau, ttest_rel

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
TRUTH_PATH = DATA_DIR / "reference_truth.csv"
RESULTS_PATH = DATA_DIR / "reference_results.csv"
EXPECTED_FOLDS = [1, 2, 3, 4, 5]


# ---------------------------------------------------------------------
# Loading and small helpers
# ---------------------------------------------------------------------

def load_truth():
    """
    Load truth values by sample size and classifier.
    Returns true_auc, a dictionary keyed by (n_sub as text, classifier),
    for example true_auc[("50", "gb")] or true_auc[("asymptotic", "gb")],
    plus the asymptotic values on their own and the list of classifiers.
    """
    # n_sub holds numbers AND the word "asymptotic", so read it as text
    truth = pd.read_csv(TRUTH_PATH, dtype={"n_sub": str})

    true_auc = {}
    for _, row in truth.iterrows():
        classifier = row["classifier_id"]
        n_sub = str(row["n_sub"]).strip()
        true_auc[(n_sub, classifier)] = row["true_auc"]

    classifiers = sorted(truth["classifier_id"].unique())

    asymptotic_auc = {
        classifier: true_auc[("asymptotic", classifier)]
        for classifier in classifiers
    }

    return true_auc, asymptotic_auc, classifiers


def truth_for(true_auc, classifiers, which):
    """
    One kind of truth as a simple {classifier: true_auc} dictionary.
    `which` is a sample size like 50, or the word "asymptotic".
    """
    return {c: true_auc[(str(which), c)] for c in classifiers}


def find_true_best(truth_dict):
    """Return the true best classifier and whether there is a tie for it."""
    best_value = max(truth_dict.values())
    best_classifiers = sorted([c for c in truth_dict if truth_dict[c] == best_value])
    return best_classifiers[0], len(best_classifiers) > 1


def pick_power_pair(truth_dict):
    """The two classifiers with the highest true AUC, truly better one first."""
    ranked = sorted(truth_dict, key=lambda c: truth_dict[c], reverse=True)
    return (ranked[0], ranked[1])


def get_mean_auc(rep_data, classifiers):
    """
    Work out the mean AUC for each classifier in one replicate.

    Cleans the data up first:
      - if the same fold number shows up twice for a classifier, only the
        first one is used
      - fold numbers outside 1-5 are ignored
      - rows with a missing auc value are ignored

    Returns a dictionary like {"gb": 0.81, "svm": 0.83}. A classifier is
    left out of the dictionary entirely if it has zero usable folds.
    """
    means = {}

    for c in classifiers:
        c_rows = rep_data[rep_data["classifier_id"] == c]

        seen_folds = []
        good_values = []

        for _, row in c_rows.iterrows():
            fold = row["fold_id"]
            auc = row["auc"]

            if fold in seen_folds:
                continue  # already saw this fold number, skip the duplicate
            seen_folds.append(fold)

            if fold not in EXPECTED_FOLDS:
                continue  # not a fold number we expect

            if pd.isna(auc):
                continue  # missing value

            good_values.append(auc)

        if len(good_values) > 0:
            means[c] = sum(good_values) / len(good_values)

    return means


def get_paired_folds(rep_data, classifier_a, classifier_b):
    """
    Match up classifier_a's and classifier_b's fold scores by fold_id, so
    fold 1 of A is paired with fold 1 of B, and so on. Drops duplicate
    fold rows, fold numbers outside 1-5, and any fold missing a value for
    either classifier. Returns two lists of the same length.
    """
    a_rows = rep_data[rep_data["classifier_id"] == classifier_a].drop_duplicates("fold_id")
    b_rows = rep_data[rep_data["classifier_id"] == classifier_b].drop_duplicates("fold_id")

    merged = pd.merge(a_rows, b_rows, on="fold_id", suffixes=("_a", "_b"))
    merged = merged[merged["fold_id"].isin(EXPECTED_FOLDS)]
    merged = merged.dropna(subset=["auc_a", "auc_b"])

    return list(merged["auc_a"]), list(merged["auc_b"])


# ---------------------------------------------------------------------
# The four quantities for one sample size (Task 1)
# ---------------------------------------------------------------------

def compute_stats(df, true_auc, classifiers, true_best, truth_tie, pair, detail_rows=None):
    """
    Compute all four statistics for one sample size.
    true_auc is a {classifier: value} dictionary (see truth_for).
    pair = (truly better classifier, truly worse classifier)
    detail_rows: optional list. If you pass one, a line describing every
    replicate is added to it, so you can see where the averages come from.
    """

    winner_correct = []
    tie_count = 0
    truth_tie_skipped = 0
    tau_list = []
    optimism_list = []
    detections = []
    dropped_replicates = 0

    for rep_id, rep_data in df.groupby("replicate_id"):

        mean_auc = get_mean_auc(rep_data, classifiers)

        # if any classifier has no usable folds, we can't compare it to
        # the others, so skip this replicate entirely
        if len(mean_auc) < len(classifiers):
            dropped_replicates += 1
            continue

        row = {"replicate_id": rep_id}
        for c in classifiers:
            row["mean_auc_" + c] = round(mean_auc[c], 6)

        # who has the highest mean AUC? (there may be more than one)
        # the 12 decimal places only guard against tiny floating point
        # noise, it is not display rounding
        best_value = max(round(v, 12) for v in mean_auc.values())
        top_classifiers = sorted([c for c in mean_auc if round(mean_auc[c], 12) == best_value])

        if truth_tie:
            # the truth file has no single best classifier, so we can't say
            # whether this replicate got the "right" winner
            truth_tie_skipped += 1
            winner = top_classifiers[0]
            row["winner_correct"] = "skipped_truth_tie"
        elif len(top_classifiers) > 1:
            tie_count += 1
            winner_correct.append(0)  # a tie is never counted as correct
            winner = top_classifiers[0]  # alphabetical, only used for optimism
            row["winner_correct"] = 0
        else:
            winner = top_classifiers[0]
            winner_correct.append(1 if winner == true_best else 0)
            row["winner_correct"] = 1 if winner == true_best else 0

        row["winner"] = winner
        row["tied_for_first"] = " ".join(top_classifiers) if len(top_classifiers) > 1 else ""

        # Kendall's tau: compare the observed order to the true order
        observed_rank = pd.Series(mean_auc).rank(ascending=False)
        true_rank = pd.Series({c: -true_auc[c] for c in mean_auc}).rank()
        tau, _ = kendalltau(observed_rank, true_rank)
        tau_list.append(tau)
        row["kendall_tau"] = round(tau, 6)

        # optimism: winner's own cross-validated score minus its own true value
        optimism_list.append(mean_auc[winner] - true_auc[winner])
        row["optimism"] = round(mean_auc[winner] - true_auc[winner], 6)

        # power: paired t-test between the two named classifiers
        better, worse = pair
        folds_better, folds_worse = get_paired_folds(rep_data, better, worse)

        if len(folds_better) < 2:
            detections.append("not_enough_data")
            row["p_value"] = ""
            row["power_result"] = "not_enough_data"
            if detail_rows is not None:
                detail_rows.append(row)
            continue

        t_stat, p_value = ttest_rel(folds_better, folds_worse)
        diff = sum(a - b for a, b in zip(folds_better, folds_worse)) / len(folds_better)

        if p_value < 0.05 and diff > 0:
            detections.append("correct")
        elif p_value < 0.05 and diff < 0:
            detections.append("sign_error")
        else:
            detections.append("no_detection")

        row["p_value"] = round(p_value, 6)
        row["power_result"] = detections[-1]
        if detail_rows is not None:
            detail_rows.append(row)

    n_power = len([d for d in detections if d != "not_enough_data"])

    return {
        "n_classifiers": len(classifiers),
        "replicates_dropped": dropped_replicates,
        "ties_observed": tie_count,
        "truth_has_a_tie": truth_tie,
        "replicates_skipped_for_truth_tie": truth_tie_skipped,
        "winner_correct_rate": (sum(winner_correct) / len(winner_correct)) if winner_correct else None,
        "mean_kendall_tau": (sum(tau_list) / len(tau_list)) if tau_list else None,
        "mean_optimism": (sum(optimism_list) / len(optimism_list)) if optimism_list else None,
        "power": (detections.count("correct") / n_power) if n_power else None,
        "sign_error_rate": (detections.count("sign_error") / n_power) if n_power else None,
    }


# ---------------------------------------------------------------------
# Power for one named pair at one sample size (Task 3)
# ---------------------------------------------------------------------

def compute_pair_power(df, true_auc, classifiers, pair, n_sub):
    """
    Calculate power and sign-error rate for one pair and sample size.
    true_auc here is the full dictionary keyed by (n_sub as text, classifier),
    because which classifier is genuinely better is decided at this n_sub.
    """
    c1, c2 = pair
    true_auc_1 = true_auc[(str(n_sub), c1)]
    true_auc_2 = true_auc[(str(n_sub), c2)]

    # Determine the genuinely better classifier at this sample size.
    if true_auc_1 == true_auc_2:
        raise ValueError(
            f"The selected pair has tied true AUCs at n={n_sub}."
        )

    true_better = c1 if true_auc_1 > true_auc_2 else c2

    correct = 0
    sign_errors = 0
    valid_tests = 0
    no_detection = 0
    insufficient_data = 0

    for _, rep_data in df.groupby("replicate_id"):
        folds_1, folds_2 = get_paired_folds(rep_data, c1, c2)

        if len(folds_1) < 2:
            insufficient_data += 1
            continue

        _, p_value = ttest_rel(folds_1, folds_2)
        observed_diff = sum(
            a - b for a, b in zip(folds_1, folds_2)
        ) / len(folds_1)

        valid_tests += 1

        if p_value < 0.05 and observed_diff != 0:
            observed_better = c1 if observed_diff > 0 else c2

            if observed_better == true_better:
                correct += 1
            else:
                sign_errors += 1
        else:
            no_detection += 1

    return {
        "sample_size": n_sub,
        "pair": f"{c1} vs {c2}",
        "true_auc_gap": abs(true_auc_1 - true_auc_2),
        "true_better": true_better,
        "power": correct / valid_tests if valid_tests else None,
        "sign_error_rate": (
            sign_errors / valid_tests if valid_tests else None
        ),
        "no_detection": no_detection,
        "insufficient_data": insufficient_data,
        "valid_tests": valid_tests,
    }


# ---------------------------------------------------------------------
# The tasks
# ---------------------------------------------------------------------

def run_task1(df, true_auc, classifiers):
    """Task 1: the Week 1 definitions (asymptotic truth) on the reference files."""
    truth = truth_for(true_auc, classifiers, "asymptotic")
    true_best, truth_tie = find_true_best(truth)
    pair = pick_power_pair(truth)

    print("=== TASK 1: Week 1 definitions (asymptotic truth) ===")
    print("Rows read:", len(df), "| classifiers:", len(classifiers), classifiers)
    print("Sample sizes:", [int(x) for x in sorted(df["n_sub"].unique())],
          "| replicates per sample size:", df.groupby("n_sub")["replicate_id"].nunique().to_dict())
    print("Power is calculated for the pair:", pair, "(truly better one first)")
    print()

    rows = []
    all_detail = []
    for n in sorted(df["n_sub"].unique()):
        df_n = df[df["n_sub"] == n]
        detail = []
        results = compute_stats(df_n, truth, classifiers, true_best, truth_tie, pair, detail)
        for d in detail:
            d["n_sub"] = n
        all_detail.extend(detail)

        print(f"--- n_sub = {n} --- (true best: {true_best})")
        for key, value in results.items():
            print(f"  {key}: {value}")
        print()

        rows.append({
            "n_sub": n,
            "winner_correct_rate": round(results["winner_correct_rate"], 4),
            "mean_kendall_tau": round(results["mean_kendall_tau"], 4),
            "mean_optimism": round(results["mean_optimism"], 4),
            f"power_{pair[0]}_vs_{pair[1]}": round(results["power"], 4),
            f"sign_error_rate_{pair[0]}_vs_{pair[1]}": round(results["sign_error_rate"], 4),
            "observed_ties": results["ties_observed"],
        })

    out_path = DATA_DIR / "Task1_results_table.csv"
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print("Saved table to", out_path)

    # one line per replicate: the table above is just the averages of this file
    detail_df = pd.DataFrame(all_detail)
    first = ["n_sub", "replicate_id"] + ["mean_auc_" + c for c in classifiers]
    last = ["winner", "tied_for_first", "winner_correct", "kendall_tau", "optimism", "p_value", "power_result"]
    detail_df = detail_df[first + last]
    detail_path = DATA_DIR / "Task1_per_replicate.csv"
    detail_df.to_csv(detail_path, index=False)
    print("Saved replicate-by-replicate results to", detail_path)
    print()


def run_task3(df, true_auc, classifiers):
    """Task 3: power for a close pair and a wide-gap pair, at every sample size."""
    print("=== TASK 3: power for a close pair and a wide-gap pair ===")

    close_pair = ("gb", "knn")
    wide_pair = ("dtree", "logreg")
    pairs = [
        ("Close pair", close_pair),
        ("Wide-gap pair", wide_pair),
    ]

    print("Classifiers:", classifiers)
    all_results = []

    for label, pair in pairs:
        c1, c2 = pair
        gap_50 = abs(true_auc[("50", c1)] - true_auc[("50", c2)])

        print(f"{label} selected at n=50: {c1} vs {c2}; true AUC gap = {gap_50:.6f}")

        if label == "Close pair" and gap_50 >= 0.01:
            raise ValueError("Close pair must have an AUC gap below 0.01.")
        if label == "Wide-gap pair" and gap_50 <= 0.05:
            raise ValueError("Wide-gap pair must have an AUC gap above 0.05.")

    print()

    for n in sorted(df["n_sub"].unique()):
        df_n = df[df["n_sub"] == n]

        for label, pair in pairs:
            result = compute_pair_power(df_n, true_auc, classifiers, pair, n)
            result["pair_type"] = label
            all_results.append(result)

            print(
                f"n={n}, {label}, pair={result['pair']}, "
                f"gap={result['true_auc_gap']:.6f}, "
                f"power={result['power']}, "
                f"sign_error_rate={result['sign_error_rate']}"
            )

    results_df = pd.DataFrame(all_results)
    out_path = DATA_DIR / "task3_power_results.csv"
    results_df.to_csv(out_path, index=False)

    print("\nSaved results to", out_path)
    print(results_df.to_string(index=False))
    print()


def main():
    which = "all"
    if len(sys.argv) > 1:
        which = sys.argv[1].lower()
    if which not in ("all", "task1", "task3"):
        print("Use one of: task1, task3 (or nothing, to run both)")
        return

    true_auc, asymptotic_auc, classifiers = load_truth()
    df = pd.read_csv(RESULTS_PATH)

    if which in ("all", "task1"):
        run_task1(df, true_auc, classifiers)
    if which in ("all", "task3"):
        run_task3(df, true_auc, classifiers)


if __name__ == "__main__":
    main()