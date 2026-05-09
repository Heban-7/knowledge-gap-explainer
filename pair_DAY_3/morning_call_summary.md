# Morning Call Summary — Day 2

**Date:** [Wednesday's date]
**Duration:** 22 minutes
**Asker:** [Your name]
**Explainer:** [Partner's name]

---

## How my question sharpened during the call

My original draft was: *"How does function calling work?"* — too broad, a topic rather than a gap. My partner pushed back on three things:

1. **API specificity.** First version didn't name a vendor. Anthropic, OpenAI, and open-source serving stacks (vLLM with grammar-constrained decoding, outlines, JSON mode in llama.cpp) all implement structured output differently. I picked Anthropic, since that's what my Week 10 Conversion Engine actually uses.

2. **False binary.** I had framed it as "is it constrained decoding OR is it fine-tuning?" My partner correctly pointed out that production systems usually use both — the question is the *relative contribution*, and which one is the load-bearing piece when things fail. I updated the question to ask about the failure mode, which forces the answer to disambiguate.

3. **Grounding clarity.** I had said "the architecture doc" without naming the file or paragraph. My partner asked "which paragraph specifically?" I went and found it: `docs/architecture.md`, Tool Invocation section. The exact sentence I cannot defend is now quoted in my question.

The final question targets two mechanisms (constrained decoding vs. training-based reliability) and one failure mode (what reliability breaking looks like at the token level), grounded in a specific paragraph I will rewrite as the grounding commit.

---

## How my partner's question sharpened

My partner's original question was about why long system prompts cause latency degradation. The first draft conflated two things: prefill cost (mechanical, predictable) and attention quality degradation at long context (subtle, model-dependent). I pushed back and asked which one was load-bearing for their Week 11 claim about "rubric prefix being free." They tightened to a single mechanism — prefill compute scaling — and dropped the attention-quality angle for a separate future blog.

---

## Both questions confirmed final

Both partners agreed the questions are now diagnostic, grounded, generalizable, and resolvable in ~800 words. We exchanged sources we already had bookmarked and split for the research phase.
