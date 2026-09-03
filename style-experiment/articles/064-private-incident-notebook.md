# Keeping an Incident Notebook That Survives the Urgency

At 02:17 on April 9, a fictional job scheduler stopped writing new task records. The queue depth climbed from 14 to 1,286 in 22 minutes, and my first notes ended up in three chat windows. It took another hour to reconstruct what had actually happened.

I invented the service, timeline, and measurements for a synthetic style exercise. I wanted to rehearse a notebook structure that works under pressure without describing a real outage.

In this post, I'll cover the notebook I now use:

- why chat and status pages made a poor record
- the five fields every entry gets
- how hypotheses and actions stay separated
- the follow-up review I run after the incident
- what still slows me down during recovery

## Chat made the record worse

The initial response was reasonable. I restarted the worker, checked the database, and paged the fictional on-call analyst. The actions were logged in a status page, but the important details were scattered.

One chat message said the queue stopped at 02:17. A different thread said the worker restart happened "around then". The database query log showed the last successful insert at 02:16:48. Those small gaps made the first timeline unreliable.

I eventually copied 47 messages into a document, and only 18 contained evidence. The rest were guesses, handoffs, or repeated status checks. The rule I took from that cleanup: write the operational record where evidence can be timestamped and read in order.

## Use five fields

I keep the notebook at `private/incidents/2026-04-09-scheduler.md`:

- `time`: the exact timestamp in UTC
- `symptom`: what I observed without interpretation
- `hypothesis`: what I think caused it
- `action`: what I did next
- `evidence`: the query, command, or log excerpt

I keep the fields on one line when the entry is short:

```text
02:22 | queue depth rising | worker consumed jobs without acks | restarted worker | queue-depth chart and worker log excerpt
```

For longer entries, I repeat the labels as list items. The format looks mechanical, and that's the advantage. During recovery, I don't have to decide how to write because I only have to fill in the next observation.

I write UTC because the scheduler, database, and alerting system used three different local time zones during the fictional incident. I add the local offset only in the follow-up summary, where humans need the bedtime context.

## Separate hypotheses from actions

I wrote the first notebook entries as ordinary paragraphs. One line often mixed a guess, a command, and a result, so I couldn't tell which action had changed system behavior.

The fields force me to preserve that distinction. If I restart a worker, that's an action even when the hypothesis says the worker was healthy. The next entry records whether the queue kept growing.

By 02:35, the notebook held six hypotheses, but only these two survived the next 20 minutes:

- the worker consumed jobs without acknowledging them
- the database had reached its write connection limit

The other guesses involved a deploy, an upstream producer, and a disk failure. Those ideas were reasonable, but the evidence never supported them. Leaving them in the notebook prevented me from inventing a clean story later.

## Record recovery in the same file

At 02:41, the query log showed the connection limit. A nightly maintenance job had left 96 open connections, while the scheduler pool expected 64. The scheduler retried inserts until its local buffer filled.

I added a temporary connection cap to `config/scheduler.yaml` and terminated 32 stale maintenance connections. Queue depth stopped rising at 02:47. By 03:03, the backlog was down to 206, and normal task completion resumed.

I kept writing entries during recovery because the incident wasn't over. I treat new behavior after mitigation as evidence, and I recorded one retry burst at 02:52 plus a stale alert that arrived afterward.

The final recovery record includes the rollback condition. If queue depth exceeded 500 again, I would disable the scheduler's enqueue endpoint and preserve incoming jobs in a file. That plan removed a decision from the most stressful moment.

## Review the notes later

The next morning, I spent 25 minutes on the follow-up. I read the notebook without editing it, then created a second section called `follow-up`. This is where interpretation belongs.

The follow-up answers the same four questions:

- what triggered the incident
- which mitigation worked
- which monitoring gap delayed detection
- what owner and date each fix needs

The trigger was the maintenance job, and the mitigation was the connection cap. Detection arrived eight minutes after the threshold crossed because the alert averaged queue depth over five minutes. The follow-up proposed a two-minute average with a sustained-load condition.

I also turned three notebook lines into permanent improvements. The worker now logs unacknowledged jobs with task IDs, and the connection dashboard separates active and stale connections. The maintenance job writes its expected duration to `status/maintenance.json`, which lets another check catch a hung run.

Each improvement got an owner and a review date in `private/incidents/actions.csv`. The scheduler incident had four actions, and I closed two within a week. The others stayed open until the next maintenance window.

## Remaining friction

The biggest remaining problem is discipline. During the first 10 minutes, I still want to fix the system before documenting it. A second person helps, but this exercise assumes I'm alone, so I set a recurring 5-minute reminder.

Some evidence doesn't fit neatly. A screenshot can show both a symptom and a hypothesis, so I save it first and write separate notebook references to the same image. Slight duplication is preferable to losing the observation.

The useful change separated urgency from explanation. I used the notebook to record what happened while I could still see it, and I used the follow-up to turn those observations into decisions. If I continue the exercise, I'll design the queue alert that should have caught this incident sooner. Subscribe if you want that follow-up.
