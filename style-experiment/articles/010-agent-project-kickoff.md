# The Project Kickoff Template I Give a Coding Agent

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. In March I asked a coding agent to add rate limiting to a FastAPI billing service. The first diff touched 14 files for a change that needed three.

That review took me 45 minutes, and most of that time went into reconstructing choices the agent had made on its own. In April I started writing a one-page kickoff note before every agent task above half an hour. My average review time dropped by half within a month.

In this post, I'll share:

- why vague requests cost so much review time
- how I state the outcome and the done check
- how I list constraints and non-goals
- how I define interfaces and boundaries
- how I describe data, fixtures and review gates
- what changed in my review time

## Vague Requests And Their Cost

My March request was a single sentence. I wrote "add rate limiting to the billing API" and named two endpoints from memory.

The agent chose a Redis-backed limiter, added a new dependency, rewrote the Docker Compose file and changed the response format on three routes. Each choice looked defensible alone, and together they formed a migration I had never requested.

The rule I took from March is simple. The agent fills each gap in the brief with its own defaults, so I close the gaps before I start the run.

## 1. State The Outcome And The Done Check

I open the kickoff file with one sentence that names the change and the place. For the billing service I wrote that the agent adds per-key rate limiting to two routes in `app/main.py`.

Next I write the done check, and I phrase it so I can verify it in under two minutes. A done check names the command I run and the output I expect to see.

I keep the skeleton fixed so I can fill it in within five minutes:

```text
Outcome:
Done check:
Constraints:
Interfaces:
Data and fixtures:
Review gates:
```

The March done check listed three verifiable outcomes:

- `pytest` stays green
- a burst of 120 requests per minute earns a 429 response
- no response body gains or loses a field

Those three lines would have blocked the entire bad diff.

## 2. List Constraints And Non-Goals

Constraints are the lines the agent must respect, and non-goals name the attractive extras I don't want yet. I write both before I describe any implementation, because defaults creep in earliest at the edges.

The March note listed four hard constraints:

- no new dependencies beyond the Redis client already in use
- no changes to response bodies on any route
- the diff stays under five files
- the limiter reads its settings from environment variables

It also named two non-goals:

- no admin dashboard for viewing blocked keys
- no per-plan limits, only one global threshold

That global threshold was 100 requests per minute per API key. The agent hit it exactly because the number sat in the note rather than in my head.

## 3. Define Interfaces And Boundaries

In this section I name the files and functions the agent may edit and the ones it must leave alone. I list paths exactly as they appear in the repo, since a vague area description invites a wide diff.

For the billing service the editable area covered two files:

- `app/limits.py` for the limiter logic
- `app/main.py` for registering the routes

It marked `app/billing.py` as read-only, because charge calculations live there and a rate limiter has no reason to touch them. It also required that response bodies stay byte-identical apart from the new 429 status code.

I verify the boundary with one command after the run:

```bash
pytest app/tests/test_limits.py -q
```

That suite contains 11 tests, and three of them assert the untouched billing totals directly. When those three pass, I know the boundary held.

## 4. Describe Data And Fixtures

Agents invent test data when the note says nothing, and invented data hides broken assumptions. I point the agent at the existing fixtures and state the row counts it should expect.

The billing service seeds its database from one script:

```text
tests/fixtures/seed.py
```

I keep that path in the note along with the counts it produces. The seed creates three API keys, 40 invoices and six months of usage rows for a single tenant.

The note also names the services the fixtures need:

- Postgres 15 with the `billing_test` database
- Redis 7 with an empty default database
- the Compose profile called `test`

I start that profile before the run and stop it after the review. The agent never manages containers, since a stuck container once ate an afternoon of debugging.

## 5. Set Review Gates

Review gates are the checks I run before I merge, written down before the agent starts. Advance agreement stops me from waving through a large diff late in the evening.

The March note set five gates:

- the diff touches at most five files
- the full test suite passes with no skipped tests
- the demo script output appears in the run summary
- no dependency file changes without a named reason
- schema changes arrive with a migration note

I read the diff myself before anything merges, and the agent never pushes to the main branch. That division stayed fixed across nine tasks, and it caught two oversized diffs early.

One gate failed usefully in May. The agent changed a timestamp column without a migration note, and the gate flagged it. I added a time-handling line to the skeleton the same day.

## Changes In Review Time

Across nine kickoff-driven tasks from April to June, my average review time fell from 45 minutes to 12 minutes. The diffs shrank from a median of nine files to a median of three, and two tasks needed zero rework.

The miss rate fell alongside review time, since four of six March tasks without the note needed a second agent run. With the note, only one of nine needed a correction, and that correction was the timestamp case above.

The template works because it moves my decisions earlier rather than adding more of them. I spend about 20 minutes writing the note, and I get that time back in the first review.

I'll share the rate-limiting follow-up after one more production cycle. If you want to follow along, don't forget to subscribe.
