"""
Simple tests for compute_statistics.py.

Each test builds a tiny, made-up dataset where we already know what the
answer should be, runs it through our actual functions, and checks that
we get that answer. This is how we prove the edge cases are actually
handled, since truth.csv and results.csv don't contain any of them.

Run this with: python3 test_edge_cases.py
"""

import pandas as pd

from compute_statistics import get_mean_auc, compute_stats

passed = 0
failed = 0


def check(description, condition):
    global passed, failed
    if condition:
        passed += 1
        print("PASS:", description)
    else:
        failed += 1
        print("FAIL:", description)


def build_data(classifier_folds):
    """
    classifier_folds looks like:
        {"c1": {1: 0.80, 2: 0.82, 3: 0.81, 4: 0.83, 5: 0.79}, "c2": {...}}
    fold_id -> auc value. A missing fold_id means that row just doesn't
    exist. A value of None means the row exists but auc is missing.
    All rows are put in replicate 1, n_sub 100, protocol cv5.
    """
    rows = []
    for classifier, folds in classifier_folds.items():
        for fold_id, auc in folds.items():
            rows.append(["toy", "cv5", 100, 1, classifier, fold_id, auc])

    columns = ["dataset_id", "protocol_id", "n_sub", "replicate_id",
               "classifier_id", "fold_id", "auc"]
    return pd.DataFrame(rows, columns=columns)


# ---------------------------------------------------------------------
# Test 1: works for more than 3 classifiers
# ---------------------------------------------------------------------
def test_more_than_3_classifiers():
    true_auc = {"c1": 0.90, "c2": 0.85, "c3": 0.80, "c4": 0.75, "c5": 0.70, "c6": 0.65}
    classifiers = sorted(true_auc.keys())

    folds = {}
    for c in classifiers:
        folds[c] = {f: true_auc[c] for f in range(1, 6)}

    df = build_data(folds)
    results = compute_stats(df, true_auc, classifiers, "c1", False, ("c1", "c2"))

    check("6 classifiers: winner_correct_rate is 1.0", results["winner_correct_rate"] == 1.0)
    check("6 classifiers: n_classifiers is 6", results["n_classifiers"] == 6)


# ---------------------------------------------------------------------
# Test 2: a tie between two classifiers in the observed scores
# ---------------------------------------------------------------------
def test_observed_tie():
    true_auc = {"c1": 0.85, "c2": 0.82, "c3": 0.76}
    classifiers = ["c1", "c2", "c3"]

    folds = {
        "c1": {f: 0.80 for f in range(1, 6)},  # c1 and c2 tie exactly
        "c2": {f: 0.80 for f in range(1, 6)},
        "c3": {f: 0.70 for f in range(1, 6)},
    }
    df = build_data(folds)

    mean_auc = get_mean_auc(df, classifiers)
    check("observed tie: c1 and c2 both come out as 0.80", mean_auc["c1"] == 0.80 and mean_auc["c2"] == 0.80)

    results = compute_stats(df, true_auc, classifiers, "c1", False, ("c1", "c2"))
    check("observed tie: winner_correct_rate is 0 (a tie never counts as correct)",
          results["winner_correct_rate"] == 0.0)
    check("observed tie: ties_observed is 1", results["ties_observed"] == 1)


# ---------------------------------------------------------------------
# Test 3: a tie in truth.csv itself
# ---------------------------------------------------------------------
def test_truth_tie():
    true_auc = {"c1": 0.85, "c2": 0.85, "c3": 0.76}  # c1 and c2 tied in truth
    classifiers = ["c1", "c2", "c3"]

    folds = {
        "c1": {f: 0.86 for f in range(1, 6)},
        "c2": {f: 0.80 for f in range(1, 6)},
        "c3": {f: 0.70 for f in range(1, 6)},
    }
    df = build_data(folds)

    results = compute_stats(df, true_auc, classifiers, "c1", True, ("c1", "c2"))
    check("truth tie: winner_correct_rate is None (nothing to compare against)",
          results["winner_correct_rate"] is None)
    check("truth tie: replicates_skipped_for_truth_tie is 1",
          results["replicates_skipped_for_truth_tie"] == 1)


# ---------------------------------------------------------------------
# Test 4: a classifier is completely missing from a replicate
# ---------------------------------------------------------------------
def test_missing_classifier():
    true_auc = {"c1": 0.85, "c2": 0.82, "c3": 0.76}
    classifiers = ["c1", "c2", "c3"]

    folds = {
        "c1": {f: 0.86 for f in range(1, 6)},
        "c2": {f: 0.80 for f in range(1, 6)},
        # c3 is missing entirely
    }
    df = build_data(folds)

    mean_auc = get_mean_auc(df, classifiers)
    check("missing classifier: c3 does not appear in mean_auc", "c3" not in mean_auc)

    results = compute_stats(df, true_auc, classifiers, "c1", False, ("c1", "c2"))
    check("missing classifier: replicate is dropped", results["replicates_dropped"] == 1)
    check("missing classifier: winner_correct_rate is None", results["winner_correct_rate"] is None)


# ---------------------------------------------------------------------
# Test 5: a missing/blank AUC value
# ---------------------------------------------------------------------
def test_missing_auc_value():
    true_auc = {"c1": 0.85, "c2": 0.82, "c3": 0.76}
    classifiers = ["c1", "c2", "c3"]

    folds = {
        "c1": {1: 0.86, 2: 0.85, 3: None, 4: 0.84, 5: 0.83},  # fold 3 missing
        "c2": {f: 0.80 for f in range(1, 6)},
        "c3": {f: 0.70 for f in range(1, 6)},
    }
    df = build_data(folds)

    mean_auc = get_mean_auc(df, classifiers)
    expected = (0.86 + 0.85 + 0.84 + 0.83) / 4  # fold 3 dropped, average of the other 4
    check("missing auc: mean uses only the 4 good folds", abs(mean_auc["c1"] - expected) < 1e-9)


# ---------------------------------------------------------------------
# Test 6: fewer than 5 fold rows for a classifier
# ---------------------------------------------------------------------
def test_missing_fold_rows():
    true_auc = {"c1": 0.85, "c2": 0.82, "c3": 0.76}
    classifiers = ["c1", "c2", "c3"]

    folds = {
        "c1": {1: 0.86, 2: 0.85, 3: 0.84},  # only 3 folds, not 5
        "c2": {f: 0.80 for f in range(1, 6)},
        "c3": {f: 0.70 for f in range(1, 6)},
    }
    df = build_data(folds)

    mean_auc = get_mean_auc(df, classifiers)
    expected = (0.86 + 0.85 + 0.84) / 3
    check("missing fold rows: mean uses just the 3 folds present", abs(mean_auc["c1"] - expected) < 1e-9)


# ---------------------------------------------------------------------
# Test 7: the same fold number appears twice
# ---------------------------------------------------------------------
def test_duplicate_fold_row():
    true_auc = {"c1": 0.85, "c2": 0.82, "c3": 0.76}
    classifiers = ["c1", "c2", "c3"]

    df = build_data({
        "c1": {f: 0.86 for f in range(1, 6)},
        "c2": {f: 0.80 for f in range(1, 6)},
        "c3": {f: 0.70 for f in range(1, 6)},
    })
    # add an extra duplicate row for c1, fold 1, with a very different value
    extra_row = pd.DataFrame([["toy", "cv5", 100, 1, "c1", 1, 0.10]], columns=df.columns)
    df = pd.concat([df, extra_row], ignore_index=True)

    mean_auc = get_mean_auc(df, classifiers)
    check("duplicate fold row: the 0.10 duplicate is ignored, mean stays 0.86",
          abs(mean_auc["c1"] - 0.86) < 1e-9)


# ---------------------------------------------------------------------
# Test 8: a fold number outside 1-5
# ---------------------------------------------------------------------
def test_unexpected_fold_number():
    true_auc = {"c1": 0.85, "c2": 0.82, "c3": 0.76}
    classifiers = ["c1", "c2", "c3"]

    folds = {
        "c1": {1: 0.86, 2: 0.85, 3: 0.84, 4: 0.83, 5: 0.82, 9: 0.10},  # fold 9 shouldn't exist
        "c2": {f: 0.80 for f in range(1, 6)},
        "c3": {f: 0.70 for f in range(1, 6)},
    }
    df = build_data(folds)

    mean_auc = get_mean_auc(df, classifiers)
    expected = (0.86 + 0.85 + 0.84 + 0.83 + 0.82) / 5
    check("unexpected fold number: fold 9 is ignored", abs(mean_auc["c1"] - expected) < 1e-9)


# ---------------------------------------------------------------------
# Test 9: two classifiers have different numbers of folds
# ---------------------------------------------------------------------
def test_unequal_fold_counts():
    true_auc = {"c1": 0.85, "c2": 0.82, "c3": 0.76}
    classifiers = ["c1", "c2", "c3"]

    # c1 has 5 folds, c2 has only 1: not enough to pair up for the power test
    folds = {
        "c1": {1: 0.86, 2: 0.85, 3: 0.84, 4: 0.83, 5: 0.82},
        "c2": {1: 0.80},
        "c3": {f: 0.70 for f in range(1, 6)},
    }
    df = build_data(folds)

    results = compute_stats(df, true_auc, classifiers, "c1", False, ("c1", "c2"))
    check("unequal fold counts: power is None because there's only 1 paired fold",
          results["power"] is None)


if __name__ == "__main__":
    test_more_than_3_classifiers()
    test_observed_tie()
    test_truth_tie()
    test_missing_classifier()
    test_missing_auc_value()
    test_missing_fold_rows()
    test_duplicate_fold_row()
    test_unexpected_fold_number()
    test_unequal_fold_counts()

    print()
    print(passed, "passed,", failed, "failed")