# Designing Handoffs in a Small Agent Team

In June, I gave a fictional agent team nine feature and repair tasks for a small analytics app. The planner created task files, a builder edited code, and a reviewer ran tests. Seven tasks worked cleanly, and the other two failed because the agents talked about work that never appeared in a file.

I invented the app, agents, tasks, and metrics for a synthetic style exercise. I'm using that fiction to study a coordination problem I keep seeing in agent workflows.

In this post, I'll cover the handoff format I settled on:

- why chat messages made poor handoffs
- the three artifacts every task needs
- how to scope changes without freezing the agents
- the review loop and rollback path
- what still goes wrong with parallel tasks

## Chat was the wrong handoff

The first implementation used one shared conversation. The planner described the task, the builder asked questions, and the reviewer added comments. It sounded efficient because all agents could see everything.

The opposite happened after 40 minutes, the conversation held 128 messages and the current task requirements were scattered across six comments. One builder summarized the goal incorrectly, then implemented its summary. The reviewer caught the mismatch only after 22 files changed.

I stopped the run and read the transcript. The useful content was present, but it was buried in status chatter. The rule I took from that run: a handoff needs an artifact that can be diffed, not a conversation that has to be reconstructed.

## The artifacts

Each task now gets its own directory under `runs/2026-06-18/` and the planner uses these artifacts:

- `task.md` states the user outcome, constraints, and done condition.
- `plan.md` lists the intended files, interfaces, and tests.
- `result.md` records evidence, deviations, and review notes.

I use the task file as the task's specification. It names the behavior, the affected command, and the evidence that will count as done. For one report task, the done condition was "the weekly CLI prints revenue by region and exits 0 when the input covers seven days". That sentence prevented two interpretations later.

The plan file makes the blast radius visible. It lists paths and marks read-only paths, so the builder knows where changes are allowed. For the report task, the builder could touch `src/analytics/reports.py` and `tests/test_reports.py`, while it could only read `src/analytics/db.py`.

## Keep the change area flexible

My first attempt at guardrails was too narrow. I listed exact functions and told the builder to avoid everything else. It followed the instructions literally and left a necessary type alias unchanged, so the new code repeated the old definition.

The better guardrail describes behavior and ownership. The plan says what the task may change and what should remain untouched. It may look at other code to understand callers, and it may propose edits only for owned paths. Human review still catches design mistakes, while the file boundary reduces accidental sprawl.

I also added a diff-size limit after the first failure. A builder stops and writes a handoff note when a patch exceeds 400 lines or touches more than eight files. The limit is crude, but it turns a large surprise into a review point.

## Review evidence first

The reviewer used to look at the final diff first. That made it hard to distinguish intent from accident. Now the reviewer reads `task.md`, `plan.md`, and `result.md` before opening the patch.

Each result file must answer four items:

- what changed
- what tests were run
- which constraints were violated
- what needs a human decision

The reviewer can then compare the claim against the evidence. For the reporting task, `result.md` showed six tests, one skipped fixture, and a deviation: the builder added a CLI flag to support missing regions. The reviewer approved the flag because the test covered it and the task file didn't forbid new interfaces.

The full workflow stayed small:

```bash
python team.py run runs/2026-06-18/07-report
python team.py review runs/2026-06-18/07-report
```

The first command gives the task directory to the agents in sequence. The second renders the evidence and the diff into a review packet. I run both locally in this fictional exercise, so nothing reaches an external system.

## Handle failure and rollback

One builder changed a shared date parser while fixing a report bug, and two unrelated tests failed. The old flow would have encouraged a cascade of edits across three tasks.

The new flow treats that as a failed task, rather than a reason to expand scope. The builder writes the shared-parser change to `result.md`, marks the task blocked, and restores the parser to its original state. A separate task can then own the parser change and name its callers.

Git provides the rollback commands:

```bash
git restore src/analytics/dates.py
git diff --stat
```

After the restore, the reviewer sees only the task's intended files. The blocker stays in the result file so the next planning session can sequence the work.

## Remaining limits

Parallel tasks remain fragile when they share a concept before anyone names it. Two agents can independently add slightly different filters, and both tasks can pass their local checks. I now keep a two-line interface list in the coordinator and forbid duplicate names unless a task explicitly owns the shared type.

Judgment is the second limit. The planner writes a good task when the requirement is concrete. When the outcome is vague, the planner should create an investigation note rather than pretending that the path is known.

I now treat a good handoff as an interface promise with evidence attached. The conversation can explain, argue, and investigate, but the agent's permission to edit code starts from the artifact. If I continue this exercise, I'll compare three task formats on the same fictional feature. Subscribe if you want the follow-up comparison.
