# Setting Budget Caps for Long-Running Agent Jobs

I generated the repository, agent runs, and costs in this draft as a synthetic style exercise. It follows the same build-log structure I use when an autonomous job runs without me at the keyboard.

On 6 April 2026, I left an agent alone with a 63-task migration. It completed 41 tasks, burned 4.8 million tokens, and produced a 2,300-line diff that took me most of Saturday to review. That incident led to a small budget layer around every run.

In this post, I'll share:

- why unbounded agent runs failed for me
- the four budgets I now set before starting work
- how the runner enforces token and wall-clock limits
- how retry and diff-size caps changed behavior
- what the runner records when it stops
- what changed after 18 controlled runs

## Unbounded Runs and Missing Review

The first version of my runner had one instruction: keep going until the task list is empty. That looked efficient, but it gave the agent no reason to stop and ask for review. It continued through ambiguous requirements and wrote increasingly speculative code.

I also had no way to distinguish productive work from churn. The log showed successful tool calls, passing tests, and a growing number of edits. The diff told a different story: the agent had replaced an internal library API twice after the tests already passed.

My mistake was treating autonomy as a single setting. The useful version separates task progress from resource use, and it makes both visible before the work continues.

## Start With Four Budgets

Before the migration attempt, I would have set a maximum token count and stopped there. That limit addresses cost while ignoring review time and repeated failures.

I now write four numbers into `agent-run.yaml`:

- `max_input_tokens` per model request
- `max_run_tokens` across the whole job
- `max_minutes` of wall-clock time
- `max_diff_lines` before human review

Two supporting limits prevent retries from hiding a bad path. A task can run three attempts, and all attempts together can spend no more than 20% of the remaining job budget. When either limit trips, the runner marks the task blocked and moves to an independent item.

These settings make the trade-off explicit. A large budget can finish more of a safe mechanical task, while a small budget preserves my attention and makes failures cheaper.

## Enforce the Token and Time Limits

The first implementation checked usage after each model response. That was easy to write, but a single long tool call could overshoot the budget.

I moved the check before each request as well:

```python
def can_continue(run: Run, next_estimate: int) -> bool:
    projected_tokens = run.used_tokens + next_estimate
    under_token_cap = projected_tokens < run.limits.max_run_tokens
    under_clock = run.elapsed_seconds < run.limits.max_minutes * 60
    return under_token_cap and under_clock
```

If `can_continue` returns false, the runner stops at a task boundary and writes a checkpoint. It doesn't kill an in-flight file edit. The current task gets a short grace period, then the runner restores the last clean tree from Git.

I deliberately left a 10% reserve for a final summary. Without it, the runner hit its token cap and produced no explanation of where work stopped. The missing summary cost more time than the reserved tokens.

## Retry Limits and Diff Size

Retries made the first controlled runs look more reliable than they were. One task failed seven times, and the token counter treated each attempt as reasonable progress. I reduced the per-task cap to three attempts and required a different approach after the second failure.

The runner now writes the retry plan into the log. After the first failure, it reproduces the failing test. After the second, it proposes either a narrower task or an explicit blocker. It can't retry a third time just because the prompt includes the word "again".

Diff size caught another problem with mixed unrelated edits. A valid 400-line change was acceptable, while a 1,200-line change usually combined changes that belonged in separate pull requests. The first pass allowed up to 900 lines. I reduced the soft limit to 500 after reviewing the first six runs, and the average accepted diff fell from 340 to 210 lines.

When an agent reaches the soft limit, it must run tests, update the task record, and stop before starting another file. That interruption feels slow in the log, but it makes the resulting pull request reviewable in one sitting.

## Record Every Stop

Each stop produces one record in `runs/2026-04-18.jsonl`.

The fields are deliberately boring:

- reason for stopping
- completed tasks
- blocked tasks and failure text
- tokens used and reserved
- elapsed time
- diff lines and files touched
- command to restart safely

The restart command includes `--from checkpoint-17`, so a new process doesn't replay completed tasks. It also sets the same budget family as the original run. If only 22% of the token budget remains, the resumed run inherits that constraint instead of starting with a fresh allowance.

I initially stored these records in a spreadsheet. It was fine for one job, but comparing 18 runs became tedious. The JSONL file made it easy to calculate medians and identify tasks that consumed more than their share.

## Caps and Measured Changes

I tested the rules on 18 fictional runs across three repositories. The average spend fell from 4.8 million to 1.9 million tokens per job. Median review time fell from 95 minutes to 35 minutes, while the completed-task rate stayed between 72% and 81%.

Those numbers hide one loss. On two runs, the agent stopped 15 minutes before it would have finished a final refactor. I accepted that cost because the earlier version had also "finished" work I eventually reverted.

The remaining gap is estimation. My initial request-size estimate was too low for browser tests, so those tasks hit the preflight limit more often. The runner currently learns nothing across jobs, and I plan to add per-task-type estimates next.

## Lessons From 18 Runs

An agent needs a budget the way a deployment needs a rollback path. Four numbers turn a long autonomous job into something I can stop, review, and resume.

The rule I took from the migration incident is simple: don't give a long-running agent more resources than I'm willing to review at one time. I'll write about per-task estimates in a future article. Subscribe for updates.
