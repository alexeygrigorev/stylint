# Converting a Conference Talk into a Standalone Article

Last March I gave a 25-minute talk called "Shipping a Retrieval Assistant" at the fictional Baltic Data Days conference. The organizers sent me a transcript two days later. I wanted to turn it into an article for readers who never attended, but I didn't want to publish a transcript with stage directions.

I wrote this piece as a synthetic style exercise. Every conference, talk, transcript, repository and measurement below is fictional.

The talk worked because the room could see me point at diagrams and react to their faces. On the page, those cues disappear. I needed a structure that held the argument without the event.

In this post, I'll share:

- how I prepared the transcript for editing
- how I chose what to keep and what to cut
- how I reorganized the talk for a reader
- how I added missing technical context
- how I reviewed the draft against the original recording
- where the article is now

## Clean Up the Raw Transcript

The transcript contained 4,180 words. It came from the event's captioning service, so it had no punctuation for the first 90 seconds and split one idea into several paragraphs.

I put the file into `transcripts/baltic-2026/shipping-retrieval-assistant.txt` and used a small script to mark speaker changes. The script didn't rewrite anything. It added a timestamp every 30 seconds and counted the words between markers.

```bash
uv run python scripts/split_transcript.py \
  --input transcripts/baltic-2026/shipping-retrieval-assistant.txt \
  --every 30
```

That gave me 49 chunks. I read them once without editing, then twice with two goals: protect the claims and remove speech artifacts. I changed "okay", "so", repeated phrases and false starts, but I didn't add a new sentence.

The cleanup reduced the file to 3,340 words. More importantly, the surviving sentences belonged to the talk's actual argument.

## Choose the Reader and the Promise

The conference audience had seen my project announcement. An article reader might arrive through search and know nothing about `lenderdesk`, the fictional internal tool from the talk. I therefore made the opening answer three questions: what the tool does, who uses it and what problem it solves.

The original talk waited until minute six for that context. It worked in the room because my slides had already introduced the project. On the page, that delay would lose readers.

I wrote a new opening paragraph before the first section. It says that loan officers used `lenderdesk` to search 12,400 policy documents. The paragraph also states that the first version answered 61% of their test questions. Those facts set up the rest of the piece.

I also changed the promise from "what I learned" to "how I reduced hallucinated policy answers". A reader can decide from the opening whether that workflow matters to them.

## Keep the Spine and Cut the Rest

After cleanup, I made a simple outline from the transcript headings:

- the business problem
- the first version
- the retrieval test and failure examples
- the second version and deployment

That outline matched the talk almost exactly.

The spoken examples forced the most judgment. I had used two long stories because they were funny in person. Together they took 610 words and made a single point. I kept the shorter story about a car-loan rule and cut the second story about an old mortgage template.

The cut material still had value, so I moved the mortgage example into a future idea file. It can support a later article about document aging.

I also removed 11 slides that only summarized previous sections. In an article, headings already do that work. The final draft has 5 H2 sections instead of the talk's 18 slides.

## Add the Context Missing From the Room

I could say "this test set" in the talk because I showed it on the next slide. For the article, I had to define the set, its size and its limits.

I added a short section after the first version. It explains that the team selected 180 real questions, removed names and account numbers, and labeled each expected answer with a source section. Three loan officers reviewed the labels over two afternoons.

The second version used a reranker, and the talk described it in one sentence.

For the article, I listed its inputs in a bullet list:

- the question
- the top 20 chunks
- metadata for document date and policy area
- the approval level allowed for the loan officer

I didn't add implementation code because readers need to understand the review boundary rather than copy the ranking library.

I also expanded two abbreviations and named every internal system in plain terms. A reader shouldn't need to reconstruct our vocabulary from a slide deck.

## Review Against the Recording

When the draft reached 1,620 words, I played the recording at 1.5x speed and compared it to the article section by section. I wasn't looking for exact wording. I wanted to catch claims that had become stronger in editing.

That pass found three issues:

- the draft said retrieval "solved" the problem, while the talk said it improved the score
- the draft dropped the caveat that the test questions came from one branch
- the draft implied the reranker ran in production before 12 May

I fixed all three with dates and percentages. In the final article, I state that the answer rate went from 61% to 78%. I also explain that 9 of 180 cases still need a human review path. The revised draft reached 1,540 words, and it reads better than the longer version.

I also sent it to Marta Ilves, the conference organizer who reviewed the program. She confirmed that the results matched the talk. She also suggested a precise definition of "approval level": the loan officer role allowed to approve that policy area. That note took five minutes to fix and removed a confusing term.

## Status and Lessons

I have kept the article in `drafts/lenderdesk-talk-article.md` for two weeks. It has six sections, 1,540 words and four diagrams copied from the talk. We published it internally first. Two engineers found a stale metric, so I corrected the answer rate before the public draft.

The process now looks like this:

- clean the transcript without adding claims
- define the reader and the article's promise
- keep the talk's chronology
- cut examples that only work with a live audience
- add definitions the room already had
- compare the draft with the recording

The conversion took about seven hours across four evenings. That's longer than I expected, but most of the time went into rebuilding context for a reader rather than editing sentences.

I plan to reuse this checklist for the next two conference talks. If you want to follow along, subscribe for updates.
