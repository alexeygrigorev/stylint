# Versioning Workshop Materials Between Cohorts

I wrote this synthetic style exercise as a how-to guide, and the workshops, dates and numbers are fictional. Since October 2025 I've run the same two-day data engineering workshop for four cohorts of 18 to 31 people. In the February cohort, three attendees downloaded the previous solution pack and ran it against the new dataset. The room watched the errors pile up.

If you teach the same workshop more than once, you need a versioning system that survives eager attendees. The four steps took about an hour to set up and now cost about 20 minutes per cohort.

In this post, I'll share:

- how we give every exercise a stable ID
- how we keep a one-page changelog
- how we mark compatibility before each cohort
- how we archive a snapshot per cohort
- the caveats I've collected since October

## 1. Give Every Exercise A Stable ID

Each exercise folder gets an ID that never changes, such as `ex-03-window-functions`. You can rewrite the content as often as you like, but the ID stays put across cohorts. Attendees compare notes between runs, and the ID is what they reference when they write to me three months later.

We number exercises in teaching order, so the ID also encodes position in the schedule.

A quick look inside the repo shows the naming scheme:

```text
exercises/
  ex-01-basic-selects/
  ex-02-joins/
  ex-03-window-functions/
  solutions/ex-03-window-functions.py
```

When two exercises merge, the surviving one keeps its ID and the retired ID never comes back. In February I reused an old ID after merging two exercises, and three attendees ran a solution against the wrong dataset. The rule I took from it: never recycle an exercise ID, even after a merge.

Numbers also leave gaps on purpose. When cohort 2 asked for an extra SQL task, it became `ex-04a-date-handling`. The letter suffix kept the teaching order intact and spared me from renumbering eight folders.

## 2. Keep A One-Page Changelog

We keep `CHANGELOG.md` at the repo root, newest first, one line per change:

```text
## 2026-02-14 - cohort 4 prep
- ex-03: dataset swapped to taxi rides from March 2026
- ex-07: removed and merged into ex-06
- ex-11: new retry task requested by cohort 3
```

A single line per change keeps the file readable at two in the morning before day one. We write the entry the same evening as the change, because backfilled changelogs forget the reasons. Nine entries cover the four cohorts so far, and every one of them names the exercise ID it touches.

The changelog doubles as my planning list for the next run. Entries tagged with an attendee request get priority, and two of the nine changes so far came directly from feedback forms. When I skip a requested change, the entry says so, and the requesting attendee hears the reason from me instead of discovering it mid-exercise.

## 3. Mark Compatibility Before Each Cohort

Every solution file has a header comment naming the earliest dataset it works on, such as `works-with: 2026-02-14`. The header costs one line, and it turns "does this solution still work" into a comparison instead of a guess.

Before a cohort starts, we run a check script against the attendee pack:

```bash
python check_compatibility.py --pack packs/cohort-2026-03.zip
```

The header date refers to the changelog entry that changed the dataset. That keeps a single date format across the whole repo, and it saves me from decoding two conventions every spring.

The script compares exercise IDs in the pack against solution headers and prints every mismatch with a file path. In March it caught two stale solutions that would have failed at runtime on day two, and fixing them took ten minutes.

## 4. Archive A Snapshot Per Cohort

The evening before day one, we tag the repo and export a zip of the exact state:

```bash
git tag cohort-2026-03
git archive --format=zip -o archives/cohort-2026-03.zip cohort-2026-03
```

The zip goes to object storage, and the tag stays in the repo for the next round of edits. Late joiners now get a download link to the exact files the rest of the room uses, which ended the February problem. Four cohorts have produced four zips of about 34 MB each.

The archive command takes seconds, so the ritual fits between dinner and a final check of the signup list. I also drop a `COHORT.md` note into each zip with the attendee count and the dates of both sessions. A year later, that note answers more questions than the rest of the archive combined.

## Other Tips

Four practical notes from running this since October:

- archives add up, so we keep the last three zips on the laptop and push the rest to storage
- the changelog decays mid-course, so we pair writing it with the evening commit
- attendees find old exercise IDs in older blog posts, and stable IDs send those references to the right exercise
- if you run fewer than two cohorts a year, a dated zip folder probably covers most of this

The last point matters as a de-escalation. You don't need git tags, a check script and object storage to run a workshop twice. You need the stable IDs and the discipline to write down what changed.

## Four Cohorts Later

The setup costs about an hour to build and roughly 20 minutes per cohort, and it has run without an ID collision since March. The changelog still depends on my evening discipline, and a missed week shows up as a gap attendees notice before I do. For the next cohort I want the compatibility check to run in CI on every push, so stale solutions fail before packing starts.

I'll write about how I design the exercises in a future post. If you want to follow along, don't forget to subscribe.
