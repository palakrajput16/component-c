#  Power (Replicate 1, Pair: c1 vs c2)

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