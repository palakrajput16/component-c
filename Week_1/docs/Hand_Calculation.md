<<<<<<< HEAD
# Winner-Correct Rate.

Winner-correct rate measures how often the classifier selected as the observed winner is also the true winner.

For each replicate:

1. Calculate the mean AUC across the 5 folds for c1, c2 and c3.
2. The classifier with the highest mean AUC is the observed winner.
3. Compare the observed winner with the true winner from `truth.csv`.
4. If they are the same, the result is counted as correct (1).
5. If they are different, the result is counted as incorrect (0).

Winner-correct rate:

Number of correct winners / Number of valid replicates


## True AUC Values

The true AUC values are given in `truth.csv`.

| Classifier | True AUC |
|---|---:|
| c1 | 0.85 |
| c2 | 0.82 |
| c3 | 0.76 |

The highest true AUC is 0.85.

Therefore:

True winner = c1


# n_sub = 100

There are 20 replicates.

For each replicate, the mean AUC is calculated across the 5 folds for each classifier.

## Observed Winner Calculation

| Replicate | Mean c1 | Mean c2 | Mean c3 | Observed Winner |
|---:|---:|---:|---:|---|
| 1 | 0.8100 | 0.8300 | 0.7540 | c2 |
| 2 | 0.8430 | 0.8035 | 0.7832 | c1 |
| 3 | 0.8456 | 0.8184 | 0.7697 | c1 |
| 4 | 0.8572 | 0.8200 | 0.7668 | c1 |
| 5 | 0.8644 | 0.8107 | 0.7648 | c1 |
| 6 | 0.8461 | 0.8245 | 0.7412 | c1 |
| 7 | 0.8552 | 0.8050 | 0.7667 | c1 |
| 8 | 0.8386 | 0.7901 | 0.7626 | c1 |
| 9 | 0.8333 | 0.8109 | 0.7676 | c1 |
| 10 | 0.8610 | 0.8135 | 0.7402 | c1 |
| 11 | 0.8853 | 0.7972 | 0.7604 | c1 |
| 12 | 0.8261 | 0.8284 | 0.7632 | c2 |
| 13 | 0.8515 | 0.7978 | 0.7745 | c1 |
| 14 | 0.8685 | 0.8254 | 0.7706 | c1 |
| 15 | 0.8443 | 0.8230 | 0.7367 | c1 |
| 16 | 0.8417 | 0.8342 | 0.7544 | c1 |
| 17 | 0.8744 | 0.8112 | 0.7281 | c1 |
| 18 | 0.8355 | 0.8283 | 0.7633 | c1 |
| 19 | 0.8453 | 0.8175 | 0.7710 | c1 |
| 20 | 0.8722 | 0.8198 | 0.7530 | c1 |


## Replicate 1 - Detailed Calculation

### c1

(0.81 + 0.78 + 0.84 + 0.80 + 0.82) / 5

= 4.05 / 5

= 0.8100


### c2

(0.86 + 0.83 + 0.80 + 0.85 + 0.81) / 5

= 4.15 / 5

= 0.8300


### c3

(0.74 + 0.77 + 0.72 + 0.79 + 0.75) / 5

= 3.77 / 5

= 0.7540


The mean AUCs are:

c1 = 0.8100

c2 = 0.8300

c3 = 0.7540

The highest mean AUC is 0.8300.

Observed winner = c2

True winner = c1

Therefore:

Winner correct = 0


## Winner-Correct Results

Since c1 is the true winner:

- If c1 is the observed winner, the replicate is correct.
- If c2 is the observed winner, the replicate is incorrect.
- If c3 is the observed winner, the replicate is incorrect.

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


## Final Calculation for n_sub = 100

Correct winners:

18

Incorrect winners:

2

Total valid replicates:

20

Winner-correct rate:

18 / 20

= 0.90

Winner-correct rate = 90%


# n_sub = 500

There are 20 replicates.

The mean AUC is calculated across the 5 folds for c1, c2 and c3.


## Observed Winner Calculation

| Replicate | Mean c1 | Mean c2 | Mean c3 | Observed Winner |
|---:|---:|---:|---:|---|
| 1 | 0.8487 | 0.8166 | 0.7568 | c1 |
| 2 | 0.8516 | 0.8254 | 0.7711 | c1 |
| 3 | 0.8473 | 0.8304 | 0.7538 | c1 |
| 4 | 0.8511 | 0.8204 | 0.7603 | c1 |
| 5 | 0.8448 | 0.8261 | 0.7593 | c1 |
| 6 | 0.8501 | 0.8223 | 0.7686 | c1 |
| 7 | 0.8530 | 0.8127 | 0.7577 | c1 |
| 8 | 0.8462 | 0.8223 | 0.7623 | c1 |
| 9 | 0.8432 | 0.8103 | 0.7694 | c1 |
| 10 | 0.8411 | 0.8228 | 0.7561 | c1 |
| 11 | 0.8441 | 0.8235 | 0.7618 | c1 |
| 12 | 0.8603 | 0.8217 | 0.7473 | c1 |
| 13 | 0.8532 | 0.8211 | 0.7653 | c1 |
| 14 | 0.8555 | 0.8183 | 0.7631 | c1 |
| 15 | 0.8387 | 0.8130 | 0.7653 | c1 |
| 16 | 0.8475 | 0.8268 | 0.7616 | c1 |
| 17 | 0.8571 | 0.8131 | 0.7554 | c1 |
| 18 | 0.8435 | 0.8210 | 0.7677 | c1 |
| 19 | 0.8399 | 0.8211 | 0.7616 | c1 |
| 20 | 0.8453 | 0.8230 | 0.7499 | c1 |


## Replicate 1 - Detailed Calculation

### c1

(0.8443 + 0.8532 + 0.8506 + 0.8465 + 0.8488) / 5

= 4.2434 / 5

= 0.84868

= 0.8487


### c2

(0.8170 + 0.8218 + 0.8377 + 0.7892 + 0.8172) / 5

= 4.0830 / 5

= 0.8166


### c3

(0.7621 + 0.7636 + 0.7555 + 0.7389 + 0.7639) / 5

= 3.7840 / 5

= 0.7568


The mean AUCs are:

c1 = 0.8487

c2 = 0.8166

c3 = 0.7568

The highest mean AUC is 0.8487.

Observed winner = c1

True winner = c1

Therefore:

Winner correct = 1


## Winner-Correct Results

Since c1 is the true winner, every replicate where c1 is the observed winner is correct.

| Replicate | Observed Winner | True Winner | Correct |
|---:|---|---|---:|
| 1 | c1 | c1 | 1 |
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
| 12 | c1 | c1 | 1 |
| 13 | c1 | c1 | 1 |
| 14 | c1 | c1 | 1 |
| 15 | c1 | c1 | 1 |
| 16 | c1 | c1 | 1 |
| 17 | c1 | c1 | 1 |
| 18 | c1 | c1 | 1 |
| 19 | c1 | c1 | 1 |
| 20 | c1 | c1 | 1 |


## Final Calculation for n_sub = 500

Correct winners:

20

Incorrect winners:

0

Total valid replicates:

20

Winner-correct rate:

20 / 20

= 1.00

Winner-correct rate = 100%


# Final Winner-Correct Rate Summary

| n_sub | True Winner | Correct Winners | Incorrect Winners | Total Replicates | Winner-Correct Rate |
|---:|---|---:|---:|---:|---:|
| 100 | c1 | 18 | 2 | 20 | 0.90 (90%) |
| 500 | c1 | 20 | 0 | 20 | 1.00 (100%) |

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
