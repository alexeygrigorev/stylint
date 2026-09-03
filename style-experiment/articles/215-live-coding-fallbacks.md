# Preparing Fallbacks for a Live Coding Session

I wrote this synthetic style exercise as a how-to guide. The session, dates and numbers are fictional. On 12 June 2026 I gave a 90-minute live coding session about background tasks in FastAPI at a local meetup with about 40 attendees. The venue wifi had dropped twice during the afternoon rehearsal, and that decided my evening.

Live coding fails in boring ways. A dependency breaks, the projector dies, or a typo hides from you while 40 people wait. Fallbacks don't remove those failures. They shrink each one to about a minute of switching.

The whole prep took one evening, about three hours, and I have reused the same plan for two sessions since.

In this post, I'll share:

- how I freeze a backup repo before the session
- where I put snapshots during the live run
- which steps I script in advance
- how the recovery rules work under pressure
- what changed after the plan ran for real

## 1. Freeze A Backup Repo

Build a second copy of the demo repository before you leave for the venue, and make it independent of your laptop and the venue network. I pushed the finished demo to a fresh GitHub repo called `fastapi-backgrounds-backup` and cloned it to a USB stick.

Two commands cover the freeze:

```bash
git push backup main --tags
git archive main -o demo-final.zip
```

The stick covers the case where the venue blocks GitHub entirely. The backup repo holds the completed state, so the worst case becomes a walkthrough of finished code instead of an improvisation. Attendees lose the live typing, and they keep the working example and the explanation. I also exported a PDF of the final slides to the same stick, because the laptop is only one of the parts that can die.

## 2. Take Snapshots At Checkpoints

Pick the checkpoints while you plan the session, and tag the repo at each one during the live run.

My June session had four checkpoints:

- after project setup and the first endpoint
- after the slow task moves to the background
- after the progress endpoint works
- after the retry logic and the final cleanup

Tagging takes ten seconds between steps:

```bash
git tag checkpoint-2 -m "background task running"
```

Each tag marks a working state you can jump to. When a live step breaks, you reset to the last tag instead of debugging in front of the room. The audience sees a short pause, and the demo continues from code that runs. Four checkpoints also pace the session well, because each one doubles as a natural stopping point for questions.

## 3. Script The Slow Steps

Every step over two minutes gets a script in `scripts/`. Installation, database seeding, and dependency downloads are boring to watch and risky to type. The June session had three scripted steps.

The setup script builds the environment and seeds the database:

```bash
uv sync && uv run python scripts/seed_db.py
```

With the script, that step took 25 seconds instead of three minutes of typing. It also removed my most common live error, installing a package into the wrong environment while talking. The scripted steps double as documentation, because attendees read them later in the repo. The scripts live in the same repo, so a checkout of any tag brings the matching scripts with it.

## 4. Plan The Recovery Path

Write the recovery rules before the session, while you're calm, and keep them on one printed page.

My June page had three rules:

- wifi dead for over two minutes: switch to the phone hotspot
- a step broken after the tag reset: open the backup repo and walk through finished code
- laptop or projector dead: present the README and the trace log from the stick

Three rules fit on half a page, and rehearsing them matters more than writing them. I rehearsed the hotspot swap once at home, which took four minutes and produced two fixes to the runbook.

## 5. Caveats From The June Run

The hotspot rule fired at minute 31, and the switch cost about 70 seconds of talk time. Nobody mentioned the outage in the feedback forms, and the plan earned its evening.

The first caveat involves tags. Tags don't help if you forget to create them, and I lost checkpoint 3 exactly that way. The rule I took from it: create the tag before you explain the step.

The second caveat involves drift. I updated the demo two days before the session and forgot to push, so the backup held Tuesday's code. The final walkthrough showed an old import line, and a sharp attendee spotted it. Push the backup again on the morning of the session.

## 6. After One Real Run And Two More

The June session ended with working code, a recovered network, and 40 people who saw about 70 seconds of silence. The prep took three hours, and most of it went into scripts I would have typed live anyway. The two later sessions needed no rule beyond the printed page. That tells me the plan is small enough to survive a real room.

The plan still has one hole. It does nothing for a dead laptop and a dead projector at the same time. That case would need a printed handout, and I haven't made one.

I'll write about that printed handout in a future post. If you want to follow along, don't forget to subscribe.
