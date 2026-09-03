# Reviewing Automations That Silently Stopped Working

I wrote this synthetic style exercise as a build log, and all project details are fictional. On 2 February 2026 I opened the backup folder on my recipe site's server. The nightly Postgres dump had stopped on 18 December, so the database had run for 46 days with no backups.

The dump job shared a crontab with 8 other jobs: a sitemap build, a certificate check and 6 cleanup scripts. The dump wrote a compressed file into /var/backups/recipes at 02:00 every night. Cron reported nothing, because a wrapper script exited with code 0 even when pg_dump failed.

In this post, I'll share:

- how the nightly dump failed without an error
- why my first alerting attempt changed nothing
- how a freshness check now watches each job
- how the daily report reaches one place I read
- what two months of monitoring changed
- which silences the setup still misses

## Nine Jobs and One Silence

The server runs Ubuntu 24.04 on a 4-euro VPS, and cron drives all of the jobs from one crontab. The dump job called pg_dump at 02:00 and compressed the result into /var/backups/recipes. On 18 December the disk filled up, pg_dump wrote a partial file, and the wrapper treated the partial file as success.

I found the silence by accident, while looking for space to unpack a laptop backup. The last healthy dump was from 17 December, 46 days earlier. The other jobs kept running through the whole period, which made the one silence harder to spot. A database that dies quietly is bad, and a backup pipeline that dies quietly is worse, because a second failure would find nothing to restore.

## Email Alerts Nobody Read

My first fix took ten minutes and changed nothing. I set MAILTO in the crontab, so cron would email me whenever a job printed errors. The mistake sat one layer lower. The wrapper script swallowed the error and exited cleanly, so cron never saw a failure and never sent mail.

Even when mail did arrive, it went to a mailbox with about 4,000 unread emails, most of them log noise from October. I found two old cron messages in that folder while cleaning it in February. An alert that arrives where I never look works like no alert at all.

The rule I took from it: an alert needs a reader before it needs a trigger.

## A Freshness Check per Job

So I stopped watching job logs and started watching job artifacts. I wrote stale-check, a small Python script that compares the age of each job's output file with that job's schedule.

Every job gets one line in a config file:

```text
postgres-nightly  /var/backups/recipes  26h
sitemap-weekly    /var/www/sitemap.xml  8d
cert-check        /var/log/cert-check   25d
```

The first field names the job, the second gives the artifact to watch, and the third sets the oldest acceptable age. The script exits with a nonzero status when any artifact is older than its limit. Writing the config for all nine jobs took about 20 minutes, because every job already wrote a file I could watch.

## One Message to One Place

The check runs daily at 08:15 through cron, and its output becomes a plain text report plus one push notification on my phone:

```bash
stale-check --config /etc/stale-check.conf --notify
```

The `--notify` flag sends the summary through ntfy, a small self-hosted push service, to a channel that sits on my phone's home screen.

One message from 4 March shows the format:

```text
postgres-nightly  age 22h  ok
sitemap-weekly    age 3d   ok
cert-check        age 41d  STALE (limit 25d)
```

That message caught the certificate checker, which had stopped writing its log in January. I fixed it the same morning with a one-line change to the renew hook, plus a manual run to confirm the log moved again. The whole review took 15 minutes from message to fix.

## Two Months With the New Setup

Between 12 February and 20 April the check ran about 60 times and caught 2 real silences. The first was the certificate checker in March, and the second was a sitemap build that failed for 5 days in April. Both were fixed within a day, which reads better than 46 days.

I also added a size floor after a close call in March. An artifact under 1 KB counts as missing, because a truncated dump once passed the age check. The floor flagged one honest but small dump that week, and it has stayed quiet since. False alarms so far: one in about 60 runs.

Every report is also written to /var/log/stale-check, so I can flip through two months of history in one file. That archive settled an argument with myself in April about when the sitemap trouble had started.

## Lessons From 46 Silent Days

The whole review compressed into one sentence: silence is the default state of a cron job, and only an observable artifact makes a job reviewable. Alerts belong where I already look, and mine now arrive on the phone I check anyway.

The setup still has gaps. It sees timestamps and sizes, so a job that writes a fresh, plausible and wrong file passes every check. The 46-day gap also taught me to open the backup folder on purpose once a month. Even a freshness check deserves an occasional audit.

I'll write about the size floor and its false alarms in a future post. If you want to follow along, don't forget to subscribe.
