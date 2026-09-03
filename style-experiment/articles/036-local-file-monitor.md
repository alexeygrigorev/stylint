# Building a Local File Monitor for Writing Intake

This synthetic style exercise uses a fictional project and invented details.

Three folders on my laptop collect raw writing material. They hold screenshots, exported voice notes, and saved code snippets. Last month they held 1,214 files. I could find almost nothing, because the names looked like `Screenshot 2026-07-14 at 09.42.11.png`.

I didn't want another note-taking app. I wanted a small local process that watched the three folders, normalized the files, and moved processed items into a permanent archive.

The folder counts and timing numbers below are invented examples for this exercise.

In this post, I'll share:

- how the file monitor works
- how it extracts metadata without inventing facts
- how the processed archive is organized
- what the first four weeks showed
- what I still review by hand

## Monitor Service

I wrote the monitor in Python with `watchdog`, a library that reports filesystem events. It runs on my laptop with a 30-second debounce window so a file is handled only once after editing stops.

I use this local configuration:

```text
intake_folders:
  - ~/Intake/Screenshots
  - ~/Intake/VoiceNotes
  - ~/Intake/CodeSnippets
archive_root: ~/WritingArchive
state_db: ~/WritingArchive/monitor.sqlite
max_file_size_mb: 50
```

Each accepted file gets a UUID (universally unique identifier), so the process can safely retry after a crash. The state database records the original path, checksum, processing status, and final archive destination.

## Extract Metadata

The first step is purely mechanical. The monitor reads creation time, image dimensions, and the active application from a screenshot. It reads duration, sample rate, and recording device from a voice note. It detects language and hashes the content of a code file.

The second step creates two labels for project and topic. Project labels come from a local list with `course-notes`, `agent-tools`, `writing-system`, and `personal`. Topic labels come from a controlled list with 27 values such as `evaluation`, `retrieval`, and `automation`.

I deliberately avoid free-form tags. They make search useful at first, and then the tags decay into synonyms such as `agent`, `automation`, and `scripting`.

For voice notes, the monitor sends audio to a local transcription model. It keeps the transcript inside the archive and creates a short summary field. The summary can't include names or credentials unless a separate privacy pass has already redacted the transcript.

## Organize the Archive

The archive uses a date-first path and stable content-based names:

```text
~/WritingArchive/2026/07/14/
  2026-07-14_agent-tools_eval_transcript-limit.png
  2026-07-14_writing-system_outline_voice-note.m4a
```

The path starts with the date the item arrived. The filename contains the project, topic, and a short human phrase. The phrase comes from a template based on file type, not from a language model inventing context. A transcript, for example, uses the first concrete noun phrase from its summary.

For screenshots, the monitor uses visible words if optical character recognition finds at least three words. Otherwise it stores the image under the project and topic only. For code, it uses the first function or class name that passes a basic parser.

The monitor moves processed items out of intake. It leaves failed items in `~/Intake/Failed`, with a JSON sidecar that records the exact exception and retry count.

## Four Weeks of Results

I ran the monitor for 28 days without changing the rules. It processed 396 screenshots, 218 voice notes, and 98 code snippets, for a total of 712 files. Another 47 files went to the failure folder, usually because the files were too large or had unreadable permissions.

The state database used 82 MB, mostly because the archive stored transcripts and checksums in full. Search across the archive took 120 milliseconds at the 95th percentile on my laptop.

The measurable win was retrieval time. Finding a relevant screenshot previously took me 45 seconds on average. With archive search it took 8 seconds. The larger win was fewer abandoned ideas, because voice notes stopped disappearing into unnamed files.

The project labeler was too eager. It put 31 screenshots into `agent-tools` that belonged in `writing-system`, so I added a manual review queue for ambiguous cases.

## Manual Review

I review three categories every Sunday:

- files in the failure folder
- items labeled with low confidence
- suggested merges for duplicate topics

The Sunday pass takes 12 to 20 minutes, and most items need only a small label change. For duplicate voice notes, I listen to the first 20 seconds and choose the better version.

The system never deletes anything. It moves files, records checksums, and leaves the original available in the failure folder or archive, which makes mistakes recoverable.

I learned to separate mechanical metadata from judgment. A monitor can safely rename, hash, and file an item. A person should decide what it means.

I'll write next about the privacy pass for transcripts. If you want to follow along, don't forget to subscribe.
