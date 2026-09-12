"""
Component C, Week 1, Step 4.

Computes, separately for each sample size (n_sub):
  1. Winner-correct rate
  2. Mean Kendall's tau
  3. Mean optimism
  4. Power (and sign-error rate) for the named pair c1 vs c2

Edge-case rules:
  - An exact tie for the highest mean AUC is never counted as a correct
    winner-correct-rate hit, even if the true best classifier is one of
    the tied classifiers. Ties are counted and reported separately.
  - If a fold's AUC is missing, that fold is excluded from the classifier's
    mean AUC and from paired comparisons.
  - If every fold for a classifier in a replicate is missing, that replicate
    is dropped from all four statistics and logged.
"""

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, ttest_rel


TRUTH_PATH = "truth.csv"
RESULTS_PATH = "results_extended.csv"

# Named pair for the power analysis
PAIR = ("c1", "c2")


def load_truth(path=TRUTH_PATH):
    """Load true AUC values and identify the true best classifier."""

    truth = pd.read_csv(path)

    true_auc = dict(
        zip(
            truth["classifier_id"],
            truth["true_auc"]
        )
    )

    true_best = truth.loc[
        truth["true_auc"].idxmax(),
        "classifier_id"
    ]

    return true_auc, true_best


def compute_for_sample_size(
    df_n,
    true_auc,
    true_best,
    pair=PAIR
):
    """
    Compute all four statistics for one sample size.
    """

    winner_hits = []
    tie_count = 0

    taus = []
    optimism_vals = []

    detections = []
    dropped_replicates = []

    # Process each replicate separately
    for rep, sub in df_n.groupby("replicate_id"):

        # -----------------------------------------
        # Classifier-level mean observed AUC
        # -----------------------------------------

        mean_auc = (
            sub.groupby("classifier_id")["auc"]
            .mean()
        )

        # If a classifier has no usable AUC values,
        # it will not appear in mean_auc.
        if len(mean_auc) < 3:

            dropped_replicates.append(rep)

            continue

        # -----------------------------------------
        # Winner-correct rate
        # -----------------------------------------

        max_val = mean_auc.max()

        top = mean_auc[
            mean_auc == max_val
        ].index.tolist()

        # Exact tie for highest observed AUC
        if len(top) > 1:

            tie_count += 1

            # Ties are never counted as correct
            winner_hits.append(0)

            # Deterministic tie-break for quantities
            # that require a single winner
            winner = sorted(top)[0]

        else:

            winner = top[0]

            winner_hits.append(
                1 if winner == true_best else 0
            )

        # -----------------------------------------
        # Kendall's tau
        # -----------------------------------------

        classifiers = mean_auc.index.tolist()

        reported_rank = mean_auc.rank(
            ascending=False
        )

        true_rank = pd.Series(
            {
                c: -true_auc[c]
                for c in classifiers
            }
        ).rank()

        tau, _ = kendalltau(
            reported_rank,
            true_rank
        )

        taus.append(tau)

        # -----------------------------------------
        # Optimism
        # -----------------------------------------

        optimism = (
            mean_auc[winner]
            - true_auc[winner]
        )

        optimism_vals.append(optimism)

        # -----------------------------------------
        # Power for c1 vs c2
        # -----------------------------------------

        c_a, c_b = pair

        # Match observations by fold_id so that:
        #
        # c1 fold 1 <-> c2 fold 1
        # c1 fold 2 <-> c2 fold 2
        # etc.
        pair_df = (
            sub[
                sub["classifier_id"].isin(
                    [c_a, c_b]
                )
            ]
            .pivot(
                index="fold_id",
                columns="classifier_id",
                values="auc"
            )
            .dropna(
                subset=[c_a, c_b]
            )
        )

        folds_a = pair_df[c_a].values
        folds_b = pair_df[c_b].values

        # Need at least two paired observations
        # for the t-test.
        if len(folds_a) < 2:

            detections.append("none")

            continue

        # Paired t-test
        t_stat, p_val = ttest_rel(
            folds_a,
            folds_b
        )

        # Positive difference means c1 > c2
        mean_diff = np.mean(
            folds_a - folds_b
        )

        # -----------------------------------------
        # Power classification
        # -----------------------------------------

        if p_val < 0.05 and mean_diff > 0:

            # c1 significantly outperforms c2
            detections.append("correct")

        elif p_val < 0.05 and mean_diff < 0:

            # c2 significantly outperforms c1
            # even though c1 is the true better classifier
            detections.append("sign_error")

        else:

            # Not statistically significant
            detections.append("none")

    # -----------------------------------------
    # Final summary
    # -----------------------------------------

    n_valid = len(winner_hits)

    return {
        "n_replicates_used": n_valid,

        "n_replicates_dropped": len(
            dropped_replicates
        ),

        "dropped_replicate_ids": dropped_replicates,

        "tie_count": tie_count,

        "winner_correct_rate": (
            np.mean(winner_hits)
            if n_valid
            else float("nan")
        ),

        "mean_kendall_tau": (
            np.mean(taus)
            if taus
            else float("nan")
        ),

        "mean_optimism": (
            np.mean(optimism_vals)
            if optimism_vals
            else float("nan")
        ),

        "power_c1_vs_c2": (
            detections.count("correct")
            / len(detections)
            if detections
            else float("nan")
        ),

        "sign_error_rate": (
            detections.count("sign_error")
            / len(detections)
            if detections
            else float("nan")
        ),
    }


def main():

    # -----------------------------------------
    # Load truth and results
    # -----------------------------------------

    true_auc, true_best = load_truth()

    results = pd.read_csv(
        RESULTS_PATH
    )

    print(
        f"True best classifier: {true_best} "
        f"(true_auc = {true_auc[true_best]})\n"
    )

    # -----------------------------------------
    # Compute statistics separately for
    # n_sub = 100 and n_sub = 500
    # -----------------------------------------

    for n in sorted(
        results["n_sub"].unique()
    ):

        df_n = results[
            results["n_sub"] == n
        ]

        stats = compute_for_sample_size(
            df_n,
            true_auc,
            true_best
        )

        print(
            f"--- n_sub = {n} ---"
        )

        for key, value in stats.items():

            print(
                f"  {key}: {value}"
            )

        print()


if __name__ == "__main__":
    main()