# Thread — Day 5: The Kappa Paradox at Ceiling Ratings

**Topic:** Evaluation and statistics — why "100% inter-rater agreement" can be a prevalence artifact

---

**1/**
Your benchmark reports 100% inter-rater agreement. Your marginals are 97% concentrated at ratings 4–5. Those two facts together mean the headline number is lying — most of that "agreement" is two raters independently landing in the same narrow basket by chance. Here's how to tell the difference.

**2/**
Cohen's kappa: κ = (p_o − p_e) / (1 − p_e). p_o is observed agreement; p_e is expected agreement by chance given the marginals. When marginals are concentrated (e.g., 62% of ratings are 5), p_e is high — on our data, p_e = 0.493. So even with p_o = 0.889, kappa = 0.781. That's "substantial," not "perfect." The denominator (1 − p_e) is what punishes you: as p_e → 1, kappa → 0 regardless of how high p_o is.

**3/**
Run the demo: sample 90 rating pairs IID from {Pr(5)=0.62, Pr(4)=0.36, Pr(3)=0.02}. No real agreement signal — pure chance. Raw ±1 agreement: ~98%. Unweighted kappa: ~0. That's the paradox in one script. The code is 68 lines of numpy: `kappa_paradox_demo.py`.

**4/**
Ordinal scales need weighted kappa (Cohen 1968). Unweighted kappa treats a 4-vs-5 disagreement the same as a 3-vs-5. Linear weights credit near-misses: κ_w = 0.801 on our data, vs 0.781 unweighted. Better — but weighted kappa still suffers the paradox at concentrated marginals. It is not a fix, just a fairer accounting.

**5/**
Gwet's AC1 (2008) is the paradox-resistant alternative. It redefines chance agreement as a function of overall rating dispersion, not marginal cross-products. When ratings are concentrated, AC1's chance term stays low instead of inflating. Our data: AC1 = 0.851. That's the honest headline number.

**6/**
The rewrite: "Across n=30 pairs and 3 ordinal dimensions with marginals concentrated at 4–5, raw ±1 agreement is 100%. Gwet's AC1 = 0.851 on exact matches. The rubric is reliably gradable in this regime; the 100% number alone overstates the conclusion." Report the triple: (raw, κ_w, AC1). Always.

**7/**
If your benchmark has concentrated ratings and you're reporting raw agreement without a chance-corrected statistic, you're publishing a prevalence artifact. The fix is five lines of numpy and one honest sentence. Full explainer on the blog: [link TBD]
