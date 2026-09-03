# Writing Handoff Notes for the Next Coding Agent Session

I wrote this synthetic style exercise as a how-to guide, and all session details are fictional. In March 2026 I reopened a coding agent session after a weekend break. I stared at 14 changed files with no memory of why three tests were skipped. The prior session had run for six hours and burned 112,000 tokens.

I had trusted the agent transcript to persist the context. I scrolled through 340 tool calls looking for the decision about Postgres indexes and never found it. The new session rebuilt the same migration I had already rejected on Friday.

In this post, I'll share:

- what goes into a 10-minute handoff note
- how I record current state and open decisions
- how I define the next task with acceptance checks
- how I list known risks before closing the laptop
- what changed after 30 days of handoff notes

## State Snapshot In Five Lines

A handoff note starts with facts that let the next session resume without reading the full transcript. I write the branch name, the last passing commit, the failing tests, and the files with uncommitted changes. The note takes about three minutes when the terminal is still open.

My template lives at `docs/handoff.md` with headings for state, decisions, next task, and risks. I fill it at the end of every agent session that touches more than two files. Short sessions with one-line fixes skip the note entirely.

I capture the working tree with one command before writing:

```bash
git status --short && git log --oneline -5
```

I paste the output at the top of the note and add one line about the test suite. Last Tuesday the note said three tests failed in `test_billing.py` after the index change. That line saved 20 minutes the next morning.

My mistake was writing long summaries that repeated the transcript. The rule I took from it: a handoff note holds decisions and pointers, and the transcript keeps the raw history.

## Decisions And Open Questions

Decisions fade faster than code changes, so I record each choice with its reason. I write what I chose, why I chose it, and what I rejected. The entry stays short at two lines per decision.

A recent note about queue workers held three entries:

- keep Celery with Redis because the team knows the retry settings
- postpone Postgres LISTEN because no one has run it in production
- use 30-second visibility timeout after the March incident with 43 stuck tasks

I mark open questions separately so the next session doesn't treat them as settled. I write the question, the two options under review, and the test that would settle it. One note left the batch size open between 500 and 2,000 rows pending a timing run.

I also note who needs to confirm product choices. I wrote that Marina from billing must approve the refund window before I change the cron schedule. That line stopped the agent from editing the schedule in the next session.

Entries name the reason alongside the choice, so the section works. A later session can reverse a decision when the reason no longer holds. Without the reason, every old choice looks like a rule.

## Next Task With Acceptance Checks

The next task needs a narrow outcome and a way to confirm it. I write one paragraph with the files to touch and the command that proves the work. The agent starts from that paragraph instead of re-reading the whole note.

A good entry names two or three files and one test command:

```text
Add retry with backoff to worker/fetch.py.
Touch worker/fetch.py and tests/test_fetch.py only.
Run pytest tests/test_fetch.py -k retry before finishing.
```

The entry above took four minutes to write and saved an hour of setup. The next session ran the test first, saw two failures, and fixed the backoff values without touching the queue config.

I keep the task small enough for one session. I scope it to a single behavior change with fewer than five files. Larger tasks get split across two notes with a checkpoint in between.

I learned to state what the task excludes. I wrote that the retry task excludes alert text and dashboard changes. That boundary kept the session from editing four extra files that were unrelated to the failure.

## Known Risks Before Closing

Risks go last because they set how bold the next session should be. I list database locks, missing backups, and external service limits. Each risk gets one line with the file or table involved.

A March note listed two risks for a billing migration:

- invoices table locks for 40 seconds during index creation on 12 million rows
- Stripe test mode allows only 25 requests per second during backfill

I add the rollback step next to each risky change. I wrote that the migration rolls back with `alembic downgrade -1` and a restore from the 02:10 backup. The next session ran the downgrade once during testing and confirmed it finished in 11 seconds.

I also flag credentials and production access. I wrote that the staging key expires on Friday and the production database allows reads only from the office network. Those two lines stopped a midnight deploy attempt that would have failed on permissions.

The risk list stays short at three entries or fewer. Longer lists hide the real danger among routine caveats. I move smaller worries into code comments where the next reader will see them in context.

## Results After 30 Days

The habit changed how fast I resume agent work after a break. I reopened 18 sessions in April with handoff notes, and 15 of them produced a passing test within 30 minutes. Sessions without notes took about twice as long to reach the same point.

Token use dropped because the next session reads one page instead of the full transcript. The average resume prompt fell from 9,400 tokens to 1,800 tokens. Over 18 sessions, that difference saved roughly 137,000 tokens and about 40 minutes of waiting.

The notes also caught two repeated mistakes. I had asked the agent to skip the same flaky test twice, and the handoff log showed both skips with dates. I fixed the test data instead of skipping a third time.

The flow still needs discipline at the end of long sessions. I skip the note when I'm tired, and those are the sessions I most need it for. I now set a 10-minute timer before closing the laptop.

I'll write about my session log format in a future post. If you want to follow along, don't forget to subscribe.
