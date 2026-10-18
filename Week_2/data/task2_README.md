# CSIT332 Component C — Week 2 Task 2

## Purpose
Calculate and compare winner-correct rate and optimism using two definitions of truth across `n_sub = 50, 100, 200, 500`, with 100 replicates per sample size (400 replicate-level records total).

- **Version A:** compare the declared winner with the best classifier at the current sample size; calculate optimism against that winner's sample-size-specific true AUC.
- **Version B:** compare the declared winner with the best classifier by asymptotic true AUC; calculate optimism against that winner's asymptotic true AUC.

## Files
- `task2_compare_truth.py` — reproducible calculation script.
- `data/reference_results.csv` — Week 2 reference results (12,000 rows).
- `data/reference_truth.csv` — Week 2 truth values, including the asymptotic row.
- `task2_per_replicate.csv` — 400 rows, one for each replicate and sample size.
- `task2_summary.csv` — four-row summary table.
- `task2_explanation.md` — plain-English interpretation and verification note.

## Run the calculation
Requires Python 3, pandas, and a working Python environment.

```bash
python -m pip install pandas
python task2_compare_truth.py
```

Run the command from this folder. It regenerates both output CSV files.

## Summary of the current calculation

| n_sub | Best at n | Best asymptotically | Winner-correct A | Winner-correct B | Mean optimism A | Mean optimism B |
|---:|---|---|---:|---:|---:|---:|
| 50 | logreg | gb | 42% | 13% | +0.105854 | -0.035243 |
| 100 | logreg | gb | 40% | 10% | +0.055894 | -0.043918 |
| 200 | svm | gb | 47% | 5% | +0.040562 | -0.021601 |
| 500 | svm | gb | 69% | 8% | +0.021963 | -0.009097 |

## Important verification note
These are the values produced from the supplied reference files using the calculation and tie rule documented in the script. The Week 2 instruction sheet gives indicative Version A optimism values of approximately +0.085, +0.062, +0.038, and +0.020. The computed values do not exactly match those indicative values, so confirm the instructor's expected calculation/tie conventions and check that the exact LMS reference files are being used before treating the numbers as final.
