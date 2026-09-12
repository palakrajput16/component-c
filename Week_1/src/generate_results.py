"""
Component C, Week 1, Step 3.

Extends the supplied replicate 1 (n_sub=100) into:
    - 20 replicates at n_sub = 100
    - 20 replicates at n_sub = 500

There are:
    3 classifiers x 5 folds x 20 replicates x 2 sample sizes
    = 600 rows.

The supplied replicate 1 is kept unchanged.

For generated data:
    - n_sub=100 has larger noise
    - n_sub=500 has smaller noise

This reflects the requirement that larger sample sizes should
produce less variable AUC estimates.
"""

import numpy as np
import pandas as pd


# -----------------------------
# Configuration
# -----------------------------

RNG_SEED = 42

NOISE_STD_N100 = 0.035
NOISE_STD_N500 = 0.012

CLASSIFIERS = ["c1", "c2", "c3"]

GIVEN_RESULTS_PATH = "results.csv"
TRUTH_PATH = "truth.csv"
OUTPUT_PATH = "results_extended.csv"


# -----------------------------
# Generate one replicate
# -----------------------------

def generate_replicate(
    dataset_id,
    protocol_id,
    n_sub,
    replicate_id,
    true_auc,
    noise_std,
    rng
):
    rows = []

    for classifier in CLASSIFIERS:

        # True AUC is the centre of the simulated distribution
        center = true_auc[classifier]

        for fold_id in range(1, 6):

            auc = rng.normal(center, noise_std)

            # AUC must remain between 0 and 1
            auc = np.clip(auc, 0.0, 1.0)

            rows.append(
                (
                    dataset_id,
                    protocol_id,
                    n_sub,
                    replicate_id,
                    classifier,
                    fold_id,
                    round(auc, 4)
                )
            )

    return rows


# -----------------------------
# Main
# -----------------------------

def main():

    # Read true AUC values
    truth = pd.read_csv(TRUTH_PATH)

    true_auc = dict(
        zip(truth["classifier_id"], truth["true_auc"])
    )

    # Read the supplied replicate 1
    given = pd.read_csv(GIVEN_RESULTS_PATH)

    rows = list(
        given.itertuples(index=False, name=None)
    )

    # Fixed seed makes the generated dataset reproducible
    rng = np.random.default_rng(RNG_SEED)

    # -----------------------------------------
    # n_sub = 100
    # Replicate 1 is supplied.
    # Generate replicates 2 through 20.
    # -----------------------------------------

    for replicate_id in range(2, 21):

        rows.extend(
            generate_replicate(
                dataset_id="toy",
                protocol_id="cv5",
                n_sub=100,
                replicate_id=replicate_id,
                true_auc=true_auc,
                noise_std=NOISE_STD_N100,
                rng=rng
            )
        )

    # -----------------------------------------
    # n_sub = 500
    # Generate all 20 replicates.
    # -----------------------------------------

    for replicate_id in range(1, 21):

        rows.extend(
            generate_replicate(
                dataset_id="toy",
                protocol_id="cv5",
                n_sub=500,
                replicate_id=replicate_id,
                true_auc=true_auc,
                noise_std=NOISE_STD_N500,
                rng=rng
            )
        )

    # Convert to DataFrame
    results = pd.DataFrame(
        rows,
        columns=[
            "dataset_id",
            "protocol_id",
            "n_sub",
            "replicate_id",
            "classifier_id",
            "fold_id",
            "auc"
        ]
    )

    # Sort for easier inspection
    results = results.sort_values(
        [
            "n_sub",
            "replicate_id",
            "classifier_id",
            "fold_id"
        ]
    )

    # Save
    results.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # Basic checks
    print(f"Total rows: {len(results)}")

    print("\nRows by sample size:")
    print(results.groupby("n_sub").size())

    print("\nRows by sample size and replicate:")
    print(
        results.groupby(
            ["n_sub", "replicate_id"]
        ).size()
    )


if __name__ == "__main__":
    main()