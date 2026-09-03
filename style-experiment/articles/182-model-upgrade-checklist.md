# The Checklist I Use Before Switching to a New Model

This synthetic style exercise follows a fictional migration with invented numbers and dates. Last March I moved a support triage script from one chat model to another newer release. No detail here describes real events or real customer data.

The script routes 340 incoming messages per day into four queues with a single model call. I had tuned the prompt for six weeks and the error rate sat at 4.1 percent.

The new release promised lower prices and faster answers in the changelog. I wanted those gains without losing the behavior I had already verified.

In this post, I'll share:

- how I built a 40-case check set
- how I compare price and latency
- how I catch regressions before release
- how I plan rollback in advance
- what the switch cost in practice

## Small Check Set Comes First

I started with 40 real messages pulled from February support logs with names removed. Each record keeps an identifier, the input text, the expected queue and the origin note.

I keep the set in `cases.jsonl` and I review it in a plain text editor. SwitchLog, a small markdown file that records model versions and scores, sits beside the data.

I chose JSONL because I know it well enough to debug at midnight without extra tools. The downside is manual editing, and that trade has stayed manageable for 40 rows.

I label each case myself and I add two tricky rewrites for every queue. That manual pass took 52 minutes and it forced me to read every message twice.

The four queues cover distinct intents I saw in February:

- billing questions about charges and refunds
- bug reports with steps and screenshots
- account access and password resets
- spam and vendor pitches to ignore

I kept ten examples per queue so the set stays balanced across the day.

One record looks like this inside the plain text file:

```json
{
  "id": "billing-012",
  "input": "Charged twice for order 2043 in February.",
  "expected": "billing",
  "origin": "support log"
}
```

I don't trust memory so I reread that file before every single run.

## Price And Latency In Practice

I ran the same 40 cases on the new model with a small Python script. The script logs prompt tokens, completion tokens and wall-clock time for every single call.

The old model averaged 1,840 prompt tokens and 320 completion tokens per message. At list prices that averaged $0.0041 per message and 1.9 seconds of latency.

The new model used fewer tokens and answered in 1.1 seconds on the same set. Its price came to $0.0018 per message, which cuts the daily bill roughly in half.

I chose the cheaper run because I pay the bill from a small consulting budget. The downside is higher variance, and I accepted an extra review pass each morning.

The daily totals show the gap clearly for 340 messages:

- old model costs about $1.39 per day
- new model costs about $0.61 per day
- median latency drops from 1.9 to 1.1 seconds

I don't chase the lowest price when latency stays above two seconds for users.

I measure latency with one short command before every comparison:

```bash
uv run python scripts/measure_latency.py --cases eval/cases.jsonl --runs 3
```

That command prints medians so a single slow call doesn't hide the trend.

## Regression Runs Before Release

I ran the full set on both models and I compared every queue assignment. The old prompt scored 38 of 40 while the new model scored 36 of 40.

Both misses came from refund requests written like billing questions with order numbers. I had missed that overlap in manual review, which turned out to be a mistake.

The rule I took from it: regressions need paired runs before any model switch. I keep both outputs in Git so I can diff decisions without rerunning paid calls.

I chose Git because I already use it for prompts and it shows line diffs fast. The downside is large diff files, and I prune old runs after two weeks.

The two misses shared obvious traits in the February sample:

- refund wording buried after billing details
- order number placed before the request
- polite apology that confuses the classifier

I added four similar messages to the set and the gap stayed visible.

I diff the two runs with one repeatable command each evening:

```bash
uv run python scripts/diff_runs.py --old runs/old.jsonl --new runs/new.jsonl
```

That output lists mismatches first so I see damage without scrolling far.

## Rollback Plan Before Switch

I wrote the rollback steps before changing the production config in March. The app reads the model name from an env var and it defaults to the old release.

I recorded the old commit tag and I kept its prompt file beside the new one. A small dual run sends five percent of traffic to the new model for one hour.

I watch error counts and median latency during that hour with Grafana dashboards. I skipped the drill once on a Friday deploy, which turned out to be a mistake.

The rule I took from it: rollback stays ready before any production switch. I chose env vars because I can flip them without a redeploy in seconds.

Stale vars cause the main downside, and I document the current value in the README.

The rollback file lists four actions I can run from my laptop:

- flip env var back to old release
- restore prompt file from recorded tag
- rerun 40-case check set for sanity
- post short note in team channel

I rehearsed those steps in staging and the full flip took 94 seconds. The staging run felt calm - the checklist removed guesswork under time pressure.

## Lessons From This Model Switch

The switch saved about $0.78 per day and it cut median latency by 0.8 seconds. Those gains matter less than the paired runs that caught two real misses.

I don't switch models for novelty now and I keep the old prompt for two weeks. That waiting period caught one late tokenizer edge case in April logs.

I chose caution because I maintain the triage queue alone without on-call help. The downside is slower adoption, and that delay has saved two weekend fixes.

I'll keep the 40-case set and I'll extend it with fresh misses each month. I'll write about the next switch after one more billing cycle. If you want to follow along, don't forget to subscribe.
