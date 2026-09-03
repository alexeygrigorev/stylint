# Publishing a Workshop Recording with Useful Chapters

For this synthetic style exercise, the workshop, recording, and measurements are invented. On May 12, 2026, I gave a 94-minute online workshop on evaluation for retrieval systems. The raw recording was 1.9 GB, the audio peaked unevenly, and the most useful 12 minutes were buried after a setup delay. Publishing the file unchanged would have wasted the best part of the session.

In this post, I'll share:

- how I prepared the recording before editing
- how I turned a transcript into chapter boundaries
- which links and corrections I added
- how I tested the result with two viewers
- what I would change for the next workshop

## Prepare the source

I exported the recording in two forms: the original MP4 and a 480p working copy. The working copy made scrubbing fast on a train, while the original stayed untouched for final render. I also extracted audio to WAV at 16 kHz for transcription.

Before editing, I wrote down the release requirements:

- a public MP4 under 600 MB
- chapters with plain descriptive titles
- corrected links for every tool mentioned
- a text landing page with exercises and timestamps
- a correction note for any live mistake

This list kept the project from expanding into a full video production. My goal was a usable artifact, not a polished course.

The working copy came from one command:

```bash
ffmpeg -i raw-workshop.mp4 -vf scale=-2:480 -c:v libx264 -crf 28 -c:a copy workshop-480p.mp4
```

That took nine minutes on my laptop and produced a 320 MB scratch file. I could scrub through it quickly without risking the original recording.

## Transcript to chapters

The automatic transcript produced 13,400 words and split the talk into 410 utterances. I aligned the text with the recording and grouped it by the slide changes in the screen capture. Then I read only the speaker labels, slide numbers, and first sentences of each group.

That pass produced 23 candidate segments.

I merged greetings and housekeeping into one short opening, then reduced the list to 12 chapters.

The final boundaries followed the argument:

- the evaluation question
- a tiny labeled set
- baseline retrieval
- reranking
- judging answers
- a deployment checklist

I kept titles under 45 characters and avoided a generic chapter called "Details". One entry read "18:42 - Building a 20-case test set". A timestamp should tell a browser user what will appear.

I saved chapter markers in a plain CSV file with time, title, and notebook cell:

```text
00:00,Welcome and setup,introduction
06:18,The evaluation question,question
18:42,Building a 20-case test set,test-set
48:10,Judging free-form answers,judge
```

The CSV became the source for the video description, the landing page, and a link in each notebook cell. One list served all three outputs.

## Links and corrections

The transcript found seven tool names, and six had a URL in the shared chat. One link pointed to a discontinued repository. I replaced it with the maintained fork and added a note on the linked release page.

For the link pass, I kept a simple review sheet:

- tool name and spoken timestamp
- public project or documentation link
- the version used during the live demo
- any correction needed after the session

I checked each URL with the same Python and Chrome version used in the demo. Two packages had released minor updates in the following week, so the page notes those versions explicitly. That prevents a viewer from blaming a new release for a difference in behavior.

I made two content corrections while reviewing. I had called a metric "recall at one" when I meant "hit rate in the top five". I also said the reranker added about 50 milliseconds, but the demo showed 180 milliseconds because it loaded the model lazily. The video keeps the live mistake, and a text overlay plus correction note explains both issues.

The exercises were easier because I copied four notebook cells from the workshop repository. I linked each cell to the chapter where I introduced it. That gave viewers a path from watching to running code.

## Viewer test

I asked two people to test the page and recording. One had attended the workshop, and one had missed it. Each had 20 minutes and a browser without access to my file system.

The attendee went directly to chapters on reranking and judging. The newcomer played the first two chapters, then jumped to the exercise link. Both found the timestamps clear, but the newcomer missed the correction note because it sat below the video player. I moved it directly under the title.

I also watched their screens without helping. The attendee used the video's progress bar once and relied on chapters otherwise. The newcomer enlarged the text twice, so I increased the base font size and added more space around the exercise buttons. Those two changes took ten minutes and made the page easier to use on a small laptop.

That test changed the page more than my editing pass did. The recording was usable, and the ordering around it was the actual interface.

## Publication setup

I rendered at 1080p with a constant rate factor of 23, which produced a 540 MB file. I kept the original audio track unchanged and burned no subtitles into the video. Instead, I published a corrected VTT file generated from my edited transcript.

I organized the landing page into chapters, exercises, and corrections. It linked the workshop repository at a tagged commit, so the notebook and data would remain reproducible even if the main branch changed later.

Total editing time was seven hours over three sessions.

The work split across five activities:

- transcription and alignment took 45 minutes
- chapter selection took two hours
- link checks and corrections took two hours
- rendering took one hour
- page testing took the remaining time

## Lessons Learned

A recording becomes useful when its structure is visible. With chapters, corrected links, and exercises, someone can spend 15 minutes on the part they need.

For the next session, I'll capture slide changes as structured events during the workshop. I'll also put corrections above the player from the beginning.

I plan to write more about turning workshop material into short course modules. Subscribe if you want the follow-up.
