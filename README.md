# Knowledge-Gap Explainer — Week 12 Submission

This repo is my Week 12 deliverable for the TRP1 program. It contains four pair folders documenting eight gaps closed across the week — four I asked about and four I researched and explained. Days 1 and 2 were merged into one session due to a program-side schedule issue, producing four pair folders instead of five.

## Public artifacts published this week

| Day | Topic | Blog | Thread |
|-----|-------|------|--------|
| 1_2 | Attention sinks and rubric-prefix bias in LLM judges | [BLOG_URL_DAY_1_2] | [THREAD_URL_DAY_1_2] |
| 3   | Agent / tool-use mechanics (function calling + tool description selection) | [BLOG_URL_DAY_3] | [THREAD_URL_DAY_3] |
| 4   | Preference optimization (DPO vs SimPO vs ORPO + confidence-gated phrasing) | [BLOG_URL_DAY_4] | [THREAD_URL_DAY_4] |
| 5   | Evaluation statistics (embedding drift + kappa paradox at concentrated marginals) | [BLOG_URL_DAY_5] | [THREAD_URL_DAY_5] |

## Repository structure

```
knowledge-gap-explainer/
├── pair_DAY_1_2/          # Days 1–2 merged: inference/attention mechanics
│   ├── explainer.md
│   ├── sources.md
│   └── thread.md
├── pair_DAY_3/            # Day 3: agent/tool-use mechanics
│   ├── question.md
│   ├── morning_call_summary.md
│   ├── explainer.md
│   ├── thread.md
│   ├── signoff.md
│   ├── grounding_commit.md
│   └── sources.md
├── pair_DAY_4/            # Day 4: preference optimization / confidence-gated phrasing
│   ├── question.md
│   ├── morning_call_summary.md
│   ├── evening_call_summary.md
│   ├── explainer.md
│   ├── thread.md
│   ├── signoff.md
│   ├── grounding_commit.md
│   └── sources.md
├── pair_DAY_5/            # Day 5: evaluation and statistics
│   ├── question.md
│   ├── morning_call_summary.md
│   ├── explainer.md
│   ├── thread.md
│   └── scripts/
│       └── kappa_paradox_demo.py
├── synthesis.md           # Week-in-review (~1,400 words)
├── canonical_list.md      # Annotated reading list contributed to the cohort canon
├── portfolio_update.md    # One-page summary: how this week improved Weeks 10/11
└── README.md              # This file
```

## Key documents

- `synthesis.md` — week-in-review covering all eight gaps, the most surprising learning, question-quality trajectory, and closing reflection
- `canonical_list.md` — annotated reading list of 14 papers/sources and 4 tools/patterns, grouped by theme, contributed to the cohort canon
- `portfolio_update.md` — one-page summary of how this week's two grounding commits improved the Week 10 architecture doc and Week 11 methodology rationale
