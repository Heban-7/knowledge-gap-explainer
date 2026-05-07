# Sources — Day 4

**For the explainer I wrote** (DPO/SimPO/ORPO loss functions and bias amplification)

---

## Primary sources (read in full or relevant sections)

### Paper 1 — Direct Preference Optimization: Your Language Model is Secretly a Reward Model
- **Authors:** Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C.D., & Finn, C.
- **Venue:** NeurIPS 2023
- **Link:** https://arxiv.org/abs/2305.18290
- **Why it matters:** Establishes the DPO loss function that reparameterizes RLHF reward maximization into a classification loss over preference pairs. The log(π_θ/π_ref) ratio is the load-bearing term for my explainer: it provides the KL-divergence anchor that penalizes policy drift from the base model's prior.
- **Specific sections used:** Section 4 (the DPO objective derivation), Section 5 (gradient analysis showing how the reference model creates an implicit per-example importance weight).

### Paper 2 — SimPO: Simple Preference Optimization with a Reference-Free Reward
- **Authors:** Meng, Y., Xia, M., & Chen, D.
- **Venue:** NeurIPS 2024
- **Link:** https://arxiv.org/abs/2405.14734
- **Why it matters:** Defines the reference-free reward as the average log-probability under the policy alone, with a target reward margin γ. The absence of π_ref in the loss is the structural reason my partner's interrogative-framing bias was fully absorbed. Length normalization addresses length gaming but not framing-distribution skew.
- **Specific sections used:** Section 2.1 (length-normalized reward), Section 2.2 (reference-free formulation), Section 3.1 (hyperparameters β and γ).

### Paper 3 — ORPO: Monolithic Preference Optimization without Reference Model
- **Authors:** Hong, J., Lee, N., & Thorne, J.
- **Venue:** EMNLP 2024
- **Link:** https://arxiv.org/abs/2403.07691
- **Why it matters:** Combines SFT and odds-ratio preference loss in a single monolithic objective L_ORPO = L_SFT + λ·L_OR. The SFT component provides weak regularization toward on-distribution outputs but no explicit KL anchor against the base model's prior. Positions ORPO between DPO (explicit anchor) and SimPO (no anchor) on the bias-resistance spectrum.
- **Specific sections used:** Section 3.2 (monolithic loss formulation), Section 4 (comparison to DPO on small datasets).

---

## Tool / documentation references

### HuggingFace TRL — DPO Trainer
- **Link:** https://huggingface.co/docs/trl/en/dpo_trainer
- **Why it matters:** Canonical implementation reference for DPO loss in the TRL library. Confirms that the reference model is a frozen copy of the SFT checkpoint loaded alongside the policy model during training.

### HuggingFace TRL — CPO Trainer (SimPO loss)
- **Link:** https://huggingface.co/docs/trl/en/cpo_trainer
- **Why it matters:** SimPO loss is implemented as an alternative loss type within TRL's CPO Trainer. Confirms the length-normalization and reference-free formulation match the paper.

### HuggingFace TRL — ORPO Trainer
- **Link:** https://huggingface.co/docs/trl/v0.11.4/en/orpo_trainer
- **Why it matters:** Documents the monolithic SFT + odds-ratio loss and the λ weighting parameter.

---

## What I deliberately did not cite

- I avoided citing blog posts or tutorials that summarize DPO/SimPO/ORPO without showing the loss functions. The gradient-level analysis requires the actual formulations from the papers, not summaries.
- I avoided speculating about quantitative bias attenuation under DPO (e.g., "DPO would have reduced the bias by X%"). That claim requires an empirical re-run on the same 121 pairs, which I did not do. The explainer is limited to the mechanistic argument.
- I avoided citing the Leng et al. (2024) "Taming Overconfidence" paper, which was relevant to my partner's explainer for my question but not directly relevant to the DPO/SimPO/ORPO comparison. Keeping scope clean.
