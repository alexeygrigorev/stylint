# Adding Chapters to Course Videos from Transcripts

This synthetic style exercise follows a fictional course project with invented details. Every name, count, and timeline below is fictional, and none of it describes real events. Last spring the project held 14 recorded lessons with transcripts and no chapter markers.

I published the lessons on a course page where each video ran 40 to 70 minutes. Students kept asking for timestamps, and I kept answering the same questions by email. I knew chapters would help, and I had postponed the work for two months.

In March I downloaded all 14 transcripts from the video host as plain text files. Each transcript included word-level timestamps, which gave me 41,000 timed lines in total.

In this post, I'll share:

- why manual chapter markers kept slipping
- how pause gaps became segment boundaries
- how each chapter earned a title and link
- what the quality check across videos showed
- what the pass cost and what still needs work

## Manual Markers and Missed Boundaries

My first attempt was fully manual, and it stalled after three videos. I opened each video, scrubbed through the timeline, and typed timestamps into a notes file. Each video took about 50 minutes, and the markers drifted by a minute or more.

The inbox told the same story every week. Four or five students asked where the deployment demo starts, and two more asked where the Q and A begins. I answered each email by rewatching the video, which added another 20 minutes per question.

The rule I took from that week: manual timestamps rot when the video gets re-exported. I re-exported one lesson with a fixed intro, and every marker after minute two shifted by 11 seconds.

## Pause Gaps as Segment Boundaries

I switched to transcripts because every lesson already had word-level timestamps. A pause longer than 2.5 seconds usually meant I had finished one thought and started another.

The naive version didn't merge short segments, so demos shattered into fragments. A fixed threshold doesn't fit every lesson, so the gap stays configurable per video.

I grouped transcript lines into segments with one short Python script:

```bash
uv run python scripts/split_chapters.py --gap 2.5 --min-len 90
```

The script reads the timed lines, cuts at long pauses, and drops segments under 90 seconds. It wrote 87 candidate segments across the 14 lessons in about 40 seconds.

Short pauses inside demos created false cuts, so I merged segments under 90 seconds with neighbors. That merge step cut the count from 121 rough segments to the final 87. There's a gap here - the gap between raw timestamps and usable chapters, and the merge step closes most of it.

## Titles and Links for Each Chapter

Raw boundaries are useless without names, so I generated one title per segment. I fed each segment transcript to a local model with a strict instruction to use eight words or fewer.

The first titles were generic, and eleven of them started with the word Introduction. I added the lesson topic to the instruction, and the repeats dropped to two. I can't trust auto titles blindly, so every title gets a glance before publishing.

Each chapter line in the export now holds three fields:

```text
00:04:12 | Loading CSVs with pandas | #loading-csvs
00:11:47 | Handling missing timestamps | #missing-timestamps
00:19:03 | First groupby aggregation | #first-groupby
```

The anchor links jump to the matching lesson notes, which I already publish per lesson. Readers can copy a chapter link straight from the course page. It's tedious work, and it caught boundary errors the script never flagged.

## Quality Check Across Fourteen Videos

I checked every chapter by hand because bad timestamps annoy students more than missing ones. The check took three evenings, about six hours in total, for all 87 chapters.

My evening review sorted all 87 chapters into four outcomes:

- 61 chapters with correct boundary, title, and link
- 14 chapters with a boundary off by under 30 seconds
- 8 chapters with a vague title I rewrote
- 4 chapters I merged with a neighbor

I fixed all 26 imperfect chapters, and the second pass took another two hours. Two boundaries stayed arguable, and I left both where the demo starts. I've reused the same script for workshop recordings since April, with the same gap defaults.

## Cost and Remaining Gaps

The full pass cost about eight hours of my time and zero dollars in services. The model ran locally through Ollama, so there's no API bill to report.

Three gaps remain on my list for the next cohort:

- re-exported videos shift timestamps by a few seconds
- demo-heavy lessons still produce extra segments
- translated captions need separate chapter files

Re-exports are the painful one, and I'll rerun the script after each export from now on. The rerun takes under a minute, so the cost is attention rather than compute.

## Lessons From the Chapter Pass

The project taught me a narrower lesson than automate everything with transcripts. Pauses contain real structure, and a simple gap rule beat my manual scrubbing.

I use chapters on every new lesson now, and students cite timestamps in questions. Email questions about locations dropped from five per week to roughly one.

I'll write about caption translation in a future post with real numbers. If you want to follow along, don't forget to subscribe.
