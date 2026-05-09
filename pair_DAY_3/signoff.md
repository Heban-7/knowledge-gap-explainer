# Sign-off — Day 2

**Asker:** Liul J. Teshome
**Explainer:** Rafia
**Status:** ✅ **CLOSED**

---

## Asker's judgment (written by my partner)

> "I confirm the gap is closed. Before today, Liul J. Teshome had a paragraph in their Week 10 architecture doc citing 'function calling is more reliable than free-text JSON' without being able to defend the mechanism. The explainer I wrote, plus our evening call, gave them enough understanding to:
>
> 1. Name the two distinct mechanisms (training-based reliability vs. constrained decoding) that get conflated under the umbrella term 'function calling.'
> 2. Identify which mechanism their specific provider (Anthropic) uses primarily — training-based, with light server-side validation.
> 3. Identify the token-level failure mode that occurs when training-based reliability breaks: the model emits structurally valid JSON but populates fields with hallucinated or schema-noncompliant values, because no grammar is enforcing field constraints during decoding.
>
> What I confirmed during the evening call: Liul J. Teshome can now explain, without referring to the blog, why an Anthropic function call can be 'syntactically valid but semantically wrong' and what guardrail (validation layer in their orchestrator) catches that failure. They could not explain this before today.
>
> The grounding commit they made to `docs/architecture.md` (see `grounding_commit.md`) reflects the new understanding correctly. The rewritten paragraph names the mechanism instead of citing the property."

— [Partner's name], end of Day 2

---

## What I (the asker) understand now that I didn't before

1. **"Function calling" is an umbrella term covering at least two different reliability mechanisms.** Anthropic's API primarily relies on the model being fine-tuned to emit valid tool-call structure (training-based), not on grammar-constrained decoding (server-side). OpenAI's `strict: true` JSON mode does enforce a grammar; the basic mode does not.

2. **The failure mode I'd been ignoring is "valid syntax, wrong semantics."** My Week 10 traces showed several cases where the model emitted parseable JSON for `calendar_book` but with wrong field types (e.g., a string where a Unix timestamp was expected). Before today I would have called this "model error." I now understand it's specifically a failure of training-based reliability without a grammar safety net.

3. **Why this matters for production:** if my orchestrator only validates that the JSON parses (and not that the schema matches), I will silently accept malformed tool calls. This is a real bug in my Week 10 code that I now need to fix.

---

## What I would have answered if a CTO asked me this on Day 0

_"Function calling is more reliable because the API handles the structured output for us."_

(Vague. Cites the API as a black box.)

## What I'd answer now

_"Function calling reliability comes primarily from the model being fine-tuned on tool-call data, not from grammar-constrained decoding at the API layer. This means the model usually emits valid structure, but can still emit valid-syntax-wrong-semantics outputs — for example, valid JSON with the wrong field types. We mitigate this with a schema-validation layer in our orchestrator that catches semantically invalid calls before they hit the tool. If we needed stronger guarantees, we'd switch to a server with grammar-constrained decoding like vLLM + outlines."_

(Specific. Names mechanism. Names failure mode. Names guardrail.)
