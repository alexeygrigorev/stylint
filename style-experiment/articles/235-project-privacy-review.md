# A Privacy Review for a Personal AI Project

I wrote this synthetic style exercise as a how-to guide. The project, dates and numbers are fictional. In January 2026 I counted the data inside my Telegram assistant project, a bot that summarizes my saved messages.

It held about 41,000 chat messages in Postgres, voice files in one S3 bucket, and no written answer to who could read them. In February I ran a privacy review over two evenings, and you can copy every step on a project of your own.

In this post, I'll share:

- how I listed every table, file and log the project keeps
- how I set retention rules for messages and backups
- how I restricted access to the database and tokens
- how I tested deletion end to end
- the common mistakes from my first pass

## 1. List The Data You Keep

Start with an inventory, because retention and deletion both need a list of containers first. My assistant runs on one VPS with Postgres, a local exports folder and an S3 bucket for voice files.

List the Postgres tables with row counts before you write any rule:

```bash
psql postgresql://bot@localhost/botdb -c "SELECT relname, n_live_tup FROM pg_stat_user_tables"
```

The query returned three tables. Messages held 38,400 rows, users held 42 rows and sessions held 1,100 rows. Row counts matter because delete time grows with the table, so the biggest table decides the batch size.

The exports folder held 94 markdown files, one per saved article. Voice files were the bigger surprise: 612 recordings, most of them under two minutes long.

Logs were the last container. The systemd journal on the VPS held message excerpts from crash reports, so the logs went into scope with everything else.

## 2. Set Retention Rules

Pick a lifetime for every container and write the numbers down in one file. I kept messages for 180 days, voice files for 30 days and weekly backups for 14 days.

A cron job enforces the message rule at 04:00 every night:

```bash
0 4 * * * psql postgresql://bot@localhost/botdb -c "DELETE FROM messages WHERE created_at < now() - interval '180 days'"
```

The job deletes 200 to 300 rows per night, so each run stays under a second. Voice files expire through a lifecycle rule on the bucket, which took about ten minutes to configure.

My first version cleaned the live table and forgot the backups, so a restore in February brought back 6,000 deleted rows. The rule I took from it: a retention policy that ignores backups protects nobody.

The cron file now runs the purge before the Sunday backup job, so no copy outlives the rule by more than seven days.

## 3. Restrict Who Can Read It

Next I listed every credential that could reach the data, and the inventory found four ways in:

- my laptop, with its SSH key to the VPS
- the root account on the VPS
- a Grafana dashboard using a full-permission database token
- one analytics script with a hard-coded password

The dashboard token could read and delete every table, which felt excessive for a private project. I replaced it with a read-only role that sees two tables and no user rows.

The grants are two lines, and the dashboard now gets a permission error instead of deleting data:

```sql
CREATE ROLE dashboard_read LOGIN PASSWORD 'REDACTED';
GRANT SELECT ON messages, sessions TO dashboard_read;
```

The analytics script switched to the same role, and its hard-coded password moved into an env file with chmod 600. My laptop kept full access, because someone has to administer the thing. Rotating both credentials took about 15 minutes. The git history still holds the old password, so history cleaning stays on the list.

## 4. Test Deletion End To End

A rule you never test is a guess. The project now has `erase-me.py`, a small script that deletes every row and file for one test user, then prints the counts before and after.

I run it before each release, which takes about five minutes:

```bash
uv run python erase-me.py --user test_user_42
```

The output fits on one screen:

```text
users: 1 deleted
messages: 317 deleted
sessions: 4 deleted
voice files: 12 deleted
leftover rows for user: 0
```

When the last line shows anything above zero, the release waits. That check caught a missed table in April, when the sessions table kept 4 rows and the script exited with a failure code.

## Common Mistakes

Three mistakes came out of the first pass:

- log files stayed out of the first inventory, and they held message excerpts
- the first deletion pass skipped the S3 bucket completely
- the analytics script kept its old password after the role change

Each fix took under an hour, and finding them took the second evening. Both numbers beat the alternative, which was explaining the data during an incident instead.

## After The Review

The review took two evenings and produced a one-page file called `privacy.md` at the repo root. It lists the containers, their retention numbers and the access rules in plain sentences.

I re-run the inventory query once a month, and the full check takes about 20 to 30 minutes. The weakest spot is still my laptop, because exports I copy for articles leave no trace in the audit.

I'll write about encrypting the voice archive in a future post. If you want to follow along, don't forget to subscribe.
