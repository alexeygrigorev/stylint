# Converting an Article Draft into a Podcast Script

I wrote this synthetic style exercise as a build log, and all project details are fictional. In January 2026 I tried to turn a 1,600-word draft about Postgres backups into a podcast episode. The text-to-speech engine read two code blocks and one URL out loud, and I deleted the recording after four minutes.

An audio feed had sat on my wish list for about a year. I listen to two shows on the tram, and I wanted the same option for my own archive of 40 articles.

In this post, I'll share:

- why raw markdown reads badly aloud
- what my first conversion script got wrong
- how the script adds spoken transitions and clean examples
- how the pronunciation pass fixes names and numbers
- where the pipeline stands after six episodes

## Drafts That Read Badly Aloud

My January draft followed the usual build-log format. It had nine headings, 14 lines of bash, and it quoted numbers like 1,840 and 30 to 45 minutes. Every one of those features works on the page, and every one of them fails when a voice reads it.

The engine handled plain sentences without trouble. But it read "bash" as a word, spelled out a link URL character by character, and turned the heading "Rollback Drill" into a confusing interruption. A parenthetical aside like "(successfully bricked it)" came out as a stage direction.

The worst moment arrived at the first code block. The engine pronounced `pg_dump` as three blunt syllables, and I stopped the playback there.

## First Conversion Attempt

My first attempt was a 20-line Python script that stripped nothing and fed the raw markdown to the engine. The episode ran 41 minutes for a text that takes about 11 minutes to read. I had shipped a file converter when the job was a rewrite.

The 41-minute file made the money problem obvious too. The synthesis service charged by the character, so narrating code cost about $0.30 per episode and delivered nothing a listener could use.

The mistake was treating audio as a formatting problem. The rule I took from it: the script has to speak for every element the listener can't see.

## Spoken Transitions And Cleaned Examples

In February I rebuilt the approach as a two-step pipeline. A script I call `spoken-draft`, a small Python program that rewrites markdown for listening, produces a plain-text episode script. The engine then reads that script instead of the original draft.

Headings come first, because they decide the episode structure.

The script turns each heading into a spoken line that names the section and connects it to the previous one:

```text
heading:  Rollback Drill
spoken:   The next part is the rollback drill I ran in March,
          and it caught two missing indexes.
```

The generated line reuses the first sentence under the heading, so the transition never invents claims. When the first sentence already works as a bridge, the script keeps it unchanged. Across the six finished episodes, about half of the transitions needed a human edit, and those edits took a minute each.

Code blocks get the opposite treatment. Each block collapses into one spoken sentence that says what the command does, and the command moves to the show notes. For the backup chapter, the spoken line says that a nightly `pg_dump` job copies a staging database. That sentence takes 20 seconds to say and replaces 14 lines of narration.

Examples inside sentences needed trimming too. My drafts hedge a lot, and hedges sound worse than they read. The script keeps one number and drops phrases like "about 50, maybe even 60".

## The Pronunciation Pass

Names and numbers needed their own pass, because the engine guessed and guessed differently each time.

I fixed this with a lexicon file called `say.json`, a small list that maps written tokens to spoken forms:

```text
"Postgres": "post gress"
"pg_dump":  "P G dump"
"Cron":     "kron"
"1,840":    "one thousand eight hundred forty"
```

The script applies the lexicon before synthesis, so every episode says the same name the same way. The file has 23 entries as of May 2026, and most of them arrived after listener complaints. One listener asked in March whether I was saying Postgres or "post grace", and both pronunciations had appeared in the same episode.

Numbers outside the lexicon get generic handling. The script spells out ranges like 30 to 45 minutes in words, because the engine pauses oddly before bare digits.

One last check trims sentences. Spoken sentences over about 20 words sound breathless, so the script splits them at the first comma when both parts keep a verb. This check caught 11 sentences in the January draft and made the retakes far rarer.

## Current State Of The Pipeline

Six episodes exist as of August 2026, and the whole pass takes about 50 minutes per post. The rewrite step costs 20 minutes, synthesis adds 8, and I spend the rest listening at 1.5 speed with a notepad.

Two limits showed up in listener messages. Jokes that work on the page die in audio, and emphasis never survives the transfer. The intro music I added in June sounded like a router rebooting, so it lost its slot in July. The pipeline also assumes my own draft structure, so a guest post with different headings needs an hour of manual cleanup.

The episode work still beats the old alternative, which was no audio feed at all. The rule I took from it: write for the page first and rewrite for the ear afterwards. I'll write about the show-notes generator in a future post. If you want to follow along, don't forget to subscribe.
