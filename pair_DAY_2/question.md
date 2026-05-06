# Day 2 — Question

**Topic of the day:** Agent / tool-use mechanics

**Asker:** Liul J Teshome
**Explainer (partner):** Rafia

---

## Final question

In my Week 10 Conversion Engine architecture doc, I claim "function calling is more reliable than free-text JSON parsing for tool invocation," which is why I migrated the HubSpot and calendar tools from prompt-instructed JSON output to native function calling.

But I cannot mechanically defend this. Specifically:

**(a)** When a model emits a function call via the API's `tools` parameter, are the JSON-structure tokens generated the same way as any other text (just sampled from the distribution), or is the decoder actually constrained to a grammar at inference time?

**(b)** If function-calling reliability comes from training (the model was fine-tuned on tool-call data) rather than constrained decoding, why does it still fail on schema-compliant outputs sometimes — what's the failure mode at the token level?

Closing this gap would let me rewrite the "function calling vs free-text JSON" paragraph in my Week 10 architecture doc (`docs/architecture.md`, the "Tool Invocation" section) with the actual mechanism, instead of citing reliability as if it were a black-box guarantee.

---

## Grounding artifact

- **File:** `docs/architecture.md`, section "Tool Invocation"
- **Specific paragraph:** "We migrated HubSpot and calendar tools from prompt-instructed JSON output to native function calling because function calling is more reliable. This reduces the parse-failure rate observed in our Week 10 traces."
- **Why I can't defend it:** I'm citing reliability as a property without explaining the mechanism. If a CTO asked "what's the reliability coming from — your prompt, the API, or the model weights?" I currently cannot answer.

---

## What "gap closed" would look like

I can rewrite the architecture-doc paragraph from a black-box reliability claim to:

> _"Function calling is reliable because [token-level mechanism], and fails when [specific failure mode], which is why we added [specific guardrail in our orchestrator]."_

A satisfying explainer answers: (1) is the API server-side enforcing a grammar during decoding, or is the model just trained to emit valid JSON? (2) when reliability breaks, what does that failure look like at the token level — wrong tool selected, valid JSON but wrong schema, or malformed JSON?

---

## Self-check against the four properties

- **Diagnostic:** Names two specific mechanisms — (a) constrained decoding vs. unconstrained sampling, (b) token-level failure mode when reliability breaks. Not "how does function calling work."
- **Grounded:** Points to `docs/architecture.md`, the Tool Invocation section, and a real migration decision in Week 10 (HubSpot + calendar).
- **Generalizable:** Every engineer building agents has this exact gap. "Constrained decoding vs. fine-tuning" is one of the most-confused topics in agent engineering.
- **Resolvable:** ~800 words can cover constrained-decoding mechanics + training-based reliability + one concrete failure mode with a small demo.
