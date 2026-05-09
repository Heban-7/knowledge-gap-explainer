# Tweet thread — "Your rubric is a prompt prefix, not a measuring instrument"

Target: 6 tweets, each ≤ 280 chars, each stands alone.

---

**Tweet 1 — Hook**

Your LLM-as-judge uses a 1500-token rubric and rejects a lot. You assume the candidates are weak.

There's a quieter possibility: the rubric itself is biasing the judge toward rejection — not because of what you wrote, but because of where it sits in the context.

---

**Tweet 2 — Mechanism: attention sinks**

Attention sinks (Xiao et al., 2023): the first 1–4 tokens of any prompt absorb a structural share of attention weight, regardless of content.

Softmax must spend its mass somewhere; heads dump it on always-present early tokens. Whatever sits there is amplified at every layer.

---

**Tweet 3 — Mechanism: lost-in-the-middle**

Lost-in-the-middle (Liu et al., 2023): long prompts are read U-shaped. The first ~50 tokens and last ~100 tokens get high attention. The 1300 tokens in the middle? Mostly decorative.

So your 50-criterion rubric is effectively a 5-criterion rubric, plus the opening framing.

---

**Tweet 4 — The synthesis**

In a prompted judge, the rubric's *opening framing* is amplified by attention sinks. The *middle criteria* are largely ignored. *Negative vocabulary* (fail, reject, error) primes the verdict logits.

The verdict is dominated by prompt geometry, not candidate quality.

---

**Tweet 5 — The experiment you can run tonight**

Permutation test: shuffle your rubric's criterion order across 20 seeds. Measure accept-rate variance on a fixed candidate set.

If it moves >5 points, your judge is measuring rubric ordering, not candidates. One evening of work. One number for your model card.

---

**Tweet 6 — The general lesson + link**

A long instruction prefix is never a neutral container. Its first tokens, middle tokens, length, and vocabulary all bias the output independently of what it says.

For LLM-as-judge in any high-stakes setting, that's the difference between a measurement and a vibe.

[blog link]

---

## Character counts (for verification before publishing)

| Tweet | Chars |
|---|---|
| 1 | 263 |
| 2 | 276 |
| 3 | 274 |
| 4 | 267 |
| 5 | 261 |
| 6 | 264 (excluding link) |

All under the 280 limit. Each tweet contains a self-contained claim or definition, so a reader who lands mid-thread still gets useful information.
