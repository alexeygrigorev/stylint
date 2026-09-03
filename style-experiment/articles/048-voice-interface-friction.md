# Voice Input Benefits and Friction

I spent June 2026 recording voice notes for a project journal. The experiment covered 214 notes, 6 hours and 20 minutes of audio, and 3 different tools. Voice input solved my capture problem, then created a new editing problem.

I wrote this as a synthetic style exercise with invented note counts and timings. The workflow conclusions come from that fictional experiment, but they match the constraints I would expect.

In this post, I'll share:

- where voice capture worked better than typing
- what transcription did well and where it failed
- why precise commands resisted dictation
- how I built a two-stage editing pass
- what I changed after the month ended

## Capture While Moving

The strongest use case was immediate capture. I dictated 78 notes while walking between meetings, 41 while cooking, and 27 in the car before driving. Typing would have delayed most of those notes or lost them entirely.

The median spoken note lasted 52 seconds and produced 118 words. It usually contained a project name, a symptom, and a next action. I could record it without opening a laptop, finding a file, or deciding where the idea belonged.

Voice also preserved more context than my typed notes. A spoken note might include the exact error, the machine name, and the reason I suspected a deployment. When I typed the same situation later, I tended to write only the conclusion.

The tradeoff appeared immediately: cheap capture produced three times as many raw fragments. Some were useful, while many repeated the previous day's idea.

## Transcription Strengths and Failures

I used a local transcription model on my laptop, then compared it with a hosted model on 60 notes. The local model produced a first draft in about 0.4 times the audio duration. The hosted model took 2 to 4 seconds per note and handled domain nouns better.

Transcription preserved numbers well when I spoke them deliberately. Dates such as "May 14, 2026" usually appeared correctly, while values such as "2.8 milliseconds" needed the word "point". "One hundred forty" sometimes became either `140` or `100 40`.

The failures clustered in three areas:

- project codenames
- file paths and shell commands
- punctuation in long compound sentences

My codename `ferro-lab` became "pharo lab", "fair row lab", and "Ferro Laboratory". File paths were worse. Saying `src/utils/retry.py` produced readable English but unusable syntax.

Transcription also kept every filler phrase. The raw notes contained many occurrences of "so", "and then", and "I mean". Those words helped me speak continuously, but they made the text slow to scan.

## Precise Review Resisted Dictation

After capture, I tried to edit by voice. The first attempt failed in a way that told me a lot about the task.

I recorded instructions such as "move the database sentence before the retry note". The speech-to-text layer usually transcribed the instruction correctly, but the edit required exact references. I had to say file names, paragraph positions, and code identifiers that dictation mangled.

Voice was also poor for checking boundaries. I wanted to know whether a note described a bug, a decision, or a question. Looking at six short paragraphs on a screen took seconds. Listening to them again took much longer and made comparison harder.

I did find one review case that worked. When a draft read awkwardly, I read it aloud and heard duplicated phrases that my eyes skipped. Voice remained useful as an output channel, while typed edits remained faster for precise changes.

## A Two-Stage Editing Pass

By the second week, I settled on two stages: capture by voice, then revise by keyboard and script.

The first stage stayed completely raw.

I saved these details for each note:

- audio file
- transcript
- duration
- location label
- temporary project tag

No cleanup happened during capture, because stopping to fix a phrase interrupted the next thought.

The second stage ran every evening. A short Python script grouped notes by project and removed duplicate sentences with a similarity threshold.

I then edited the remaining notes into three fields:

- observation
- decision or open question
- next action

The normalized form looked like this:

```text
Observation: ferro-lab failed at 21:12 after the retry change.
Decision: Treat retries over 30 seconds as a separate error class.
Next action: Add test_retry_timeout to the backend suite.
```

The script couldn't decide which fields mattered. It only prepared the material, and I made the final classification while reading the screen.

The daily pass took 12 to 18 minutes, usually after dinner. That was longer than I expected, but it replaced two failed habits. I had never sustained a desk journal or a reliable search through old phone recordings.

Storage stayed manageable because I deleted audio after transcription unless the note contained a difficult name or an unexplained error. Fourteen recordings remained after the month. The transcripts and normalized journal entries stayed in a local Git repository.

## Final State

After 30 days, 86 raw voice notes became 47 project journal entries. Thirty-one entries led directly to tasks. Nine became paragraphs in project documentation. The remaining seven turned out to duplicate an existing decision.

I now use voice for observations, errors, and next-action reminders. I don't dictate file paths, code edits, or final documentation. Keyboard and screen remain better for precise review.

The useful rule is boring: dictate while the context is fresh, then transcribe and edit before the context disappears. I plan to write about the grouping script next month. Subscribe if that sounds useful.
