Edge Cases

1. Exact tie for highest observed AUC
If two or more classifiers have exactly the same highest observed AUC, the replicate is not counted as correct for
winner-correct rate.

2. Tie in truth winner
Describe how a tie in the truth ranking is handled.

3. Missing / unusable AUC
If a classifier has no usable AUC values, it is not included in the classifier-level mean AUC calculation.

4. Insufficient paired observations
A paired t-test requires at least two paired observations. If fewer than two valid pairs exist, the replicate cannot
undergo the paired t-test.

5. Fold matching
Paired observations are matched using fold_id: c1 fold 1 is paired with c2 fold 1, etc.

6. Rounding
Winner determination should use the appropriate underlying precision rather than creating artificial ties through display
rounding.

7. Statistical classification
A replicate is classified as:
- Correct detection
- No detection
- Sign error
according to the predetermined significance rule.
