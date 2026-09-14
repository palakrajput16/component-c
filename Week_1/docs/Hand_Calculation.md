
##  Power (Replicate 1, Pair: c1 vs c2)
=======
# Observed AUC, Kendall's Tau + Optimism (Replicate 1)

We're comparing the observed ranking of c1, c2, and c3 with their true ranking, using the 5 fold AUC values from replicate 1 (n_sub = 100).

## Step 1 — Truth table

| classifier | true AUC |
|---|---|
| c1 | 0.85 |
| c2 | 0.82 |
| c3 | 0.76 |

The true ranking is:

**c1 > c2 > c3**

Therefore, c1 is the genuinely best classifier.

## Step 2 — Mean AUC for c1

mean AUC (c1) = (0.81 + 0.78 + 0.84 + 0.80 + 0.82) / 5

mean AUC (c1) = 4.05 / 5

mean AUC (c1) = **0.810**

## Step 3 — Mean AUC for c2

mean AUC (c2) = (0.86 + 0.83 + 0.80 + 0.85 + 0.81) / 5

mean AUC (c2) = 4.15 / 5

mean AUC (c2) = **0.830**

## Step 4 — Mean AUC for c3

mean AUC (c3) = (0.74 + 0.77 + 0.72 + 0.79 + 0.75) / 5

mean AUC (c3) = 3.77 / 5

mean AUC (c3) = **0.754**

## Step 5 — Summary of mean AUCs

| classifier | mean AUC |
|---|---:|
| c1 | 0.810 |
| c2 | 0.830 |
| c3 | 0.754 |

## Step 6 — Determine the observed ranking

The observed mean AUCs are:

c1 = 0.810  
c2 = 0.830  
c3 = 0.754

Therefore, the observed ranking is:

**c2 > c1 > c3**

The observed winner is **c2**.

# Kendall's Tau

## Step 7 — Compare the observed ranking with the true ranking

True ranking:

**c1 > c2 > c3**

Observed ranking:

**c2 > c1 > c3**

There are 3 possible classifier pairs:

1. c1 vs c2
2. c1 vs c3
3. c2 vs c3

## Step 8 — Identify concordant and discordant pairs

### Pair 1 — c1 vs c2

Truth: **c1 > c2**

Observed: **c2 > c1**

The order is different, so this pair is **discordant**.

### Pair 2 — c1 vs c3

Truth: **c1 > c3**

Observed: **c1 > c3**

The order is the same, so this pair is **concordant**.

### Pair 3 — c2 vs c3

Truth: **c2 > c3**

Observed: **c2 > c3**

The order is the same, so this pair is **concordant**.

## Step 9 — Count concordant and discordant pairs

Concordant pairs = **2**

Discordant pairs = **1**

Therefore:

C = **2**

D = **1**

## Step 10 — Calculate Kendall's Tau

Kendall's Tau = (C − D) / (C + D)

Kendall's Tau = (2 − 1) / (2 + 1)

Kendall's Tau = 1 / 3

Kendall's Tau = **0.3333**

Therefore, the Kendall's Tau for replicate 1 is **0.3333**.

# Optimism

## Step 11 — Identify the declared winner

The observed mean AUCs are:

c1 = 0.810  
c2 = 0.830  
c3 = 0.754

The highest observed mean AUC is for **c2**.

Therefore:

Observed winner = **c2**

## Step 12 — Find the observed AUC of the winner

Observed mean AUC of c2 = **0.830**

## Step 13 — Find the true AUC of the same classifier

From the truth table:

True AUC of c2 = **0.820**

## Step 14 — Calculate Optimism

Optimism = observed AUC of the declared winner − true AUC of the same classifier

Optimism = 0.830 − 0.820

Optimism = **0.010**

Therefore, the Optimism for replicate 1 is **0.010**.

## Step 15 — Final results

| Quantity | Result |
|---|---:|
| True ranking | c1 > c2 > c3 |
| Observed ranking | c2 > c1 > c3 |
| Observed winner | c2 |
| Kendall's Tau | **0.3333** |
| Optimism | **0.010** |

#  Power (Replicate 1, Pair: c1 vs c2)
>>>>>>> sinchana-dev

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
<<<<<<< HEAD

=======
>>>>>>> sinchana-dev
