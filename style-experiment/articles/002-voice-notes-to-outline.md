# Turning Voice Notes into an Article Outline

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. On 14 February I recorded four minutes of voice notes while walking to a client review. By the end of the day, those fragments became a nine-section outline for a post about queue monitoring.

That step used to disappear inside drafting. I would paste a transcript into a blank page and start rearranging sentences before I knew the argument. In January I turned the process into a repeatable workflow after abandoning two drafts of 2,100 words that said almost nothing.

In this post, I'll share:

- how I record a brain dump
- how I prepare the transcript
- how I group related fragments
- how I turn groups into an outline
- how I revise the outline against the source
- what changed in my drafting time

## Raw Notes And Their Limits

A raw voice note is useful because it's honest. It contains the order in which I remember problems, not the order in which an article should explain them. My 14 February recording had 611 words and one sentence that lasted nearly 40 seconds.

The obvious approach is to edit while transcribing. I tried that on an earlier post about Airflow retries. I corrected the wording too early and removed a hesitation that hid a useful caveat, so I forgot the main complaint by the end.

So I separated the stages into capture, transcription and arrangement. The rule is simple: the outline comes from the complete dump, and the draft comes from the outline.

## 1. Record The Brain Dump

I use a two-minute walk, a cup of tea or the ten minutes after a failed deployment. I talk for three to five minutes without checking notes. I start with the concrete event, state the problem and then explain what I tried.

Before recording, I run a short script from `~/bin`:

```bash
voice-note "queue monitoring ideas"
```

The command creates `~/notes/voice/2026-02-14-queue-monitoring.m4a` and starts a recording. The filename matters because I search old notes by topic later.

I try to say numbers while they're still fresh. In this example I mentioned 43 delayed tasks, two dead-letter queues and the Grafana panel that had been empty since Tuesday.

## 2. Transcribe And Clean

I transcribe with `whisper`, a local speech-to-text tool, because the audio often contains client names I don't want to send to another service. My medium-quality recording of 4 minutes and 11 seconds took 38 seconds to process.

The transcription command is short:

```bash
whisper ~/notes/voice/2026-02-14-queue-monitoring.m4a --model small --language en
```

The first transcript had 19 obvious transcription errors. It changed "dead-letter queue" into "dad letter queue" and turned "RabbitMQ" into "rabbit em queue". I fix only words, names and punctuation at this stage. I don't reorder sentences.

## 3. Group Related Fragments

Next I paste the transcript into a flat markdown file and mark each idea with a dash. The 611-word transcript produced 27 fragments. Some were only three words long, and one was a complaint about my own dashboard.

I create four working groups in a file called `groups.md`:

- the production incident and its timeline
- the monitoring panels that failed to help
- the retry rules and dead-letter queues
- possible article examples

I keep duplicates in place. If the same warning appears four times, that repetition tells me which idea matters. On 14 February, the phrase "alerts arrived too late" appeared five times.

## 4. Build The Outline

The outline starts as one sentence per group. Under each sentence, I place the fragments that support it. I don't write transitions yet, and I don't try to make complete paragraphs.

After I joined two closely related sections, the first outline contained five headings:

- why the alerts arrived late
- what the queue metrics showed
- how retries concealed the delay
- the dead-letter queue design
- the monitoring changes I made next

Each line is a claim, and each claim has at least one fragment beneath it. If a line has no supporting fragment, it moves to an idea list for another article.

## 5. Revise Against The Source

Before drafting, I read the cleaned transcript from top to bottom. Then I read the outline and verify that every useful fragment has a place. This check is private, but the result goes into the outline.

This pass caught two useful details. The first was a date: the queue had grown slowly for 40 minutes before the alert fired. The second was a caveat: the retry delay was intentional, so a larger delay would hide the problem differently.

I also mark one fragment as the opening. For this article, that was the paragraph about 43 delayed tasks. A number makes a stronger start than a general statement about observability.

## Changes In Drafting Time

The first complete outline took 31 minutes, including grouping and revision. Drafting the article took another 68 minutes. In January, comparable drafts took me about two and a half hours, and I often rewrote the opening twice.

The method has one limitation: it works best when the voice note already contains a concrete event. A general idea without numbers or actions may still need research before it becomes an outline.

I now keep the transcript and the outline together in `~/notes/articles`. That pair gives me a record of what I noticed before writing. If the draft drifts, I can compare it with the original dump.

I'll share the full queue-monitoring article after one more production cycle. If you want to follow along, don't forget to subscribe.
