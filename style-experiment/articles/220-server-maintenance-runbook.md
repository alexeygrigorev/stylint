# Writing a Runbook for Monthly Server Maintenance

This synthetic style exercise follows a fictional maintenance routine with invented details. Every name, count, and timeline below is fictional, and none of it describes real events. Last October I inherited a VPS running three course services with no maintenance notes.

The server cost $24 per month and hosted a course page, a small API, and Postgres. Nobody had updated it in five months, and the disk sat at 81% full. I spent one nervous evening checking whether backups even existed.

In November I wrote a four-page runbook in `docs/server-runbook.md` from scratch. The full run takes about 45 minutes, and I have run it six times since.

In this post, I'll share:

- how I verify backups before touching anything
- the fixed order I apply updates in
- how I reclaim disk and check certificates
- how I practice recovery once per quarter
- what six maintenance runs taught me

## 1. Verify Backups Before Touching Anything

My first maintenance attempt skipped the backup check, and I regretted it within an hour. A Postgres minor update restarted the container with a fresh empty volume. I lost no data, but I spent the evening proving that fact to myself.

The runbook now starts with backups because everything else assumes they exist. I check the nightly snapshot timestamp, the weekly off-site copy, and the database dump age. All three checks take under five minutes.

I run the backup checks with three commands:

```bash
ls -lt /var/backups/snapshots | head -5
pg_dump --version && ls -lt /var/backups/db | head -3
df -h / /var/lib/postgresql
```

The output tells me the newest snapshot date, the newest dump date, and current disk use. I don't continue when any backup is older than 48 hours. It's a strict gate, and it has stopped two runs already.

I log every run in a dated section at the bottom of the runbook. Each entry lists duration, surprises, and deferred items for next time. The log now holds six entries, and reading them shows the server getting calmer.

## 2. Apply Updates in a Fixed Order

Random update order caused the container incident, so the runbook fixes the sequence. System packages go first, then Docker images, then the application code. Each stage gets its own health check before the next one starts.

The runbook lists the order as five steps:

- update system packages and reboot only when required
- pull new Docker images for the API and the page
- restart containers one at a time, never together
- run database migrations with the backup dump verified
- load the course page and call two API endpoints

I keep a 10-minute observation pause after the restarts. Twice that pause caught a container restart loop before students noticed anything. I didn't invent the order from theory, since each position in it marks a past incident.

One reorder deserves a note. I used to update the application first because it felt productive. The rule I took from the container incident: lower layers settle before upper layers move.

## 3. Reclaim Disk and Check Certificates

Disk pressure caused two of my three past incidents, so this section runs every month without exception. Log files grow by roughly 1.2 GB per month, and Docker keeps old images until someone removes them. The 81% I inherited is now a 45 to 55% range after each run.

The cleanup covers four locations:

- rotated application logs older than 30 days
- Docker images without a running container
- Postgres WAL archives already shipped off site
- temp upload files older than seven days

Certificates get checked in the same section because expiry is equally silent.

One short command prints every certificate expiry date for review:

```bash
certbot certificates | grep -E "Expiry|Domains"
```

The output shows each domain with its expiry date. I renew anything under 30 days, which has happened once in six runs. There's a comfort here - the comfort of seeing 60-plus days on every line.

## 4. Practice Recovery Once Per Quarter

Backups nobody restores are rumors, so the runbook includes a quarterly restore drill. I spin up a local container, load the newest dump, and run the migration chain from scratch. The drill takes about 30 minutes on my laptop.

The drill follows four steps:

- download the newest off-site dump to the laptop
- restore it into a fresh Postgres container
- run all migrations and the seed script
- boot the API against the restored database

The first drill failed because the seed script assumed a newer Postgres version than the dump. I set both to Postgres 16, and the next two drills passed in 26 and 31 minutes. I don't trust green dashboards alone, since only a restore proves the backup chain.

## Maintenance Log After Six Months

I spent about five hours on six runs, spread across half a year. Disk use has never passed 62% since the first cleanup. I have seen zero certificate warnings since March, and no update has caused an incident.

The runbook taught me a narrower lesson than automate everything with cron. I check the server every month instead of waiting for emergencies, and I follow the fixed order each time. The runbook is four pages, and the slowest step was writing the first version from scattered notes.

I'll write about the off-site copy setup in a future post with real numbers. If you want to follow along, don't forget to subscribe.
