#!/usr/bin/env python3
"""
Kappa paradox demo — shows how concentrated marginals inflate raw agreement
while collapsing Cohen's kappa.

Uses the actual marginal distribution from Eyoel's inter_rater_agreement.json:
  {3: 2, 4: 32, 5: 56} across 90 (pair × dimension) cells.
  Pr(5) ≈ 0.622, Pr(4) ≈ 0.356, Pr(3) ≈ 0.022.

The script generates 90 rating pairs sampled IID from that marginal — this
is the "null" scenario where two raters agree only by chance (no real
agreement signal). Even under pure chance, raw agreement at ±1 tolerance
is near 100% because both raters almost always land in {4, 5}.

Run:  python kappa_paradox_demo.py
Modify: change MARGINALS to explore how concentration affects the gap.
"""

import numpy as np

# --- Configuration -----------------------------------------------------------
MARGINALS = {3: 2, 4: 32, 5: 56}  # actual t0 counts from the JSON
N_PAIRS = 90                        # 30 pairs × 3 dimensions
SEED = 42
# -----------------------------------------------------------------------------

rng = np.random.default_rng(SEED)
cats = np.array(sorted(MARGINALS.keys()))
counts = np.array([MARGINALS[c] for c in cats])
probs = counts / counts.sum()
k = len(cats)

# Sample two independent raters from the same marginal (null: no real agreement)
r1 = rng.choice(cats, size=N_PAIRS, p=probs)
r2 = rng.choice(cats, size=N_PAIRS, p=probs)

# --- Raw agreement at ±1 tolerance ------------------------------------------
agree_pm1 = np.mean(np.abs(r1 - r2) <= 1)

# --- Build confusion matrix --------------------------------------------------
C = np.zeros((k, k), dtype=int)
for a, b in zip(r1, r2):
    C[np.searchsorted(cats, a), np.searchsorted(cats, b)] += 1

n = C.sum()
p_o = np.trace(C) / n
row_m = C.sum(axis=1) / n
col_m = C.sum(axis=0) / n

# --- Unweighted Cohen's kappa -----------------------------------------------
p_e = (row_m * col_m).sum()
kappa = (p_o - p_e) / (1 - p_e) if p_e < 1.0 else 0.0

# --- Linear-weighted Cohen's kappa ------------------------------------------
W = 1 - np.abs(cats[:, None] - cats[None, :]) / (cats[-1] - cats[0])
p_o_w = (W * C).sum() / n
p_e_w = (W * np.outer(row_m, col_m)).sum()
kappa_w = (p_o_w - p_e_w) / (1 - p_e_w) if p_e_w < 1.0 else 0.0

# --- Gwet's AC1 --------------------------------------------------------------
pi_k = (row_m + col_m) / 2
p_e_ac1 = (1 / (k - 1)) * (pi_k * (1 - pi_k)).sum()
ac1 = (p_o - p_e_ac1) / (1 - p_e_ac1) if p_e_ac1 < 1.0 else 0.0

# --- Print results -----------------------------------------------------------
print("=" * 60)
print("KAPPA PARADOX DEMO — null (chance-only) agreement")
print(f"Marginals: {dict(zip(cats.tolist(), probs.round(3).tolist()))}")
print(f"N pairs:   {N_PAIRS}  (IID, no real agreement signal)")
print("=" * 60)
print(f"\nConfusion matrix (rater1 rows × rater2 cols):")
print(f"  cats:  {cats.tolist()}")
for i, row in enumerate(C):
    print(f"  {cats[i]}:  {row.tolist()}")
print(f"\n  Raw agreement at ±1:       {agree_pm1:.3f}  ({agree_pm1*100:.1f}%)")
print(f"  Exact agreement (p_o):     {p_o:.3f}")
print(f"  Expected by chance (p_e):  {p_e:.3f}")
print(f"  Unweighted Cohen's kappa:  {kappa:.3f}")
print(f"  Linear-weighted kappa:     {kappa_w:.3f}")
print(f"  Gwet's AC1:                {ac1:.3f}")
print()
print("Interpretation: raw ±1 agreement is near 100% even under pure")
print("chance because both raters almost always land in {4,5}.")
print("Kappa is near 0 because p_e ≈ p_o — the paradox in action.")
print("AC1 stays moderate because its chance term uses dispersion,")
print("not marginal cross-products.")
