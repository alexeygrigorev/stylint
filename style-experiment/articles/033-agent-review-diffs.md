# Reviewing Large Agent Diffs in Small Batches

This synthetic style exercise uses a fictional project and invented details.

Last month a coding agent returned a 1,842-line diff for a fictional inventory dashboard. The build passed, all 74 tests were green, and the feature appeared to work. I still rejected the pull request because I couldn't review it responsibly in one pass.

That rejection changed how I assign work. I stopped asking for a complete feature in a single run and started designing tasks around the size of attention I actually have. Smaller diffs needed less rework, and saved repeated review.

The repository, diff sizes, and approval counts in this article are invented examples.

In this post, I'll share:

- how I sort a large diff into review batches
- what I check before behavior and polish
- how I use a batch manifest with an agent
- what the approach changed in four fictional tasks
- when I still ask for a larger diff

## Sort by Review Risk

My first pass separates changes into five batches:

1. public interfaces and data schemas
2. database schema and migrations
3. business behavior and state changes
4. tests and fixtures
5. UI text, styling, and comments

Interface mistakes propagate through every caller, while a bad button label is easy to fix later. I review the expensive layer first because that decision determines whether the rest deserves attention.

Each batch gets a number, a purpose, and a file list. The manifest turns a scary diff into a sequence of reviewable decisions.

## Check Interfaces Before Behavior

For each interface change, I read the input types, output types, and naming. I also read the failure cases before implementation quality. I only ask whether another developer could use the API without guessing.

This review caught a fictional `InventoryAdjustment` object with an optional `quantity`, and the agent intended `None` to mean "no change". Every caller would have needed a branch for that case, so we changed the API to two explicit methods. Those methods were `set_quantity` and `adjust_quantity`.

That small interface change deleted 63 lines of defensive checks from the later implementation. It also made the type checker useful instead of noisy.

## Review State Changes

Next I look at risky state operations and scheduled jobs. For each business action, I want a simple trace. The trace shows which tables change, what happens on timeout, and whether a retry avoids duplicates.

In one batch, the agent updated stock counts and wrote an audit record in separate transactions. The happy path worked, but a timeout between writes could make inventory correct while the audit history remained incomplete.

We moved both writes into one transaction and added an idempotency key supplied by the client. The change was eight lines. Reviewing the state batch alone made that eight-line risk visible.

## A Batch Manifest

I give the manifest back to the coding agent as a constraint:

```text
Batch 2 of 5
Files: src/db/migrations/0042_adjustments.sql, src/db/schema.py
Purpose: add adjustment_reason and an idempotency key
Do not change API handlers, services, UI, or tests in this run.
Stop after migrations and model updates. Print the exact commands you ran.
```

The prompt keeps each run narrow and makes the stop point explicit. It also turns review feedback into a new batch instead of a growing pile of edits.

For the inventory project, I used five batches in descending review priority. Their sizes ranged from 238 to 496 lines. The largest was still substantial, but each had one purpose.

## Results in Four Tasks

I compared this approach with four older feature requests. The newer tasks averaged 368 lines per agent run, while the older tasks averaged 915. First-pass approval rose from two of four older runs to four of five newer runs.

Total wall-clock time improved less than the diff numbers suggest. Small runs added planning and startup overhead, so the overall improvement was only about 15%. The real gain was lower review fatigue and fewer hidden interface mistakes.

New problems appeared in the experiment. Agents sometimes left temporary compatibility code after an early batch. They also updated tests for a removed interface. A short cleanup batch solved both.

## Larger Diffs That Make Sense

I still allow large generated changes for mechanical work. The work can rename a symbol, upgrade a dependency, format files, or replace one repeated structure everywhere. The transformation is broad but easy to verify with compilation, tests, and a grep review.

The rule is simpler than the five-batch process: match the batch to the type of judgment it needs. A large mechanical change needs one kind of attention. A large feature needs several.

Small batches are a review strategy rather than a productivity cult. If a future tool can summarize and prove state changes reliably, I'll happily widen the batches again.

I'll write next about the cleanup batch and its checklist. If you want to follow along, don't forget to subscribe.
