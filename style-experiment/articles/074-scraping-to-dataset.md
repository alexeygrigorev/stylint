# From Web Page to Usable Dataset in One Afternoon

On a Saturday in May, I turned 1,142 public event listings into a small local
dataset. I wrote this synthetic style exercise with an invented website, dates,
counts, and code. The workflow shows how to move from messy HTML to data that
someone else can check.

I gave myself about 4 hours. I could ship an imperfect dataset if it had a
clear scope and a validation report.

The goal was a table of event names, dates, venues, and ticket types, grouped
by neighborhood. In this post, I'll share:

- the scrape and its politeness rules,
- how I normalized inconsistent fields,
- the sampling and validation pass,
- the dataset documentation,
- what I deliberately left unfinished.

## Scrape only what the scope needs

I started with the listing pages. Each page showed 30 events and a link to a
detail page. The HTML had several useful classes, but the site wasn't built for
extraction, so I treated its structure as unstable.

The scraper has three jobs, and I turned them into bullets:

- fetch a listing page,
- collect detail URLs,
- stop at a configured limit.

I used `requests` for HTTP calls and BeautifulSoup for parsing. A small SQLite
database (a file-based database) held the raw pages before any parsing.

The core command looked like this:

```bash
python scrape_events.py --category music --max-pages 40
```

The script used one request every 1.5 to 2.5 seconds, a user agent identifying
the project, and a local cache. If a URL had already been downloaded that day,
it read the cached page. The 40 pages produced 1,198 detail URLs. After
removing 56 duplicates, 1,142 remained.

I wrote the raw HTML immediately, even for pages I didn't expect to use. Raw
pages made the parse step repeatable. When I changed the parser 40 minutes
later, I didn't need to touch the site again.

The first parser failed in a useful way. It assumed every venue was in a
`venue-name` element. On 73 pages, that element held a neighborhood instead.

I changed the parser to extract both fields and record the selector used. That
choice made later cleaning decisions easier.

## Normalize fields without erasing evidence

The raw records went into a staging table. Each row had the event URL, capture
time, and separate extracted fields. I kept the extracted text next to the
cleaned value, so a normalization rule could be audited later.

Dates came in at least nine formats.

My extraction log contained these examples:

```text
Sat, June 14
14.06.26
June 14-15
Doors 19:30, starts 20:00
Every Friday until Aug 29
```

I split this work into rules. Absolute dates became ISO dates, while a range
became `start_date` and `end_date`. A recurring event became a Boolean field
and a raw recurrence string. I didn't expand every recurrence into individual
occurrences, because that would have required a separate scope.

Venue names needed lighter cleaning. I removed extra spaces, standardized the
abbreviation St to Saint, and preserved casing. Then I created a lookup table
with 273 unique raw values. For each, I added a canonical name and a confidence
score from 1 to 3.

Ticket fields were the least reliable. I saw words such as "donation",
"free before 22:00", and "from €12", so I mapped them into these categories:

- free,
- donation,
- fixed,
- minimum,
- unknown

The numeric minimum, when present, went into its own column. A value of unknown
was acceptable, but a silently wrong value wasn't.

## Sample and validate before declaring success

After normalization, I sampled 80 records in two groups:

- 40 randomly selected records,
- 40 records selected from fields with warnings.

I opened each sampled detail page from the local cache and compared five fields
with the extracted table.

The validation script checked mechanical rules first:

```text
start_date <= end_date
start_date between 2026-05-01 and 2026-08-31
venue_name not empty
neighborhood in known list or marked unmapped
ticket_category in the five allowed values
```

The first run found 81 failed rows. Thirty-nine had no venue, and twenty-two
had a start date after the website's stated end date. Twelve had contradictory
ticket text. Eight had a neighborhood that was actually a transit stop.

The random sample told a different story. Of its 40 records, 37 had correct
event names, dates, and venues. Two had missing neighborhoods that the page
also lacked. One had a date range reversed in the source. The 40 warning-based
samples were much worse: 12 had a genuinely bad date, and 9 had ambiguous
ticket text.

That distinction informed the dataset documentation. The overall random sample
looked reasonably accurate, but the warning bucket identified exactly where to
spend another hour. I fixed the date parser for four formats and marked 17 rows
unknown instead of inventing a value.

## Document the dataset like a small product

The final output is intentionally boring. It contains one Parquet file (a
columnar data format), one SQLite file, one README, and a validation report.
Parquet holds the clean table, while SQLite preserves the raw pages and
extraction records.

In the README, I start with the research question: which music events were
listed in one fictional city between May and August. I then state the capture
window, URL format, page limit, and exclusions. The file names the 17 unknown
ticket rows and 22 recurring events.

Each field has a short entry with five pieces:

```text
name, type, allowed values, extraction source, known limitations
```

The validation report records every rule, the number of passes, and the number
of failures. It also links to the sample review sheet, where each reviewed row
has a note. A future reader can disagree with my judgment because the evidence
remains local.

I added a small data dictionary generated from the schema. It lists 14 fields,
including three that I added during cleaning: `recurrence_flag`,
`venue_confidence`, and `ticket_numeric_min`. Without those fields, the clean
table would hide useful uncertainty.

## Work I Left Unfinished

The dataset covers one category and one capture window. It doesn't claim to
represent every event in the city. Sites can show different listings by time,
language, or location, and I didn't test those dimensions.

Three tasks remain open:

- expand the recurrence field without duplicating events,
- resolve 46 neighborhoods that map to transit stops,
- compare a second capture date with the first.

I could have spent another afternoon on each. For the original question, the
current scope was enough. With it, I counted events by neighborhood, identified
the largest venue clusters, and measured how often ticket information was
absent.

This project reinforced a simple rule. Data work becomes usable when its scope,
evidence, and uncertainty travel together. A clean-looking table with no
validation report is harder to trust than a smaller table that explains its
limits.

I plan to use this dataset in a future article about small local analysis. If
you want to follow along, don't forget to subscribe.
