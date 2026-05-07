# Thread: Why SimPO Absorbed Your Biased Preference Signal

---

**1/**
My partner trained a SimPO judge on 121 preference pairs. 9 of 12 seed pairs required interrogative framing. The judge then approved interrogative outputs on ~12% of tasks that required assertive framing. His memo blames the data. The real answer: SimPO's loss function has no mechanism to resist a skewed signal. DPO does. Here's why. 🧵

**2/**
DPO's loss computes log(π_θ/π_ref) — the ratio of the policy's probability to a frozen reference model. When training pushes the policy far from the base model's prior (e.g., toward interrogative framing that the base model didn't favor), the ratio grows, the sigmoid saturates, and the gradient shrinks. The reference model is a brake.

**3/**
SimPO drops the reference model entirely. The reward is just the average log-probability under the policy itself — no anchor, no brake. If 75% of your chosen responses use interrogative framing, SimPO increases that probability with nothing pulling back. The skew in your data becomes the skew in your policy. Fully absorbed.

**4/**
ORPO sits in between. It's also reference-free, but it combines an SFT loss with an odds-ratio preference loss. The SFT component weakly regularizes toward fluent, on-distribution outputs — but it doesn't specifically penalize divergence from the base model's framing prior. Weaker brake than DPO, but not zero.

**5/**
The real-world failure: a judge trained on interrogative-skewed data via SimPO approved interrogative outputs on assertive-required tasks ~8/65 times. This isn't random noise. It's a direct consequence of a reference-free loss fully absorbing a data skew. DPO's KL term would have attenuated it — not eliminated it, but dampened it.

**6/**
The fix for the "unresolved training failure" paragraph: name both causes. The data cause (9/12 seeds interrogative). The algorithmic cause (SimPO has no anchoring term to dampen the skew). Adding assertive pairs is necessary under any loss. But choosing SimPO made the data fix load-bearing.

**7/**
Full explainer with loss functions, the reference model's mechanical role, and the exact rewrite for docs/memo.md → pair_DAY_4/explainer.md
