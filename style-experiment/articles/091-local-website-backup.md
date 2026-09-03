# A Simple Backup System for My Static Sites

I wrote this synthetic style exercise as a build log, and all project names and numbers are fictional. In January 2026 a broken deploy script deleted the images folder of my recipe site, and I lost about 340 photos that existed nowhere else.

I run four static sites from markdown sources that live on one VPS. The sites rebuilt within an hour, but the drafts and the photos stayed gone. That incident turned backups from a someday task into a weekend project, and this post is the report from that weekend.

In this post, I'll share:

- the disk layout that made one bad script so destructive
- a nightly tarball job that failed in a quiet way
- the versioned artifacts I now push to object storage
- a restore test I run once a quarter
- alerts that fire when the nightly job goes quiet
- current costs and the gaps I still accept

## Four Sites And One Aging Disk

The four sites share one VPS with a 40 GB disk that costs $12 per month. The markdown sources sit in `/srv/sites`, and each site keeps an `images` folder beside its content folders. I edit on a laptop, push with rsync, and the server rebuilds the HTML with a static site generator. The recipe blog has the largest image collection of the four, and it had grown to about 6 GB by the end of 2025.

Until January, my whole backup plan was a weekly archive in `/backups` on the same VPS. That plan protected the files against my own typos during editing. It did nothing against a failing disk or a script with a wrong path.

My mistake was treating a copy on the same disk as a backup. The rule I took from it: a backup belongs on a different machine in a different region.

## A Nightly Tarball That Failed Quietly

The first attempt after the incident was quick and lazy.

In late January I added a cron entry that packed `/srv/sites` into a dated archive at 02:00 each night:

```bash
tar -czf /backups/sites-$(date +%F).tgz /srv/sites
```

The archives piled up in `/backups`, and for three weeks the job looked finished. It had two holes I only saw later. A disk failure would have taken the originals and every archive in one event, and nothing watched the cron job.

The second hole showed up in February. The disk filled, the job died, and the newest archive sat 11 days old before I noticed while looking for something else. I freed space, restarted the job, and moved on, which fixed nothing about the monitoring gap.

## Versioned Artifacts In Object Storage

In March 2026 I moved the archives into Amazon S3 and rewrote the job as `backup-sites`, a 30-line bash script in `/usr/local/bin`.

The script packs the sources, names the artifact by date, and uploads it:

```bash
stamp=$(date +%F)
tar -czf /tmp/sites-$stamp.tgz -C /srv --exclude node_modules sites
aws s3 cp /tmp/sites-$stamp.tgz s3://my-static-site-backups/weekly/
```

The exclude flag matters because a stray `node_modules` folder had grown to 4 GB. Dropping it cut a full artifact from about 7 GB to 3.1 GB. The date-stamped names act as versions, and a lifecycle rule in the bucket keeps 12 weekly and 12 monthly artifacts before it deletes anything older.

The nightly run takes about 12 minutes end to end. Between the lifecycle rule and the infrequent-access storage class, the bucket costs about $0.55 per month. I also turned on bucket versioning, so an overwritten object keeps its previous copies for 30 days.

## The Quarterly Restore Test

In April I ran the first restore test, and it caught a real defect on the first try.

The test downloads the newest artifact to a scratch directory on my laptop, unpacks it, and rebuilds all four sites:

```bash
aws s3 cp s3://my-static-site-backups/weekly/sites-2026-06-06.tgz .
tar -xzf sites-2026-06-06.tgz -C /tmp/restore
```

I then run the site generator against `/tmp/restore` and open each rebuilt site in a browser. The April run produced three of four sites. The recipe blog failed to build because an asset folder included a symlink that pointed outside `/srv/sites`, and tar had stored it as a broken link. I flattened that symlink the same evening and re-ran the test until the rebuild passed.

The test is now a calendar entry for the first Saturday of each quarter. It takes about 30 to 40 minutes, and most of that time goes to the download and the rebuilds.

## Alerts When Backups Go Quiet

The quiet failure in February needed a fix at the monitoring layer. The backup script now pings healthchecks.io, a dead man's switch service that sends an email when an expected ping fails to arrive. A missed nightly window produces an email after 26 hours.

I tested the alert by pausing the cron job for two days in May, and the email arrived on schedule. A second check runs every Sunday morning and lists the bucket with `aws s3 ls`, so an upload that silently skipped a week surfaces within days. Between the two checks, the worst silence dropped from 11 days to about two.

The alerting covers uploads and nothing else. It can't tell me whether a restored site would build, and that blind spot is exactly what the quarterly test covers. Keeping the two jobs separate keeps each one simple enough to debug at 07:00 with a coffee.

## The Setup Today

The whole system is one script, one bucket, and two cron entries, and I have rebuilt it twice since January. Nightly artifacts cost about $0.55 per month, and each quarterly restore takes about half an hour.

Two gaps stay open for now. The job skips the deploy logs, and nothing checks the content of an artifact between quarterly restores. I accept both, and the second one sits as a comment at the top of `backup-sites` where I see it on every edit.

I'll write about the deploy pipeline in a future post. If you want to follow along, don't forget to subscribe.
