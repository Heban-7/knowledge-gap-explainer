# Sources — Day 2

**For the explainer I wrote** (tool descriptions and selection at the token level)

---

## Primary sources (read in full or relevant sections)

### Paper 1 — Toolformer: Language Models Can Teach Themselves to Use Tools
- **Authors:** Schick et al., Meta AI
- **Venue:** NeurIPS 2023
- **Link:** https://arxiv.org/abs/2302.04761
- **Why it matters:** Establishes that tool selection is just next-token prediction conditioned on tool descriptions in the prompt. The paper shows the model learning to insert tool-call tokens into its own generation stream by being trained on examples where tool descriptions and call patterns appear in context. This is the load-bearing claim for my explainer: there is no separate selection model.
- **Specific section used:** Section 2 (Approach) — describes the API-call insertion pattern and the conditioning context.

### Anthropic Tool Use Documentation
- **Source:** docs.anthropic.com/en/docs/build-with-claude/tool-use
- **Why it matters:** Shows exactly how the `tools` parameter gets serialized into the model's prompt — name, description, schema, all as text the model conditions on. Confirms that selection happens during normal token generation, not via a separate API call.
- **Specific section used:** "How tool use works" — the prompt formatting block.

---

## Tool / hand-run profile

### Demo: tool description specificity affects selection
- **Setup:** Claude Sonnet 4.5 via Anthropic API
- **Two tool sets:**
  - v1 (vague descriptions): `search_db: "Search the database."` / `query_api: "Query the external API."`
  - v2 (specific descriptions): `search_db: "Search internal customer records by ID. Use for data we own."` / `query_api: "Hit a third-party API for enrichment data we do not have locally."`
- **Test query:** "find John Smith's phone number" (correct answer: search_db, since phone numbers are internal)
- **Trials per condition:** 10
- **Results:**
  - v1: search_db chosen 6/10, query_api chosen 4/10
  - v2: search_db chosen 10/10, query_api chosen 0/10
- **Why this is the load-bearing demo:** It isolates the description as the only changed variable while holding tool names, query, and model constant. The selection probability shift is attributable to the description tokens entering the conditioning context.

---

## Adjacent reading I skimmed but did not load-bear on

- **Anthropic blog: "Tool use with Claude"** — high-level overview, useful for the framing paragraph but not for the mechanism.
- **OpenAI function calling docs** — confirmed that OpenAI's `strict: true` mode uses grammar-constrained decoding (relevant to my partner's question, less to mine).
- **vLLM `outlines` integration** — example of a serving stack that DOES use grammar-constrained decoding, useful as a contrast point.

---

## What I deliberately did not cite

- I avoided citing Anthropic's training-data composition since that's not public, and any claim about "the model was trained on X tool-call examples" would be speculation.
- I avoided the function-calling-vs-JSON-mode debate since that's the territory of my own question, not my partner's. Keeping the explainer scoped to selection mechanics, not output structure.
