# Your Rubric Is a Prompt Prefix, Not a Measuring Instrument

## How attention sinks and long-prefix behavior silently bias an LLM judge toward over-rejection

You built a prompted judge for your Week 11 pipeline. You wrote a careful rubric — fifty criteria, clear definitions, examples of failure modes. You drop it in front of every candidate output and ask the model for a verdict. The judge feels rigorous. It rejects a lot. You assume that means the candidates are weak.

But there is a quieter possibility worth taking seriously: **the rubric itself is making the judge stricter than the criteria warrant**. Not because the criteria are wrong. Because of *where* the rubric sits in the context window, and *how* transformer attention treats that position.

This post is about the mechanism behind that bias, why it is structural rather than fixable by "writing a better rubric," and what you can do about it tonight.

## The mechanism: attention is not neutral over position

A prompted judge is just an LLM doing next-token prediction. The verdict it emits — `accept` or `reject` — is the highest-probability next token given the entire context: rubric, candidate, instruction. There is no special "evaluator" mode. The model is computing a weighted average of every token's value vector, where the weights come from softmax attention.

Three things distort those weights.

First, **attention sinks**. Xiao et al. (2023) showed that in a trained transformer, the first one to four tokens of any sequence absorb a structurally large share of attention weight, regardless of their semantic content. Softmax forces every attention head to spend its full probability mass somewhere. Heads that don't need information at a given step learn to dump that mass on always-present early tokens. Those tokens become a "null channel" — visible to every layer, every head, every later position. Whatever sits there is amplified.

Second, **lost-in-the-middle**. Liu et al. (2023) found that long prompts are not weighed uniformly. Models attend strongly to the start and end and weakly to the middle. For a 1,500-token rubric, this means roughly the first 50 tokens and the last 100 tokens are heard. The 1,300 tokens in between are largely decorative.

Third, **prefix priming**. Long, stylistically uniform prefixes narrow the model's output distribution. After 1,500 tokens of evaluator-voice text — full of words like *fail, reject, error, harmful, incorrect* — the model's hidden state has settled into a higher-criticism register. It then judges the candidate from inside that register.

The combined effect: the verdict is dominated by the rubric's *opening framing*, the rubric's *closing instruction*, and the negative-vocabulary *prior* the prefix has built up. The middle of the rubric — where most of the actual criteria live — barely participates.

## A worked intuition

Imagine the judge is a courtroom jury. The rubric is the bench's instructions. The candidate is the defendant's testimony.

In a fair courtroom, the jury weighs the testimony on its merits. In this courtroom, however: the first sentence of the instructions is shouted through a megaphone for the entire trial (attention sinks). The middle 80% of the instructions is whispered (lost-in-the-middle). The judge's last sentence echoes loudest (recency). The defendant testifies for five minutes after sitting through two hours of "here is everything that makes a defendant guilty" (prefix priming).

This jury is structurally biased toward conviction before the defendant has spoken. Not because the instructions were wrong. Because of how the room is built.

That room is your judge.

## Why this matters for any LLM-as-judge

Two production failures fall directly out of this mechanism.

**Calibration depends on rubric ordering, not candidate quality.** Move a criterion from position 25 to position 1 and you can swing the accept rate by five to fifteen percentage points on the same candidates. The judge's verdicts are a function of "the parts of the rubric that landed in attention-favored positions," not "the candidate met the rubric." This is the smoking gun for poor calibration — and it is testable.

**Rubric-induced over-rejection is invisible to the rubric author.** The author reads the rubric and sees fifty fair criteria. The model reads the rubric and effectively sees three to four criteria plus a strict opening framing plus a closing instruction. Good candidates that fail one of the amplified criteria — or that simply trigger the negative-vocabulary prior — get rejected. The author concludes "the model is generating weak outputs." The actual cause is that the judge has a structural rejection prior baked into its prompt geometry.

For LLM-as-judge in any high-stakes setting (model evaluation, content moderation, agent acceptance gates), this is the difference between a measurement and a vibe.

## What to do about it

Three concrete moves, in order of effort:

1. **Run a permutation test.** Shuffle the order of your rubric criteria across, say, twenty seeds. Measure the variance in accept rate on a fixed candidate set. If accept rate moves more than five points across permutations, your judge is not measuring the candidates — it is measuring rubric ordering. This is a one-evening experiment and the number belongs in your model card.

2. **Rewrite the rubric in neutral or positive voice.** "An ideal answer demonstrates X" generalizes better than "reject if X is missing." Same content, different priming. The negative-vocabulary prior weakens substantially.

3. **Move the candidate before the rubric, or interleave.** Putting the candidate at the front of the context disrupts sink-amplification of strict framing and forces the rubric to compete for attention on content rather than position.

The deeper point is one that applies to any prompted system, not just judges: a long instruction prefix is never a neutral container for instructions. It is a load-bearing part of the model's computation, and its geometry — first tokens, middle tokens, length, vocabulary — biases the output independently of its content. Knowing that geometry is part of knowing your tool.

