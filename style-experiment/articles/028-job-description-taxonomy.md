# Creating a Job Description Taxonomy from Free-Text Skills

I wrote this synthetic style exercise as an analysis essay. The project, dates and measurements are fictional. Since January I scrape AI engineering job posts monthly, and the pile has grown to 4,894 descriptions with free-text skill lists.

Every posting phrases skills differently, and that variety blocks counting. One ad asks for "LLM evals", the next wants "model evaluation", and a third lists "testing AI systems" for the same work.

In this post, I'll share:

- why raw skill strings resist counting
- the five taxonomy buckets I settled on
- how I normalize titles before mapping skills
- where the mapping breaks down
- what the normalized counts show

## Five Buckets, Stated Bare

The taxonomy holds five buckets, and each bucket maps to one question I ask of a posting. I list them here once, then cover each in more detail below.

1. Model interaction, covering prompting, agents and tool use
2. Evaluation, covering tests, judges and scoring
3. Data handling, covering pipelines, retrieval and storage
4. Deployment, covering serving, monitoring and cost control
5. Collaboration, covering reviews, docs and stakeholder work

Those buckets emerged from reading 200 postings by hand in February. I tried seven buckets first, and two of them never collected more than a dozen postings each.

## 1. Model Interaction

This bucket collects every skill about driving a model toward a task. Prompt design, agent frameworks and function calling all map here, since postings treat them as one hiring need.

The raw strings vary most in this bucket. I found 63 distinct phrases for agent work alone, from "LangGraph" through "multi-step tool use" to "autonomous workflows".

Normalization here means lowercasing, stripping version numbers and mapping 40 known tool names to 12 canonical labels. That pass reduced 1,140 distinct strings to 214 labels, and manual review merged those into 31 skills.

## 2. Evaluation

Evaluation skills ask whether the model output meets a bar. Postings phrase them as "evals", "quality gates", "red-teaming" or "A/B testing", and all four map to this bucket.

I kept this bucket separate from testingML libraries because postings separate them too. Ads that mention `pytest` for application code still ask for LLM-as-judge methods in a different paragraph.

The counts surprised me here. Evaluation appears in 61 percent of postings, ahead of data handling at 54 percent, although my own hiring conversations had ranked data work higher.

## 3. Data Handling

Data handling covers getting facts into and out of the system. Ingestion scripts, embedding pipelines, vector stores and cache layers all map here.

This bucket needed the least normalization, since tool names dominate it. Postgres appears in 44 percent of postings, Redis in 29 percent, and three vector stores split another 31 percent.

One caveat applies to those shares. My scraper collects English-language postings from four job boards, so teams hiring in other languages never enter the sample.

## 4. Deployment

Deployment covers running the system where users reach it. Model serving, latency budgets, GPU scheduling and usage dashboards all map here.

Postings split this bucket by company size in a way the others don't split. Startups under 50 people ask for one engineer covering the full serving stack, while larger firms name platform teams separately.

I map infrastructure phrases conservatively here, and anything ambiguous stays unmapped. Roughly 12 percent of deployment strings remain unmapped, which beats the alternative of inflating counts with guesses.

## 5. Collaboration

Collaboration covers the human half of the role. Code review, documentation, incident write-ups and roadmap discussions all map here.

This bucket looks soft until you count it. Mentions of review and docs appear in 73 percent of postings, ahead of every technical bucket. Senior postings mention them twice as often as junior ones.

I normalize this bucket mostly by hand, since phrasing varies without tool names to anchor it. I read 150 collaboration strings by hand, and the bucket stabilized after about 100.

## Limits Of The Mapping

Three failure classes survive every normalization pass I attempt. New tools arrive monthly with unfamiliar names, senior postings bundle skills into vague phrases, and some ads paste generic tech lists unrelated to the role.

New-tool churn costs the most attention. Each monthly scrape adds 20 to 40 unknown strings, and I spend about an hour mapping the frequent ones by hand.

Vague senior phrases resist mapping by design. A line like "own the AI roadmap" spans all five buckets, so I tag it as multi-bucket instead of forcing it into one.

The generic tech lists I drop outright. When a posting lists 30 skills from Java to Kubernetes without context, no taxonomy can recover which three the team actually needs.

## Counting With Stated Limits

The normalized counts support one claim I trust. Evaluation demand grew from 48 percent in January to 61 percent in June, and that climb survives every sensitivity check I ran.

Other comparisons stay suggestive rather than firm. Data-handling demand looks flat, deployment demand tilts toward startups, and collaboration demand rises with seniority, although the sample skews toward venture-backed firms.

The taxonomy works because it normalizes enough to count and no more. I spent roughly 15 hours building it, and the monthly upkeep takes about two hours per scrape.

I'll publish the bucket definitions and the mapping script in a future post. If you want to follow along, don't forget to subscribe.
