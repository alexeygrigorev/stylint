# Turning Podcast Notes into a Course Module Draft

I wrote this synthetic style exercise as a build log, and all project details are fictional. In April 2026 I recorded a 52-minute podcast episode about evaluation datasets. Its notes became the raw material for module 4 of my small testing course.

The episode produced 7,800 words of transcript and 6 pages of handwritten notes. In my course, a module is a markdown file with claims, two exercises, three examples and a ten-question assessment. Writing one by hand used to take me two evenings.

In this post, I'll share:

- how the transcript and notes became raw material
- why one prompt over the full transcript failed
- how the claims pass extracts statements with evidence
- how exercises and examples come out of the claims
- how the assessment maps to the claims
- what two modules cost after the change

## Podcast Notes As Raw Material

The transcript had a structure I didn't expect. Real claims arrived buried inside stories, and my handwritten notes held only 11 of the 43 claims the episode actually made. The notes also included timestamps, which later became the bridge back to the audio.

A module needs claims before it needs explanations, so I treated the episode like a source document instead of a draft. That decision shaped everything after it.

Module 4 sits in the middle of the course, and it needs the practical tone the episode already had. Reusing a recorded conversation also keeps the guest's voice in the course, which my own summaries always flattened.

## One Prompt Didn't Work

My first attempt skipped structure entirely. I pasted the transcript into Claude Code and asked for a course module about evaluation datasets.

The draft came back in 70 seconds with 1,600 words of smooth text. Two exercises covered topics the episode never mentioned, and zero quotes came from the actual conversation. It read like a generic article with my title on top.

My mistake was asking for a finished module from raw talk. The rule I took from it: separate the claims from the teaching before any writing starts.

## Claims With Evidence

The pipeline now starts with a claims pass. A script splits the transcript into 10-minute chunks and sends each chunk to the agent with the same prompt.

The prompt fits in five lines:

```text
From this transcript chunk, list every claim about evaluation.
For each claim, quote the exact sentence as evidence.
Mark claims without a quote as unsupported.
Ignore introductions and small talk.
Output one markdown row per claim.
```

The April episode produced 43 claims, and 9 of them came back unsupported. The 43 rows took me 25 minutes to review, and I cut 12 rows that repeated the introduction. Each kept row went into `module-04/claims.md` with its timestamp. When a reader wants the original wording, the timestamp points back to the minute in the audio.

## Exercises And Examples

Claims don't teach on their own, so the module format fixes the counts at two exercises, three examples and one worked answer per exercise. Each exercise needs a task the reader can fail at, and each example needs a number the reader can check.

Two unsupported claims became exercises. One asks the reader to explain why 95% accuracy means little without the class balance. The other reuses the episode's story about a mislabeled validation set.

One exercise from the April draft shows the format:

```text
Exercise 2
The validation set in evals/case-study-3 holds 4 mislabeled rows.
Task: find them, and give the accuracy before and after.
Answer format: two numbers and two sentences.
```

The examples come from the guest's own projects, with names and numbers changed. Readers get a concrete case to check, and the guest keeps the credit in a footnote. The worked answer for each exercise lists the command or the calculation, so a stuck reader can check the path instead of the result alone.

## Assessment And Rollout

Each module ends with ten questions, and eight of them map to a specific claim row. Every question names the claim it checks, so a wrong answer tells me which claim failed to teach.

A question from the draft shows the mapping:

```text
Q7: What recall did the baseline reach in the case study?
Checks: claim 22 - baseline recall of 61% before rebalancing
```

I taught the module twice in May to two study groups of 6 people. The first run sent three questions back to the claims pass, and the second run needed no corrections. Both runs took 90 minutes, and the claims mapping made grading fast. A wrong answer pointed at one row, and I fixed the row instead of rewriting the whole question set.

## After Two Modules

The pipeline turned one 52-minute episode into a teachable module in about three hours of my time, against two evenings of manual work before. The stages stay boring on purpose: claims, exercises, examples, assessment.

Two limits remain, and both showed up in April. The claims pass still misses claims told as jokes, and I added 2 of those by hand. The assessment also repeats my question style, because one writer wrote both sides, and a second reviewer would catch that.

I'll write about reusing the same pipeline for conference talks in a future post. If you want to follow along, don't forget to subscribe.
