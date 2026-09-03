# Scoping What a Coding Agent May Change

In February, a coding agent edited 38 files for what I thought was a small
logging task. I wrote this synthetic style exercise afterwards and invented the
repository, dates, measurements, and incidents. The useful habit came from the
scenario: I now write an explicit scope file before I let an agent touch code.

The repository was a FastAPI service (a Python web framework project) with a
separate frontend.

The request said, "Use structured logging for the upload endpoint". The agent
interpreted that as permission to standardize logging across the backend and to
adjust frontend calls that consumed the old error structure. In this post, I'll
share:

- the scope file I now create for every agent task,
- how I separate allowed, forbidden, and review-only paths,
- the commands and checks in the review checklist,
- a three-week trial across 17 tasks,
- what still needs a human decision.

## The uncontrolled first run

The run completed in 46 minutes and produced a green test suite. The agent
added request IDs, replaced print calls, and changed 4 shared exception classes.
Those changes were internally coherent. They were also 2,340 lines larger than
the task required.

I spent almost 2 hours reviewing the diff. Two frontend changes fixed a real
problem, but the task had never asked for them. One change renamed an internal
error key, which would have broken an internal client on the next deploy.

I reverted the branch, and I extracted a rule from the failure: an agent should
never infer project-wide authority from a local request. A clear goal tells it
what to accomplish, and a scope file tells it what it may disturb.

## Write the scope file first

I created `.agent/scope.md` in the fictional repository. The file has three
short parts:

- the first names the outcome and the primary module,
- the second lists paths the agent may edit,
- the third lists paths it may read but may not edit.

My reusable template contains these sections:

```text
Outcome:
- Add structured request logs to the upload endpoint.

Allowed:
- app/uploads/router.py
- app/uploads/logging.py
- tests/uploads/test_router_logging.py

Forbidden:
- app/common/errors.py
- web/**
- infra/**

Review-only:
- app/uploads/models.py
```

Allowed paths are the only write targets, and forbidden paths are hard
boundaries. Review-only paths require a proposal in the plan, a code reference,
and my approval before an edit. The distinction matters because reading a model
or configuration file is often useful, while editing it changes behavior for
many callers.

I named the template sections Allowed, May not edit, and Review-only. Those
labels match the language I use in review comments.

For a new task, I copy the last scope file and change only what the task needs.
That takes 3 to 5 minutes. It also creates a small history of decisions, so I
can see when a boundary moved and why.

## Put the boundary in the run policy

The scope file explains intent, and the run policy enforces it. My `run-agent`
script is a thin wrapper that starts an agent and records commands.

The same script applies a diff filter. It reads the YAML section at the top of
a task file.

The logging task uses this policy:

```yaml
paths:
  write: ["app/uploads/*", "tests/uploads/*"]
  deny: ["app/common/*", "web/", "infra/", ".github/"]
max_files_changed: 6
max_diff_lines: 350
require_plan_before_write: true
```

Before the first write, the agent must output a plan with each intended file.
The wrapper rejects writes outside `write` and stops the run when either limit
is exceeded. The first version of this check caught 3 accidental changes to a
generated client in one week.

I also record the rejected paths in `agent-run.log`. The log entry contains the
task ID, timestamp, attempted file, and matching rule. That evidence focuses
the review conversation. I can say, "You tried to change the shared errors, and
the policy forbids that," instead of arguing from memory.

## Review the plan, then the diff

My checklist has two stages.

Before the run, I check the plan:

- the outcome uses observable behavior,
- allowed paths map directly to that behavior,
- no forbidden path appears as an edit target,
- new dependencies are named with a reason,
- tests are included in the allowed set.

After the run, I review the result in a fixed order:

- interface changes,
- database and configuration changes,
- application behavior,
- tests,
- names and formatting.

Interface and configuration changes have the largest blast radius, so they get
attention first.

The checklist asks for evidence. A logging change should show a request ID in
the output. A validation change should show both accepted and rejected inputs.
A migration should show the command, the rollback command, and the result on a
copy of the database.

For the logging task, the scoped agent changed 5 files and 247 lines. The test
diff covered three cases:

- a successful upload,
- a rejected file type,
- a storage timeout.

I still found one issue. The agent logged the full filename, which could expose
user data, so I replaced it with a hash.

## Results From the Trial

I used this policy for 17 tasks over 3 weeks. The work included:

- bug fixes,
- small features,
- test additions,
- dependency updates.

Twelve finished inside the original scope. Four requested an expansion through
the plan. One ignored the scope, and the wrapper rejected its first write.

The median changed file count fell from 9 to 3. The median review time fell
from about 28 minutes to 9. Those numbers include my own learning curve, so I
would treat them as directional evidence, not a controlled benchmark.

Expansion was usually justified. Two tasks needed a shared helper, and one
needed to update a generated client after an API change. In each case, the
agent listed the exact path, the reason, and the callers. I approved it in a
follow-up message, and the wrapper logged the approval.

The hardest case was a refactor with no single owner. Several small files
implemented the same rule. The agent proposed all 7 of them, and the diff fit
under the line limit. I allowed it because the plan named each file and the
tests covered the shared behavior.

## Lessons From the Policy

A scope file is a review tool before it becomes a restriction. Writing it
forces me to decide which parts of the system the task touches.

Three rules now guide my agent work:

- define behavior before paths,
- make reading broad and writing narrow,
- require a proposal before every boundary change.

The system still trusts my judgment. A bad scope can exclude the right file or
hide a necessary migration. It makes that mistake visible earlier, though, and
it keeps a large change from arriving as a finished surprise.

Next I plan to add ownership labels to the fictional service so generated
clients and shared helpers require a second reviewer. I'll describe that
experiment in a future article. Subscribe to stay updated.
