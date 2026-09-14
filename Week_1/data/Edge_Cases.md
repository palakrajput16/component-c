## Edge Cases

### 1. Exact tie for highest observed AUC

If two or more classifiers have exactly the same highest observed AUC, the
replicate is not counted as correct for the winner-correct rate.

The tie is recorded separately as a tie.

If a single winner is required for a statistic that cannot use a tied winner,
the deterministic tie-break rule is to select the alphabetically first
classifier.

For example, if c1 and c2 are tied for the highest observed AUC, c1 is selected
as the deterministic winner because c1 comes alphabetically before c2.

Winner-correct rate does not count the tied replicate as correct.


### 2. Tie in truth winner

If two or more classifiers have exactly the same highest true AUC, there is no
unique true winner.

The replicate is recorded as a truth tie and is not counted as a correct or
incorrect winner for the winner-correct rate.

If a single true winner is required for a statistic, the alphabetically first
classifier is used as the deterministic tie-break.


### 3. Missing / unusable AUC

If an AUC value is missing or unusable for a fold, that fold is dropped from the
classifier's mean AUC calculation.

The remaining usable folds are used to calculate the classifier-level mean.

If all folds for a classifier are missing or unusable, the classifier has no
usable mean AUC.

In this case, the whole replicate is dropped from all four statistics:

- winner-correct rate
- Kendall's tau
- optimism
- power

The dropped replicate is also logged.


### 4. Insufficient paired observations

For the c1 versus c2 power calculation, observations are paired using the same
fold_id.

Only complete c1/c2 fold pairs are used.

If a fold is missing or unusable for either c1 or c2, that fold pair is dropped.

A paired t-test requires at least two valid c1/c2 fold pairs.

If fewer than two valid pairs remain, the replicate does not undergo the paired
t-test and is logged as having insufficient paired observations.


### 5. Fold matching

Paired observations are matched using fold_id.

For example:

c1 fold 1 <-> c2 fold 1

c1 fold 2 <-> c2 fold 2

c1 fold 3 <-> c2 fold 3

c1 fold 4 <-> c2 fold 4

c1 fold 5 <-> c2 fold 5

A c1 observation must never be paired with a different fold from c2.


### 6. Rounding

Winner determination uses the underlying AUC precision rather than the
displayed rounded value.

Rounding is applied only when displaying results.

Therefore, two values that appear equal after rounding are not treated as a
tie if their underlying values are different.


### 7. Statistical classification

The paired statistical test uses the predetermined significance level:

p < 0.05

The classification rule is:

- **Correct detection:** p < 0.05 and c1 has the higher observed mean AUC.
- **Sign error:** p < 0.05 and c2 has the higher observed mean AUC.
- **No detection:** p >= 0.05.

A statistically significant result in favour of c2 is therefore a sign error
because c1 is the true better classifier in the specified truth values.

A non-significant result is always classified as no detection, regardless of
which classifier has the higher observed mean AUC.
