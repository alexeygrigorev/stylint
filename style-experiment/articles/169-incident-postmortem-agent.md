# Using an Agent to Draft an Incident Postmortem

This synthetic style exercise invents the incident, logs, and agent output. At 02:14 on June 18, 2026, the fictional billing API for a project called Meterhaus returned HTTP 500 for 19 minutes. I was asleep, the on-call engineer restarted one worker, and the dashboard recovered before I saw the page.

The next morning, I had 1,900 log lines, four Slack threads, two Grafana screenshots, and a deploy that looked suspicious. I wanted a factual timeline, but I didn't want an agent to invent a cause.

In this post, I'll share:

- how I prepared the incident material
- how the agent extracted a timeline
- how it linked evidence to each statement
- where human review changed the draft
- what the final postmortem changed

## Prepare the Evidence

My first instinct was to paste logs into Claude Code and ask for a postmortem. That produced fluent prose and two unsupported claims. It said configuration drift caused the failure, but the material contained no configuration diff.

So I narrowed the job. The agent could organize and quote evidence; it couldn't name the root cause. I also removed customer names, API keys, and request bodies before giving it files.

The evidence bundle had four parts:

- `logs.jsonl`, with 1,912 lines between 02:00 and 02:45
- `deploys.csv`, with 14 deployments from June 16 to June 18
- `metrics.csv`, with one-second request counts and latency
- `slack-thread.md`, with on-call messages through 03:10

Each file stayed under 2 MB, and timestamps used UTC. I added a short note defining the incident window and the service owner. That note became more useful than the prompt engineering.

## Extract the Timeline

The agent prompt asked for one row per event, with a timestamp, source file, line number, and verbatim evidence. It could group repeated messages only if it preserved the first and last occurrence.

The first draft had 47 events. Many were repeated health checks or retries. I asked it to mark those as `noise` instead of deleting them, so I could check what it had excluded. The second draft had 23 events, plus a noise appendix.

Here is the format it used:

```text
02:14:06 | logs.jsonl:482 | first 500 in window
02:15:31 | metrics.csv:95 | error rate reaches 41%
02:24:50 | slack-thread.md:31 | on-call restarts worker-2
02:33:12 | logs.jsonl:1508 | first successful charge after restart
```

This moved the work forward because every claim had a place to be checked. The agent also flagged a gap between 02:26 and 02:31 where neither logs nor metrics explained the partial recovery.

That gap forced the useful question. The on-call engineer remembered a second restart, and the missing Slack message provided the 02:31 timestamp.

## Link Evidence to Claims

After the timeline, I allowed one summary paragraph per phase. Each sentence had to end with evidence IDs in square brackets. The IDs pointed back to the timeline rows, not directly to log lines.

The phases were clear:

- 02:14 to 02:16, errors spread across three workers
- 02:17 to 02:24, worker memory reaches the 1.5 GB limit
- 02:24 to 02:33, restart reduces the error rate
- 02:33 onward, traffic returns to normal

The agent noticed that worker-4 emitted an out-of-memory message 90 seconds before the first HTTP 500. That was a good observation. It did not prove causation, so the summary called it a candidate event.

It also connected the deploy list to behavior. Deployment 431 changed a batch size from 50 to 120. Worker memory rose after that time, but the deployment happened 41 minutes before the incident. The draft marked it as context, not cause.

This distinction was the biggest quality improvement. The agent could say what happened near the failure without turning proximity into explanation.

## Review as Humans

I read the draft with the on-call engineer and the developer who owned the billing worker. We spent 45 minutes on 23 timeline rows. The agent's structure stayed intact, but four facts changed.

First, the 41% error-rate line used a Prometheus query that included health checks. The corrected peak was 33%. Second, the restart command used a different worker name than the log suggested. Third, the 02:31 restart was manual, while the first restart came from systemd. Fourth, we already had a memory alert; it waited five minutes and fired at 02:19.

We rejected the phrase "rapid recovery" because some charges entered a retry queue and completed 11 minutes late. The customer-facing note later said "delayed completion" instead.

Human review also added impact numbers. There were 638 failed requests and 212 delayed charges. The finance team confirmed that no charge was lost, which mattered more than the error rate.

## Change the System

The final postmortem had five action items:

- lower the worker memory alert from 90% to 80%
- alert on three consecutive payment-service timeouts
- add a load test for a batch size of 120
- restore the batch size to 50 until that test passes
- require a second restart timestamp in the incident channel

The load test reproduced the failure after 7 minutes. It showed that worker memory climbed to 1.68 GB when 120 invoices arrived together. We kept batch size at 50 and scheduled a queue-depth limit for the next sprint.

The postmortem took 4 hours and 20 minutes. Extracting the timeline took the agent about 6 minutes, but checking and correcting its work took most of the session.

## What I Learned

An agent is useful for turning scattered evidence into a checkable draft. It's a poor root-cause oracle. Giving it a narrow job produced facts I could defend and gaps I could fill.

The evidence IDs also changed the conversation. Instead of arguing about memory, we inspected row 14 and corrected one query.

I plan to write more about incident evidence bundles in a future article. Subscribe if you want the follow-up.
