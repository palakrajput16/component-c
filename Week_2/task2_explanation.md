# Task 2 — Comparing the Two Definitions of Truth

Version A evaluates the declared winner against the classifier with the highest true AUC at the same sample size. This answers whether a researcher selected the best classifier for the amount of training data available. Version B evaluates the declared winner against the classifier with the highest asymptotic AUC, which represents the abundant-data benchmark.

The best classifier changes with sample size in the supplied truth file. Logistic regression has the highest true AUC at sample sizes 50 and 100, while SVM has the highest true AUC at 200 and 500. Gradient boosting has the highest asymptotic AUC. Therefore, a classifier can be the correct choice for a small sample even though it is not the asymptotic winner.

In the supplied reference results, Version A winner-correct rate is 42%, 40%, 47%, and 69% at sample sizes 50, 100, 200, and 500. Version B is 13%, 10%, 5%, and 8%. Version A improves overall at the largest sample size, while Version B remains low because it judges every decision against gradient boosting's abundant-data ranking, even where another classifier is genuinely better at the current sample size.

Mean optimism is calculated as the declared winner's mean cross-validation AUC minus that same classifier's true AUC. Version A optimism is +0.105854, +0.055894, +0.040562, and +0.021963. Version B optimism is -0.035243, -0.043918, -0.021601, and -0.009097. The negative Version B values mean the winning classifier's observed cross-validation score is, on average, below its asymptotic true AUC. This comparison illustrates that asymptotic truth mixes selection effects with changes in model performance as training size changes, whereas sample-size-specific truth targets the decision a researcher can make with the data they actually have.

## Verification note
The Week 2 brief lists indicative Version A optimism values of approximately +0.085, +0.062, +0.038, and +0.020. The values calculated from the supplied reference CSVs do not exactly match that sequence. These results should be verified against the exact LMS files and the instructor's intended treatment of ties and aggregation before final submission. Do not change values merely to force agreement with the indicative figures.
