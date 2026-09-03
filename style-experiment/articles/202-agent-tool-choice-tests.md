# Testing Whether an Agent Chooses the Right Tool

I wrote this synthetic style exercise as a how-to guide. The project, dates and numbers are fictional. In April 2026 my coding agent answered a question about retry limits from memory. The project has a `docs-search` tool, a small script that greps the internal docs, and the agent never called it. The answer sounded confident and was wrong by a factor of four.

A skipped call is a behavior, and behaviors can take tests. Since May 2026 I run a suite of ten scenarios against every prompt change, and the suite catches most regressions before I ship anything.

In this post, I'll share:

- how I write one scenario per decision
- how I name the expected tool call
- how the grading script judges each run
- what the runs cost in tokens and money
- the caveats after two months of nightly runs

## An Agent That Ignored Its Own Tool

I found the wrong answer during a staging review in April, one day after praising the tool setup to a teammate. The tool worked when I called it manually, so the gap sat in the agent's choice, and no amount of reading output proved anything. Guessing at prompt wording felt lazy, so I treated tool choice like any other behavior and wrote tests for it.

## 1. Write The Scenario

Each scenario is one realistic request plus the context the agent gets at session start.

I write them in a `jsonl` file, one scenario per line, and keep everything in `agent-tests/scenarios.jsonl`:

```text
{"id": "retry-limit",
 "ask": "What is the retry limit for webhook deliveries in staging?",
 "context": "docs-search is available",
 "expect_tool": "docs-search"}
```

The question must be answerable only through a tool. If the model can answer from memory, the test measures nothing, so I pick questions about internal values. The real retry limit, five attempts, lives only in our staging docs.

Most scenarios come from real questions I fumbled. I keep a note file where I paste questions that forced me to open the docs manually. Every question in that file becomes a scenario candidate, and five of the current ten started as notes from March.

## 2. Name The Expected Call

A scenario also names the call the agent should make.

For the retry question the expectation is `docs-search` with a query that mentions retries, and the check compares recorded calls against that expectation:

```text
expect: docs-search with query mentioning "retry"
fail:   zero tool calls before the final answer
```

The comparison runs against the session log that Claude Code writes anyway, so the setup needs no extra instrumentation. Ten scenarios took one evening to write, and most of that evening went into picking requests that felt like real work. Four scenarios expect the call, and six expect the agent to answer without one. A suite that always wants a call just trains the agent to call everything.

## 3. Grade The Result

The grading script reads the session log and checks two things: the expected call happened, and the final answer quotes the doc line. A run passes only when both hold, because calling the tool and then ignoring the result is the sneakiest regression I have seen.

The suite runs with one command:

```bash
uv run python grade_runs.py agent-tests/scenarios.jsonl --logs runs/
```

The April suite scored four passes out of ten, which matched my suspicion and gave the problem a number. After two prompt changes the same suite reached nine out of ten, and a nightly cron job keeps it there. The one failure it still reports is a scenario where the agent searches the docs and then answers from an older changelog entry.

A failed run leaves its log in `runs/`, so every failure is reproducible after the fact. I re-run failures once by hand before touching a prompt. Roughly one in ten failures is a flaky retrieval miss rather than a real regression.

## 4. Track The Cost

Each run costs money, and the suite runs nightly, so the bill needs a ceiling. My setup uses a small model as the test driver, at about $0.04 per scenario. The full suite of ten scenarios costs about $0.40 per night and roughly $12 per month.

Cost moves with document size, because the tool returns chunks and the driver re-reads them. Treat these numbers as an order of magnitude, and re-check them after every docs reorganization. The spread is real: my cheapest month came in at $9.20, and the most expensive hit $14.60 after I doubled the doc set.

The ceiling forced a useful decision. The driver uses the small model for nightly runs, and I escalate to the bigger model only when a scenario fails twice in a row.

## Caveats And Lessons

Two caveats keep the suite honest. Ten scenarios cover one evening of real work, so they drift from what users actually ask, and I add or retire one scenario most months. Grading also rewards the expected call, so a scenario can pass while the answer behind it stays wrong.

A deeper lesson came from the first April run: I had reviewed agent behavior by reading output and guessing, and guessing found nothing. A four-times-wrong answer survived three reviews because every sentence sounded right.

The suite now sits between my prompts and my users, and it turns a vague worry into a number. Tool choice is trainable behavior, and training needs a scoreboard. I'll write about the nightly cron setup in a future post. If you want to follow along, don't forget to subscribe.
