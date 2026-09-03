# A Pipeline for Turning Course Recordings into Searchable Notes

I wrote this piece as a synthetic style exercise. Although the recordings, dates, and measurements are fictional, the pipeline follows the steps I would use on a real course.

In September 2026, I finished teaching a 12-session data engineering course. The recordings totaled 19 hours and 42 minutes, and they sat in one folder named `course-final`. Students asked for searchable notes, so I built a local pipeline that turned the videos into sectioned summaries and quiz questions.

In this post, I'll share:

- how I prepared and transcribed the recordings

- how I split transcripts into useful sections

- the summary format we tested with students

- how quiz questions were generated and reviewed

- what the search index still misses

## Prepare the recordings first

The original folder had inconsistent names such as `DE-2026-09-03.mp4`, `week 3 final.mov`, and `postgres ingestion.mp4`. Before transcription, I normalized 12 files into a simple schema: `session-01-intro.mp4` through `session-12-project-review.mp4`.

I also extracted audio with `ffmpeg` and removed four minutes of dead air from each recording. That reduced total audio length to 18 hours and 12 minutes. More important, it gave the transcription step cleaner boundaries.

The first transcription attempt used automatic speech recognition on each full file. It produced useful text, but timestamps drifted by 4 to 11 seconds after music intros and screen-sharing pauses. Those errors made section lookup frustrating.

So I changed the input. I split each video at detected silences, transcribed 20-minute chunks, and reattached timestamps by chunk offset. The worst drift fell to about two seconds. Total transcription time was 3 hours and 20 minutes on a local workstation.

## Split content by teaching sections

A transcript is a terrible unit for studying. One 96-minute session can contain a review, three concepts, two demonstrations, and a question period. I wanted sections a student could open before rewatching a segment.

I used a three-pass process, beginning when a script detected slide changes and long pauses. A model then proposed boundaries using the transcript, course syllabus, and slide-change times. Finally, I reviewed every boundary for all 12 sessions.

The model proposed 87 sections. I accepted 64 unchanged, moved 19, merged 8, and split 6. The most common problem was treating a student question as a new topic. I added a rule that questions remain with the section that triggered them.

Each section has a stable record with five fields:

```text
session-03__002__postgres-copy
start: 00:31:20
title: Loading CSV files with COPY
type: demonstration
video: session-03-postgres-ingestion.mp4
```

That record is small, but it makes the note linkable. A student can jump to 31 minutes and 20 seconds without searching through the full session.

## Summaries keep the teaching order

Our first summary experiment produced polished explanatory text that erased the lesson structure. It often combined the instructor's mistake, the corrected explanation, and the student discussion into one abstract paragraph.

We tried a stricter format. Each section now has a two-sentence purpose statement, a numbered walkthrough, an example with exact command names, and a "common mistakes" list. The output is longer, but it maps directly to the recorded segment.

For the `COPY` section, the summary includes the command and required file path. It also covers delimiter handling and one warning about header rows. Finally, it links the failed command from the live demonstration, because that mistake generated the best questions.

I reviewed all 89 final sections in four passes of about 22 sections. Review took 9 hours and 15 minutes, more than half of the project time. Automatic drafting was cheap, while checking technical accuracy and teaching order was the real work.

Students tested the notes during a revision week. Eight of ten said the numbered walkthroughs were most useful, while six wanted shorter summaries. We kept the longer format but moved the purpose statement to the top so it could stand alone.

## Generate quizzes for review

For each section, we generated three question types:

- one recall question about a definition or command

- one application question using a small dataset

- one mistake diagnosis question based on a known error

The model produced 267 questions, and I rejected 81. Forty-one had ambiguous wording, while 22 assumed an untaught tool. Another 18 had incorrect expected output, and 19 needed a narrower data example.

Human review used a simple rule. A question passes only if a student can answer it from that section and its linked video segment. We also required one exact expected answer or a testable output range.

The remaining 167 questions went into a JSONL file with section IDs and difficulty labels. The course site chooses three questions per section during revision. When a student answers incorrectly, it links back to the exact recording timestamp.

## Search and the remaining gaps

The search index contains section titles, purpose statements, walkthrough text, and quiz questions. It also contains transcript chunks. Transcripts are stored separately with timestamps, so search can show both the note and the source video range.

I built the first version with SQLite and a small local embedding model. The index is 410 MB and answers a query in about 120 milliseconds on my workstation. A query for "header row COPY" returns the correct section first and links to 31:20 in session three.

The index still misses cross-session ideas. A student who searches "idempotent loading" finds fragments in four sessions, but the system doesn't yet assemble a learning path across them. Building that graph is the next project.

Another gap is speech recognition noise because column names sometimes came out as ordinary words. We added a course-specific replacement list, but a new term can still slip through until someone reports it.

## Lessons from the pipeline

Clean boundaries mattered more than clever summarization. Stable section IDs, corrected timestamps, and a fixed note format made every later step easier to review.

The project also showed where automation should stop. The model drafted sections and questions, while I checked teaching order, technical accuracy, and whether a question could actually be answered from the course material.

I plan to describe the cross-session learning-path index in a future article. Subscribe if you want to see how the next version handles connections between sessions.
