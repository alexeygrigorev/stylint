# Setting Up a Sandbox for Risky Agent Work

In February, a coding agent had permission to run shell commands against a
billing service. The task was to clean up unused database tables, and it
identified 27 candidate tables from a stale report. I stopped the job before it
wrote anything, then built a repeatable sandbox for that class of work. I wrote
this synthetic style exercise with fictional projects, permissions, timings, and
incidents.

The billing service had 4 years of operational data and no safe place for an
agent to experiment. I don't trust an agent with production credentials, even
when the prompt sounds narrow. A sandbox gives the agent room to work and gives
me a boundary I can look at.

In this post, I'll share:

- how I define a risky task,
- how I create disposable snapshots,
- how I limit network access,
- how I substitute fake credentials,
- how I clean up after a run.

## 1. Classify the task

The first useful step is to decide what "risky" means for the project. I use a
short rule.

An agent may work directly on disposable files, and it needs a sandbox when a
task touches these surfaces:

- persistent data,
- external services,
- secrets,
- anything users can see.

For the billing service, I put cleanup work in the second group. The agent had
to query table sizes, trace foreign keys, write deletion scripts, and prepare a
dry-run report. Those actions are safe when they target a copy and dangerous
when they target the live database.

I also record the permission boundary before writing the prompt.

For that job, the agent could:

- read schema metadata and row counts,
- run queries against the sandbox database,
- write files under `work/cleanup/`,
- execute SQL through one project script.

It couldn't connect to the live database, install packages, read the secret
directory, or send network requests except to the local database server. Writing
the list down made the next steps easier to review.

## 2. Snapshot the environment

I run the sandbox in Docker Compose. The service uses PostgreSQL 16, so the
compose file starts PostgreSQL and mounts a restore script. The agent works in
a container named `billing-agent`, while the database is a separate container
named `billing-sandbox-db`.

Before every run, I restore a sanitized snapshot from object storage. The
snapshot contains a schema, 250,000 synthetic rows, and indexes. Restoring it
takes about 80 seconds. Real customer records are removed by the anonymizer
before the snapshot is stored.

I give each run an ID in the format `2026-02-14-cleanup-01`.

The restore script creates a matching Docker volume and writes a small manifest:

```text
run_id: 2026-02-14-cleanup-01
snapshot: billing-2026-02-09-sanitized
created_at: 2026-02-14T09:20:00+01:00
expires_at: 2026-02-17T09:20:00+01:00
```

The volume is disposable, while the manifest lives in `runs/`. If a result looks
promising, I can reproduce the environment with the same snapshot for another
80 seconds.

## 3. Limit the network

The default container configuration allowed outbound access, which was broader
than the task required. I changed the compose network to `internal` and exposed
only the sandbox database port to the agent container. DNS resolution inside
that network reaches the database service and nothing else.

For package installation, I use a prebuilt image. The image contains Python
3.12, `psycopg`, `pgcli`, and the repository's local package. Building it once
removed the main reason the agent wanted the public internet.

I verify the boundary with two commands before handing over the prompt:

```bash
docker compose exec billing-agent pgcli -h billing-sandbox-db -U sandbox -c "select 1"
docker compose exec billing-agent curl --max-time 3 https://example.com
```

The first command must succeed, and the second must fail. That 10-second check
has caught two configuration mistakes: a typo in the network name and a second
compose file that overrode it.

## 4. Use fake credentials

I stopped putting production secrets in environment files that an agent might
read. The sandbox gets its own database user named `sandbox`, and the password
exists only inside the local compose environment. The user owns the sandbox
database and has no role in the live cluster.

External services use local fakes. A payment provider is replaced by `fake-pay`,
a small FastAPI application that returns fixed success, decline, and timeout
responses. The Stripe client still points at a base URL configured through
`PAYMENTS_BASE_URL`, so the application code doesn't change between
environments.

The fake payment service has three fixtures:

- a card that succeeds after 120 milliseconds,
- a card that returns a decline code,
- a request that hangs for five seconds.

That gives the agent enough behavior to test retries and error paths. It also
keeps test data obvious: every fake card number starts with `9`, while anonymized
records never do.

## 5. Clean up on a schedule

Cleanup has to happen even when a session ends badly. A timer script runs every
12 hours and removes volumes whose manifest has passed `expires_at`. It also
deletes abandoned work directories older than seven days and prints a summary to
the terminal.

The agent must leave two artifacts in `work/cleanup/`: a report and an SQL
migration. The report lists each table, row count, foreign-key references, and
the evidence for treating it as unused. The migration contains the deletion
statements but doesn't run against live data.

After review, I promoted one migration for 21 tables. Six candidates stayed in
place because the report showed references from an archival job. That result is
the point: the agent prepared evidence, and a person made the production change.

I now reuse the setup for incident reproduction and model-configuration
experiments. Each variant gets a new run ID and volume, so a mistake can't leak
into the next experiment.

## Current use

Sandboxes work best when the boundary is boring and mechanical. Snapshots make
mistakes cheap, network rules remove an entire class of accidents, and fake
credentials make secret leakage impossible rather than discouraged.

The rule I took from the February scare: give agents a disposable copy and a
reviewable output, and keep the irreversible action behind human review. Next
month I plan to publish the compose files as a project template. Subscribe if you
want to see that template.
