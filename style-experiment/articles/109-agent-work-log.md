# Making Agents Produce Work Logs I Can Review Later

Last month I let a coding agent change 17 files across two services. The tests passed, but I spent almost two hours reconstructing why the agent made each change.

I wrote this project log as a synthetic style exercise. I invented the repository, the 42 tasks, the elapsed time, and the token counts for this article.

In this post, I'll share:

- why git history was insufficient for agent review
- the log format I asked the agent to append
- how I validate a log without reading every line
- what the logs revealed after 42 tasks
- where human judgment still sits

## Commit History Without Reasons

My first setup relied on commit messages. I told the agent to write clear messages and make one commit per task. The rule worked for simple edits.

It failed when a task touched shared code. One commit named `refactor user handling` contained changes to authentication, database indexes, tests, and two unrelated CLI messages. The final state was clear. The reasoning was gone.

I also had three unanswered questions after the run:

- which instructions changed during the task
- which files the agent read before editing
- which alternatives it considered and rejected

Those questions matter more with agents than with ordinary commits. The commit records an outcome, while the review needs the decision path.

I needed a work log, a per-task record of actions, evidence, and outcomes.

## Require a Structured Log

I gave each task its own YAML file (a plain configuration format). The agent had to append entries while working, and the wrapper script refused to accept a task if the file was missing.

The initial schema stayed small:

```yaml
task: ORDERS-214
instruction_file: tasks/orders-214.md
allowed_paths:
  - src/orders
  - tests/orders
entries:
  - action: read
    target: src/orders/repository.py
    reason: find current validation rules
  - action: edit
    target: src/orders/service.py
    reason: reject negative quantities
  - action: test
    command: uv run pytest tests/orders -q
    result: pass
```

Each entry has an action, a target, and a reason. The reason line is short and references a file, test result, error message, or instruction.

I deliberately excluded model tokens, confidence scores, and internal monologue. Those fields made early versions feel scientific and gave me nothing I could check.

The important addition was a decision field. When the agent chose between approaches, it recorded both options and the rule it applied.

## Validate the Log

Reading every entry would replace one review with another. I wrote a 60-line Python validator that checks structure and runs six rules.

The wrapper runs it after every task:

```bash
uv run python tools/validate_work_log.py runs/ORDERS-214.yaml
```

The validator enforces structural rules. It requires every changed file to appear in an edit entry and requires every edit to list a reason. It also requires every failed test to lead to another action, and it requires a decision entry to name at least two options.

It can't judge whether the reason is good. That's fine because the check turns missing evidence into a mechanical failure.

In the first week, 9 of 14 tasks failed validation.

The usual problem was a changed file that had no edit entry, often because the agent ran a formatter. I added a `format` action and required the agent to name the formatter command.

After that, validation failures became rare and meaningful. In the remaining 28 tasks, only 3 failed because the agent omitted a rejected alternative.

## Learn From the Complete Run

Across 42 tasks, the agent completed 31 without human intervention. Two needed a small correction, six were rejected, and three were split into new tasks.

The logs showed a clearer distribution than the test results:

- 14 tasks required reading at least four source files
- 11 contained a rejected alternative
- 8 ended with a test-first change
- 6 touched a path outside the declared allowed paths

The final line mattered most. The repository diff showed the damage, while the logs showed when it happened and what instruction preceded it.

Five of the six boundary violations followed the same wording in the instructions. The agent saw a helper function in a neighboring directory and edited it because the task said "fix all related tests".

The revised rule now says to report the neighboring helper and stop. That one sentence removed the most expensive class of rework.

The logs also revealed a less dramatic issue. When tasks lacked acceptance criteria, the agent made reasonable choices that didn't match our interface conventions.

## Keep the Human Review

The log changed the order of review. I read the task instruction, the final diff, and only the decision entries. For a typical task, that takes 8 to 12 minutes instead of 35.

I still run the tests myself and look at authentication, database migrations, and public interfaces. The log narrows where I look, but it doesn't decide what ships.

For rejected tasks, the log is equally useful. It records what the agent tried before I stopped the run. That prevents the same approach from entering next week's prompt.

## Lessons From 42 Tasks

Git history answers what changed in the repository. A structured work log also records why the agent believed the change was necessary.

The rule I took from the run: require evidence at each decision point, and make missing evidence a failed task.

I'll describe the validator rules in more detail in a future article. Subscribe to stay updated.
