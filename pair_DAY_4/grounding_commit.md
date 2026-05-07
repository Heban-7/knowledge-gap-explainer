# Grounding Commit — Day 4

**File edited:** `docs/methodology_rationale.md` (my own Week 11 repo)
**Section:** SimPO selection rationale
**Commit hash:** [abc1234] (placeholder — replace with real hash after commit)

---

## Why this edit was needed

My Week 11 `methodology_rationale.md` justifies picking SimPO on operational grounds: VRAM savings (no reference model), length normalization, and clean preference-only objective. These are the same three arguments my partner used in his `docs/methodology_rationale.md`. After writing today's explainer, I now understand that dropping the reference model also drops the gradient-level mechanism that resists data-distribution skew. My rationale was incomplete — it named the benefits of going reference-free without naming the risk.

---

## The diff

### BEFORE

```markdown
## SimPO Selected

SimPO is chosen over DPO and ORPO for three reasons:
1. No reference model required — halves VRAM, enabling 16-bit LoRA on
   Colab T4 without quantization.
2. Length normalization prevents the model from inflating scores by
   generating longer outputs.
3. Clean preference-only objective makes it easier to diagnose whether
   the preference signal or something else is driving improvement.
```

### AFTER

```markdown
## SimPO Selected

SimPO is chosen over DPO and ORPO for three operational reasons:
1. No reference model required — halves VRAM, enabling 16-bit LoRA on
   Colab T4 without quantization.
2. Length normalization prevents the model from inflating scores by
   generating longer outputs.
3. Clean preference-only objective makes it easier to diagnose whether
   the preference signal or something else is driving improvement.

**Tradeoff accepted:** By dropping the reference model, SimPO also drops
the KL-divergence anchor that resists policy drift from the base model's
prior distribution. Under DPO, the log(π_θ/π_ref) ratio penalizes large
departures from the base model — if a training signal is skewed toward a
particular framing style, the gradient shrinks as the policy diverges,
attenuating the skew. SimPO's reference-free reward has no such mechanism.
This means preference-data skew (e.g., overrepresentation of interrogative
framing in seed pairs) will be absorbed more fully under SimPO than under
DPO. This is an acceptable tradeoff given our VRAM constraints, but it
makes balanced preference-pair coverage load-bearing: the data fix that
DPO's KL term would have partially handled must be handled entirely in
data curation.
```

---

## Why this matters operationally

This is not just a documentation fix. My Week 11 preference pairs have a similar coverage question: if any framing style is overrepresented in my seed data, SimPO will absorb that skew without resistance. The Day 2 grounding commit taught me that a paragraph I could not defend was hiding a real code bug. This one is hiding a real data-curation requirement: I need to audit my preference-pair distribution for framing-style balance before retraining, because the loss function will not compensate.

---

## What this proves

I had a rationale paragraph that listed three benefits of SimPO without naming the tradeoff that comes with each one. The VRAM benefit comes with a bias-amplification risk. The clean objective comes with a missing regularizer. Now the paragraph names both sides. A reviewer reading this and asking "what happens if your training data is skewed?" gets a real answer instead of silence.
