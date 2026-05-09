# Portfolio Update — Post Week 12

## What changed in my Week 10/11 portfolio this week

I shipped a Conversion Engine in Week 10 and built a preference-trained judge in Week 11. This week I closed knowledge gaps that produced two concrete edits: the Tool Invocation section of `docs/architecture.md` (Week 10) now names the reliability mechanism and failure mode instead of citing a black-box property, and the SimPO selection rationale in `docs/methodology_rationale.md` (Week 11) now names the bias-amplification tradeoff of dropping the reference model.

## The two grounding commits

| Day | File edited | What went from indefensible to defensible | Mechanism now named | Follow-up surfaced |
|-----|------------|-------------------------------------------|---------------------|--------------------|
| 3 | `docs/architecture.md` (Week 10), Tool Invocation section | "Function calling is more reliable" → names training-based reliability, the "valid syntax, wrong semantics" failure mode, and the schema-validation guardrail in `orchestrator/validate.py`. | Training-based reliability vs constrained decoding; residual failure mode under unconstrained sampling | `validate.py` only checks JSON parsing, not schema compliance (issue #47) |
| 4 | `docs/methodology_rationale.md` (Week 11), SimPO selection rationale | Three-benefit list with zero risks → adds "Tradeoff accepted" paragraph naming the KL-divergence anchor SimPO drops and the data-curation load it shifts to the engineer. | DPO's log(π_θ/π_ref) as gradient-level bias resistance; SimPO's reference-free reward absorbs data skew fully | Preference-pair distribution must be audited for framing-style balance before retraining |

Days 1_2 and 5 do not have grounding commits in the repo. The explainers I wrote on those days are complete (attention-sink rubric bias, kappa paradox at concentrated marginals), but the asker-side artifacts — signoff and grounding commit — were not committed before this synthesis.

## What this changes for a CTO interrogating my portfolio

On Day 0, if asked "what makes your function calling reliable?", I would have said: "The API handles structured output for us." Now I can say: "Reliability comes primarily from the model being fine-tuned on tool-call data, not from grammar-constrained decoding. The residual failure mode is valid-syntax-wrong-semantics — structurally valid JSON with schema-noncompliant field values. We catch these with a schema-validation layer in the orchestrator, and if we needed stronger guarantees, we'd switch to vLLM + outlines for grammar-constrained decoding."

On Day 0, if asked "why SimPO instead of DPO?", I would have said: "It doesn't need a reference model, which saves VRAM." Now I can say: "SimPO saves VRAM by dropping the reference model, but that also drops the KL-divergence anchor that resists policy drift from the base model's prior. If our preference data has a framing-style skew — and ours did — DPO's log(π_θ/π_ref) ratio would attenuate it at the gradient level; SimPO absorbs it fully. We accepted this tradeoff given our VRAM constraints, but it makes balanced preference-pair coverage load-bearing."

## Public artifacts shipped this week

- Day 1_2: [BLOG_URL_DAY_1_2] · [THREAD_URL_DAY_1_2]
- Day 3: [BLOG_URL_DAY_3] · [THREAD_URL_DAY_3]
- Day 4: [BLOG_URL_DAY_4] · [THREAD_URL_DAY_4]
- Day 5: [BLOG_URL_DAY_5] · [THREAD_URL_DAY_5]
