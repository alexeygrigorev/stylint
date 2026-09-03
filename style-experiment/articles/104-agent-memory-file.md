# Using a Single Memory File Instead of a Complex Memory System

I wrote this analysis as a synthetic style exercise, and all project details are fictional. Between October 2025 and March 2026, I tried three memory systems with a coding agent on a small inventory service called Shelftrack. One Markdown file per repository survived all three trials.

The service had 14 endpoints, 61 tests, and two part-time maintainers. It was exactly the scale where memory should make onboarding cheaper.

In this post, I'll share:

- why the vector memory experiment failed
- what belongs in a repository memory file
- how I append decisions without creating noise
- how I prune stale context
- what changed in later agent runs

## The Vector Experiment Failed

The first version stored every useful message in SQLite and embedded each entry. On a new task, it retrieved the eight closest memories by cosine similarity.

It looked sophisticated for two weeks. Then it retrieved an abandoned plan from November 2025 while the current code already used the replacement module. The agent restored an obsolete helper and opened a pull request that failed 9 of 61 tests.

Similarity answered the wrong question. It found text that resembled the current prompt, while I needed decisions that still governed the repository.

I tried adding timestamps and project tags. That reduced bad retrievals from 14 per week to about 6, but it also hid useful older constraints. The database became another system to debug, and review took longer than writing code.

My mistake was optimizing recall before asking who would curate the memories. The rule I took from it: repository memory is an edited artifact, not a search index.

## One File

Shelftrack now keeps decisions in `.agent/memory.md`. The file is versioned with the code, visible in pull requests, and readable without an agent.

It contains only five sections, and each section has short bullets:

- project goal
- interfaces
- commands
- decisions
- known risks

The current file is 148 lines, including 41 dated decisions.

I wrote these stable rules into the interface section:

```text
- POST /items accepts an optional location_id.
- A missing location resolves to the default warehouse.
- Do not rename the inventory_event table in a routine change.
```

I recorded the test command, the lint command, and the local seed command in the command section. In the risk section, I noted that webhook retries may duplicate events and that the idempotency check is only partially implemented.

Because the file lives beside the code, a normal review can reject a bad "memory" before it affects the next run. That property mattered more than retrieval quality.

## Append Decisions

When an agent makes a nonobvious choice, I add one dated bullet to the decisions section. The bullet states the decision, the evidence, and the boundary.

I keep the entry format deliberately plain:

```text
- 2026-02-14: Store stock counts as integers. The API multiplies
  by 1000 for kilograms. Floats caused rounding drift in report ST-42.
```

I write the entry myself or ask the agent to propose it in the pull request description. The important step is review by a person who understands why the old approach failed.

Not every prompt deserves memory. A typo fix, one-off migration, and generated test fixture stay out. A change to a public API, accepted tradeoff, or recurring failure goes in.

During six weeks, I added 18 entries and rejected 11 agent proposals. The run log showed that most rejections were session-specific instructions, such as "use port 5057 while the normal port is occupied".

Those rejections gave me useful evidence. Most session details were already visible in the diff, the test, or the run log.

## Prune Stale Context

An append-only file eventually becomes misleading, so pruning is part of the workflow. At the end of each milestone, I review every decision older than six months.

I mark each bullet with keep, replace, or move-to-history, and history moves to `docs/decisions-history.md`:

- keep
- replace
- move to history

A replaced decision includes a short reference to the new decision.

For example, Shelftrack first stored images on local disk, and in January 2026 it moved to object storage. The old rule now says only that local paths are invalid and points to the new storage decision.

The prune review takes about 25 minutes per repository. I read the current interfaces, then each old bullet, and run the commands if they look doubtful.

I apply one test during the review: if following the bullet would fail or contradict current code, it can't stay in active memory. The test forced 12 deletions in March and exposed two undocumented interface changes.

## Later Runs

To compare approaches, I used 20 repeat tasks across Shelftrack, and each task started from a clean session:

- eight bug fixes
- six small features
- six documentation updates

The comparison gave these results:

- vector memory: 11 tasks needed a correction after the first pull request
- edited file: 5 tasks needed a correction
- median review time: down from 19 minutes to 8 minutes

The sample was small and biased because I wrote the second prompts more carefully.

Token use changed less than I expected. Loading 148 lines cost about 2,100 tokens, while the vector retrieval averaged 1,700 tokens. The edited file cost 23% more, but every token passed review.

I trusted the later runs more. I could open one file before a run and see what the agent would treat as constraints. When it made a mistake, I could fix the file rather than tune an embedding model.

The approach has an obvious limit. A single file doesn't scale to hundreds of services or to a team with conflicting ownership boundaries. At that point, repository-specific files plus a shared engineering handbook seem more sensible than one global memory store.

## Lessons

Memory should preserve constraints that survive the current session. A teammate should be able to review, edit, and blame the storage format without learning another system.

My current rule is to start with one Markdown file and measure where it breaks. A vector index may make sense when memories are personal, numerous, and unrelated to one repository. For code, the review path usually matters more than recall.

I plan to write separately about the 20-task comparison and the prune checklist. Subscribe if you want the next part of this agent-workflow series.
