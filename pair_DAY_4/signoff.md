# Sign-off — Day 4

**Explainer (me):** Liul J. Teshome
**Asker (partner):** Mamaru Yirga
**Status:** CLOSED

---

## Explainer's judgment

I am the explainer today. I am signing off on whether my explainer closed Mamaru's gap on why DPO, SimPO, and ORPO produce different judges even on the same preference pairs — and specifically whether DPO's reference-model KL term would have dampened the interrogative-framing bias in his 121 preference pairs.

**Status: CLOSED.** My explainer is mechanistically correct, grounded in his specific situation, and gives him a concrete edit he can make to `docs/memo.md`.

**Justification:**

1. **Mechanistic correctness.** The explainer presents the three loss functions side by side and names what each penalizes at the gradient level. DPO's loss computes log(π_θ/π_ref), meaning every update is measured against the reference model — the gradient vanishes when the policy already matches the prior. SimPO's loss uses the average log-probability under the policy alone with no reference anchor. ORPO combines SFT + odds-ratio loss with no explicit KL term. These are correct characterizations grounded in Rafailov et al. (2023), Meng et al. (2024), and Hong et al. (2024).

2. **Grounded in his specific situation.** The explainer directly references his 121 preference pairs, his 9/12 interrogative-skewed seed pairs, and the ~8/65 dev-task failure mode from his `docs/memo.md` Skeptic's Appendix. It explains why SimPO specifically — not just "preference optimization in general" — absorbed the skew: the reference-free formulation has no mechanism to resist policy drift away from the base model's framing distribution.

3. **Concrete edit provided.** The explainer includes a rewritten paragraph for the "One unresolved training failure" section of `docs/memo.md`. The rewrite names both the data cause (9/12 seeds interrogative) and the algorithmic cause (SimPO's reference-free loss has no anchoring term). This is the exact paragraph he said he wanted to revise.

4. **Explicit epistemic boundaries.** The "What I deliberately did not claim" section states that DPO would not have eliminated the bias — only that the KL term provides a dampening mechanism SimPO lacks. It names the experiment that would confirm the claim (re-run training under all three losses on the same 121 pairs). This prevents over-reading the explainer.

---

## What he understands now that he didn't before

1. "The interrogative-framing bias in my judge is not purely a data problem. SimPO's reference-free loss function has no term that resists divergence from the base model's framing distribution, so a skewed preference signal gets fully absorbed into the policy. DPO's log(π_θ/π_ref) ratio would have created gradient resistance at exactly the point where the policy drifted from the base model's prior."

2. "My `methodology_rationale.md` justifies SimPO on operational grounds — VRAM savings, length normalization, clean objective. Those are real advantages. But the rationale is missing a risk: by dropping the reference model, I also dropped the mechanism that would have dampened data-distribution skew. The VRAM savings came with a bias-amplification tradeoff I did not name."

3. "The fix for my 'unresolved training failure' paragraph is not just 'add more assertive pairs.' That is necessary under any loss. But the algorithmic reason the bias manifested as strongly as it did — 12% false-approval on assertive tasks — is that SimPO provided no resistance. Under DPO, the same data skew would have produced a smaller effect."

---

## Before/after: how he would answer if a CTO asked the question

### Before (Day 0)

> "We picked SimPO because it doesn't need a reference model, which saves VRAM. The judge has a bias toward interrogative framing because most of our seed pairs were interrogative. We need more assertive training pairs."

(Names the data cause only. Does not explain why SimPO specifically amplified the skew.)

### After (Day 4)

> "We picked SimPO for VRAM efficiency and clean objective isolation, but the reference-free formulation has a tradeoff: it provides no gradient resistance to data-distribution skew. Our 9/12 interrogative seed pairs created a biased preference signal, and SimPO absorbed it fully because there is no π_ref term pulling the policy back toward the base model's framing prior. DPO's KL term would have attenuated — not eliminated — the bias by penalizing large departures from the base distribution. The fix is two-part: add assertive-framing pairs (data fix, necessary under any loss) and consider whether the reference-free tradeoff is worth it given our seed-pair coverage (algorithmic decision)."

(Names the mechanism. Names the tradeoff. Names both the data fix and the algorithmic decision.)
