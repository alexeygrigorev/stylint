# Using Forum Analytics to Find Confusing Course Material

This synthetic style exercise describes a fictional course project with invented forum data. All names, counts and dates below are fictional, and no real events are reported.

Last spring I helped review a Python course with 1,840 enrolled learners. The forum held 3,214 threads across 12 lessons, and mentors answered about 40 new threads per week. Homework scores dipped in lessons 7 and 9, but nobody knew which pages left learners confused.

I first blamed the homework. Lessons 7 and 9 cover decorators and concurrency, so lower scores felt expected for harder topics. Mentors also reported fatigue, and I assumed difficult material plus tired reviewers explained the dip.

The forum export told a different story. Lesson 4 had the most repeated questions despite strong homework scores, and lesson 7 drew fewer threads than I expected. I decided to rank lessons by evidence from forum behavior rather than by score averages alone.

In this post, I'll share:

- how I pulled view paths and thread counts from the forum export
- why sorting lessons by raw views misled me
- how I grouped repeated questions by lesson and week
- how I compared homework failures against those groups
- what I changed in two lessons and what stayed unresolved

## Forum Exports And First Counts

The forum software exports one CSV row per thread with timestamps and view counts. I downloaded the March export on a Monday morning and found 3,214 rows covering January through March. Each row included a lesson tag, an author id, a reply count and a last-activity timestamp.

I loaded the export into SQLite with a small Python script and ran counts per lesson. ThreadMap, a small Python script that reads the export, printed threads, median replies and median views for each of the 12 lessons. Lesson 4 led with 412 threads, while lesson 11 closed the list with only 96 threads.

The view paths added useful context to those counts. I joined thread views against lesson page views from the course platform logs for the same period. Lesson 4 pages drew 9,800 views against those 412 threads, while lesson 9 pages drew 11,200 views against only 238 threads.

## The Naive Sort By Views

My first ranking sorted lessons by total page views, and lesson 9 came out on top. I told the course team that lesson 9 needed a rewrite because it combined high views with low homework scores. The team agreed, and I spent a full weekend reworking two pages in that lesson.

The rewrite changed nothing in the April cohort. Homework scores in lesson 9 moved from 71 percent to 72 percent across 214 submissions, which is statistical noise. Forum threads about lesson 9 stayed flat at 58 threads for the month.

I had confused attention with confusion. High views can mean strong interest, repeated reference visits or links from other lessons. Lesson 9 pages include a setup checklist that learners revisit, so views pile up without showing trouble.

The rule I took from that weekend: views measure traffic, and only repeated questions measure confusion.

## Grouping Questions By Lesson

The second version ignored views and grouped threads by repeated wording within each lesson. I normalized titles to lowercase, stripped lesson numbers and counted near-duplicate phrases per week. A phrase counted as repeated when it appeared in three or more threads during one week.

The groups exposed lesson 4 as the real trouble spot.

Four phrases repeated across February and March with steady volume:

- install fails on Windows with path errors
- decorator example throws an argument error
- fixture scope confuses setup and teardown
- import error after moving files between folders

Lesson 4 produced 96 threads containing one of those four phrases, which is nearly a quarter of its total. Lesson 9 produced only 21 repeated-phrase threads, and most of them concerned the setup checklist rather than lesson concepts.

I ran the grouping with one command:

```bash
uv run python scripts/group_threads.py --input march.csv --weeks 8
```

The command reads the export, normalizes titles and writes one JSON file per lesson. Each file lists repeated phrases with weekly counts and links to three example threads. The full run takes about 90 seconds on my laptop.

## Homework Failures Against Confusion

Thread groups alone don't prove that confusion hurts scores, so I joined them against homework results. The course stores one row per submission with a lesson id, a score and an error code for failed tests. I pulled 4,620 submissions from January through March for the same 12 lessons.

The join used a simple definition:

```text
match = same lesson id and submission week within 7 days after thread peak
repeated = 3 or more threads sharing a phrase in that week
failure = score below 60 percent on first attempt
```

Lessons with repeated phrases showed first-attempt failure rates between 31 and 38 percent during peak weeks. Lessons without repeated phrases stayed between 17 and 22 percent in the same weeks. Lesson 4 failed 34 percent of first attempts during its worst week, against a baseline of 19 percent.

That comparison deserves a caveat. I matched weeks loosely, so some learners who failed never read the forum threads. A stricter test would join individual learner ids across both tables, and I didn't have that permission in the export. The numbers suggest a link rather than proving one.

My next step narrowed the work to two lessons. Lesson 4 earned a rewrite of its Windows setup page plus a worked decorator example with argument traces. Lesson 9 earned only a shorter checklist, because its threads asked for clarification rather than reporting errors.

## Keeping The Useful Parts

The April rerun gave lesson 4 a calmer forum. Repeated-phrase threads fell from 96 in March to 41 in April across 1,120 enrolled learners. First-attempt failures in lesson 4 dropped from 34 percent to 26 percent, while other lessons stayed near their baselines.

Lesson 9 confirmed the earlier caution. Its shorter checklist cut checklist questions from 21 to 12 threads, but homework scores stayed at 72 percent. Attention never indicated misunderstanding there, and the smaller fix fit the evidence.

The project taught me a narrower lesson than "measure everything". Raw views flatter popular pages, raw thread counts flatter early lessons and only grouped repeats survive both biases. I now run the grouping script monthly, and it takes less than 20 minutes including the read-through.

I'll write about the rewrite checklist in a future post. If you want to follow along, don't forget to subscribe.
