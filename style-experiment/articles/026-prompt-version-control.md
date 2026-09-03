# Versioning Prompts Like Small Functions

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. In January I edited a support-reply prompt directly in a chat window, and two weeks later nobody could reconstruct the version that had worked best.

The working version had answered 40 tickets with a 90 percent approval rate. The replacement answered the same tickets with new mistakes, and I had no diff, no backup and no way back.

In this post, I'll share:

- how I name prompts and store them
- how I describe the inputs a prompt accepts
- how I store examples inside the prompt file
- how I build a regression set around it
- how I review prompt changes like code changes
- what versioning changed in my debugging time

## Lost Prompts And Their Cost

The January prompt drafted replies for refund requests in a small SaaS helpdesk. I had tuned it across three evenings against 25 real tickets, and the approval rate had climbed from 70 to 90 percent.

Then I rewrote two sentences from memory during a live incident. The new wording sounded clearer to me, and it dropped the instruction that forced a ticket-ID lookup before drafting.

The rule I took from January is simple. I keep every production prompt in git with a name, a version and a test, exactly as I keep utility functions.

## 1. Give The Prompt A Name And A Home

I store each prompt as a text file under `prompts/` with a short stable name. The refund prompt lives at `prompts/refund_reply_v3.txt`, and the name never changes meaning after release.

The file opens with four header lines:

```text
name: refund_reply
version: 3
owner: support-bot
updated: 2026-01-28
```

I read those headers before I edit anything, and I bump the version on every change. The old file stays in history, so I can check out any version in seconds.

Names stay short and concrete across the folder. I now keep nine prompt files, and each name maps to exactly one task the bot performs.

## 2. Describe The Inputs It Accepts

Below the headers I list the inputs the prompt expects, with one line per field. The refund prompt takes three fields, and each field states its format plainly.

The March revision documented its inputs this way:

- `ticket_id`, a six-digit number from the helpdesk
- `order_total`, a decimal amount in USD
- `customer_tier`, one of `basic`, `plus` or `team`

I validate those fields in code before the prompt ever sees them. A small Python function checks types and ranges, and it rejects bad input with a logged error.

That validator caught 17 malformed calls in February. Each one would have produced a confident reply grounded in missing data, and each one now fails loudly instead.

## 3. Anchor The Prompt With Examples

Abstract instructions drift in meaning, so I anchor each prompt with two worked examples. Each example shows the exact input fields and the exact reply I want for them.

The refund file holds a short example pair:

```text
ticket_id: 481516
order_total: 84.00
customer_tier: plus
reply: approved, 5-day window, case #481516
```

I chose examples that cover the common case and one partial-refund case. The second example involves a partial refund, since partial amounts caused three of the January mistakes.

When I change the prompt, I run both examples first by hand. If either output drifts from the stored reply, I stop and decide whether the drift is an improvement.

## 4. Build A Regression Set Around It

Two examples guard the intent, and a regression set guards the behavior. I keep 30 real tickets with approved replies under `prompts/regression/refund_reply/`.

The runner script scores a prompt version against all 30 cases:

```bash
uv run python scripts/score_prompt.py --prompt refund_reply --version 4
```

That run takes about four minutes against a local model endpoint. It reports approvals, mismatches and the three worst diffs with full text.

Version 4 scored 27 of 30 in March, and the three misses shared one trait. Each involved a ticket older than 90 days, where the refund window rule differs, so I added a dedicated example for aged tickets.

## 5. Review Changes Like Code Changes

No prompt version goes live without a pull request. The request shows the diff, the two stored examples and the regression score, and a teammate approves before merge.

My review checklist fits on five lines:

- the version header increased by exactly one
- the stored examples still produce the stored replies
- the regression score didn't drop
- the diff touches one prompt file only
- the change note names the ticket that motivated it

That last line matters most, because it connects each edit to a real failure. In April a reviewer caught a change with no motivating ticket, and we reverted it before release.

I deploy prompts with the same pipeline that ships the bot. The file rides inside the Docker image, and a rollback means redeploying the previous image tag.

## Fewer Surprises Per Release

Since January I have shipped 14 prompt versions across nine files. Eleven improved the regression score, two held it steady, and one dropped it by a single case before a same-day revert.

Debugging time fell because every failure now starts from a version number. When support flags a bad reply, I read the logged version, check out that file, and reproduce the case locally within minutes.

The version history also settled arguments about wording. When two wordings compete, I run both against the 30 cases and keep the higher score, and the loser stays in history for reference.

I'll cover the scoring script internals in a future post. If you want to follow along, don't forget to subscribe.
