# Summarizing Podcast Transcripts Without Flattening the Argument

Last month I summarized 14 podcast transcripts for my private research notes.
I invented the shows, speakers, and measurements for this synthetic style
exercise. The longest episode ran 3 hours and 9 minutes, and my early
one-paragraph summaries removed exactly the disagreement I wanted to remember.

The problem was easy to see once I compared a summary with the transcript.

The guest made one claim, the host offered a careful objection, and the guest
narrowed the claim. My summary made it sound like a clean consensus. In this
post, I'll share five parts of the revised workflow:

- the summary format I now use for long conversations,
- how I preserve counterpoints and the order of the argument,
- the timestamp and quoting rules I added,
- a 22-episode quality check,
- where the workflow still needs human judgment.

## The first summaries

I began with a small Python script. It downloaded audio with `yt-dlp`, sent the
file to a local Whisper model, and wrote a Markdown transcript next to the
audio. Whisper made about one obvious error every 8 to 10 minutes, usually with
product names. I added a correction dictionary, but I left the spoken sentences
alone.

My first prompt asked the model for a summary, three takeaways, and a list of
tools. On a 41-minute episode, it produced a tidy answer in about 90 seconds.
It also turned a conditional recommendation into a firm rule. That was my
mistake: I had asked for conclusions and given the model no reason to keep the
conditions.

The rule I took from it: a summary of an argument has to represent movement,
and movement needs sequence. A list of takeaways can still be useful, but it
should sit after the sequence, and it should never replace it.

## Segment claims, then decide what to keep

The next version worked in two passes. First, a script split the transcript
into 4-minute chunks, each with an overlap of 30 seconds. Each chunk got the
same instruction to identify claims, objections, examples, and decisions. The
model returned JSON, and `summary_build.py` validated the fields before it
accepted the result.

The format now looks like this:

```json
{
  "minutes": [18, 22],
  "claims": [{"speaker": "guest", "claim": "...", "condition": "..."}],
  "objections": [{"speaker": "host", "objection": "...", "example": "..."}],
  "resolution": "narrowed to early-stage datasets"
}
```

Second, the builder reads those segment records from start to finish and writes
a section for each major turn in the conversation. A turn can be a new topic, a
strong example, or a direct disagreement. Most episodes produce 6 to 12 turns,
so the final note is usually 700 to 1,100 words.

I kept the local model for segmentation because the task is repetitive. I
switched to a hosted model for the final pass because it follows instructions
more reliably. Together, a 2-hour episode takes 11 to 18 minutes and costs me
about $0.14.

## Keep counterpoints attached

The important change was relational. Each objection must name the claim it
responds to, and the builder writes them together. The reader therefore sees
both sides in one paragraph. If a guest later revises the claim, that revision
goes directly under the objection.

A fictional draft note now contains these lines:

```text
18:10 - The guest says that batch processing covers most evaluation work.
21:35 - The host asks about late-arriving labels and a one-week delay.
22:04 - The guest narrows the claim: batch checks are useful only when the
label delay is shorter than the release cycle.
```

That note preserves the useful answer and the boundary. It also gives me a
timestamp I can check later. If I quote the guest, I include the range and mark
cleaned grammar in brackets. I cap direct quotes at 40 words unless the whole
point is the phrasing.

For decision-heavy episodes, I add one final bullet called "Where they settled".
The builder fills it only when both speakers agree, partly agree, or explicitly
leave the question unresolved. It can't invent a synthesis when the guests
changed subjects.

## Timestamps and retrieval

Every section starts with a minute range. That small field changed how I use
the notes. In March, I needed one exact exchange for a workshop exercise, and
the timestamp sent me to minute 54 instead of forcing me to scan the transcript
again.

The builder creates an index with five fields:

```text
episode_id, episode_date, minute_start, minute_end, topic
```

I load that file into SQLite (a small embedded database) and use it for three
searches. The first searches topics, the second searches claims, and the third
searches guest names and dates. The transcript stays in the same folder as the
note, so every result has a source.

I also add a link back to the original episode in a local field, but I don't
put external URLs into the notes. My notes may name tools, people, and dates
discussed in the invented episode. They don't claim to verify any real-world
fact.

## Testing the summary quality

I built a small review set from 22 synthetic episodes. Each episode had a
transcript, an outline I created manually, and three requirements. A passing
summary had to identify at least 90% of marked objections. It also had to
preserve their resolution and assign a timestamp within 30 seconds of the right
location.

The sequence-only version passed objection detection on 18 of 22 episodes, and
the relational version passed on 21. The one miss merged two similar objections
about tool latency and model latency. The model chose the speaker's second
explanation and dropped the first, which had contained the useful benchmark.

That failure led to another rule: two objections that sound alike still need
separate records if they attack different assumptions. I now prompt the model
to split by assumption, and the validator rejects records with more than one
assumption.

The current cost is about $0.20 for a 2-hour episode, up from $0.14. The extra
cost supports more careful separation. I can accept that for episodes I plan to
cite, and I can still use the cheaper path for casual listening notes.

## Lessons From the Project

I started this project to save time. I ended it with a lesson in representing
conversations honestly. Compression always chooses, so the format has to show
those choices.

Three habits now provide most of the value:

- keep the sequence before the conclusions,
- attach every counterpoint to a claim,
- put a timestamp on every major turn.

The workflow still depends on my final pass. I read the generated note against
the transcript and add a one-line caveat when the speakers talk past each
other. For dense episodes, that takes 10 to 15 minutes. For lighter episodes,
it takes 5.

Next I want to compare the same format on panel discussions, where three
speakers can hold overlapping objections. I expect the speaker attribution to
get harder. I'll write about that test in a future article. If you want to
follow along, don't forget to subscribe.
