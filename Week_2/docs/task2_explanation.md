# Week 2 Task 2 — Comparing the Two Definitions of Truth

**Version A** compares the selected classifier with the classifier that has the highest true AUC at the current sample size. **Version B** compares the selected classifier with the classifier that has the highest asymptotic true AUC.

In these results, Version A follows the expected qualitative pattern: its optimism is positive and generally decreases as sample size grows, while its winner-correct rate rises to 0.69 at n=500. Version B has negative optimism at all four sample sizes, and its winner-correct rate stays low, between 0.05 and 0.13. This happens because Version B always judges the selected classifier against the asymptotic winner, even when a different classifier has the highest true AUC at the current sample size.

Our calculated Version A optimism values, rounded to three decimal places, are **+0.106, +0.056, +0.041, and +0.022** for n=50, 100, 200, and 500. The Week 2 sheet states **+0.085, +0.062, +0.038, and +0.020**. The overall pattern is similar, but the values differ. Note: Need to seek clarification regarding the intended input files and calculation methodology. Not changed the calculated values to force a match.

The combined results file `data/Task1_Task2_combined_results.csv` brings together the Week 2 winner-correct and optimism values with Kendall's tau, power, and sign-error rate from `Task1_results_table.csv`. The power and sign-error columns retain the Task 1 comparison `gb_vs_svm`.

## Tie handling

When classifiers share the highest observed mean cross-validation AUC, the alphabetically first classifier is recorded as the declared winner, and that replicate is counted as incorrect for both winner-correct rates. This convention should be confirmed with the professor if the course specifies a different tie rule.
