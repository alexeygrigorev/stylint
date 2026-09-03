# Keeping Agent Diffs Small Enough to Review

For this synthetic style exercise, the repository, dates, and measurements are fictional. In February 2026 I let a coding agent add a multi-file export feature to a Django service. The result contained 41 changed files, 1,240 added lines, and 410 deleted lines. The tests passed, and I still didn't want to merge it.

In this post, I'll share:

- why the first large change failed review
- how I defined a normal diff budget
- how I split work along clear interfaces
- what I measured across six tasks
- where the limits need exceptions

## The first large change failed

The agent did respectable work in several files. It added models, serializers, background tasks, and a management command. It also renamed a helper, reformatted a settings module, and introduced a retry wrapper used by exactly one caller.

My review attention ran out before the important parts did. I found one obvious naming issue and approved a different change that affected scheduled exports. I missed that the retry wrapper silently swallowed a permission error. It was my fault for accepting an enormous surface with a promise to read it later.

The rule I took from it: if the agent can change 40 files in one run, my review becomes the bottleneck.

## The normal budget

I added a normal budget to the project's agent instructions:

- at most five files
- a maximum of 250 changed lines
- a single user-visible behavior

Lockfile generation and migrations were exceptions, but each exception still needed its own justification.

Before editing, the agent had to submit a task note with four items:

- the outcome and the files it expected to change
- the interfaces it would preserve
- the tests that would prove the outcome
- a rollback action if the change failed

I reviewed the note before granting write access. If the note already named more than five files, the task was too broad.

These numbers were limits on attention, not quality scores. A 40-line change to a parser could deserve more review than a 240-line set of repetitive template edits. Still, the budget gave both of us a shared stopping point.

I also required every task to state the integration seam it touched. Examples included an HTTP request, a database transaction, a queue message, or a CLI output. That made scope drift visible early.

## Splitting the work

For the export feature, the first interface was the CSV schema. The agent produced a pure function, fixtures, and tests, with no route or model changes. The diff had four files and 190 lines. I could verify the columns, quoting rules, and timezone behavior without opening Django.

The second task added a query object that selected eligible orders. It returned typed records and stayed independent of serialization. The third task added a management command with a `--dry-run` flag. Only after those pieces looked correct did the agent connect a POST endpoint and a queued job.

Each task ended with a short note naming inputs, outputs, tests, and a rollback action. The final connection task changed two files and 70 lines. That was the only part where I had to think about the whole system.

## Effects of the limits

I applied the budget to six comparable tasks in the same service. My review notes showed a clear change in workload, though the sample was small.

The median changed lines fell from 780 to 220, and median first-review comments fell from 14 to 5. Two tasks still needed rework after review, and both involved unclear acceptance criteria rather than diff size.

Wall-clock time didn't improve much. Coordinating five runs took about 20% longer than one broad request. The extra time produced a review I could actually finish, and it reduced the chance of a late rollback.

The biggest quality win came from interface-first ordering. The agent couldn't invent a serializer before the CSV function existed, and it couldn't connect a route before the query object returned stable records. That sequence made design arguments happen while the diff was still small.

## Exceptions that still work

A mechanical rename can touch many files, while remaining easy to review. I allow it as a dedicated run with no behavior change, a short explanation, and a clean test run. The same applies to a dependency upgrade with a lockfile and changelog entry.

Database migrations need a different gate. The agent may draft an expansion migration, but I review the rollback path and data assumptions separately. For one table rewrite, I required a copy of production row counts by status and a script to compare them after deployment.

I now check whether a large diff contains one kind of change. If it mixes rename, behavior, and infrastructure work, I split it.

## Current limits

The budget lives next to the repository instructions, and the agent reports files and line counts before editing. It has refused two requests that would have mixed unrelated cleanup with feature work. I have also learned to write smaller outcomes, which may be the bigger benefit.

The remaining gap is semantic review. A small diff can still be wrong in a way tests don't catch. A change to a public API deserves a human-written example even when the implementation is short.

## Lessons Learned

Small diffs protect attention, and attention is the scarce resource in AI-assisted development. The agent doesn't need permission to think broadly, but it needs boundaries for writing.

I now treat a large proposed change as several proposals. If they can't be sequenced, the design is probably coupled in a way I should fix first.

I plan to write more about acceptance criteria for agent tasks in an upcoming article. Subscribe to stay updated.
