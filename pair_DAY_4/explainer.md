# Why DPO's Reference Model Would Have Dampened the Bias That SimPO Absorbed

**A 900-word answer to my Day 4 partner's question, who asked:**
> *"Why do DPO, SimPO, and ORPO produce different judges even on the same preference pairs — specifically, whether DPO's reference-model KL term would have dampened the interrogative-framing bias in my 121 preference pairs, while SimPO's reference-free formulation amplified it."*

---

## The load-bearing claim

DPO, SimPO, and ORPO penalize different things at the gradient level. When your preference data has a systematic skew — like 9 of 12 style-guide seeds requiring interrogative framing — the presence or absence of a reference-model anchor determines whether the skew gets absorbed into the policy wholesale or gets attenuated by a pull toward the base model's prior. SimPO has no such anchor. That is the algorithmic reason your trained judge approved interrogative outputs on ~8/65 assertive-framing dev tasks.

---

## The three loss functions side by side

**DPO** (Rafailov et al., 2023) reparameterizes the RLHF reward-maximization objective into a classification loss over preference pairs. The loss for a single pair is:

L_DPO = −log σ(β · (log π_θ(y_w|x)/π_ref(y_w|x) − log π_θ(y_l|x)/π_ref(y_l|x)))

The key term is the ratio π_θ/π_ref. Every gradient step pushes the policy π_θ to increase the log-probability of the chosen response y_w relative to the rejected response y_l — but only the *difference* from the reference model π_ref counts. If the base model already assigns low probability to interrogative framing for a given prompt, DPO penalizes moving the policy far from that prior. The reference model acts as an anchor: updates that push the policy too far from the base distribution are down-weighted because the log-ratio π_θ/π_ref grows large, and the sigmoid saturates. The gradient vanishes for already-learned distinctions, concentrating learning on genuinely new preference signal.

**SimPO** (Meng et al., 2024) drops the reference model entirely. The implicit reward for a response y is the average log-probability under the policy alone: r(y) = (1/|y|) Σ log π_θ(y_i|x, y_{<i}). The loss becomes:

L_SimPO = −log σ(β · (r(y_w) − r(y_l) − γ))

where γ is a target reward margin. There is no π_ref anywhere. The gradient pushes the policy to increase the chosen response's average log-probability and decrease the rejected response's, with no anchor pulling it back toward a prior. Length normalization (the 1/|y| term) prevents the model from gaming reward by generating longer outputs, but it does nothing about framing-style skew — it normalizes for length, not for content distribution.

**ORPO** (Hong et al., 2024) combines SFT and preference optimization in a single monolithic loss:

L_ORPO = L_SFT + λ · L_OR

where L_OR is the log-sigmoid of the log odds ratio between chosen and rejected responses. ORPO is also reference-free — no π_ref — but the SFT term acts as a weak regularizer: it keeps the model close to producing fluent, on-distribution outputs. This is not the same as DPO's explicit KL anchor. The SFT loss penalizes bad generation broadly; it does not specifically penalize divergence from the base model's prior over framing styles.

---

## The reference model's actual job

In DPO, π_ref is typically a frozen copy of the base model (or the SFT checkpoint). Its job is mechanical: it provides a per-token baseline probability. When the policy moves to assign much higher probability to interrogative framing than the base model ever did, the log-ratio log(π_θ/π_ref) grows large. The sigmoid in the DPO loss saturates, the gradient shrinks, and the update stalls. The reference model does not "know" that interrogative framing is overrepresented in your data — it simply resists any large departure from the base distribution, regardless of direction. That resistance is the dampening mechanism.

---

## Why SimPO would amplify a biased preference signal

Your 121 preference pairs contain 12 style-guide seed pairs, 9 of which have `required_signal_framing: interrogative`. The task-rewrite pairs show a similar skew. SimPO sees this distribution and does exactly what it is told: it increases the average log-probability of chosen responses (mostly interrogative) and decreases that of rejected responses (mostly assertive-when-they-should-be-interrogative). There is no π_ref to push back. The policy absorbs the skew fully.

The result is what you observed: on the ~65 dev tasks requiring assertive framing, the judge approves interrogative outputs ~12% of the time. The bias is not random noise — it is a direct consequence of the training signal. SimPO learned that interrogative framing correlates with "chosen," and nothing in the loss function told it to be skeptical of that correlation.

ORPO sits between the two. Its SFT component keeps the model generating fluent text, which indirectly limits how far framing distributions can shift. But the SFT loss has no explicit mechanism to penalize divergence from the base model's framing prior — it just penalizes bad generation in general. The dampening effect exists but is weaker and less targeted than DPO's KL term.

---

## What this means for the "unresolved training failure" paragraph

The current paragraph in `docs/memo.md` names the data reason (9/12 seeds skewed interrogative) and proposes a data fix (add 20 assertive-framing pairs). The algorithmic reason is missing. A revised version:

> "The bias appeared not only because 9 of 12 style-guide seeds share `required_signal_framing: interrogative`, but because SimPO's reference-free loss has no anchoring term to dampen the skewed signal. Under DPO, the KL divergence from the reference model would have penalized policy updates that shifted the framing distribution away from the base model's prior, attenuating — though likely not eliminating — the bias. ORPO's SFT regularizer would have provided weaker, less targeted resistance. The data fix (adding assertive-framing pairs) is necessary under any loss function; the choice of SimPO made the data fix load-bearing."

---

## What I deliberately did not claim

I am not claiming DPO would have eliminated the bias. A 9/12 skew in the seed data is severe enough that even DPO's KL term would allow some drift — the reference model resists large departures, not all departures. Empirical confirmation would require re-running training under all three losses on the same 121 pairs and comparing the assertive-framing approval rate on the same 65 dev tasks. I am claiming only that the mechanism exists and that SimPO is structurally more vulnerable to this class of bias than DPO.

---

## Sources

- Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C.D., & Finn, C. (2023). "Direct Preference Optimization: Your Language Model is Secretly a Reward Model." NeurIPS 2023. [arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290)
- Meng, Y., Xia, M., & Chen, D. (2024). "SimPO: Simple Preference Optimization with a Reference-Free Reward." NeurIPS 2024. [arxiv.org/abs/2405.14734](https://arxiv.org/abs/2405.14734)
- Hong, J., Lee, N., & Thorne, J. (2024). "ORPO: Monolithic Preference Optimization without Reference Model." EMNLP 2024. [arxiv.org/abs/2403.07691](https://arxiv.org/abs/2403.07691)
- HuggingFace TRL documentation: [DPO Trainer](https://huggingface.co/docs/trl/en/dpo_trainer), [CPO Trainer (SimPO loss)](https://huggingface.co/docs/trl/en/cpo_trainer), [ORPO Trainer](https://huggingface.co/docs/trl/v0.11.4/en/orpo_trainer)
