# Searching PDFs and Slides on My Own Machine

I wrote this piece as a synthetic style exercise, so I invented every file count and measurement in it. Last winter I needed one slide about eval harnesses from a talk I gave in 2024. I knew the slide existed, and I couldn't find it among 312 PDFs and 48 slide decks on my drive.

My files span eight years of courses, talks, and saved papers in folders named by year. System search reads some PDFs, skips scanned ones entirely, and never looks inside my Keynote exports.

One evening of opening files by hand convinced me to build a small local index. Two weekends later I could find any slide in under a second.

In this post, I'll share:

- how I pulled text from PDFs and slide decks
- how filenames and folders became usable metadata
- how title matches outrank body matches
- how the local search page works today
- where the index still fails and what it costs

## Buried Slides and Papers

The collection breaks into three rough groups with different problems. Course readings are clean PDFs with selectable text and real titles. Talk decks are Keynote exports where each slide holds five short lines. The third group holds scanned papers, and those are images wrapped as PDFs with no text layer at all.

System search handled only the first group. It indexed the clean PDFs through their text layer and ignored everything else. My eval harness slide lived in a Keynote export, so the system never saw a single word of it.

I counted the collection before building anything. The drive held 312 PDFs and 48 exported decks across 9 year folders, totaling 4.1 GB. About 60 files were scans, and those needed OCR before any search could touch them.

Extraction came first because nothing else works without text, and OCR came last because only 60 files needed it.

## Text Extraction That Mostly Worked

I extracted text with pdftotext from Poppler, a tool I already used for course prep. It converts each PDF page into plain text in milliseconds, and it preserves enough line breaks to keep slide bullets readable. One shell loop processed 300 clean PDFs in 11 minutes on my ThinkPad.

The loop I ran looked like this:

```bash
mkdir -p extracted
for file in papers/*.pdf; do
  base=$(basename "$file" .pdf)
  pdftotext -layout "$file" "extracted/${base}.txt"
done
```

The exports needed one converter pass, and 12 of the 48 decks lost speaker notes I never searched anyway.

The 60 scans went through Tesseract with default English settings in 38 minutes. I marked every OCR file so results show a quality warning.

The rule I took from extraction week: plain text files beat clever direct indexing, and reindexing never touches the originals.

## Filenames Became Metadata

Filenames held more clues than I expected once I parsed them consistently. Most course files followed a year-first convention like 2023-evals-survey.pdf, and most decks included the event name. I wrote one parser that splits names on dashes and records year, topic, and kind.

Each indexed file now stores five metadata fields:

- file path on the local drive
- year taken from the folder or filename
- kind, which is paper, deck, or notes
- page count from the extraction step
- OCR flag for scanned files

The parser guessed wrong on 34 oddly named files, and I fixed those by hand in 25 minutes. Talk-final-v3.pdf became 2024-eval-harness-talk.pdf with its course prefix restored.

Metadata powers the filters on the search page. I can restrict results to decks from 2024, or hide OCR files when I need exact quotes. Those two filters answer most of my real questions before ranking even matters.

## Ranking With Title Boosts

The first ranking attempt scored every match equally, and long papers buried every slide. A 40-page survey mentioning evals 30 times outranked the 5-line slide I actually wanted. The results were technically relevant and practically useless for my questions.

I changed the scorer to boost short documents and title matches. A match in the filename or first page counts triple, and the score divides by the log of the page count. Those two adjustments moved decks above surveys for nearly every test query I cared about.

I tested ranking with 20 questions from my own history:

```python
results = search_index("eval harness gating", kind="deck", year=2024)
for hit in results[:5]:
    print(hit["file"], round(hit["score"], 2))
```

That query now returns the 2024 talk deck first with a wide margin. Across the 20 test questions, the file I wanted appeared in the top 3 results 17 times. The 3 misses were all OCR scans where the key term had lost a letter to confusion.

Ranking still ignores recency beyond the year filter, and a polished deck scores the same as my rough brown-bag version. Neither gap has annoyed me enough to fix yet.

## Search Page on Localhost

I built the search page as a single FastAPI app with one input box and two dropdown filters. I query the SQLite index with the same scorer and render 10 results with highlighted snippets.

Last month it found the eval harness slide in 4 seconds, eleven months after I had given up looking by hand. The snippet showed the exact bullet about gating releases on eval scores.

Access stays local by design. The index holds unpublished drafts alongside published decks, and localhost is the entire access policy for this one-user tool.

The full index rebuilds in 14 minutes including OCR checks, and I rerun it monthly. Fourteen minutes of fan noise beats a sync daemon I would have to debug.

## Lessons From the Paper Pile

I recovered the build cost during spring course prep. I reused 6 slides across 3 lectures without redrawing a single diagram, and each reuse started from a search that took seconds. The old workflow of opening folders from memory is gone.

The project taught me a narrower lesson than search quality. Extraction plus metadata answers most personal questions, and ranking only needs to prefer short titled matches. Fancy retrieval can wait until the basics stop working.

Handwriting in scans stays invisible, video lectures stay outside the index, and snippets sometimes split mid-sentence. If scans ever dominate my questions, I'll tune the OCR pass before touching anything else.

I'll cover the snippet highlighter in a future post on this blog. If you want to follow along, don't forget to subscribe.
