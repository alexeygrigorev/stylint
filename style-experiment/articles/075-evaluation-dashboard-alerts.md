# Adding Alerts to an Evaluation Dashboard

For six weeks, our fictional translation team watched an evaluation dashboard
that told us nothing until someone opened it. I invented the team, scores,
incidents, and thresholds for this synthetic style exercise. The dashboard
updated every morning at 07:00, and the first quality drop sat there for three
days before anyone noticed.

The system translated short customer-support replies and generated a daily
score against 180 labeled cases. Scores moved by a few tenths of a point all
the time, so checking every wiggle was useless.

We needed alerts that represented actionable changes.

In this post, I'll share five parts of our alerting setup:

- the four metrics we chose for alerts,
- how we set thresholds from past scores,
- the false-alarm budget,
- ownership and runbooks,
- the first month of operation.

## Choose metrics that require action

The dashboard already showed 19 charts. We could alert on all of them, but an
alert should map to a decision. We reduced the first version to four metrics.

Each metric has a direct consequence:

- weighted quality score: pause automatic suggestions and investigate,
- retrieval hit rate: look at the index and recent source changes,
- latency p95: check infrastructure and model capacity,
- evaluation coverage: repair the scheduled evaluation job.

We weighted quality by adequacy, terminology, and safety, with safety weighted
heaviest. Retrieval hit rate measured whether the expected reference passage
appeared in the top five results. Latency p95 came from the production service.
Coverage measured the share of expected cases that produced a score.

We deliberately kept a fifth chart for token cost without alerts. Cost trends
help with planning, but the team had no immediate action for a 3% change. An
alert without an owner or a next step only trained us to ignore it.

The first metric list produced a useful argument. One engineer wanted alerting
on every model score, while another wanted only safety failures. We settled on
the weighted score plus a separate safety-failure count because those two had
different runbooks.

## Set thresholds from evidence

We exported 60 days of historical scores before choosing thresholds. The mean
weighted score was 86.4, with a standard deviation of 1.7 points. Daily changes
ranged from -3.2 to +2.6 points. That distribution told us a fixed lower bound
would need context.

We used two alert types:

```text
score below 82.0 for 1 day
score below 84.5 for 3 consecutive days
```

The first catches a sharp drop, while the second catches a slow decline that
might otherwise become the new normal. We chose the numbers by marking every
historical day as alert or no alert, then calculating what a responder would
have done. This gave us 7 triggered weeks out of 60.

For retrieval hit rate, the threshold was simpler. The 60-day median was 91%,
so we set a warning at 85% for one day and a page at 78%. Latency p95 normally
ran 1.4 seconds, so we set a warning at 2.5 seconds for 15 minutes and a page
at 4.0 seconds.

Coverage got the strictest rule: below 95% for one scheduled run. A partial
evaluation can make other metrics look safe. On May 12, for example, only 61
of 180 cases ran, and the visible average happened to be high.

## Budget for false alarms

Every alert costs attention.

Before enabling pages, we wrote down this budget:

- no more than two non-actionable pages per week,
- no more than one page outside working hours,
- an exception only when safety failed or coverage dropped.

We classified each alert after the fact with these labels:

```text
actionable: a responder changed code, config, or capacity
investigate: a responder looked and found no change to make
duplicate: another alert already covered the incident
noise: threshold or data problem
```

We stored the classification next to the alert in a small Postgres table (our
relational database). It included the responder, incident channel, duration,
and one sentence describing the outcome. The review meeting took 20 minutes
each Friday.

During the first two weeks, we received 11 warnings and 3 pages. Seven were
actionable, and two were duplicates from latency and coverage during the same
incident. Five were noise caused by an incomplete data upload. We added a
freshness check before evaluation and reduced the noise class to zero in week
3.

The false-alarm budget changed one threshold. The initial latency warning at
2.1 seconds fired during every Friday batch job. Moving it to 2.5 seconds
kept the page threshold unchanged and made the warning useful again.

## Give every alert an owner and a first action

An alert without a runbook becomes a puzzle for whoever wakes up first. For
each alert, we wrote one sentence naming the service owner and the first five
minutes of work.

The quality-score runbook says:

```text
Owner: translation platform engineer on rotation.
First actions:
1. Confirm evaluation coverage is at least 95%.
2. Compare model version, prompt version, and index revision.
3. Look at the ten largest score drops.
4. Pause suggestions if safety failures exceed 2 cases.
```

The latency runbook asks for the request stage first. That stage can be queue
time, retrieval, model, or rendering. The retrieval runbook asks for the index
build time and the last source update. Each runbook ends with the command or
dashboard link needed for that step.

We also defined escalation, and a warning goes to the team channel, while a page
goes to the on-call engineer. If the owner can't identify a cause in 30
minutes, a second engineer joins. If safety failures exceed 5 cases in a day,
automatic suggestions stop until a human reviews the sample.

Those rules weren't abstract, and on June 3, safety failures rose from 0 to 3. The
alert arrived at 09:12, and the on-call engineer paused suggestions by 09:19.
She found a terminology dictionary change and restored service after a review
at 12:40.

## Results From One Month

After the first noisy two weeks, the month followed a useful cadence. We
received 9 warnings and 4 pages. Six pages were actionable, including the
safety incident and two coverage failures caused by a broken data file.

The median time to acknowledge a page was 6 minutes, and the median time to
identification was 34 minutes. Two latency pages overlapped a known capacity
change, so we added a maintenance window to suppress that expected load.

The most useful change was small. Every alert now includes the evaluation run
ID, model revision, data revision, and the previous day's score. A responder can
see the relevant versions without opening four tabs.

We still review thresholds monthly. A metric that never fires may be wrong, and
a metric that always fires may be describing normal work. The dashboard
continues to show trends, while the alerts only mark moments that need a
decision.

Our current rule is plain. Every alert should name an owner, an action, and a
stop condition. I plan to write more about the evaluation cases behind these
metrics in a future article. Subscribe to stay updated.
