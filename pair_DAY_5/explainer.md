# Why "100% Agreement" Lies When Your Marginals Are Concentrated — The Kappa Paradox at Ceiling Ratings

**Day 5 explainer · Topic: Evaluation and statistics · Asked by: Eyoel Nebiyu · Explainer by: Liul J. Teshome**

**Repo under interrogation:** [eyorata/sales_evaluation_bench](https://github.com/eyorata/sales_evaluation_bench)
**Files in scope:** `inter_rater_agreement.json`, `inter_rater_agreement.md`, `memo/memo.md`

---

## The question, restated

Your `inter_rater_agreement.json` reports 100% agreement at ±1 tolerance across n=30 pairs on three ordinal dimensions, and your memo cites this as evidence the rubric is "mechanically gradable." But 97.8% of your t0 ratings are 4 or 5. The question is: how much of that 100% is real agreement, and how much is two raters independently landing in the same narrow basket by chance? Chance-corrected agreement statistics decompose observed agreement into "agreement expected given the marginals" plus "agreement above chance," and at your specific marginals the chance term consumes most of the observed term. That is the kappa paradox, and it means your memo's headline number does not measure what the prose says it measures.

## Cohen's kappa at one confusion matrix

Take the actual confusion matrix from your 90 (pair × dimension) cells, collapsing t0 as rows and t1 as columns over categories {3, 4, 5}:

|       | t1=3 | t1=4 | t1=5 | Row sum |
|-------|------|------|------|---------|
| t0=3  |  2   |  0   |  0   |    2    |
| t0=4  |  4   | 26   |  2   |   32    |
| t0=5  |  0   |  4   | 52   |   56    |
| **Col sum** | **6** | **30** | **54** | **90** |

Observed agreement: p_o = (2 + 26 + 52) / 90 = 80/90 = **0.889**. That is, 88.9% of the time both raters assign the exact same score.

Expected agreement by chance: p_e = Σ_k (n_{k·}/n)(n_{·k}/n), where n_{k·} and n_{·k} are the row and column marginal counts for category k. Concretely: p_e = (2/90)(6/90) + (32/90)(30/90) + (56/90)(54/90) = (12 + 960 + 3024)/8100 = **0.493**.

Cohen's kappa: κ = (p_o − p_e) / (1 − p_e) = (0.889 − 0.493) / (1 − 0.493) = **0.781**.

So raw exact agreement is 89%, but after subtracting what two independent raters would achieve by chance given the marginals, kappa is 0.78 — "substantial" on Landis & Koch's scale, but far from the 1.0 that "100% raw agreement (±1)" implies.

## The kappa paradox: why p_e eats p_o at concentrated marginals

This is the mechanism Feinstein & Cicchetti (1990) named. When one category dominates the marginals — here, 62% of t0 ratings are 5 and 36% are 4 — the chance-agreement term p_e is pulled upward because p_e ≈ Σ π_k², which is maximized when the distribution is concentrated. In the limit where every rating is 5 (π_5 = 1.0), p_e = 1.0 and kappa = (1.0 − 1.0)/(1.0 − 1.0) = 0/0, undefined. Just short of that limit, even high p_o produces low or negative kappa because the denominator (1 − p_e) shrinks faster than the numerator (p_o − p_e). Byrt, Bishop & Carlin (1993) decompose this into a prevalence index and a bias index: your dataset has high prevalence (ratings concentrated at 4–5) and low bias (t0 and t1 marginals are similar), which is exactly the configuration that collapses kappa below what the raw agreement would suggest.

## Linear-weighted kappa for ordinal ratings

Your scale is ordinal (1–5), so a 4-vs-5 disagreement is not the same as a 3-vs-5 disagreement. Unweighted kappa treats both as full disagreements, which understates the rubric's reliability on ordinal data. Cohen (1968) proposed linear weights: w_ij = 1 − |i − j|/(k − 1), where k is the number of categories. On your data with k=3 active categories {3, 4, 5}, the weighted observed agreement is p_o_w = 0.944 and weighted expected agreement is p_e_w = 0.719, giving **κ_w = 0.801**. The improvement over unweighted (0.781 → 0.801) is modest because most of your off-diagonal mass is already at distance 1 — the weighting credits the near-misses but does not escape the paradox. At concentrated marginals, weighted kappa still suffers because p_e_w is still inflated by the dominant categories.

## Gwet's AC1: the paradox-resistant alternative

Gwet (2008) redefines the chance-agreement term. Instead of computing expected agreement from the cross-product of the two raters' marginals (which inflates when one category dominates), AC1 uses the overall dispersion of ratings: p_e_AC1 = (1/(q−1)) Σ π_k(1 − π_k), where π_k is the pooled proportion for category k. When ratings are concentrated, the π_k(1 − π_k) terms are small (a variable near 0 or 1 has low variance), so p_e_AC1 stays low even when kappa's p_e is high. On your data: p_e_AC1 = 0.5 × [0.044 × 0.956 + 0.344 × 0.656 + 0.611 × 0.389] = **0.253**, yielding **AC1 = (0.889 − 0.253)/(1 − 0.253) = 0.851**. That is the honest headline number.

## Numerical prediction on your dataset

From the actual 90-cell confusion matrix above:

| Statistic | Value |
|-----------|-------|
| Raw agreement at ±1 tolerance | 100% (90/90) |
| Exact agreement (p_o) | 88.9% (80/90) |
| Unweighted Cohen's κ | 0.781 |
| Linear-weighted Cohen's κ_w | 0.801 |
| Gwet's AC1 | 0.851 |

```python
import numpy as np

# Actual confusion matrix from inter_rater_agreement.json (90 cells)
# Rows = t0 (rater 1), Cols = t1 (rater 2), categories {3, 4, 5}
C = np.array([[2, 0, 0],    # t0=3
              [4, 26, 2],   # t0=4
              [0, 4, 52]])  # t0=5
n = C.sum()
cats = np.array([3, 4, 5])
k = len(cats)

# Unweighted kappa
p_o = np.trace(C) / n
row_m, col_m = C.sum(axis=1) / n, C.sum(axis=0) / n
p_e = (row_m * col_m).sum()
kappa = (p_o - p_e) / (1 - p_e)

# Linear-weighted kappa
W = 1 - np.abs(cats[:, None] - cats[None, :]) / (cats[-1] - cats[0])
p_o_w = (W * C).sum() / n
p_e_w = (W * np.outer(row_m, col_m)).sum()
kappa_w = (p_o_w - p_e_w) / (1 - p_e_w)

# Gwet's AC1
pi_k = (row_m + col_m) / 2          # pooled proportions
p_e_ac1 = (1 / (k - 1)) * (pi_k * (1 - pi_k)).sum()
ac1 = (p_o - p_e_ac1) / (1 - p_e_ac1)

print(f"Raw ±1 agreement:      100.0%")
print(f"Exact agreement (p_o): {p_o:.3f}")
print(f"Unweighted kappa:      {kappa:.3f}")
print(f"Linear-weighted kappa: {kappa_w:.3f}")
print(f"Gwet's AC1:            {ac1:.3f}")
```

The raw-agreement number (100%) and the kappa (0.78) tell different stories. The gap is the paradox: at your marginals, chance alone accounts for ~49% of exact agreement, leaving only 40 percentage points of "real" agreement out of the 51 percentage points available above chance. AC1 at 0.85 is the most defensible single number because it does not punish you for having concentrated marginals — it only asks whether the agreement is higher than what dispersed random ratings would produce.

## Recommendation for the memo

Replace the "100% inter-rater agreement" claim in `memo/memo.md` with:

> "Across n=30 pairs and three ordinal dimensions with rating marginals concentrated at 4–5 (97.8% of ratings), raw agreement at ±1 tolerance is 100%. Gwet's AC1 = 0.851 on exact matches, indicating substantial inter-rater reliability in the regime where the rubric assigns high scores. AC1 is the paradox-resistant statistic (Gwet 2008); unweighted Cohen's κ = 0.781 and linear-weighted κ = 0.801 are reported alongside for convention. The rubric is reliably gradable in this rating regime; the 100% raw-agreement number alone would overstate this conclusion."

## Grounding commit suggestion

Three artifacts to change:

1. **`inter_rater_agreement.json`** — add a `kappa_and_ac1` block at the top level:
   ```json
   "kappa_and_ac1": {
     "raw_agreement_pct": 100.0,
     "exact_agreement_pct": 88.9,
     "cohens_kappa_unweighted": 0.781,
     "cohens_kappa_linear_weighted": 0.801,
     "gwets_ac1": 0.851,
     "note": "Computed over 90 (pair x dim) cells; categories {3,4,5}; marginals concentrated at 4-5 (97.8%)"
   }
   ```

2. **`inter_rater_agreement.md`** — rewrite the certification sentence to report the triple (raw, kappa, AC1). Drop the "mechanically gradable" framing until AC1 supports it — at 0.85, it does support "reliably gradable in the high-score regime," but not "mechanically gradable" as a blanket claim.

3. **`memo/memo.md`** — replace the "100% IRR" evidence point with the paragraph drafted above.

## What I deliberately did not cover

Bootstrap confidence intervals on kappa at n=30 — Eyoel flagged this out of scope, and correctly so: the point estimate and the paradox mechanism are the gap; uncertainty quantification is a follow-up. Krippendorff's alpha is out of scope per the question. Whether the rubric dimensions themselves are well-designed (e.g., whether "input coherence" and "rubric application clarity" are measuring distinct constructs) is a different question entirely.

## Sources

- Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*, 20(1), 37–46.
- Cohen, J. (1968). Weighted kappa: nominal scale agreement provision for scaled disagreement or partial credit. *Psychological Bulletin*, 70(4), 213–220.
- Feinstein, A. R., & Cicchetti, D. V. (1990). High agreement but low kappa: I. The problems of two paradoxes. *Journal of Clinical Epidemiology*, 43(6), 543–549.
- Gwet, K. L. (2008). Computing inter-rater reliability and its variance in the presence of high agreement. *British Journal of Mathematical and Statistical Psychology*, 61(1), 29–48.
- Byrt, T., Bishop, J., & Carlin, J. B. (1993). Bias, prevalence and kappa. *Journal of Clinical Epidemiology*, 46(5), 423–429.
