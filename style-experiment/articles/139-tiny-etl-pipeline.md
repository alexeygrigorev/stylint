# A Tiny ETL Pipeline for Course Enrollment Data

Our fictional DataCamp course platform had 3,412 enrollment records in a
partner's CSV export, and I couldn't answer a basic question about them. I wrote
this synthetic style exercise with a fictional platform, dates, prices, and
failures. The export changed column names between March and April, so the course
team's spreadsheet undercounted April enrollments by 218.

I first copied the CSV into a spreadsheet and fixed the columns by hand. That
took 35 minutes and worked until the partner sent a second file with a new
"coupon code" field. At that point, I accepted that the import needed a pipeline.

In this post, I'll share:

- how I extracted the partner export,
- how I validated records before loading,
- how I loaded and reconciled the data,
- how I alerted the course team,
- what the pipeline still doesn't do.

## Extract the export

The partner exposes a nightly CSV file behind a token in its API. The file is
about 4 MB on weekdays and 9 MB after a weekend. I used Python 3.12 with
`requests` and put the token in an environment variable called
`ENROLLMENT_TOKEN`.

The extractor keeps every download in its original form:

```text
enrollment-data/
  raw/
    2026-04-01-enrollments.csv
    2026-04-02-enrollments.csv
  logs/
    2026-04-01.log
```

Raw files make reconciliation possible. When a count looked wrong in May, I
could rerun that day's exact file instead of trusting my memory of the partner's
statement. Disk use was 420 MB after four months, so I set raw retention to 18
months.

The download script writes a checksum beside each file and refuses to overwrite
an existing day. That sounds defensive, but it caught a real-looking problem in
our fictional partner feed: two files published under the same date. We asked
for a corrected file and preserved both deliveries.

## Validate before loading

The CSV taught me that validation belongs before the database. Pandas, a Python
library for tabular data, reads the file quickly, but its permissive types can
hide messy values. I load each row into a Pydantic model (a data-validation
library) before it gets near the enrollment table.

The validation rules are:

- `enrollment_id` is unique and nonempty,
- `course_id` exists in our course catalog,
- `status` is one of `reserved`, `paid`, or `refunded`,
- `enrolled_at` parses as a timestamp,
- an email address contains exactly one `@`.

I kept rejection separate from failure. A bad row goes into
`rejected/2026-04-01.csv` with the original line number and reason. The daily
import continues if rejections are below 2% of the file. Otherwise, the process
stops and waits for a person.

In April, the first version rejected 4.6% of rows because 167 emails contained
trailing spaces. That was useful data about the export, but it stopped a useful
load. The final validator trims whitespace, records the original value, and
passes the cleaned address onward.

## Load and reconcile

I used SQLite (a small embedded relational database) because the course team
needed one file they could open. The database contains three tables:
`enrollments`, `courses`, and `import_runs`. Each row stores its import run ID,
so a corrected file can replace one day without deleting history.

The load runs inside a transaction. If any required insert fails, the run
records the exception and leaves the database unchanged. If it succeeds, the
loader writes five row counts into `import_runs`. Those counts cover read rows,
accepted rows, and rejected rows. The remaining two counts cover rows inserted
and rows updated.

After loading, the pipeline compares three totals:

```text
source rows:        4,204
accepted rows:      4,193
database rows:      4,193
refunds: source 118 / database 118
```

These four lines go into the run log, and they're the first thing I read after
a deployment. A row count alone isn't enough: two identical rows can hide a
changed status. The refund total catches that case because it uses a business
field rather than only record identity.

## Alert the course team

The first version printed to standard output, which meant the course team
learned about a failure from a missing number in a spreadsheet. I added three
alerts to the daily run.

The alert conditions are:

- the download fails twice,
- rejections reach 2% of a file,
- reconciliation totals differ.

The pipeline posts a short message to a private Slack webhook. The message
contains the date, two row counts, the rejection percentage, and the log path.
It ends with a single status word and doesn't include enrollment data, because
the webhook channel is broader than the enrollment group.

For example:

```text
Enrollment import failed: reconciliation mismatch
Date: 2026-06-14
Accepted 1,884, loaded 1,879
Log: enrollment-data/logs/2026-06-14.log
```

Five notifications in June were enough to find two real causes. A partner
renamed a status from `paid` to `paid_success`, and one course ID disappeared
from our catalog during a course migration. Each fix took under 30 minutes once
the alert named the exact mismatch.

## Current limits

This pipeline is deliberately small. It handles one CSV feed, one destination,
and one daily run. It doesn't support incremental API pages, multiple partners,
or streaming updates. Those features would add stored state, late data, and
partial page loads that the course team doesn't need yet.

The reconciliation is also narrower than a full audit. It checks row counts and
refund totals, and it samples 20 random accepted rows per day. It doesn't compare
every field in every record. A partner change to a coupon field could survive
that check until someone notices a report.

## Lessons from the import

Keeping raw files, rejected rows, and run counts made the pipeline debuggable.
The database load was easy once the validation errors had a place to live.

The rule I took from the project: reconcile with a business total, not only a
row count. I plan to write more about the reporting queries in a future article.
Subscribe to stay updated.
