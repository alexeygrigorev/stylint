# Classifying Files in a Messy Intake Folder

I wrote this synthetic style exercise as a build log, and all folder names, counts, and dates in it are fictional. In January 2026 the intake folder on my home server held 1,240 files with no subfolders at all. Finding an invoice from February 2025 meant scrolling a flat list sorted by nothing in particular.

The folder collects whatever arrives, from printer scans to bank exports to ad-hoc CSV downloads. It had been flat since I set it up in 2023, and every tool I own can write to it. In February I needed one specific invoice and spent 25 minutes scrolling for it.

The mess cost more than time. Twice in 2025 I paid a bill late because its invoice arrived in that folder and sat unseen for three weeks.

In this post, I'll share:

- what the folder looked like before the classifier
- why sorting by extension failed
- how the rules and confidence scores work
- how manual moves become new rules
- where processed files go and what still fails

## Twelve Hundred Unsorted Files

About 400 of the files were PDFs, 310 were images, and the rest were CSV exports and assorted downloads. The names told me almost nothing, because the printer produced `scan_0093.pdf` and the bank produced `export (3).csv`. Purpose lived in my head, and my head was the only search index.

## Sorting by Extension

My first attempt was a ten-line shell loop that made four folders and moved files by suffix. It ran once, moved 1,180 files, and looked great for two days.

The sort put a bank statement beside a scanned warranty, because both end in `.pdf` and nothing else about them matches. By the weekend the intake folder had 40 new files sitting unsorted at the top level, and my invoice was still missing.

The rule I took from that week: classify by purpose first, and only then by file type.

## Rules With Confidence Scores

In March I wrote `intake-sort`, a Python script that scores every file against a list of rules. Each rule names a piece of the file name or sender, a target folder, and a confidence between 0 and 1. I wrote the first 20 rules in one evening from a frequency list of the 30 most common name prefixes.

The first entries in `rules.yaml` look like this:

```text
- name_contains: "invoice"
  target: money/invoices
  confidence: 0.90
- sender_contains: "city utilities"
  target: money/utilities
  confidence: 0.95
- name_contains: "screenshot"
  target: screenshots
  confidence: 0.80
```

At 0.9 or higher the file moves without asking me, between 0.5 and 0.9 it moves to review, and below 0.5 it stays put. When two rules match, the higher confidence wins, and ties go to the longer name match.

Running the sorter is one command:

```bash
python intake-sort.py --scan ~/intake --apply
```

Without `--apply` the script prints the plan and touches nothing, which is how I ran it for the first week. With the flag, the scan on 2 March found 1,420 files, because two months of arrivals had followed the January count.

```text
scan: 1420 files
auto-move: 1090
review: 210
stay: 120
```

I read the review pile over two evenings of about 30 minutes each and agreed with 188 of the 210 proposed moves. The rest went back to the intake folder, and eleven wrong moves taught me to lower two confidences to 0.8.

## Overrides From Manual Moves

Every manual move from the review folder appends a line to `overrides.yaml`, a second file that pairs the file name with the target folder. Nothing gets deleted, and nothing moves twice.

Once a month I read the overrides and promote the repeated ones into rules. In March I promoted 11 overrides, and the weekly review pile shrank from about 60 files to about 15.

The overrides file also keeps me honest about near-misses, because a bad promotion shows up as a repeat within days.

## The Processed Archive

A moved file keeps its name and gains a dated home under `~/intake/processed/`, in subfolders like `2026-07/money/invoices`. The archive is plain folders by month, so any backup tool can sync it. A monthly cron job closes each month with a one-line index, so `2026-07/index.txt` lists every file that moved. The invoice from February 2025 now takes about 30 seconds to find, because money has one level of subfolders and nothing else.

## Remaining Blind Spots

The classifier reads names and senders, so a scanned invoice named `scan_0142.pdf` ends up in review every time. An OCR pass would fix that. I haven't built one, because the review folder now collects only about 15 files a week and empties in five minutes.

Matchless files are the second blind spot. About 120 files matched nothing on the first scan, and a few new ones still match nothing every month. They sit in the intake folder until I notice them, which is honest but slow.

New senders are the third gap, and the overrides file catches most of them within their first two emails. What it catches is a guess until I promote it, and the guess is right about nine times in ten.

The arc ran from January to April. A flat folder of 1,240 files became 34 rules, one review folder that empties in five minutes, and an archive sorted by month and purpose. The rule from the extension week still runs the whole thing: classify by purpose, and only then by type.

I'll write about the OCR layer if I ever get to it. If you want to follow along, don't forget to subscribe.
