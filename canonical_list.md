# Canonical List — Week 12 Contributions to the Cohort Canon

Annotated reading list from four pair sessions covering inference mechanics, training mechanics, and evaluation statistics. Grouped by theme; within each theme, ordered by "read this first."

## Theme 1 — Inference mechanics: how prompt structure biases model output

### Xiao et al. (2023) — *Efficient Streaming Language Models with Attention Sinks*
- arXiv: [2309.17453](https://arxiv.org/abs/2309.17453)
- **Why load-bearing:** Establishes that the first 1–4 tokens of any sequence absorb structurally large attention weight due to softmax-must-sum-to-one. Any FDE building a prompted judge or long-prefix system needs to know that early tokens are amplified regardless of content.
- Informed: Day 1_2 (rubric-prefix bias in LLM judges)

### Liu et al. (2023) — *Lost in the Middle: How Language Models Use Long Contexts*
- arXiv: [2307.03172](https://arxiv.org/abs/2307.03172)
- **Why load-bearing:** Models attend U-shaped over long inputs — strongly to the start and end, weakly to the middle. A 50-criterion rubric is effectively a 5-criterion rubric. Empirical foundation for any claim about prompt-position effects.
- Informed: Day 1_2 (rubric-prefix bias)

### Schick et al. (2023) — *Toolformer: Language Models Can Teach Themselves to Use Tools*
- NeurIPS 2023. arXiv: [2302.04761](https://arxiv.org/abs/2302.04761)
- **Why load-bearing:** Tool selection is next-token prediction conditioned on tool descriptions in the prompt — no separate selection model. Description specificity directly shifts selection probability.
- Informed: Day 3 (tool description selection)

### Zheng et al. (2023) — *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*
- NeurIPS 2023. arXiv: [2306.05685](https://arxiv.org/abs/2306.05685)
- **Why load-bearing:** Canonical catalogue of LLM judge biases — position, verbosity, self-enhancement. Baseline awareness for any FDE using LLM-as-judge in production.
- Informed: Day 1_2 (supporting context)

### Wang et al. (2023) — *Large Language Models are not Fair Evaluators*
- arXiv: [2305.17926](https://arxiv.org/abs/2305.17926)
- **Why load-bearing:** Prompt phrasing — including criterion order and instruction framing — shifts judge verdicts. Direct empirical support for the claim that prompt geometry can dominate evaluation outcomes.
- Informed: Day 1_2 (supporting)

### Anthropic Tool Use Documentation
- Source: [docs.anthropic.com/en/docs/build-with-claude/tool-use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- **Why load-bearing:** Shows how the `tools` parameter is serialized into the model's prompt as conditioning text. Confirms selection happens during normal token generation.
- Informed: Day 3 (tool description selection)

## Theme 2 — Training mechanics: what loss functions protect and don't protect

### Rafailov et al. (2023) — *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*
- NeurIPS 2023. arXiv: [2305.18290](https://arxiv.org/abs/2305.18290)
- **Why load-bearing:** The log(π_θ/π_ref) ratio is the gradient-level anchor that resists policy drift from the base model's prior. The reference model isn't just a training cost — it's a bias-resistance mechanism. Read this first if you only read one paper from this theme.
- Informed: Day 4 (DPO vs SimPO vs ORPO)

### Meng et al. (2024) — *SimPO: Simple Preference Optimization with a Reference-Free Reward*
- NeurIPS 2024. arXiv: [2405.14734](https://arxiv.org/abs/2405.14734)
- **Why load-bearing:** Defines the reference-free reward as average log-probability under the policy alone. Length normalization addresses length gaming but not framing-distribution skew. The VRAM-savings-for-bias-resistance tradeoff is the load-bearing insight.
- Informed: Day 4 (DPO vs SimPO vs ORPO)

### Hong et al. (2024) — *ORPO: Monolithic Preference Optimization without Reference Model*
- EMNLP 2024. arXiv: [2403.07691](https://arxiv.org/abs/2403.07691)
- **Why load-bearing:** SFT + odds-ratio in one loss. The SFT component provides weak regularization but no explicit KL anchor. Positions ORPO between DPO (explicit anchor) and SimPO (no anchor) on the bias-resistance spectrum.
- Informed: Day 4 (DPO vs SimPO vs ORPO)

## Theme 3 — Evaluation statistics: when summary metrics mislead

### Feinstein & Cicchetti (1990) — *High agreement but low kappa: I. The problems of two paradoxes*
- Journal of Clinical Epidemiology, 43(6), 543–549
- **Why load-bearing:** Names the kappa paradox: concentrated marginals inflate chance-expected agreement, collapsing κ even at high observed agreement. Any FDE reporting inter-rater reliability on a benchmark with concentrated ratings needs this. Read this first from this theme.
- Informed: Day 5 (kappa paradox)

### Gwet (2008) — *Computing inter-rater reliability and its variance in the presence of high agreement*
- British Journal of Mathematical and Statistical Psychology, 61(1), 29–48
- **Why load-bearing:** AC1 redefines chance agreement using overall dispersion instead of marginal cross-products, making it paradox-resistant. The honest replacement for raw agreement when ratings are concentrated.
- Informed: Day 5 (kappa paradox)

### Cohen (1960, 1968) — *A coefficient of agreement for nominal scales* / *Weighted kappa*
- Educational and Psychological Measurement (1960); Psychological Bulletin (1968)
- **Why load-bearing:** Foundation for all chance-corrected agreement. The 1968 paper adds linear/quadratic weights for ordinal scales. Necessary background, but insufficient alone — the paradox makes κ misleading at concentrated marginals.
- Informed: Day 5 (kappa paradox)

### Byrt, Bishop & Carlin (1993) — *Bias, prevalence and kappa*
- Journal of Clinical Epidemiology, 46(5), 423–429
- **Why load-bearing:** Decomposes the paradox into prevalence index and bias index. Diagnostic for understanding *why* your specific dataset triggers the collapse.
- Informed: Day 5 (supporting)

## Tools and patterns

| Tool / pattern | What it does | Day | Path in repo |
|---------------|--------------|-----|--------------|
| HuggingFace `transformers` with `output_attentions=True` | Exposes per-layer, per-head attention weights. Requires `attn_implementation="eager"`. | 1_2 | `pair_DAY_1_2/sources.md` (code pattern) |
| Claude Sonnet 4.5 tool selection profile | 10-trial comparison: vague vs specific tool descriptions on a fixed query. Isolates description tokens as the only variable. | 3 | `pair_DAY_3/sources.md` |
| HuggingFace TRL (DPO / CPO-SimPO / ORPO trainers) | Canonical implementations of all three loss functions. | 4 | `pair_DAY_4/sources.md` |
| `kappa_paradox_demo.py` | 87-line numpy script: samples IID pairs from concentrated marginals, computes raw agreement / κ / κ_w / AC1 under null conditions. | 5 | `pair_DAY_5/scripts/kappa_paradox_demo.py` |
