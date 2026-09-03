# The Database Migration Checklist I Should Have Used Sooner

I wrote this how-to guide as a synthetic style exercise, and all project details are fictional. In March 2026, I locked a 41 GB PostgreSQL database for 34 minutes while I renamed a column in a customer billing service called Ledgerway. The outage was small, but the retrofit to the deployment process took three weeks.

In this post, I'll share:

- why the migration locked the billing tables
- the backup gate I added before every database change
- how I now expand and migrate in separate deployments
- how I remove old columns after verification
- the checklist I use for every schema change

## The Accidental Lock

The first migration looked harmless in staging. It renamed `customer_id` to `account_id` in 12 tables and completed in 11 seconds on a 300 MB copy.

Production was different because PostgreSQL had to rewrite indexes and wait for long billing transactions to release their locks. Twenty-two requests to `/invoices` queued behind the change, and the status page showed a complete outage.

My mistake was treating a schema rename as a deployment detail. The rule I took from it: a database migration is a product change with its own release plan.

I could have stopped the deployment when lock waits passed 30 seconds. The migration runner had no timeout, so it waited for the schema lock and made every new transaction wait too.

## The Backup Gate

Ledgerway now refuses to run a migration unless a fresh backup and a restore test exist. A compressed file can be unreadable while it still looks complete.

The nightly job creates a base backup at 02:10 Berlin time.

Before a release, I run a restore into a temporary database and check these facts:

- row counts
- the latest invoice ID
- a checksum on the account balances table

The preflight command is short:

```bash
scripts/restore-check --source prod-backup-2026-03-14 --target migration-preflight
```

The script restores the backup, compares 14 row counts with production read replicas, and exits with a nonzero status on any mismatch. Only then does the release workflow allow `alembic upgrade head`.

This step costs about eight minutes. That's less than one-third of the March incident, and it removes the worst case in which we migrate forward with no known-good copy.

## Expand and Migrate

The checklist splits incompatible changes into two deployments. The first deployment adds the new column and keeps both code paths working. The second deployment removes the old column.

For the rename, I stopped trying to rename the column during a request. Alembic added `account_id`, an application flag filled it for new rows, and a background job copied historical values in batches of 50,000.

Each batch ran in its own transaction:

```python
for low in range(0, total_rows, batch_size):
    copy_account_ids(low, low + batch_size)
    mark_batch_complete(low)
```

The job checkpointed every batch, so a restart at 71% continued from the last completed range. The full copy took 4 hours 20 minutes, and read traffic stayed under 180 milliseconds at the 95th percentile.

Application code read from `account_id` when it existed and fell back to `customer_id` otherwise. I deployed that change on Tuesday and watched canary traffic for 24 hours before I enabled writes to both columns.

That sounds slow after years of one-shot migrations. But staging had hidden the true cost, and the two-step path let me stop without shipping a broken rollback.

## Remove and Verify

After two clean days, I removed writes to `customer_id`, then removed the column in a third release. I also dropped the compatibility flag and fallback branch.

Verification stayed mechanical, and the release job compared counts, confirmed zero null values, and replayed invoices through the billing code.

The SQL check is deliberately dull:

```sql
select
  count(*) filter (where account_id is null) as missing_accounts,
  count(*) filter (where customer_id is not null) as old_ids
from invoices;
```

It had to return two zeros before the cleanup step could run. A reconciliation job then compared 10,000 invoice totals with the values captured before the migration.

Only after that did the job send a migration report to the team channel. It listed elapsed time, row counts, rejected records, and the rollback commit. The report made the evidence visible without asking anyone to trust the deploy log.

The final cleanup release dropped 4 old indexes and recovered 6.2 GB. It ran at 04:30, outside the billing window, and held its schema lock for 9 seconds.

## Lessons From the Migration

The checklist now has six gates, and each gate names the artifact that must exist before the next one starts:

- intent
- backup
- expand
- migrate
- verify
- cleanup

The intent note is one paragraph with the reason, rollback point, and blast radius. The backup gate points at a tested restore. The expand gate identifies old and new code paths.

The migrate gate records progress, the verify gate stores queries and results, and the cleanup gate schedules the removal.

I still write each migration as a small task. The checklist hasn't made every change painless, but it has made the cost explicit before I type the first SQL statement.

The March incident also changed how I review generated migrations. I ask the coding agent for the lock behavior, the backfill plan, and the verification query before it writes schema changes.

I plan to write separately about the reconciliation job and how I choose rollback points. Subscribe if you want the next part of this deployment series.
