# Preparing for Demo Failures in a Live Course

During a live session in March, a fictional homework checker called `taskgrade` refused to start for 11 students in the same cohort. The API was healthy, the database was reachable and the demo repository hadn't changed. The problem turned out to be a stale Python virtual environment on three university lab machines.

I wrote this piece as a synthetic style exercise. Every course, student count, tool, failure and timing detail is fictional.

That evening I recovered the session, but I spent too long improvising. Since then I've treated the demo as a system that needs rehearsals, snapshots, fallbacks and a recovery script.

In this post, I'll walk through the preparation checklist:

- rehearse with the real environment
- create snapshots before each session
- prepare fallback examples
- write a recovery script for common failures
- keep students informed during downtime
- review the incident afterwards

## 1. Rehearse With the Real Environment

A clean laptop hides the failures students actually have. I now rehearse on the same three surfaces used in the fictional course: Ubuntu 24.04, macOS 15, and a lab image based on Ubuntu 22.04.

Each rehearsal follows the student setup steps from scratch. I clone the repository, install dependencies, run `taskgrade --check` and submit one sample assignment. I use the campus network on one run and a mobile hotspot on another.

The March incident came from a lab image with Python 3.10. The course required 3.12, and `uv` couldn't find a compatible interpreter on that image. A rehearsal two days earlier would have exposed the error before 74 students saw it.

After the incident, I added a preflight command:

```bash
uv run taskgrade preflight --course "data-pipelines-2026"
```

The command checks Python, package versions, disk space, API reachability and the sample submission. It prints one green line for each check and stops at the first problem. Students run it before every live session.

## 2. Create Snapshots Before Each Session

Snapshots make recovery boring because they remove guesswork. Before each live session, I create a tagged container image for the teaching environment and an archive of the sample repository.

The image contains the course dependencies, the database seed and the first working version of each demo. The archive contains solution files, sample data and the output the students should see. Both live in `backups/course-data-pipelines`.

For database-backed examples, I snapshot PostgreSQL too.

In our rehearsal workflow this looks like:

```bash
pg_dump --format=custom \
  --file=backups/course-data-pipelines/demo-2026-03-24.dump \
  course_demo
```

Then I restore that dump into a disposable database and run a query count. If the counts match the rehearsal log, I know the snapshot works. The whole check takes about four minutes.

## 3. Prepare Fallback Examples

Some failures don't affect the code, but they affect the network or the platform. For those cases, I keep three fallback examples that work offline.

The fallbacks cover different depths:

- a static copy of expected output for the current demo
- a local CSV example with the same schema and edge cases
- a recorded 90-second clip of the database step

The static copy lets me discuss the result while I fix the live example. The CSV example keeps the lesson usable if the database can't start. The recording is a last resort for a failure that would consume too much class time.

Each fallback has a one-line note explaining when to switch. Without that note, I once spent nine minutes debugging while students watched. The recorded clip would have preserved the lesson and given me time to investigate after class.

## 4. Write a Recovery Script for Common Failures

The recovery script has to be simple enough to run under pressure.

Ours lives in `scripts/recover-demo.sh` and supports five commands:

- reset the demo database from the latest dump
- restore the solution files for the current step
- clear generated caches and temporary uploads
- run the preflight checks again
- print the fallback command and the current lesson step

The script writes a log to `logs/recovery.txt` and prints the elapsed time. It never deletes student repositories or the database dump. Those are the two assets I can't reproduce during a session.

We rehearse the script once a month. During the April rehearsal, the reset command took 22 seconds and the cache command took 3 seconds. That's fast enough to use while answering a student question.

## 5. Tell Students What's Happening

Silence makes a technical failure feel worse. I use a simple public message: what stopped, what I'm trying and what they should do.

The message follows this structure:

```text
The demo database isn't accepting writes. I'll restore the demo
database from a snapshot and return in two minutes. Please leave
your terminal open and read the expected output in the README.
```

The two-minute promise sets an expectation. It also reminds me to choose the fallback if the first repair fails. I post it in the course chat even when only one student reports the failure.

If recovery takes longer, I switch to the fallback and continue. The original problem becomes an after-class note rather than a live investigation.

## 6. Review Every Demo Failure

After each session, I write a short incident note with the date, symptom, cause and recovery time. The note also records the setup change and lives next to the course repository.

Our last three notes produced three changes:

- pin Python 3.12 in `pyproject.toml` and the lab instructions
- add a `preflight` step to the first homework
- add a lab-image test to the rehearsal checklist

The incident notes are deliberately boring. A one-page record of 11 failed starts is more useful than a memory that the lab machines "sometimes behave strangely".

## Status After Four Sessions

The course has run four live sessions since the first failure. We had three smaller incidents, and all three recovered in under two minutes. Average downtime across 12 demos fell from about 4 minutes to 70 seconds.

Students noticed the difference in an anonymous survey after the fourth session. In that survey, 58 of 63 students said the instructor handled technical issues clearly. We also saw 61 completed setup attempts before the second session.

Preparation can't remove every failure, but it can turn one into a short, explained pause and a documented fix. The next live cohort starts in September, and I'll use the same rehearsal plan with one addition: a recovery drill during the first instructor onboarding.

If you want to follow along, don't forget to subscribe.
