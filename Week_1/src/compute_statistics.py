"""
Component C - Week 1 statistics code

Reads truth.csv and results_extended.csv, then works out four things for
each sample size (n_sub = 100 and n_sub = 500):

1. winner_correct_rate - how often the classifier with the highest mean
   AUC is actually the best classifier according to truth.csv
2. mean_kendall_tau - how close the observed ranking of classifiers is to
   the true ranking
3. mean_optimism - how much the winning classifier's reported score is
   higher than its own true value
4. power - for two chosen classifiers, how often a paired t-test correctly
   says the better one is better

The classifier list is read from truth.csv, not typed in by hand, so this
works no matter how many classifiers there are. Before using a replicate's
data, the code also checks for a few common problems: a classifier with no
rows at all, duplicate fold rows, fold numbers that shouldn't exist, and
ties (both in the observed scores and in truth.csv itself).
"""

import pandas as pd
from scipy.stats import kendalltau, ttest_rel

TRUTH_PATH = "../data/truth.csv"
RESULTS_PATH = "../data/results_extended.csv"
EXPECTED_FOLDS = [1, 2, 3, 4, 5]


def load_truth():
    """Read truth.csv and return the true AUC values, the list of
    classifiers, the true best classifier, and whether truth.csv itself
    has a tie for the best classifier."""

    truth = pd.read_csv(TRUTH_PATH)

    true_auc = {}
    for _, row in truth.iterrows():
        true_auc[row["classifier_id"]] = row["true_auc"]

    classifiers = sorted(true_auc.keys())

    best_value = max(true_auc.values())
    best_classifiers = [c for c in classifiers if true_auc[c] == best_value]
    truth_tie = len(best_classifiers) > 1
    true_best = sorted(best_classifiers)[0]  # alphabetical tie-break if tied

    return true_auc, classifiers, true_best, truth_tie


def get_mean_auc(rep_data, classifiers):
    """
    Work out the mean AUC for each classifier in one replicate.

    Cleans the data up first:
      - if the same fold number shows up twice for a classifier, only the
        first one is used
      - fold numbers outside 1-5 are ignored
      - rows with a missing auc value are ignored

    Returns a dictionary like {"c1": 0.81, "c2": 0.83}. A classifier is
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


def compute_stats(df, true_auc, classifiers, true_best, truth_tie, pair):
    """Compute all four statistics for one sample size."""

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

        # who has the highest mean AUC? (there may be more than one)
        best_value = max(mean_auc.values())
        top_classifiers = sorted([c for c in mean_auc if mean_auc[c] == best_value])

        if truth_tie:
            # truth.csv has no single best classifier, so we can't say
            # whether this replicate got the "right" winner
            truth_tie_skipped += 1
            winner = top_classifiers[0]
        elif len(top_classifiers) > 1:
            tie_count += 1
            winner_correct.append(0)  # a tie is never counted as correct
            winner = top_classifiers[0]
        else:
            winner = top_classifiers[0]
            winner_correct.append(1 if winner == true_best else 0)

        # Kendall's tau: compare the observed order to the true order
        observed_rank = pd.Series(mean_auc).rank(ascending=False)
        true_rank = pd.Series({c: -true_auc[c] for c in mean_auc}).rank()
        tau, _ = kendalltau(observed_rank, true_rank)
        tau_list.append(tau)

        # optimism: winner's own reported score minus its own true value
        optimism_list.append(mean_auc[winner] - true_auc[winner])

        # power: paired t-test between the two named classifiers
        c1, c2 = pair
        folds_1, folds_2 = get_paired_folds(rep_data, c1, c2)

        if len(folds_1) < 2:
            detections.append("not_enough_data")
            continue

        t_stat, p_value = ttest_rel(folds_1, folds_2)
        diff = sum(a - b for a, b in zip(folds_1, folds_2)) / len(folds_1)

        if p_value < 0.05 and diff > 0:
            detections.append("correct")
        elif p_value < 0.05 and diff < 0:
            detections.append("sign_error")
        else:
            detections.append("no_detection")

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


def main():
    true_auc, classifiers, true_best, truth_tie = load_truth()
    df = pd.read_csv(RESULTS_PATH)

    pair = (classifiers[0], classifiers[1])

    print("Classifiers:", classifiers)
    print("True best classifier:", true_best, "| truth has a tie:", truth_tie)
    print("Power is calculated for the pair:", pair)
    print()

    for n in sorted(df["n_sub"].unique()):
        df_n = df[df["n_sub"] == n]
        results = compute_stats(df_n, true_auc, classifiers, true_best, truth_tie, pair)

        print(f"--- n_sub = {n} ---")
        for key, value in results.items():
            print(f"  {key}: {value}")
        print()


if __name__ == "__main__":
    main()