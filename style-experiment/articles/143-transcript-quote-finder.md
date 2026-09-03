# Finding Quotable Passages in Long Transcripts

Last year I recorded 27 fictional conference talks for a research group called RoomLab. Each recording had a cleaned transcript, but preparing a report meant scrolling through 90-minute files to find one exact sentence about instrumentation or deployment.

I wrote this synthetic style exercise as part of a writing project. The recordings, transcripts, speaker names, measurements and project names are fictional.

In this post, I'll share:

- how I defined a quotable passage
- how I detected claims and kept their timestamps
- how I presented candidates for human selection
- what the first evaluation showed
- where the tool still makes mistakes

## Search Missed Claims

The transcripts lived in one directory as Markdown files. Every line had a speaker label and a timestamp, but the important content was buried among introductions, jokes and questions from the audience. My first method was manual reading with keyword search.

Keyword search found words such as "database" and "latency", yet it missed the sentences I remembered. A speaker often said "we instrumented every retry" without using the word "observability". A session on service ownership also mentioned latency 23 times without a quotable sentence.

I set a narrower target. Given a transcript, the tool should return 10 to 30 candidates, each with a timestamp, speaker and reason for selection. A person would choose no more than five passages for the final report.

## Define a Quotable Passage

I labeled 60 passages from six transcripts before writing detection code. I wanted a definition that a reviewer could apply consistently.

A quotable passage met these conditions:

- it makes one complete claim
- it includes a number, tool, decision or causal link
- it stands alone without a preceding question
- it names its scope rather than speaking only about one private incident

The labels produced a concrete baseline. Of 1,240 candidate sentences, 118 were quotable, which is about 9.5%. The most common reject was a summary sentence such as "we learned a lot", and the second most common depended on an earlier sentence.

I also wrote negative rules. Product names alone don't make a passage quotable, and a repeated sentence from a slide isn't a new claim. A passage that names an unnamed customer or contains personal data goes to a separate review list.

## Detect Claims and Timestamps

I used a hosted LLM for the first pass because the job involved judgment across 6,100 transcript lines. The script splits each transcript into windows of 12 sentences, with two sentences of overlap. It sends the window to the model and asks for JSON only.

Each returned object contains:

```json
{
  "text": "We instrumented every retry because silent timeouts hid the actual failure.",
  "start": "00:37:12",
  "end": "00:37:29",
  "speaker": "Priya N.",
  "reason": "names a decision and its cause",
  "confidence": 0.82
}
```

The model returns character offsets too. Before accepting a passage, the script compares its text against the transcript at those offsets. If the characters don't match, it searches a small neighborhood and recalculates the offsets. If that search fails, the script rejects the candidate.

The prompt bans paraphrase, requires exact text and asks the model to mark uncertainty. This reduced hallucinated quotations in a 20-transcript test from 11 to 2. Both remaining failures came from sentence boundaries, and neither passed the character-offset check in the final version.

## Present Candidates to a Person

Detection produces candidates, and a report needs judgment. I therefore built a local review page with FastAPI and htmx. It displays each candidate with surrounding transcript lines, a 20-second audio link, the model's reason and three buttons.

The review workflow has four states:

- new candidates appear in transcript order
- keep adds the passage to the report draft
- edit opens the exact text with the timestamps locked
- reject records a short reason and hides the candidate

Every action writes to a SQLite table, so I can stop after 10 minutes and resume. The final report generator reads only kept passages and adds the talk title, speaker names and start time.

Human review changed the ranking substantially. In one talk, the detector put a statistic first, while I kept a sentence about on-call responsibility because it better explained the statistic. The tool worked well as a scanner, but it couldn't know which passage served the report's argument.

## Evaluate the First Pass

I evaluated the detector against the same six labeled transcripts and then against 14 new talks. I counted a returned passage as correct only when its text matched exactly. Its timestamp also had to fall within two seconds, and a human had to accept the passage as quotable.

The results were useful, though the sample remains small:

- precision was 72% on the 14 new talks
- recall was 54% against my original labels
- 91% of accepted candidates kept the original ranking in their top 20
- the average review took 11 minutes for a 90-minute talk

The false positives were mostly broad conclusions, while the false negatives were compound sentences with two claims. Splitting candidate text at discourse markers improved recall to 61%, but it also produced fragments that a reviewer had to merge.

Audio links reduced another class of mistakes. Five passages looked odd because of punctuation, and listening showed that the speakers had used emphasis or pauses that the transcript didn't preserve.

## Current Failure Cases

Interviews create one difficult class of failures because two people interrupt and complete each other's sentences. Humor and sarcasm also look like factual claims in transcript text, so the detector raises unsuitable candidates for a serious report.

Third, the model favors concrete nouns. It finds statements about databases, latency and Docker, but it misses a policy sentence such as "we rotate every credential after 90 days". For that reason, I now run a second pass focused on policy, governance and process claims.

The second pass found 8 additional passages across 14 talks, and I kept 3. It costs about $0.42 more per talk at fictional API prices. I run it only for transcripts above 12,000 words because ordinary talks already produce enough candidates.

## Closing Notes

The essential design was exact text plus a timestamp. That let me verify every quotation mechanically, while a person supplied the judgment about what belonged in the report.

I plan to test speaker diarization on the interview set and to add a rule for two-claim sentences. I want a better candidate list, and the final selection will remain human.

Subscribe to stay updated.
