# Day 5 — Question

**Topic of the day:** Evaluation and statistics — centroid-based embedding drift and the first-moment trap

**Asker:** Liul J. Teshome
**Explainer (partner):** Eyoel Nebiyu
**Date:** 2026-05-08

---

## Final question

In my Week 7 Data-Contract-Enforcer evaluation artifacts (`report_final_pdf_ready.md` and `contracts/ai_extensions.py`), I claim a "centroid-based cosine distance" embedding drift method with "Sample size: 251," then interpret `drift_score: 0.0` as evidence of stability (the report says "Status: PASS" and the interpretation section claims "stable AI data contracts"). I cannot mechanically defend that claim. Specifically:

**(a)** What is the correct effective sample and statistic definition when the implementation caps embeddings at 200 (`embed_sample(texts, n=200)` in `contracts/ai_extensions.py`, line 53) but the report cites "Sample size: 251" (the length of the input text list, not the number of embeddings actually computed)?

**(b)** What evidence chain is required before calling this "semantic" stability, given that centroid-based cosine distance is a first-moment summary that is blind to dispersion, multimodality, model identity changes, and fallback-vector contamination?

Closing this gap would let me rewrite the drift-results section in `report_final_pdf_ready.md` (lines 211–215) and make metric/reporting semantics explicit in `contracts/ai_extensions.py`.

---

## Grounding artifacts

- **File:** `report_final_pdf_ready.md`, Section 5.1 (Extension 1 — Embedding Drift Detection)
  - Specific lines: "Sample size: 251 extracted fact texts / Drift score: 0.0 / Threshold: 0.15 / Status: PASS"
  - Why I can't defend it: The number 251 is the input count, not the embedding count. The "PASS" maps to "stable" in the interpretation, but the statistic only measures the first moment of the embedding distribution.

- **File:** `contracts/ai_extensions.py`, function `check_embedding_drift` and `embed_sample`
  - `embed_sample` caps at `n=200` (line 53)
  - `check_embedding_drift` returns `"sample_size": len(texts)` — i.e., the input length, not the capped count
  - The function uses `compute_simple_embedding` (a local SHA-512 hash fallback) when the OpenAI API is unavailable — a provenance concern the report does not name

---

## What "gap closed" would look like

I can rewrite the drift-results paragraph from a black-box "PASS → stable" claim to:

> _"Centroid-cosine drift = [value] over n_effective = [capped count] using [model id] with [fallback rate]. The first-moment summary is unchanged; a [second-moment statistic] and a [distribution-level statistic] would be needed before claiming semantic stability."_

A satisfying explainer answers: (1) what the n_eff vs n_reported discrepancy costs in precision and provenance, (2) which properties of the embedding distribution centroid distance is blind to, (3) what the minimum evidence chain is before "semantically stable" is a defensible sentence.

---

## Self-check against the four properties

| Property | Self-rating (1–5) | Justification |
|----------|------------------:|---------------|
| **Diagnostic** | 5 | Names two specific sub-problems: (a) the n_eff mismatch between implementation and report, (b) the evidence-chain gap between a first-moment summary and a "semantic stability" claim. Not "how does embedding drift work?" |
| **Grounded in cohort work** | 5 | Cites two files with line-level pointers: the report paragraph at lines 211–215 and the `embed_sample(n=200)` cap at line 53 of `ai_extensions.py`. The grounding commit is concrete: rewrite the drift-results paragraph and change the metric output from scalar to structured. |
| **Generalizable** | 5 | Any ML pipeline using centroid-based drift detection — and there are many, because it's the simplest thing to implement — faces this exact gap. The first-moment trap is a recurring evaluation-methodology pitfall. |
| **Resolvable in one explainer** | 5 | The centroid-as-first-moment argument is a one-paragraph derivation; the four blind spots are enumerable; the evidence chain is a concrete list. ~800–1000 words covers mechanism + prediction + recommendation + demo. |
