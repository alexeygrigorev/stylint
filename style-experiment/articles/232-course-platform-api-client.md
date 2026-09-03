# Writing a Client for a Course Platform API

This synthetic style exercise follows a fictional integration I built in May. My cohort dashboard needed enrollment data from a course platform with 1,200 students. The platform offered a REST API and I had two weeks before the next cohort started.

I run registration, reminders, and feedback from small scripts. I've copied enrollment CSV files by hand for three cohorts and I don't want another manual term. The dashboard runs on a VPS with Python 3.12 and Postgres.

I built CourseClient, a small Python module for auth, paging, and retries with the platform API. It exposes five functions and it stores nothing except a cache file. I started from 80 lines I wrote on a Saturday.

In this post, I'll share:

- why manual CSV exports stopped working
- how auth and paging work in the client
- what retries and validation catch during sync
- how caching keeps the dashboard fast
- where the client still needs manual review

## Manual Exports That Broke Down

The CSV export worked for the first cohort with 180 students. I downloaded the file every Monday and I imported it with a script in about ten minutes. That routine felt fine when the numbers stayed small.

The second cohort grew to 640 students and the export started missing late enrollments. The platform generated the file at midnight and anyone who enrolled after that time appeared only the next week. I sent welcome emails late twice and I apologized to 23 students.

A third failure came from renamed columns. The platform changed `student_email` to `email` in March without notice and my import script skipped every row. I found the empty table on a Tuesday morning and I fixed the mapping before lunch.

The rule I took from those weeks: pulls from the API beat downloads from the dashboard, and the pull has to run on a schedule.

I chose a small client over a full integration because I know the API surface I need. Five endpoints cover enrollments, progress, and completions. That narrow scope keeps the code reviewable in one sitting.

## Auth And Paging In Practice

Auth uses a per-project API key with read-only scope. I store the key in an environment file and I load it at runtime without printing it to logs. The key rotates every 90 days and the rotation takes about five minutes.

The client sends the key in a header on every request. The header name is `X-API-Key` and the value comes from `COURSE_API_KEY`. I validate the variable at startup and the client stops with a clear message when the variable is missing.

Paging follows cursor style with a limit of 100 records per call. The response includes a `next_cursor` field and an empty value means the last page. My largest sync pulled 1,214 enrollments across 13 pages in 41 seconds.

The paging loop looks like this:

```python
records = client.list_enrollments(course_id="ml-zoomcamp-2026")
```

I call that function with a course identifier and it returns a list of dicts. The function handles cursors internally and it raises after three failed pages. That behavior keeps calling code short and predictable.

I picked cursor paging because the API team recommends it for large cohorts. Offset paging skipped rows when enrollments changed during the pull.

## Retries And Validation During Sync

Network failures happen often enough to plan for them. My first sync run failed on page nine with a timeout after 30 seconds. The script exited and I had no partial file to resume from.

The client now retries idempotent GET requests with exponential backoff. It waits two seconds, then four seconds, then eight seconds before giving up. That sequence fixed 11 of 13 transient failures in May without manual reruns.

Validation runs on every record before the insert into Postgres. I check for a present email, a valid course identifier, and a timestamp within the cohort window. Records that fail validation go to a quarantine table with a reason code.

The quarantine table held 17 rows after the May sync. I reviewed all 17 in about 15 minutes and I deleted the test rows.

One mistake taught me to log the request identifier with each error. I debugged a 500 response for an hour without knowing which page triggered it. I added the identifier to every log line the next day and the next debug took nine minutes. The rule I keep: every error line names the page or record that caused it.

I don't retry POST requests automatically because duplicate enrollments confuse students. The client returns the error to the caller and I resolve those cases by hand. That boundary added three manual reviews in May and it prevented duplicate welcome emails.

## Cache Behavior And Dashboard Speed

The dashboard reads enrollment counts on every page load. Direct API calls added 900 milliseconds to each load and the pages felt sluggish during live sessions. Students noticed the delay and two of them mentioned it in feedback.

The client writes a cache file after each successful sync. I store the course identifier, sync time, record count, and payload hash in that file. Dashboard views read the file first and they fall back to Postgres when the file is older than one hour.

The cache update runs every 20 minutes from cron. A full sync touches about 1,200 records and it finishes in under a minute. The dashboard p95 load time dropped from 1.4 seconds to 320 milliseconds after I added the file.

The cache format stays simple for debugging:

```text
course_id
synced_at
record_count
payload_hash
enrollments
```

I read that file with a ten-line loader and I display the sync time in the footer.

## Reflection And Next Steps

The client replaced manual CSV work with one cron job and a short review. Weekly sync time dropped from 40 minutes of CSV work to about ten minutes of log review.

I still review the quarantine table by hand every Monday. The table catches test accounts and edge cases the validator doesn't know yet. That review takes 15 minutes and it keeps bad rows out of the dashboard.

I plan a small diff email that summarizes new enrollments, completions, and quarantined rows. I'll generate the summary from the sync log and send it to myself after each run. That message should take an hour to build.

I'll write about that summary email format in a future post. If you want to follow along, don't forget to subscribe.
