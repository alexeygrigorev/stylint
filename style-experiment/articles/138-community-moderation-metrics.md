# Measuring Moderation Work Without Ranking People

I moderate Repair Club, a fictional community with 24,000 members. I wrote this
synthetic style exercise with fictional counts, dates, and moderation rules. In
March 2026, the two moderators answered 412 flagged messages and closed 68
threads, but our dashboard could say only that both accounts were active.

That number wasn't useful because it didn't show response time, outcomes,
repeated abuse, or the hours swallowed by one argument. I wanted enough
measurement to plan work, without turning moderation into a leaderboard.

In this post, I'll share:

- what I chose to count,
- how I recorded outcomes,
- how I measured response time,
- how I combined the numbers,
- what the dashboard still can't see.

## Decide what to count

My first attempt used one metric: messages acted on per moderator. I built it in
20 minutes, and I removed it two weeks later. It rewarded easy cases and made
the moderator who handled appeals look slower, even though appeals took 35
minutes on average.

So I listed the decisions the numbers had to support:

- schedule moderator coverage,
- find rule text that causes repeated arguments,
- see when a case needs a second person,
- notice a rising class of abuse,
- protect moderators from invisible workload.

Those decisions led to five families of measurements. I measure volume and
response time, and I also measure outcomes, recurrence, and workload. None of
them describes a person as good or bad, and each one describes part of the queue.

I also wrote the measurement policy in `moderation/metrics.md`. It says the
dashboard is for scheduling and process changes. Individual metrics stay
private to the moderator who handled the case.

## Record outcomes

Volume only makes sense when every action has an outcome, so I expanded the
moderation form. It now records a warning, a removed message, a locked thread,
or a member suspension. It can also record no action. A case can have more than
one outcome, and the form stores those outcomes as a list.

The form also captures the rule that applied:

```text
rule: harassment
action: message removed, warning issued
second_reviewer: none
follow_up: 2026-04-18
```

In April, that single field settled a long debate. The team thought sales spam
was our largest category, but it was 19% of 486 cases. "Off-topic promotion" was
31%, and most of those cases needed a redirect rather than a punishment. We
rewrote two rules and added a thread for self-promotion on Fridays.

Outcomes also exposed a training gap. Ten percent of harassment cases had no
recorded second reviewer, even though our policy requires one. The dashboard
didn't blame anyone, but it showed that the form allowed that state, so we made
second review required for that rule.

## Measure response time

I measure two clocks for flagged messages. First response starts when a member
flags a message and ends when a moderator records any action. Resolution starts
at that same moment and ends when the case leaves every follow-up queue.

First response tells us whether the community sees attention, and resolution
tells us whether the workload actually clears. Those two numbers can move in
opposite directions, so I stopped averaging them into one score.

In May, median first response was 34 minutes and median resolution was 11 hours.
The 90th percentile told a more useful story: first response reached 5 hours,
and 27 cases stayed open for more than three days. Every one of those cases
required a second reviewer or a member appeal.

I use percentiles, never an average, when reporting these numbers to the team.
One three-day appeal case is exactly the information a median can hide.

## Combine the numbers

The weekly dashboard has four panels:

- cases by rule and outcome,
- first response and resolution percentiles,
- recurrence within 30 days,
- open cases and estimated hours.

A moderator estimates the hours in the estimated-hours field, in 15-minute
increments. I keep the estimate rough on purpose. In June, appeal cases were 8%
of volume and 41% of the estimated workload. That proportion, rather than any
individual score, justified moving appeal review to a shared rota.

Recurrence showed another process problem. Members who received a warning
appeared again within 30 days in 23% of cases. For removed spam accounts, the
number was 4%. We stopped treating both actions as equivalent follow-up and
added a check-in reminder for first warnings.

The panels don't produce a moderator score. They produce questions such as "why
did copyright cases rise from 6 to 19" or "which rule needs a clearer example".

## Limits of the metrics

The dashboard omits context because it can't see a private apology or a member
deleting their own message. It also can't see the emotional cost of reading a
harassment thread.
We handle those with a monthly 30-minute review and a rule that any moderator
can decline an appeal round without explaining themselves in the channel.

It also omits the quiet work that prevents reports. I fixed rules in place,
added automatic warnings, and improved thread titles. Those changes reduce cases
before they enter the queue.
In July, we added examples to the promotion rule and saw cases fall from 44 to
31 the next month. The dashboard records the drop, but it can't prove which edit
caused it.

## Closing note

Good moderation metrics describe the work, and people should stay outside the
ranking. Volume without outcomes hides difficulty. Response time without
workload hides appeals. The dashboard is useful because it keeps those views
separate.

The rule I took from the experiment: measure the queue first, and let a person
interpret the moderator. I'll write more about the appeal rota in another
article. Subscribe to stay updated.
