# Repurposing a Blog Post into a Newsletter Issue

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional. In May I rewrote a blog post for my newsletter from scratch, and the rewrite took longer than the original post had taken.

The original post ran 1,800 words with setup, benchmarks and appendices. The newsletter needed the same claim in 700 words with a next step, and I produced that version only after three discarded drafts.

In this post, I'll share:

- why the rewrite took so long
- how I extract the claim from a post
- how I cut the setup without losing readers
- how I add a next step readers finish
- where the repurposing routine stands now

## A Rewrite That Cost More Than Writing

The May post covered a retrieval benchmark I had run on 12,000 support tickets. The blog version opened with data collection, described the hardware and spent 400 words on failed approaches.

My first newsletter draft kept that order and trimmed sentences. It read like a compressed report, and two test readers replied that they had stopped halfway through.

The rule I took from May is simple. I keep the claim, cut the setup and add a next step, in that order, every time I repurpose.

## The First Version

My first routine was sentence-level trimming with a target ratio. I cut every paragraph by half, kept all six sections, and produced a 900-word version that preserved the structure nobody wanted.

The trimmed draft failed its only job. Newsletter readers open for one useful idea they can apply, and my draft still asked them to follow a benchmark narrative.

Trimming preserves structure, and structure is what must change. A blog post argues toward a conclusion, while a newsletter issue starts from the conclusion and points forward.

I deleted the trimming routine after that week. The repurposing pipeline stayed manual for a month while I worked out the claim-first order.

## Extracting The Claim

The routine starts with one sentence that states what the reader can now do. For the retrieval post the claim read that hybrid search with a reranker beats dense search on support tickets by 11 points.

I find that sentence by reading the blog conclusion first, not the introduction. The conclusion holds the result after the caveats, and the introduction holds the throat-clearing I plan to cut.

The claim goes through two checks before it leads the issue:

- a reader can act on it without reading the original post
- it names a number, a tool or a file the reader can verify

When the claim fails either check, the post is a bad candidate for repurposing. I skip it and pick a post with a portable result instead. Two May candidates failed the checks, and both became short notes instead of issues.

## Cutting The Setup

With the claim fixed, I delete every paragraph that exists to motivate the original investigation. Data collection stories, hardware notes and failed approaches all go, however much I liked writing them.

The retrieval issue kept 120 words of setup from 900. I kept the dataset size and the baseline score, since the claim means nothing without them, and I cut the crawler anecdotes entirely.

Readers who want the full path get one link at the end. I place that link after the next step rather than in the opening, since an early link sends readers away before the claim reaches them.

That deletion ratio repeats across every repurposing I attempt. Setup that took 40 percent of the blog post takes under 15 percent of the newsletter issue. The retrieval issue kept its dataset paragraph verbatim, since those two numbers do the motivating work alone.

## Adding A Next Step

The next step turns a read claim into a used one. I close each repurposed issue with one action the reader can finish in under 20 minutes.

The retrieval issue asked readers to run a provided script against their own FAQ file:

```bash
uv run python scripts/compare_search_modes.py --faq faqs.csv
```

That script compares keyword and hybrid search on the reader's own data. It prints the same two scores the issue cites, and the reader sees the gap on familiar ground.

I choose next steps I have personally run to completion. In June I drafted a step around a GPU reranker I had never executed. A reader replied within a day that the script failed on their machine.

## The Routine Today

Repurposing now takes 75 minutes against four hours in May. Claim extraction takes 15 minutes, setup cutting takes 30, and the next step with its verification takes the rest.

The routine has converted nine posts since June. Six issues beat the blog version on reply rate, two matched it, and one underperformed because the claim needed the full benchmark context.

I track each conversion in a small ledger file:

```text
repurpose/ledger.md
```

That file records the source post, the claim sentence and the reply counts for both versions. When a claim type underperforms twice, I stop repurposing posts built around it.

The ledger works because it compares matched pairs rather than vibes. I spend five minutes per issue logging the numbers, and the record across nine conversions already guides my picks.

I'll cover the ledger analysis in detail in a future post. If you want to follow along, don't forget to subscribe.
