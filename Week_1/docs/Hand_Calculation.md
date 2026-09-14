# Component C - Week 1 Hand Calculations

## 1. Winner-Correct Rate

Winner-correct rate measures how often the classifier selected as the observed winner is also the true winner.

For each replicate:

1. Calculate the mean AUC across the 5 folds for c1, c2 and c3.
2. The classifier with the highest mean AUC is the observed winner.
3. Compare the observed winner with the true winner from `truth.csv`.
4. If they are the same, the result is counted as correct (1).
5. If they are different, the result is counted as incorrect (0).

Winner-correct rate:

\[
\text{Winner-correct rate}
=
\frac{\text{Number of correct winners}}
{\text{Number of valid replicates}}
\]

### True AUC Values

| Classifier | True AUC |
|---|---:|
| c1 | 0.85 |
| c2 | 0.82 |
| c3 | 0.76 |

The highest true AUC is 0.85.

Therefore:

**True winner = c1**

---

# n_sub = 100

There are 20 replicates.

For each replicate, the mean AUC is calculated across the 5 folds for each classifier.

## Replicate 1: Detailed Calculation

### c1

\[
(0.81 + 0.78 + 0.84 + 0.80 + 0.82)/5
\]

\[
=4.05/5
\]

\[
=0.8100
\]

### c2

\[
(0.86 + 0.83 + 0.80 + 0.85 + 0.81)/5
\]

\[
=4.15/5
\]

\[
=0.8300
\]

### c3

\[
(0.74 + 0.77 + 0.72 + 0.79 + 0.75)/5
\]

\[
=3.77/5
\]

\[
=0.7540
\]

Therefore:

- c1 = 0.8100
- c2 = 0.8300
- c3 = 0.7540

The highest mean AUC is 0.8300.

**Observed winner = c2**

**True winner = c1**

Therefore:

**Winner correct = 0**

## Winner-Correct Results

| Replicate | Observed Winner | True Winner | Correct |
|---:|---|---|---:|
| 1 | c2 | c1 | 0 |
| 2 | c1 | c1 | 1 |
| 3 | c1 | c1 | 1 |
| 4 | c1 | c1 | 1 |
| 5 | c1 | c1 | 1 |
| 6 | c1 | c1 | 1 |
| 7 | c1 | c1 | 1 |
| 8 | c1 | c1 | 1 |
| 9 | c1 | c1 | 1 |
| 10 | c1 | c1 | 1 |
| 11 | c1 | c1 | 1 |
| 12 | c2 | c1 | 0 |
| 13 | c1 | c1 | 1 |
| 14 | c1 | c1 | 1 |
| 15 | c1 | c1 | 1 |
| 16 | c1 | c1 | 1 |
| 17 | c1 | c1 | 1 |
| 18 | c1 | c1 | 1 |
| 19 | c1 | c1 | 1 |
| 20 | c1 | c1 | 1 |

Correct winners = 18

Incorrect winners = 2

Total valid replicates = 20

\[
\text{Winner-correct rate}
=
\frac{18}{20}
=
0.90
\]

**Winner-correct rate = 90%**

---

# n_sub = 500

There are 20 replicates.

The mean AUC is calculated across the 5 folds for c1, c2 and c3.

## Replicate 1: Detailed Calculation

### c1

\[
(0.8443 + 0.8532 + 0.8506 + 0.8465 + 0.8488)/5
\]

\[
=4.2434/5
\]

\[
=0.84868
\]

\[
=0.8487
\]

### c2

\[
(0.8170 + 0.8218 + 0.8377 + 0.7892 + 0.8172)/5
\]

\[
=4.0830/5
\]

\[
=0.8166
\]

### c3

\[
(0.7621 + 0.7636 + 0.7555 + 0.7389 + 0.7639)/5
\]

\[
=3.7840/5
\]

\[
=0.7568
\]

Therefore:

- c1 = 0.8487
- c2 = 0.8166
- c3 = 0.7568

The highest mean AUC is 0.8487.

**Observed winner = c1**

**True winner = c1**

Therefore:

**Winner correct = 1**

## Winner-Correct Results

All 20 replicates have c1 as the observed winner.

Correct winners = 20

Incorrect winners = 0

Total valid replicates = 20

\[
\text{Winner-correct rate}
=
\frac{20}{20}
=
1.00
\]

**Winner-correct rate = 100%**

---

# 2. Kendall's Tau

We compare the observed ranking of c1, c2 and c3 with their true ranking using replicate 1 at n_sub = 100.

## Step 1: True Ranking

True AUCs:

| Classifier | True AUC |
|---|---:|
| c1 | 0.85 |
| c2 | 0.82 |
| c3 | 0.76 |

Therefore:

**True ranking = c1 > c2 > c3**

## Step 2: Observed Mean AUCs

From replicate 1:

| Classifier | Mean AUC |
|---|---:|
| c1 | 0.810 |
| c2 | 0.830 |
| c3 | 0.754 |

Therefore:

**Observed ranking = c2 > c1 > c3**

## Step 3: Concordant and Discordant Pairs

There are 3 classifier pairs.

### Pair 1: c1 vs c2

Truth: c1 > c2

Observed: c2 > c1

This pair is **discordant**.

### Pair 2: c1 vs c3

Truth: c1 > c3

Observed: c1 > c3

This pair is **concordant**.

### Pair 3: c2 vs c3

Truth: c2 > c3

Observed: c2 > c3

This pair is **concordant**.

Therefore:

- Concordant pairs, C = 2
- Discordant pairs, D = 1

Kendall's tau:

\[
\tau = \frac{C-D}{C+D}
\]

\[
\tau = \frac{2-1}{2+1}
\]

\[
\tau = \frac{1}{3}
\]

\[
\boxed{\tau = 0.3333}
\]

**Kendall's tau for replicate 1 = 0.3333**

---

# 3. Optimism

Optimism is calculated using the declared observed winner, not necessarily the true winner.

## Step 1: Identify the Declared Winner

Observed mean AUCs:

- c1 = 0.810
- c2 = 0.830
- c3 = 0.754

Therefore:

**Declared winner = c2**

## Step 2: Observed AUC of Declared Winner

Observed mean AUC of c2:

\[
0.830
\]

## Step 3: True AUC of the Same Classifier

True AUC of c2:

\[
0.820
\]

## Step 4: Calculate Optimism

\[
\text{Optimism}
=
\text{Observed AUC of declared winner}
-
\text{True AUC of same classifier}
\]

\[
=0.830-0.820
\]

\[
\boxed{\text{Optimism}=0.010}
\]

**Optimism for replicate 1 = 0.010**

---

# 4. Power: Paired t-test for c1 vs c2

We test whether c1 is detectably better than c2 using the 5 paired fold scores from replicate 1 at n_sub = 100.

## Step 1: Paired Fold Differences

| Fold | c1 | c2 | Difference (c1 - c2) |
|---:|---:|---:|---:|
| 1 | 0.81 | 0.86 | -0.05 |
| 2 | 0.78 | 0.83 | -0.05 |
| 3 | 0.84 | 0.80 | +0.04 |
| 4 | 0.80 | 0.85 | -0.05 |
| 5 | 0.82 | 0.81 | +0.01 |

## Step 2: Mean Difference

\[
\bar d =
\frac{-0.05-0.05+0.04-0.05+0.01}{5}
\]

\[
=\frac{-0.10}{5}
\]

\[
\boxed{\bar d=-0.02}
\]

## Step 3: Deviations from the Mean

| Fold | Difference | Difference - Mean | Squared Deviation |
|---:|---:|---:|---:|
| 1 | -0.05 | -0.03 | 0.0009 |
| 2 | -0.05 | -0.03 | 0.0009 |
| 3 | +0.04 | +0.06 | 0.0036 |
| 4 | -0.05 | -0.03 | 0.0009 |
| 5 | +0.01 | +0.03 | 0.0009 |

Sum of squared deviations:

\[
0.0009+0.0009+0.0036+0.0009+0.0009
=0.0072
\]

## Step 4: Sample Variance

There are 5 paired observations.

\[
s^2=\frac{0.0072}{5-1}
\]

\[
\boxed{s^2=0.0018}
\]

## Step 5: Sample Standard Deviation

\[
s=\sqrt{0.0018}
\]

\[
\boxed{s=0.04243}
\]

## Step 6: Standard Error

\[
SE=\frac{s}{\sqrt{n}}
\]

\[
SE=\frac{0.04243}{\sqrt5}
\]

\[
\boxed{SE=0.01897}
\]

## Step 7: t-statistic

\[
t=\frac{\bar d}{SE}
\]

\[
t=\frac{-0.02}{0.01897}
\]

\[
\boxed{t=-1.054}
\]

## Step 8: Degrees of Freedom

\[
df=n-1=5-1=4
\]

For a two-tailed test at α = 0.05 with 4 degrees of freedom, the critical t-value is approximately 2.776.

## Step 9: Statistical Decision

\[
|t|=1.054 < 2.776
\]

Therefore, the result is **not statistically significant**.

The two-tailed p-value is approximately:

\[
\boxed{p\approx0.351}
\]

Since:

\[
p>0.05
\]

there is **no detection**.

Although the mean difference is negative and therefore points in c2's favour, this is **not a sign error**, because a sign error requires a statistically significant result in the wrong direction.

Therefore:

**Classification = No detection**

---

# Final Hand-Calculation Summary

| Statistic | Result |
|---|---:|
| Winner-correct rate, n_sub = 100 | 0.90 |
| Winner-correct rate, n_sub = 500 | 1.00 |
| Kendall's tau, replicate 1 | 0.3333 |
| Optimism, replicate 1 | 0.010 |
| Paired t-statistic, c1 vs c2 | -1.054 |
| p-value | 0.351 |
| Power classification, replicate 1 | No detection |

## Note

The hand calculations above are based on the supplied toy data for replicate 1 and the generated extended results. The Python statistics code should reproduce the corresponding results programmatically.
