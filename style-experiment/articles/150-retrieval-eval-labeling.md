# Labeling Retrieval Results Without Burning a Week

I built a retrieval assistant over 3,200 course documents and couldn't tell
whether its improvements were real. In January, I decided to label enough
queries to compare two versions, but I gave myself only three evenings. I wrote
this synthetic style exercise with fictional document counts, names, timings, and
results.

The assistant, CourseFinder, answers questions by retrieving passages and asking
a model to cite them. A full manually labeled benchmark would have taken weeks.
I needed a useful comparison before the next cohort started.

In this post, I'll share:

- how I sampled the queries,
- how I used binary judgments,
- how I resolved disagreements,
- how I audited the labels,
- how the results changed the deployment decision.

## 1. Sample the questions

I exported 1,864 search queries from three months of logs, and many were
duplicates. "deadline", "deadline extension", and "when is the deadline" asked
the same product question. Deduplication reduced the set to 871 unique strings.

I grouped the strings by expected document type:

- logistics
- assignment rules
- grading
- installation
- model APIs
- project requirements
- community policy

Then I took a stratified sample of 120 queries, with at least 8 from every
group.

The sample also included 15 known hard cases:

- queries that mix two courses,
- abbreviations such as "MAE",
- questions about a policy that changed in December,
- installation questions naming operating systems,
- vague questions such as "project idea".

I kept the original query text, even when it had typos. Cleaning it would have
measured the lab version of the system rather than the version users actually
hit.

## 2. Make binary judgments

The first rubric asked for relevance scores from 0 to 3. That was a mistake
because I gave the same passage a 2 and later a 3, depending on my coffee
supply. The boundary was impossible to maintain across three evenings.

The working rule became binary: a result is useful if it contains evidence a
teaching assistant could paste into an answer without adding another document.
Everything else isn't useful, and the judge doesn't ask whether the passage is
beautiful, complete, or ideally phrased.

For each query, I labeled the top 10 passages from each system. Two systems and
120 queries produce 2,400 judgments at first sight. In practice, many passages
appeared in both lists, so the actual count was 1,713.

I also wrote one line of evidence for every useful result. For a deadline
question, the line named the date and the course. Those lines caught labeling
mistakes much faster than a numeric score.

## 3. Resolve disagreements

I asked Maren Keller, a fictional teaching assistant, to label 40 of the 120
queries independently. We chose 20 ordinary queries and 20 that covered the
hard-case list. We didn't discuss the rubric until after her first pass.

We agreed on 498 of 531 passage judgments, which is 93.8%. Then we examined all
33 disagreements together. Sixteen were rubric misunderstandings, 12 were actual
ambiguities, and 5 were transcription errors in my spreadsheet.

The ambiguous cases were informative. A passage about a general deadline was
useful for "when is the deadline" in one course and misleading for a question
naming another course. We added one rule: a useful passage must match the course
or policy named in the query, even if it answers the general topic.

We recorded every disagreement and its resolution in `evals/label-decisions.md`.
The file became the second-most important artifact after the labels. A new
labeler can read the examples instead of reconstructing the boundary.

## 4. Audit before benchmarking

Before running the comparison, I audited 60 random judgments. I checked them
against the query, passage, evidence line, and decision file. The audit found 4
inverted labels and 2 cases where I had judged a title rather than the passage
body.

The mistake with titles made the older system look worse than it was. Its
retriever returned several section titles with useful nearby text. I corrected
the labels and added a note to the rubric: judge the passage contents, and use
the title only as context.

I wrote a short script to validate the final file:

```python
labels = read_labels("evals/2026-01-labels.jsonl")
assert labels.missing_evidence() == []
assert labels.unknown_query_ids() == []
assert labels.duplicate_pairs() == []
```

That check can't tell me whether a label is correct. It can catch malformed
rows, missing query IDs, and repeated judgments, which are annoying to discover
during analysis.

## 5. Read the results honestly

The labeled sample gave each system a hit@5 score. Version A returned a useful
passage in the top five for 87 of 120 queries. Version B reached 95. The
difference looked promising.

The group breakdown changed the interpretation. Version B improved retrieval
for model APIs and installation questions by 11 cases total. Version A was still
better on 4 mixed-course queries, and the systems tied on logistics. The average
advantage came mostly from two groups.

I computed a rough confidence interval with bootstrapping. Repeating the sample
assignment 2,000 times showed an interval from 3 to 12 improved queries. That's
wide enough to justify more testing, and narrow enough to keep version B in a
staged rollout.

After three weeks, CourseFinder's support threads showed 9 retrieval complaints
for version B and 14 for version A over comparable traffic. That isn't a clean
benchmark, but it agrees with the labeled sample.

## Closing note

Binary judgments made a small benchmark possible. The evidence line and the
disagreement log mattered as much as the final score, because they showed which
decisions the labels encode.

The rule I took from the exercise: label enough to make a decision, then record
the boundary cases. Next month I'll expand the sample to 200 queries and test a
new embedding model. Subscribe if you want the comparison.
