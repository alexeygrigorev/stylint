# Extracting Structured Data from Course PDFs

This synthetic style exercise follows a fictional course project with invented details and numbers. Last February I inherited 214 course PDFs from two older cohorts and needed structured lesson data. The files held slides and assignments across nine messy years with mixed layouts.

I wanted one clean JSON record per lesson with title, date and author. The PDFs had grown organically since 2017, and no two years shared the same layout. Some files were text exports, some were scanned images, and a few were slide decks with notes.

My first instinct was to parse everything in one pass and fix errors later. That instinct cost me two evenings, and I relearned an old lesson about validation order. I should have built the review step before scaling the parser.

In this post, I'll share:

- why the first parser produced confident garbage
- how layout detection split text, scans, and slides
- what the validation rules catch before human review
- how the review queue keeps decisions fast and consistent
- what the export format looks like and where it still breaks

## Course PDFs on Disk

The archive lived in one shared folder with 214 files and 1.9 GB of history. File names mixed dates, initials and version tags from hurried uploads. A typical name looked like `ml2023_week4_v2_final.pdf`, and three files shared that exact name.

I listed every file with size, page count, and text layer presence. That inventory took one Python script and about six minutes on my ThinkPad. The numbers gave me a map with 148 clean files, 41 scans, and 25 slide decks.

The inventory also exposed duplicates I hadn't expected to find there. Eleven files were byte-identical copies under different names, and six more differed only in their cover page. I removed the exact copies and kept a small alias file so old links still resolve.

Those counts shaped the plan more than any parser design could have. Text files needed layout logic, scans needed OCR, and slides needed a separate path entirely. I split the work into three lanes and tracked each lane in its own SQLite table.

## First Parser Attempt

The obvious choice was a single Python script with a PDF library I already knew. I picked `pdfplumber` because I had used it in a prior workshop and trusted its table output. The script read each file and pulled titles from the largest font and wrote one JSON record per file.

The first run processed all 214 files in about eleven minutes and produced 214 confident records. I opened twenty records at random and found nine with wrong dates and four with merged titles. The script had treated every two-column page as one wide column, so reading order collapsed.

I had skipped the layout check, and that omission broke nearly every downstream field. The rule I took from that evening: read order comes before field extraction, and no regex fixes a scrambled page.

The fix started with a small classifier that labels each page before any extraction runs.

The classifier uses page size, text density, and image count:

```bash
uv run python scripts/label_pages.py --input ./pdfs --db ./lessons.db
```

That command labels every page as text, scan, or slides and stores the label in SQLite. I ran it on the full archive, and it finished in about eight minutes with only nine pages flagged for manual labeling.

## Validation and Review Queue

With page labels in place, I wrote validation rules that reject suspicious records before they reach a human. Each rule is a plain function with a name and a threshold. A record must pass all rules before it leaves the staging table.

The rules catch the errors I kept seeing in the first run:

- missing title or a title longer than 140 characters
- dates outside the 2017 to 2026 course window
- durations below five minutes or above six hours
- author names that match footer boilerplate
- resource links that return connection errors

Records that fail any rule move to a review queue built with FastAPI and one screen per page. Each screen shows the page image, the extracted fields, and three buttons for accept or edit or skip. I kept the layout tight so review stays fast during a long session.

I reviewed 96 flagged records across three evenings in March 2026, spending about 25 minutes per session. Most fixes took under a minute, and only seven records needed a second look with the slide deck open. That's a manageable rate for an archive of this size.

## Export Format That Stuck

I moved accepted records to a clean table with one row per lesson and stable identifiers. Each lesson gets an identifier like `ml2023-w04` plus title, date, and author. I freeze that table before every export so reruns stay comparable.

The export is one JSON file per cohort year plus a small index file.

A sample record uses six fixed fields:

```text
id: ml2023-w04
title: Regularization for small tabular sets
date: 2023-10-18
author: course team
duration_min: 75
resources: slides, notebook, reading list
```

That record layout survived three rewrites because every consumer reads the same six fields. The course site reads the JSON directly, and the search index copies title and summary. I don't add fields without updating all three readers in the same week.

Two gaps remain, and I've stopped pretending they'll fix themselves. Scans with handwriting from 2017 still fail OCR, and slide decks without notes lose the spoken context. Those 31 records hold a flag until someone writes a two-sentence summary.

## Reflections After Three Weeks

The project worked because the review queue arrived early instead of last. I spent roughly fourteen hours total with six hours of review and three hours of parser work. The archive now has 203 clean lesson records with a clear next step for the rest.

This project taught me a narrower lesson than "parse everything with one script". Layout labels decide quality, validation rules protect attention, and a small review screen beats a clever regex every time. I chose tools I already knew, and I accepted the OCR gap instead of chasing perfect coverage.

I'll write more about the alumni search index in a future post. If you want to follow along, don't forget to subscribe.
