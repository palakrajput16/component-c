
## 1. Winner-Correct Rate

Winner-correct rate measures how often the classifier with the highest observed mean AUC is also the classifier with the highest true AUC.

For each replicate:

1. Calculate the mean AUC for each classifier.
2. Select the classifier with the highest mean AUC as the observed winner.
3. Find the true winner from `truth.csv`.
4. If the observed winner and true winner are the same, record 1.
5. If they are different, record 0.
6. Repeat for all valid replicates.

Winner-correct rate = Number of correct winners / Number of valid replicates

### Example: Replicate 1

For `n_sub = 100`, replicate 1:

| Classifier | Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5 | Mean AUC |
|---|---:|---:|---:|---:|---:|---:|
| c1 | 0.81 | 0.78 | 0.84 | 0.80 | 0.82 | 0.810 |
| c2 | 0.86 | 0.83 | 0.80 | 0.85 | 0.81 | 0.830 |
| c3 | 0.74 | 0.77 | 0.72 | 0.79 | 0.75 | 0.754 |

Mean AUC for c1:

(0.81 + 0.78 + 0.84 + 0.80 + 0.82) / 5

= 4.05 / 5

= 0.810

Mean AUC for c2:

(0.86 + 0.83 + 0.80 + 0.85 + 0.81) / 5

= 4.15 / 5

= 0.830
Mean AUC for c3:

(0.74 + 0.77 + 0.72 + 0.79 + 0.75) / 5

= 3.77 / 5

= 0.754

Therefore:

Observed winner = c2

The true winner is determined using the highest true AUC in `truth.csv`.

If the true winner is c2:

Winner-correct = 1

If the true winner is c1:

Winner-correct = 0

The same process is repeated for all 20 replicates.

Final calculation:

Winner-correct rate = Number of correct replicates / 20

##  Power (Replicate 1, Pair: c1 vs c2)

We're testing whether c1 is detectably better than c2, using the 5 paired fold scores from replicate 1 (n_sub = 100).

## Setup

| fold | c1 | c2 | diff (c1 − c2) |
|---|---|---|---|
| 1 | 0.81 | 0.86 | −0.05 |
| 2 | 0.78 | 0.83 | −0.05 |
| 3 | 0.84 | 0.80 | +0.04 |
| 4 | 0.80 | 0.85 | −0.05 |
| 5 | 0.82 | 0.81 | +0.01 |

## Step 1 — Mean of the differences

mean = (−0.05 + −0.05 + 0.04 + −0.05 + 0.01) / 5
mean = −0.10 / 5
mean = **−0.02**

## Step 2 — Deviation of each difference from the mean

| fold | diff | diff − mean | (diff − mean)² |
|---|---|---|---|
| 1 | −0.05 | −0.05 − (−0.02) = −0.03 | 0.0009 |
| 2 | −0.05 | −0.03 | 0.0009 |
| 3 | +0.04 | 0.04 − (−0.02) = +0.06 | 0.0036 |
| 4 | −0.05 | −0.03 | 0.0009 |
| 5 | +0.01 | 0.01 − (−0.02) = +0.03 | 0.0009 |

## Step 3 — Sum of squared deviations

sum = 0.0009 + 0.0009 + 0.0036 + 0.0009 + 0.0009 = **0.0072**

## Step 4 — Sample variance

Divide by (n − 1), not n, since this is a sample standard deviation. n = 5, so n − 1 = 4.

variance = 0.0072 / 4 = **0.0018**

## Step 5 — Sample standard deviation

std dev = √0.0018 = **0.04243**

## Step 6 — Standard error of the mean difference

standard error = std dev / √n = 0.04243 / √5 = 0.04243 / 2.2361 = **0.01897**

## Step 7 — t-statistic

t = mean difference / standard error = −0.02 / 0.01897 = **−1.054**

## Step 8 — Degrees of freedom and critical value

Degrees of freedom = n − 1 = 4.

For a two-tailed test at α = 0.05 with 4 degrees of freedom, the critical t-value (from a t-table) is **2.776**.

## Step 9 — Compare

|t| = 1.054, which is less than the critical value of 2.776.

Since |t| doesn't clear the critical value, the result is **not statistically significant** (p > 0.05). The exact p-value, computed as the area beyond ±1.054 on a t-distribution with 4 degrees of freedom, comes to **p ≈ 0.351**.

## Step 10 — Classify the replicate

- p ≥ 0.05, so this is not a significant result either way.
- Classification: **no detection**

Note that even though the mean difference (−0.02) actually points the wrong way, in c2's favor, that alone doesn't make it a "sign error." A sign error only applies when the test is significant AND points the wrong direction. Here it's not significant at all, so "no detection" is the correct label, not "sign error." That distinction is worth remembering if the professor asks about it in the oral defence, since it's an easy point to get backwards.

