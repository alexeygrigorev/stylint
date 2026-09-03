# Validating Article Ideas with Search Queries and Community Questions

This synthetic style exercise uses a fictional project and invented details.

My drafts folder once held 214 article ideas. Most were fragments such as "evaluation friction" or "small data problems". They felt interesting, but I had no way to tell which ideas solved a problem someone already wanted to discuss.

So I built a short validation pass using two sources I already had. The sources were search-query exports from a fictional blog and 1,268 questions from three fictional community forums. The goal was to pick ideas with evidence and a clear focus.

The query, cluster, and timing counts in this article are invented examples.

In this post, I'll share:

- how I normalized messy queries and forum titles
- how I clustered demand without pretending it was clean
- how I checked competition and my own distinct focus
- which ideas survived the first pass
- how the validation sheet works now

## Normalize First

The search export contained 4,741 rows over 18 months. People searched for the same subject with different word forms, plural endings, and product names. The forum titles were even messier because writers often framed a configuration problem as a request for a tutorial.

My first normalization pass used four rules:

1. lowercase all terms
2. collapse repeated whitespace and punctuation
3. map product nicknames to one canonical name
4. remove branded queries and clearly irrelevant terms

I also added a stop list for "free", "download", and "course". Those terms showed interest in material, but they hid the underlying problem.

The rules removed 812 rows and left 3,929 usable queries. I kept the removed rows in a separate tab in case a rule was too aggressive.

## Cluster the Demand

I started with keyword-only clustering, but it split related questions. One cluster contained "agent evaluation", another "LLM tests", and another "judge prompts". They overlapped enough that separate articles would repeat the same setup.

Then I combined three pieces of evidence:

```text
query text
forum title and first reply
link clicked from the search result
```

For each candidate cluster, I read 15 random rows instead of trusting the algorithm. I labeled the row as tool choice, workflow, evaluation, or operations. Four labels were enough because a finer taxonomy made disagreements explode.

I settled on 27 clusters with at least 40 rows each. Evaluation had 718 rows, model routing had 322, and local deployment had 198, so the sizes remained uneven. The long tail stayed unclustered because it had no repeated demand.

## Check Competition and Focus

For the ten largest clusters, I searched the fictional blog and two public platforms. I recorded three fields for each existing article. The fields were promise, audience, and evidence. A review could then show where a new piece actually differed.

Six clusters felt crowded because several articles explained what an evaluation set is. Few showed how to revise one after a model upgrade, and I had run that migration twice.

Two clusters had high demand but no plausible focus. "Choose a vector database" was mostly comparison shopping, and my experience was too narrow to be useful. I put those ideas back in the backlog.

The remaining ideas passed a one-sentence test. Each had to name the reader, the trigger, and the measurable outcome. "How to refresh an evaluation set after a model upgrade" passed. "More about evaluations" didn't.

## Ideas That Survived

Seven ideas made it to the writing queue:

- refresh an evaluation set after a model upgrade
- turn forum threads into a troubleshooting guide
- choose between local and API models for batch jobs
- add tracing to a small retrieval workflow
- design a course project that can scale to many reviewers
- write a failure log that agents can consume
- audit search queries for content gaps

I ranked them by demand, competition, and my ability to show evidence. The evaluation-refresh idea won on all three. It appeared in 214 queries, 61 forum threads, and it connected to two projects I had already built.

The validation pass took 11 hours over four evenings. That sounds expensive for an article queue, but the queue now has a measurable basis. I expect to reuse the clusters for two course lessons.

## The Current Sheet

The validation sheet has four tabs:

1. normalized rows
2. cluster definitions
3. competition notes
4. decision log

Each candidate article must include the cluster name, sample size, distinct focus, and first evidence source. The decision log also records rejection reasons. A missing focus is acceptable in an early note, but "sounds interesting" isn't.

The biggest limitation is sample bias. The queries come from people who already found my blog, and the forums lean toward beginners. I treat the numbers as directional evidence, and I pair them with my own project failures.

Validation doesn't guarantee a good article. It prevents me from writing another fragment that only makes sense to me.

I'll share the evaluation-refresh draft soon. If you want to follow along, don't forget to subscribe.
