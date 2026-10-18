# CSIT332 Component C — Week 2 Task 2

## Folder layout

- `src/task2_compare_truth.py` — calculates Version A and Version B.
- `data/reference_results.csv` — observed fold-level AUC values.
- `data/reference_truth.csv` — sample-size-specific and asymptotic true AUC values.
- `data/task2_per_replicate.csv` — one row per replicate and sample size.
- `data/task2_summary.csv` — Task 2 summary by sample size.
- `data/Task1_results_table.csv` — Task 1 summary used for the combined table.
- `data/Task1_Task2_combined_results.csv` — combined Task 1 and Task 2 quantities.
- `task2_explanation.md` — explanation of both versions and the optimism discrepancy.

## Run the script

Install pandas if necessary:

```bash
python -m pip install pandas
```

From the `Week_2` folder, run:

```bash
python src/task2_compare_truth.py
```

The script reads its input files from `Week_2/data` and saves `task2_per_replicate.csv` and `task2_summary.csv` into that same data folder.

## Versions

- **Version A:** compares the selected winner with the best classifier's truth at the current sample size.
- **Version B:** compares the selected winner with the best classifier's asymptotic truth.

The calculated Version A optimism values are +0.106, +0.056, +0.041, and +0.022 for sample sizes 50, 100, 200, and 500. The Week 2 sheet states +0.085, +0.062, +0.038, and +0.020. The pattern is similar, but the values differ, so we will ask the professor to confirm the expected files and calculation convention.

## Tie rule

If multiple classifiers share the maximum observed mean AUC, the alphabetically first classifier is recorded as the declared winner. That replicate is counted as incorrect for both winner-correct rates.
