# Week 12 Synthesis

## Note on structure

Day 1 and Day 2 were worked as one merged session due to a program-side schedule issue — I was paired with the same partner across both days and we worked a single question/explainer pair. The week therefore produced four pair folders (`pair_DAY_1_2`, `pair_DAY_3`, `pair_DAY_4`, `pair_DAY_5`) and closed eight gaps total: four I asked about and four I researched and explained. All references in the program brief to "10 gaps / 5 + 5" should be read as "8 gaps / 4 + 4" for my specific case.

I should also note upfront that two of my four pair folders are incomplete on the asker side. `pair_DAY_1_2` is missing `question.md`, `signoff.md`, and `grounding_commit.md`. `pair_DAY_5` is missing `signoff.md` and `grounding_commit.md`. I'll note these gaps where they affect the narrative below rather than writing around them.

## The eight gaps closed

| Day | Role | Topic | Mechanism named | Status | Grounding commit |
|-----|------|-------|-----------------|--------|-----------------|
| 1_2 | Asker | *(Missing — no question.md in repo)* | Unknown | Unknown | None |
| 1_2 | Explainer | Attention sinks + rubric-prefix bias in LLM judges | Softmax sink amplification + U-shaped attention + negative-vocabulary priming | *(Signoff in partner's repo)* | — |
| 3 | Asker | Function-calling reliability mechanism | Training-based reliability vs constrained decoding; "valid syntax, wrong semantics" failure mode | CLOSED | `docs/architecture.md` (Week 10) |
| 3 | Explainer | Tool descriptions and selection at the token level | Descriptions as conditioning context for next-token tool-name prediction | *(Signoff in partner's repo)* | — |
| 4 | Asker | Confidence-gated phrasing enforcement | LogitsProcessor + independent send gate; four-condition ablation | *(No formal signoff — evening call confirms it landed with caveats)* | None for this question |
| 4 | Explainer | DPO vs SimPO vs ORPO on biased preference data | Reference-model KL as gradient-level bias dampening | CLOSED | `docs/methodology_rationale.md` (Week 11) |
| 5 | Asker | Centroid-based embedding drift: the first-moment trap | n_eff mismatch + first-moment blindness to dispersion/multimodality | *(No signoff in repo)* | None |
| 5 | Explainer | Kappa paradox at concentrated marginals | Chance-inflated agreement; Gwet's AC1 as paradox-resistant alternative | *(Signoff in partner's repo)* | — |

## What I asked: the four gaps I named in my own work

**Day 1_2.** No `question.md` exists in the repo for this day. The explainer I wrote is present (rubric-prefix bias), but I cannot document what question I asked my partner or what I learned as asker. This is a gap in the record, not a gap I chose to leave open.

**Day 3.** My Week 10 architecture doc claimed "function calling is more reliable than free-text JSON parsing" without explaining why. I asked whether the reliability comes from constrained decoding at the API layer or from training, and what the failure mode looks like when reliability breaks. Rafia's explainer gave me the answer: Anthropic uses primarily training-based reliability (no grammar enforcement during decoding), and the failure mode is structurally valid JSON with semantically wrong field values — for example, a string where a Unix timestamp is expected. I rewrote the Tool Invocation section to name the mechanism, the failure mode, and the schema-validation guardrail in `orchestrator/validate.py`. The edit also surfaced a real bug: `validate.py` was checking JSON parsing but not schema compliance (issue #47 filed).

**Day 4.** My Week 10 `method.md` claimed that "the mechanism links source reliability and signal confidence directly to message phrasing and send eligibility" without naming what part of the stack enforces this. I asked where enforcement lives — in the prompt, in a logits processor, or in a post-generation filter — and how to separate generation from eligibility for a clean ablation. Mamaru's explainer gave me the structural answer: a `LogitsProcessor` operating below the RLHF-trained distribution makes non-compliant phrasing structurally impossible at low confidence, and an independent send gate runs after generation. A four-condition ablation (no gate/no processor, gate only, processor only, both) enables single-variable attribution. The evening call confirmed this landed, though with caveats: the token-masking list was too coarse and no before/after diff of my actual artifact was provided. There is no formal signoff in the repo, and I did not commit a grounding edit for this question.

**Day 5.** My Week 7 evaluation artifacts reported "centroid-based cosine distance" with "Sample size: 251" and "drift_score: 0.0 → PASS → stable AI data contracts." I asked what the correct effective sample size is when the code caps embeddings at 200 but the report cites the input list length, and what evidence chain is required before "semantically stable" is a defensible sentence. No signoff or grounding commit exists in the repo for this question.

## What I taught: the four explainers I wrote

**Day 1_2: Rubric-prefix bias in LLM judges.** My partner's question (not preserved in my repo) was about LLM-as-judge calibration. I explained that a long rubric is not a neutral container: attention sinks (Xiao et al. 2023) amplify the first tokens, lost-in-the-middle (Liu et al. 2023) drops the middle criteria, and prefix priming narrows the output distribution toward negative-vocabulary tokens. The combined effect is that the verdict is dominated by prompt geometry — the rubric's opening framing, its closing instruction, and its vocabulary prior — not by candidate quality. I proposed a concrete diagnostic: a rubric-criterion permutation test across 20 seeds, measuring accept-rate variance on a fixed candidate set.

**Day 3: Tool descriptions and selection at the token level.** Rafia's question was about why her sales agent picked the wrong tool when two were plausible, and whether the tool description string actually participates in selection or whether the model just pattern-matches on the name. I explained that there is no separate selection model — tool selection is next-token prediction, and every tool's name, description, and schema are serialized into the prompt as conditioning context. I ran a 10-trial demo on Claude Sonnet 4.5 showing that switching from vague to specific descriptions (same tool names, same query) moved selection accuracy from 60% to 100%. I did not receive a formal signoff from Rafia in my repo; that would be in hers.

**Day 4: DPO's reference model vs SimPO's reference-free reward on biased preference data.** Mamaru asked why his SimPO-trained judge had an interrogative-framing bias, and whether DPO's reference model would have dampened it. I wrote out the three loss functions (DPO, SimPO, ORPO) side by side and traced what each penalizes at the gradient level. The load-bearing insight: DPO's log(π_θ/π_ref) ratio creates gradient resistance to policy drift — when the policy moves far from the base model's prior, the sigmoid saturates and the gradient shrinks. SimPO has no such anchor; it absorbs data skew fully. ORPO's SFT term provides weaker, untargeted resistance. I provided a rewritten paragraph for Mamaru's `docs/memo.md`. Signoff: **CLOSED**.

**Day 5: The kappa paradox at concentrated marginals.** Eyoel's benchmark reported 100% inter-rater agreement, but 97.8% of ratings were 4 or 5. I computed Cohen's κ on the actual 90-cell confusion matrix (κ = 0.781) and explained the paradox: when marginals are concentrated, chance-expected agreement p_e inflates because p_e ≈ Σπ_k², which is maximized when the distribution is concentrated. Gwet's AC1 (0.851) is paradox-resistant because its chance term uses dispersion rather than marginal cross-products. I wrote an 87-line numpy demo (`kappa_paradox_demo.py`) that shows the paradox under null conditions. I did not receive a formal signoff from Eyoel in my repo.

## The most surprising thing I learned

The DPO/SimPO comparison on Day 4 — specifically, the realization that an infrastructure decision (dropping the reference model to save VRAM) is also a statistical decision (dropping the gradient-level mechanism that resists data-distribution skew).

I expected the three preference-optimization losses to differ in convergence speed or benchmark scores. I did not expect them to differ in *what they protect against*. The reference model in DPO is usually discussed as a training cost (doubles VRAM, requires a frozen copy of the base model). What I learned by writing the loss functions side by side is that π_ref provides a per-example importance weight: updates that push the policy far from the base distribution get down-weighted because the log-ratio grows large and the sigmoid saturates. SimPO has no such term. Its reward is the average log-probability under the policy alone, and its gradient pushes the chosen response's probability up and the rejected response's down with no anchor pulling back.

This changes how I'd evaluate any preference-optimization choice in production. The question isn't just "can I afford the VRAM?" — it's "can I afford the bias exposure if my preference data is skewed?" My Week 11 methodology rationale now names both sides. Before Day 4, it named only benefits.

## What I'd do differently in Weeks 10 and 11 with this knowledge

Three specific changes. First, I would have added a schema-validation step (not just JSON-parse validation) to `orchestrator/validate.py` in Week 10 from the start — the "valid syntax, wrong semantics" failure mode should have been anticipated the moment I chose a training-based provider without constrained decoding. Second, I would have audited my Week 11 preference-pair distribution for framing-style balance before training with SimPO, because I now know the loss function will not compensate for skew. Third, I would have reported Gwet's AC1 alongside raw agreement in any evaluation artifact with concentrated rating marginals — the five-line computation in `kappa_paradox_demo.py` is trivial, and the interpretive difference between "100% agreement" and "AC1 = 0.85" is the difference between a defensible claim and a prevalence artifact.

## Trajectory: question quality from Day 1 to Day 5

Day 1_2's question is missing from the repo, so the earliest comparison point is Day 3.

Day 3: "When a model emits a function call via the API's `tools` parameter, are the JSON-structure tokens generated the same way as any other text (just sampled from the distribution), or is the decoder actually constrained to a grammar at inference time?" This names a binary mechanism distinction and points to a specific paragraph in `docs/architecture.md`. The question is diagnostic but grounded at the file level — it doesn't name a line number or a specific discrepancy in the code.

Day 5: "What is the correct effective sample and statistic definition when the implementation caps embeddings at 200 (`embed_sample(texts, n=200)` in `contracts/ai_extensions.py`, line 53) but the report cites 'Sample size: 251' (the length of the input text list, not the number of embeddings actually computed)?" This names the file, the function, the line number, the exact numerical discrepancy, and frames the gap as a provenance issue rather than a vague correctness concern. Day 5 also includes a self-rating table against the four question properties — a metacognitive step absent in Day 3.

Diagnosticity improved. The Day 3 question asks *which of two mechanisms* is at work; the Day 5 question identifies a *specific inconsistency between code and report* and asks what evidence chain would resolve it. The morning call summaries show the same trajectory: Day 3's call sharpened "how does function calling work?" into a mechanism question; Day 5's call started from "my drift detection is probably too simple" and Eyoel pushed it to the exact n_eff mismatch and the evidence-chain gap between a geometric statistic and a semantic claim. The sharpening process itself got more targeted.

## Canonical contributions to the cohort

The full annotated reading list is in `canonical_list.md`. The three most load-bearing items I'd point a fellow FDE to: Feinstein & Cicchetti (1990) on the kappa paradox, because anyone reporting inter-rater reliability on a benchmark with concentrated ratings is publishing a prevalence artifact without knowing it; Rafailov et al. (2023) on DPO, specifically the gradient analysis in Section 5 that reveals the reference model's role as a bias-resistance mechanism, not just a training cost; and Xiao et al. (2023) on attention sinks, because the implication — that the first tokens of any prompt are structurally amplified regardless of content — changes how you think about every prompted system, not just judges.

## Closing reflection

The trajectory across Weeks 10, 11, and 12 is: ship a system, evaluate it under adversarial conditions, then find the places where you cited a property without knowing the mechanism and close those gaps by teaching someone else. The specific capability gain this week is the ability to name mechanisms where I previously named behaviors. "Function calling is reliable" became "reliability comes from training, fails as valid-syntax-wrong-semantics, and needs a schema-validation guardrail." "SimPO is efficient" became "SimPO trades bias resistance for VRAM savings, and that tradeoff is load-bearing when preference data is skewed." "100% agreement" became "AC1 = 0.85, and the gap is a prevalence artifact." Ship, evaluate, teach — the program's closing line — is a compression pipeline: each stage forces you to understand the previous stage's output at a deeper level than the stage itself required.
