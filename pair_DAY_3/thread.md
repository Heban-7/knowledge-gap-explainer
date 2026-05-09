# Tweet Thread — Day 2

**Topic:** Where tool selection actually happens in an LLM agent
**Length:** 6 tweets
**Audience:** Engineers building agents who think tool selection is a separate classifier

---

**1/**
"Tool selection" in agents isn't a separate classifier.

It's the same next-token prediction that generates everything else — just conditioned on every tool's description in your prompt.

Which means your tool descriptions are doing more work than you think. 🧵

---

**2/**
When you register tools via the API (Anthropic, OpenAI, etc.), they get serialized into the prompt as structured text — name + description + schema for each tool.

The model reads all of this before it generates ANY token, including the one where it picks a tool.

---

**3/**
So when an agent picks the wrong tool, it's not a "routing bug."

It's that the description for the right tool didn't shift enough probability mass at the moment the next-token decision happened.

The fix is in your descriptions, not your orchestrator.

---

**4/**
Quick demo. Two tools:

v1: "Search the database" / "Query the external API"
v2: "Search internal customer records — data we own" / "Hit third-party API for enrichment data we don't have locally"

Same names. Just better descriptions.

Selection accuracy: 60% → 100%.

---

**5/**
What makes a description load-bearing for selection:

✅ Describe WHEN to use it, not just what it does
✅ Distinguish from sibling tools explicitly
✅ Include "do NOT use for X" if relevant

❌ "Sends an email."
✅ "Sends a follow-up email after a discovery call. Do NOT use for cold outreach."

---

**6/**
Implication for your model card / architecture doc:

Don't write "detailed descriptions improve selection accuracy."

Write: "Descriptions are part of the conditioning context for the tool-name token. They shift selection probability between overlapping tools."

That's the mechanism. /end
