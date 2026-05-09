# Sources

Canonical primary sources for `explainer.md`, plus the tool/pattern used and a runnable experiment your partner can reproduce in one evening.

---

## Load-bearing citations

These two papers carry the technical argument of the explainer. If either is wrong, the explainer's central claim collapses.

### 1. Xiao et al. (2023) — *Efficient Streaming Language Models with Attention Sinks*

- **arXiv:** [2309.17453](https://arxiv.org/abs/2309.17453)
- **Code:** [github.com/mit-han-lab/streaming-llm](https://github.com/mit-han-lab/streaming-llm)
- **Why it matters here:** Introduces and characterizes the *attention sink* phenomenon. Section 3 documents that the first 1–4 tokens of any sequence absorb a structurally large share of attention weight in trained transformers (Llama-2, Falcon, MPT, Pythia). Demonstrates the mechanism is rooted in the softmax-must-sum-to-one constraint of attention heads. This is the source for every claim the explainer makes about attention sinks.
- **Specific result the explainer relies on:** Figure 2 — attention scores collapse onto the first few tokens after the immediate-recency window, regardless of content.

### 2. Liu et al. (2023) — *Lost in the Middle: How Language Models Use Long Contexts*

- **arXiv:** [2307.03172](https://arxiv.org/abs/2307.03172)
- **Why it matters here:** The empirical foundation for the "U-shaped attention" claim. Shows across multiple closed-source and open-source LLMs that performance on retrieval-style tasks degrades sharply when relevant information sits in the middle of a long input — even when total context length is well within the model's stated window. This is the source for the "your 50-criterion rubric is effectively a 5-criterion rubric" line in the thread.
- **Specific result the explainer relies on:** Figures 3–5 — accuracy is highest when relevant information is at the start or end of the prompt, lowest in the middle.

---

## Supporting citations

These corroborate the synthesis but are not load-bearing. Cite them in the model card, not in tweet-thread headlines.

### 3. Zheng et al. (2023) — *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*

- **arXiv:** [2306.05685](https://arxiv.org/abs/2306.05685)
- **Why it matters here:** The canonical reference for LLM-as-judge biases — *position bias* (the judge prefers whichever candidate appears first), *verbosity bias* (longer answers are scored higher), and *self-enhancement bias* (the judge prefers outputs from its own model family). Establishes that LLM judges are not neutral measuring instruments and quantifies several systematic biases on real benchmarks.
- **Connection to the explainer:** Demonstrates that judge bias is real and measurable. The explainer adds a *new* mechanism (rubric-prefix-induced rejection bias) to the catalogue Zheng et al. opened.

### 4. Wang et al. (2023) — *Large Language Models are not Fair Evaluators*

- **arXiv:** [2305.17926](https://arxiv.org/abs/2305.17926)
- **Why it matters here:** Shows that prompt phrasing — including the order in which evaluation criteria appear and the framing of the instruction — significantly shifts judge verdicts. Provides direct empirical support for the explainer's claim that *prompt geometry, not candidate quality, can dominate the verdict*.
- **Connection to the explainer:** Most direct prior work on the bias the explainer is naming.

---

## Tool / pattern used

**HuggingFace `transformers` with `output_attentions=True`.**

The explainer's mechanism claims (sinks, U-shape) can be verified directly on any open-weight model by inspecting raw attention tensors during a forward pass. The `transformers` library exposes per-layer, per-head attention via the `output_attentions=True` flag. This is the cheapest way to *see* sink behavior on your own rubric.

Minimal pattern:

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "Qwen/Qwen2.5-1.5B-Instruct"
tok = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype=torch.bfloat16, device_map="auto",
    attn_implementation="eager",
)

prompt = build_judge_prompt(rubric, candidate)
inputs = tok(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    out = model(**inputs, output_attentions=True)

attentions = out.attentions
last_layer = attentions[-1][0]
last_token_attn = last_layer[:, -1, :].mean(dim=0)
```

`last_token_attn[i]` is the attention weight from the verdict position to token `i`. Plot it against position and you will see the sink (high values at positions 0–4) and the recency window (high values near the end), with most of the rubric body in between scoring near zero.

> Note: `attn_implementation="eager"` is required to expose attention weights. Flash-attention kernels skip materializing the full attention matrix and will return `None`.

---

## Suggested experiment — *the rubric permutation test*

The experiment that puts a number on the explainer's claim and that becomes the **grounding commit** to your Week 11 model card.

### Hypothesis

If the judge is well-calibrated, shuffling the order of independent rubric criteria should not change the accept rate on a fixed candidate set by more than a few points (within Monte Carlo noise). If the judge is dominated by prompt geometry, shuffling will move the accept rate substantially.

### Setup

- **Judge model:** the same model used in your Week 11 pipeline.
- **Candidate set:** 50–100 candidate outputs with known ground-truth labels (or stable human-rated quality scores). Reuse your Week 11 eval set.
- **Rubric:** your existing rubric, decomposed into N independent criteria. Hold the *opening framing* and *closing instruction* fixed; only permute the criteria block.
- **Permutations:** 20 random orderings, fixed seed.

### Procedure

```python
import random
import numpy as np

ORIG_FRAMING  = "You are a strict evaluator. Score the candidate against the criteria below."
CLOSING       = "Output JSON: {\"verdict\": \"accept\" | \"reject\", \"reason\": ...}"

criteria = load_rubric_criteria()
candidates = load_eval_set()

results = []
for seed in range(20):
    random.seed(seed)
    shuffled = random.sample(criteria, len(criteria))
    rubric = ORIG_FRAMING + "\n" + "\n".join(shuffled) + "\n" + CLOSING

    accept_rate = run_judge_over_candidates(rubric, candidates)
    results.append(accept_rate)

print(f"mean   accept rate: {np.mean(results):.3f}")
print(f"stddev across perms: {np.std(results):.3f}")
print(f"range              : {np.min(results):.3f} — {np.max(results):.3f}")
```

### Pass / fail criterion

- **Range < 5 percentage points** → judge is roughly invariant to rubric ordering. Calibration is at least defensible.
- **Range 5–10 points** → meaningful position-induced miscalibration. Document in the model card; consider remediation.
- **Range > 10 points** → the judge is largely measuring rubric geometry. Remediate before relying on the judge for any production decision.

### What to do with the result

Whatever the number, it goes into the model card. The act of measuring is the grounding commit; the number itself is the diagnostic. If the result is bad, the three remediation moves in the explainer (neutral framing, candidate-first ordering, criteria reduction) become the next experiment.

### Approximate cost

For a 1.5B-parameter judge over 50 candidates × 20 permutations = 1000 forward passes. Roughly 10–20 minutes on a single L4 / A10G, or ~$0.50 on hosted inference.

---

## Cited but not used

For honesty in the citation graph: I read but did not cite the following. Useful for further reading.

- Press et al. (2022), *Train Short, Test Long: Attention with Linear Biases* (ALiBi) — alternative positional encoding scheme that interacts with long-prefix behavior differently than RoPE.
- Han et al. (2024), *LM-Infinite: Zero-Shot Extreme Length Generalization for Large Language Models* — extends the StreamingLLM observation to longer contexts; relevant if your judge ever runs >8k.
