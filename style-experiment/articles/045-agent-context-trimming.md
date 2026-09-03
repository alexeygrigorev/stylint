# Trimming Agent Context Without Removing the Wrong Things

In May 2026, a coding agent working on `inventory-service` began missing decisions that were already recorded in its task file. The context had grown to 74,000 tokens. The useful material was still present, but it was buried under 180 tool messages and three abandoned approaches.

I wrote this as a synthetic style exercise with invented repository names, token counts, and dates. I still use the same trimming rules when a long agent session starts to drift.

In this post, I'll share:

- how I measured which context the agent used
- why removing old messages first made the session worse
- which four context layers I kept
- how I moved decisions into a compact file
- what I now check before starting a new session

## Measuring Actual Use

My first instinct was to delete old messages until the token count reached 30,000. Before I did that, I exported the session to JSONL and labeled every item.

The labels included these categories:

- system instructions
- repository files
- task requirements
- decisions
- tool output
- failed attempts
- current diff

After labeling every line, I counted 412 entries in total. Task requirements took only 1,900 tokens, while tool output took 46,000. Message 38 recorded the reservation decision that the agent later dropped.

I also wrote a small script to count references. For each file and function name, it counted later mentions in prompts, patches, and test output. This gave me a rough usage ranking, though it couldn't prove that an unmentioned item was useless.

The measurements showed me that I had framed the problem poorly. I didn't need to make the context smaller at any cost. I needed to preserve decisions while reducing transient output.

## The Wrong First Attempt

I still tried the simple route and removed everything older than message 100. The context fell from 74,000 to 28,000 tokens.

The agent worked normally for a while. It then changed a function named `allocate_stock` and removed a check for reserved quantities. The rule had been decided in message 38 after a failed test.

I restored the session from a checkpoint and ran the same task with the original context. The agent kept the check. The old message was expensive, but it contained the reason for current code.

The rule I took from that failure: age is a weak proxy for importance. A decision from hour one can constrain every later edit.

## Four Context Layers

After that test, I sorted context into layers and treated each one differently:

- contracts: interfaces, data schemas, and acceptance criteria
- decisions: chosen options, rejected options, and reasons
- evidence: current test results, logs, and relevant errors
- working memory: the last few tool calls and current diff

Contracts stay in full because edits elsewhere can violate them. Decisions stay, but I compress them into one line per choice. Evidence remains only if it supports an unresolved question or a failing test. Working memory can be truncated aggressively.

I moved completed tool output into a separate run log. If the agent needs an old result, it can request the file by ID. That keeps the model's immediate context short without destroying the evidence.

## A Compact Decision File

Next, I created `docs/agent-decisions.md` for the session.

Each entry used these five fields:

- date
- decision
- reason
- rejected option
- affected files

The first version contained 18 decisions in 620 words.

A representative entry looked like this:

```text
Date: 2026-05-18
Decision: Reserve quantities before allocating stock.
Reason: A concurrent order could otherwise allocate the same unit twice.
Rejected option: Reserve after payment confirmation.
Affected files: src/inventory/allocator.py, tests/test_allocator.py
```

I asked the agent to read this file at the start of every continuation session. It then repeated any decision that affected its next edit. If it couldn't find a relevant decision, it said so before changing code.

This file became more useful than the raw transcript. The transcript recorded what happened, while the decision file told the next session what still governed the code.

## Session Start Checklist

Before starting a new session now, I run a 10-minute audit. I list the acceptance criteria, copy relevant decisions from `agent-decisions.md`, attach only failing tests, and remove successful tool output from earlier tasks.

I also state what the session shouldn't do. For the inventory work, the prompt said the agent could change allocator code and tests, but couldn't touch migration files or the public API schema.

The checklist added about 10 minutes of preparation. It saved more time later: continuation sessions produced 38% smaller diffs and needed 22% fewer review comments across the next nine tasks. Those numbers come from my own local review log, so they're directional rather than a benchmark.

The method has a maintenance cost. Someone has to update the decision file when an interface changes, and a stale decision can be worse than no decision because it looks authoritative. I added a one-line check to the task template: before each new session, confirm that affected decisions still match the current schema.

The trimming rules also depend on the type of work. They fit long maintenance tasks, where an old constraint can reappear. They fit a new feature less well, because most early exploration becomes throw-away evidence within a few hours.

## Final State

The service repository now keeps three artifacts: `TASK.md`, `agent-decisions.md`, and a run log outside the repository. A session starts with contracts and decisions, works with recent evidence, and leaves detailed output in the log.

Trimming works best as classification. I remove transient evidence first, compress stable decisions, and only delete an old discussion after checking whether it still constrains the code.

I plan to describe the run-log format in a separate article. Subscribe if you want the next part.
