# Writing Down Data-Cleaning Decisions Before I Regret Them

I wrote this synthetic style exercise as a build log. The dataset, project names, dates and measurements are fictional.

Last March I inherited 214,180 rows of electricity-meter readings for a fictional housing cooperative. The project needed monthly summaries for 18 buildings, and the data arrived as six CSV exports from three billing systems. Two of those exports had already been edited by hand.

The first summary looked plausible until I compared March across the three sources. Building 12 had 41,900 kilowatt-hours in one file and 39,220 in another. I removed rows until the totals matched, then couldn't reconstruct my exclusions two weeks later.

In this post, I'll share:

- how I made every exclusion a recorded decision
- how I handled missing readings and duplicate timestamps
- how I normalized building names and units
- how I tested the cleaning code against six exports
- what the provenance record looks like now

## The First Notebook Failed

I put the six exports in one folder and wrote 180 lines of pandas in a notebook named `clean_readings`. The first version removed blank readings, dropped duplicates, converted kilowatt-hours to kilowatt-hours, and produced a monthly table.

It worked once, but the setup was fragile. When the cooperative sent the April files, 14 new buildings appeared and 11 had the old names with extra spaces. My implicit assumptions were spread through the notebook. Changing one filter changed three downstream totals, and I spent 90 minutes trying to reproduce the original March result.

The rule I took from that failure: if deleting a row changes a reported total, I record why before the row leaves the data.

## Decisions Become Rows

I moved the cleaning rules into a SQLite table called `cleaning_decisions`. Every row records the rule ID, CSV file, building ID and date range. It also stores the affected row count and the person who approved the change.

The current schema has seven columns:

```sql
CREATE TABLE cleaning_decisions (
    rule_id TEXT,
    input_file TEXT,
    building_id TEXT,
    date_start DATE,
    date_end DATE,
    affected_rows INTEGER,
    approved_by TEXT
);
```

For an obvious defect, I use a shared rule ID. For a judgment call, the ID references one discussion. The first decision, `R-003`, covered 1,412 meter tests run on 14 February 2026. Those readings were valid measurements of a test, so we excluded them from consumption rather than treating them as zero use.

This structure made the choices reviewable. Elena from the cooperative could read 23 decision rows in ten minutes, and she could approve them without opening Python. On 2 April she found one date range that crossed a billing-month boundary. We corrected the range, reran the build and got 41 rows back.

## Missing Values and Duplicates

The six exports contained three kinds of missing data.

Each kind got its own treatment:

- blank fields stayed missing until the monthly aggregation
- estimated readings kept an `is_estimated` flag
- meter faults got a rule ID and were excluded

The April export alone had 3,187 blank fields, 744 estimated readings and 96 meter faults. A blank reading lacks an observation, an estimate has lower confidence, and a meter fault records a failed measurement. Treating them the same produced monthly totals that looked certain because they had no gaps.

Duplicates were harder because three systems use different timestamp precision. The same reading can appear at 06:00 in one export and at 06:00:00 in another. I normalize timestamps to UTC and minute precision, then keep the record whose source is marked canonical.

If two records remain, the build fails and writes a candidate list to a file named `duplicate_candidates`. That deliberate failure turned 11 silent duplicates in March into 11 reviewable decisions in April.

## Normalization With Evidence

Building names caused 64 of the first 100 discrepancies because the same 44-unit building appeared as `Building 12`, as `bldg_12` and with surrounding spaces. I replaced handwritten mapping code with a small mapping table and moved normalization to the start of the build.

The mapping table contains only evidence-backed rows:

```text
raw_name,business_id,evidence
bldg_12,B-012,billing export and meter register
Building  19,B-019,meter register and owner letter
HVAC Meter A,B-980,installation report
```

Unit conversion lives beside the mapping. The two older billing systems report kilowatt-hours, while the newest reports megawatt-hours. We don't infer the unit from column values because two small buildings had peak readings under one megawatt-hour. Instead, each input file has a declared source unit, and the loader checks that column against its declared unit.

On 19 April the check rejected one file. Its unit column said megawatt-hours, but 2,204 rows were clearly in kilowatt-hours. The cooperative confirmed that their export tool had changed on 12 April. The failed check gave us the right conversation three weeks before month-end reports.

## Tests Before Reports

I kept the pandas code, but made it a script called `build_monthly_readings.py` and put it under version control. The script reads the mapping table and the decision table, then writes `monthly_readings.parquet` and `provenance.json`.

The checks run before any report is built:

- every raw row is absent, present once or referenced by a decision
- every building ID resolves to exactly one meter register entry
- monthly totals reconcile to the canonical source within 0.1%
- decision rows never overlap on one building and date range

The first full test run caught decision ranges I had copied incorrectly and one report query that filtered estimates by accident. Fixing those took 55 minutes. The same checks now take 41 seconds on all 218,870 rows through April.

I still read the monthly table before publishing it. The checks protect me from arithmetic mistakes and silent exclusions. They don't decide whether a building closure should change the comparison basis.

## Lessons From Clean Data

The project now has one build script, two reviewable tables and one provenance file. Preparing April took 3 hours and 20 minutes, compared with two days for March. Elena approved every exclusion before the report went out, and no one asked me to explain a disappeared row.

The provenance file is deliberately boring. It names each input's checksum, row count, cleaning-script commit and decision-table version. When a number changes next month, I can answer whether the meter data, the cleaning rules or the report query changed.

Cleaning is a set of decisions about evidence. A notebook can perform those decisions, but only a record can preserve them. I'll write about the monthly anomaly review after we finish the May run. If you want to follow along, don't forget to subscribe.
