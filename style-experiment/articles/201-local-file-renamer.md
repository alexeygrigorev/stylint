# Building a Renamer for Screenshots and Voice Notes

I wrote this synthetic style exercise as a build log, and all project details are fictional. In December 2025 my screenshots folder held 4,200 files with names like "Screenshot 2025-12-03 at 09.41.13". Voice notes were worse, because the recorder named every file `recording.m4a` and buried it in a folder named by date.

In January 2026 I spent 40 minutes hunting for one October screenshot of an invoice, and the search produced three candidates with identical names. Filenames had become a system I worked around, so I decided to replace it.

In this post, I'll share:

- why the default filenames stopped working
- what my first shell loop broke
- the naming rules the renamer applies
- how the preview step prevents collisions
- where the renamer stands after four months

## Filenames Without Context

The defaults describe the capture event and nothing else. A name like "Screenshot 2025-12-03 at 09.41.13" gives me the date, and then I still open 20 files from that day to find the receipt. Voice notes hid their content completely, so a note about a client review looked identical to one about a grocery list.

Desktop search didn't help either. Image text stays invisible to it, audio stays invisible until transcription, and the only searchable part was the one part with no meaning.

The voice-note side was quantifiably worse. A folder scan in December found 1,900 recordings named `recording.m4a`, spread across 240 date folders. About a third were stale reminders, and the rest were raw material I couldn't match to anything.

## First Attempt With A Shell Loop

My first attempt was a bash one-liner that prepended the date and moved everything in one pass. It renamed 312 files in nine seconds, and it overwrote nine of them, because two screenshots taken in the same minute shared the resulting name. The nine files were gone, and the screenshots app kept no history.

The mistake was renaming in place with no rehearsal. The rule I took from it: never run a mass rename without a dry-run mode that prints the plan first.

The data loss also taught me the second requirement: a renamer has to be boring about collisions. "Same minute, so same name" is a collision factory, because I often take four screenshots in a burst.

I nearly repeated the same move on the voice-note folders that evening. The near-miss is why `renamer.py` got a dry-run flag before it got anything else.

## Naming Rules For The Renamer

In February 2026 I wrote `renamer.py`, a small Python script that applies a fixed name format to a folder of captures.

The format looks like this:

```text
2026-01-14_pqtool_backup-drill.png
2026-01-14_pqtool_backup-drill-2.png
2026-02-02_voice-note_82s_client-review.m4a
```

Every name has the date, the project, and a content slug I type during capture. The project token comes from a list of 11 names I keep in the script. `pqtool` covers the backup utility, `invoices` covers expense paperwork, and the rest follow the same scheme. The slug is two or three words about content, and for voice notes I add the duration in seconds.

When a target name already exists, the script appends `-2`, then `-3`, and so on instead of overwriting. The suffix search runs against the planned names too, so a burst of four screenshots in one minute becomes four distinct files. Durations in voice-note names came from a small metadata read, and the header parse added about two lines of code.

Slugs sound like overhead, but typing two words at capture costs about five seconds and saves the ten-minute hunt later. For screenshots the slug records why I pressed the keys.

## Preview Before Any Rename

The script never moves a file on its first pass. A plain run prints the plan, one `old -> new` line per file, and only a second run with `--apply` touches the disk.

For a test folder of 41 captures, the plan prints like this:

```text
Screenshot 2026-01-14 at 09.41.13.png -> 2026-01-14_pqtool_backup-drill.png
recording.m4a -> 2026-02-02_voice-note_82s_client-review.m4a
```

I read the plan before every apply, which takes under a minute for a normal folder. The review pass has caught three wrong slugs and one wrong project token so far, and each fix cost one edit in the plan file. Because the preview is just text, I can also paste it into a note and keep a record of what moved. The `--apply` run then replays the same plan and prints one confirmation line per file, so the output stays comparable.

## Current State After Four Months

The February cleanup renamed 3,880 files in about 25 minutes, including the slug typing. Four months later the folders hold only well-formed names, and finding that invoice now takes one search instead of 40 minutes. The script has run unchanged since April, and its only maintenance was adding two project tokens to the list.

The limits sit at capture time. The slug depends on the two words I bother to type, and a lazy capture produces names like `2026-03-01_misc_stuff.png` that the renamer happily keeps. The script also does no content analysis, so a screenshot renamed with a wrong slug stays wrong until I notice.

The renamer solved a small problem, and the daily friction it removed turned out to be bigger than the 40-minute disasters. Clean names changed how I save files, because the format made capture deliberate. I'll write about the voice-note transcription step in a future post. If you want to follow along, don't forget to subscribe.
