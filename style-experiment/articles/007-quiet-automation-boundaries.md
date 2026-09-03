# I Stop Automating a Writing Workflow

I wrote this synthetic style exercise as an analysis piece with fictional details, not real events. In March I counted 184 draft fragments across three folders and felt the pull to automate every step. The notes held interviews, terminal snippets and half-formed outlines from six months.

Automation had already saved me hours on transcription and formatting. I used Whisper for voice notes and a small Python script for cleanup. Those steps felt safe because mistakes were easy to spot and cheap to fix.

Selection felt different from the start. Choosing which idea deserved a full draft required judgment about audience, timing and proof. I didn't want a script making that call for me.

In this post, I'll share:

- why transcription and cleanup were easy to automate
- how selection broke the first automated workflow
- what editing passes stayed manual after testing
- which publication checks I kept human
- what automation I keep today

## Drafts That Wrote Themselves

My first workflow covered everything from voice note to published draft. I recorded ideas on walks, transcribed them overnight and let a coding agent group fragments by topic. The agent then proposed outlines and opened draft files in `~/notes/articles`.

Volume went up immediately across the next twelve days of runs. The chain produced 23 outlines in twelve days from 61 voice fragments. Each outline had a title, three claims and supporting quotes from the transcripts.

Quality dropped just as fast across those twelve days of output. Only four outlines matched questions readers had actually asked in comments. Six outlines combined unrelated fragments into confident arguments that fell apart on review.

The rule I took from those two weeks: automation multiplies output before it improves judgment, and judgment decides what deserves output.

## Selection Needs a Human

Selection means choosing one idea from many and accepting the cost of ignoring the rest. I tried to score ideas with counts of mentions, recency and keyword overlap. The scoring script ran in 11 seconds across 184 fragments and ranked every idea.

The top-ranked idea in March mentioned Postgres indexes nine times across four weeks. It looked strong on every count. It lacked a concrete failure or measurement I could show, so readers would have gained little from it.

A lower-ranked fragment mentioned a 34-minute outage caused by a missing index on a 2.1 GB table. It appeared only twice in the full set of transcripts. That fragment became a draft because it had a timeline, a cost and a fix I had tested.

I now select manually every Sunday in about 25 minutes. I read the newest 20 fragments and mark two candidates in a file called `candidates.md`.

My selection notes cover these points:

- the reader problem in one sentence
- the proof I can show from my own work
- the reason this week is a good time

No script writes those three lines for me. I tried scoring again in April with different weights, and the top pick still missed the human context. Selection stays manual because it asks what matters, not what repeats.

## Editing Passes I Kept Manual

Editing looked like a good target for automation after selection failed. I asked the coding agent to tighten sentences, cut filler and align headings with the outline. The agent processed a 1,400-word draft in 47 seconds and returned cleaner text.

The cleaner text lost specifics. The agent replaced "34-minute outage on a 2.1 GB table" with "brief outage on a large table". It changed "Whisper small model, 38 seconds for four minutes" into "fast transcription". Each edit removed evidence readers use to trust the piece.

I reverted those changes and built a narrower checklist instead. The agent now flags long sentences, repeated openers and missing file paths. It doesn't rewrite sentences on its own. I make every edit in my editor after reading the flags.

The current editing flow uses three short commands:

```bash
uv run python scripts/check_draft.py drafts/current.md
```

That command prints sentence lengths, repeated openers and missing concrete details. I read the report in about five minutes and edit for another 30 minutes.

These checks don't change my words. They show me where evidence is thin, and I decide how to fix each gap. Editing stays manual because clarity comes from choices about what to keep.

## Publication Checks Before Sending

Publication felt safe to automate because it looked mechanical. I wrote a script that checked links, copied the draft to my blog folder and set the publish date. The script ran in nine seconds and never complained.

It published a draft with a broken install command in April. The command referenced `pip install whisper-small`, which doesn't exist as a package name. Three readers wrote in within two hours, and I spent the evening correcting the post and replying.

The failure was mine for letting the script publish without a final read. The rule I took from it: a human reads the rendered post once before anything goes live.

My publication checklist lives in `publish.md` and takes twelve minutes. I open the preview, click every link and run every command in a terminal.

The checklist covers these final items:

- every command runs without edits in a clean shell
- every file path matches the repository layout
- every number matches the source note or log
- the opening names a concrete event with a date

I still use a script for copying files and stamping dates. The script doesn't decide readiness. I mark the draft ready by renaming the file from `draft.md` to `ready.md` after the manual pass.

That rename takes two seconds and records my whole decision. Automation moves files after I choose, and it never chooses for me.

## Automation I Keep Today

Today the workflow splits cleanly between machine steps and human steps. Machines transcribe, count and copy files. I select, edit and approve every piece that reaches readers.

Transcription runs through Whisper on my ThinkPad with 32 GB of RAM. A four-minute note takes about 38 seconds to process.

Selection takes 25 minutes on Sundays across the newest 20 fragments. Editing takes about 60 minutes per draft with agent flags as input. Publication review takes twelve minutes with the preview open.

The split taught me a narrower lesson than "automate everything". Automation fits steps where errors are visible and cheap. Judgment belongs where errors mislead readers or waste their time.

I'll keep testing new steps in trials with ten drafts at a time. If you want to follow along, don't forget to subscribe.
