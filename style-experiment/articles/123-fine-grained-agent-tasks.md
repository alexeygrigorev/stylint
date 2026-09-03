# Splitting a Large Feature into Agent-Sized Tasks

I wrote this synthetic style exercise as a how-to guide. The feature, dates and numbers are fictional. In March 2026 I gave a coding agent one task called "add bulk import to the tracker app". It came back with 14 new files of half-working code.

The agent did what I asked, and the task was simply too large for one session. The session burned a full evening, and I rewrote most of the result anyway. Since April 2026 I plan agent work as task cards instead. Each card states a narrow outcome, the files it touches, and runnable acceptance checks.

In this post, I'll share:

- how I write the outcome in one sentence
- how I list the files each task touches
- how I add acceptance checks that can run
- how I sequence tasks and mark dependencies
- where the method needs judgment
- what the switch changed in delivery

## 1. Write The Outcome In One Sentence

A task card starts with the outcome, and the outcome gets one sentence. If the sentence needs a second clause about another behavior, that's a second task.

The March import outcome read: "users can upload a 50 MB CSV and see 10,000 rows imported with a per-row error report". That outcome filled a whole session and died halfway, so it split into three tasks.

My size test is time. A task should fit one focused agent session of about 30 to 60 minutes, and sessions that run longer start to drift. When a card can't fit that budget, it splits again.

You can write the cards yourself, or you can groom them with a coding agent. I draft them by hand, because the outcome sentence is where I notice that a task is two tasks in disguise.

## 2. List The Files Each Task Touches

Each card names the files it expects to touch. The list turns vague work into checkable work, and it tells you when two tasks will collide.

My limit is about 5 files per card. The March list had one card with 9 files, and splitting it produced 2 tasks that finished the same day. If two cards touch the same file, they get sequenced. Parallel sessions on one file gave me two merged rewrites I had to untangle by hand in February.

The parser card from March looked like this:

```text
task: parse uploaded CSV into row objects
outcome: parse_buffer() returns rows plus a per-row error list
files: app/import/parser.py, tests/test_parser.py
depends on: nothing, this is the first task
```

Four lines, and the agent knows where to work and where to stop. The file list also makes review faster, because I open exactly those files when the task reports done.

## 3. Add Acceptance Checks That Can Run

Every card ends with checks I can run in a terminal. Three checks have been enough in practice, one for the happy path, one for an edge case, and one for a failure.

My first cards had a check that said "handle errors properly". The agent marked it done and handled nothing. The rule I took from it: a check I can't run as a command isn't a check.

Each check is a command I paste at review time:

```bash
uv run pytest tests/test_parser.py -q
```

If that command fails, the task isn't done, no matter what the agent's summary says. The command also gives the next session a clean starting point, because I run it before writing the next card.

## 4. Sequence The Tasks And Mark Dependencies

The cards get an order, and the order follows the file lists. Tasks that touch the same file go back to back, and the first version of each file exists before anything builds on it.

Each task starts from a state where the previous check command passes. That rule cost me one rework in March, and it has saved more than one session since. In the end the import feature became 11 cards. Nine of them went through cleanly, and 2 needed a second session after failed checks.

I commit after every card, and the commit message names the card. When a later card breaks an earlier check, `git bisect` finds the card in minutes instead of an afternoon.

## Limits Of The Method

Splitting costs planning time, and the planning is real work. The 11-card list took about 45 minutes to write, and a 4-card version of the same feature took 10.

Some work resists the split. A schema migration that touched every model stayed one card, and I shrank its scope until it fit an hour. Narrow cards can also produce narrow code, so I review the whole feature at the end. That review found duplicated validation between the parser and the loader, which one cross-file pass fixed.

Card lists also go stale. When the schema changed in May, 3 cards pointed at files that no longer existed, so I now re-read the file lists before each session.

## Delivery Numbers After The Switch

The first March attempt spent one evening and produced code I rewrote. The card version used 4 sessions across 2 days and passed review with 2 small fixes.

Per-card time estimates are still guesses, and 2 of the 11 cards split badly enough to redo. I also haven't found a good way to card exploratory work, where the outcome is a decision rather than code.

I'll write about the end-of-feature review pass in a future post. If you want to follow along, don't forget to subscribe.
