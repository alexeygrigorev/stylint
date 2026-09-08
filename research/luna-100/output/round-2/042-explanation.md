# A Practical Agent Team for Software

When a project has many moving parts, asking one coding agent to implement everything and approve its own work creates an obvious gap. I tried to close it by treating the main Claude Code session as an orchestrator and giving separate agents narrow responsibilities.

The team has four roles. The Product Manager turns an idea into user stories, acceptance criteria, and test scenarios.

The Software Engineer writes implementation and tests. QA runs those tests and checks each acceptance criterion with evidence.

The On-Call Engineer watches CI/CD after code is pushed and fixes pipeline failures. The PM returns at the end for a user-facing acceptance review.

The sequence matters because a task enters the backlog, gets groomed by the PM, and moves to the SWE.

QA either rejects it with evidence or accepts it, and the SWE fixes rejected work.

The PM gives accepted work a final review, after which the orchestrator commits and closes it. Passing tests alone aren't enough because a feature can satisfy an engineering interpretation while missing the user story.

I keep the process in repository files. Role definitions live in `.claude/agents/`, `PROCESS.md` describes the workflow, and `CLAUDE.md` provides project instructions.

An execute skill starts the pipeline. For larger backlogs, I usually process two tasks in parallel and then pull the next pair.

A recurring task-list instruction tells the orchestrator to continue, so the pipeline doesn't stop after every batch.

The choice of tracker depends on the project. GitHub Issues provide visible coordination and attach reports to tasks.

A lighter project can use filenames such as `.todo.md`, `.groomed.md`, and `.in-progress.md`, eventually moving files into `done/`. The tracker is less important than keeping the PM, SWE, QA, and acceptance stages explicit.

There are practical reasons to keep the roles separate. An agent can report completion while its task widget still contains work.

A subagent can spend an hour without making progress visible. An orchestrator can also skip grooming and launch the SWE directly.

Those are process failures, so adding more prompt text isn't always enough. This is why I started Codehive, a coding orchestrator where the pipeline can enforce responsibilities and definitions of done.

The projects gave me different tests of the method. AI Shipping Labs reached 41 completed tasks out of 46 overnight.

DataTasks showed that a serverless application could start from a short dictated specification, although I paused it because I lacked time to evaluate it. Merm demonstrated that benchmarks can decide whether a renderer is useful enough to publish.

Rustkyll showed the cost of skipping requirements: its first implementation fit one website instead of Jekyll generally.

The method doesn't remove supervision. Instead, it makes supervision more specific by defining what each stage must produce.

Instead of watching every line, I define what each stage must produce, look at evidence at the boundaries, and intervene when the process drifts. That's the useful part of an agent team: independent checks around the work, with a clear place to send a task when it fails.
