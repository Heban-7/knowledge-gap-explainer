# Day 4 — Question

**Topic of the day:** Preference optimization mechanics / confidence-gated phrasing

**Asker:** Liul J. Teshome
**Explainer (partner):** Mamaru Yirga

---

## Final question

In my Week 10 `method.md`, I claim "The mechanism links source reliability and signal confidence directly to message phrasing and send eligibility, reducing factual over-claims while preserving conversion performance." I cannot mechanically defend this. Specifically:

**(a)** When confidence changes from high to medium or low, what part of the post-training/prompt-policy stack should force the model from assertions into probabilistic or question-only wording rather than merely hoping the prompt complies?

**(b)** How should send eligibility be separated from generation so the ablation can attribute over-claim reduction to the confidence gate rather than generic prompt cleanup?

Closing this gap would let me rewrite `method.md` Core Mechanism/Ablation Variants and align `agent/composer.py` plus `agent/policy.py` with the claimed intervention.

---

## Grounding artifact

- **File:** `method.md`, section "Core Mechanism / Ablation Variants"
- **Specific claim:** "The mechanism links source reliability and signal confidence directly to message phrasing and send eligibility, reducing factual over-claims while preserving conversion performance."
- **Why I can't defend it:** I cite confidence-gated phrasing as a property but cannot name the structural mechanism that enforces it. If a reviewer asked "what stops the model from generating assertive language when confidence is low?" my answer is currently "the prompt tells it not to" — which is not a mechanism, it is a hope.

---

## What "gap closed" would look like

I can rewrite the mechanism claim from a property statement to:

> _"Confidence-gated phrasing is enforced by [specific structural mechanism in the generation stack], and send eligibility is checked by [independent gate] that runs after generation. This separation allows the ablation to attribute over-claim reduction to [specific component] by disabling each in isolation."_

A satisfying explainer answers: (1) where in the stack does enforcement live (prompt, logits processor, post-generation filter), and (2) how does the architecture make single-variable ablation possible.

---

## Self-check against the four properties

- **Diagnostic:** Names two specific sub-problems — (a) the enforcement mechanism for confidence-to-phrasing mapping, (b) the generation/eligibility separation for clean ablation. Not "how does confidence work."
- **Grounded:** Points to `method.md`, `agent/composer.py`, and `agent/policy.py` with a specific claim I cannot defend.
- **Generalizable:** Any engineer building a production LLM system with confidence-dependent output constraints faces this exact gap — prompt compliance is unreliable when RLHF priors push toward assertiveness.
- **Resolvable:** ~800 words can cover logits-processor mechanics + two-step architecture + ablation design.
