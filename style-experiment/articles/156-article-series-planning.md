# Planning an Article Series Before Publishing Part One

For this synthetic style exercise, the projects and numbers are invented. In March 2026 I wanted to explain retrieval systems without cramming indexing, ranking, evaluation, and operations into one giant post. I sketched five parts, wrote the first one twice, and changed the plan before publishing. The series became easier to sustain once the shared example and promise came first.

In this post, I'll share:

- how I tested the promise against real questions
- why I mapped dependencies before writing part one
- how one example repeated across every part
- what I planned for cadence and catch-up material
- where the series still needs another pass

## The promise

The first draft promised to cover "everything about RAG". That sounded large and told a reader little, so I rewrote the promise as a concrete outcome. A developer could build a searchable prototype, measure whether retrieval helped, and decide what to run next.

I listed the target reader as someone comfortable with Python who had used an LLM API. I also listed outcomes the series would avoid, such as model fine-tuning and vector database procurement. That boundary made the promise easier to keep. A good series should be possible to finish.

## Dependencies before deadlines

Then I drew the content on paper, with one box per article. The first version put evaluation in part four because it felt advanced. That failed a practical test. A reader could build an index in part one and have no way to know whether it was good for three weeks.

I moved a tiny evaluation into part two. The reader only compared ten queries against a simple keyword baseline, but that was enough to establish the habit. The revised order started with indexing and measurement, then moved through ranking and feedback before operations. Each part needed the previous part to make sense, and none needed knowledge from a later part.

I learned a simple ordering rule from that change. Publish the measurement loop early, so a reader can stop after any part and still have a useful artifact.

## One running example

I chose a fictional support archive with 4,800 question-and-answer pairs and used it in every section. The archive had a title, body, product area, and date. It was small enough to fit on a laptop and messy enough to demonstrate real problems.

This choice removed a tax from every article. I didn't need to introduce a new dataset, explain a new business, or write new setup steps. When part three added reranking, the improvement used the same ten-test queries and the same support answers. The reader could see the delta rather than learn another domain.

It also exposed gaps I would have hidden with separate examples. Part four needed user feedback, so I added a `helpful` flag to the archive schema. Part five needed deletion and refresh behavior, so I documented how long an answer stayed canonical after its source changed. Writing those sections forced the details out early.

## Cadence and catch-up

I planned a biweekly cadence and wrote two articles before publishing part one. The buffer covered travel and a release week. It also gave me time to revise part one after seeing how part three developed.

Each article opened with three reminders:

- what the reader built before
- what this part added
- what artifact should exist afterward

The reminder stayed under 120 words. That was enough orientation for a new reader and not enough to feel like a rerun.

I also kept a shared project folder with the current dataset, notebook, and tests. For the final article, I linked a tagged version of that folder. A reader starting late could reproduce the endpoint state instead of merging five sets of edits.

## Naming and structure

I tried titles such as "Retrieval Systems, Explained", but they described a topic and hid the order. The final titles used a numbered promise: "Build a Small Search Index", then "Measure Your Search Before Tuning It". The word "part" appeared in the subtitle and in a link block near the top.

Each part used the same structure, starting with a concrete failure and then showing the smallest fix, measurements, and a limitation. I resisted adding a new architecture diagram to every part. One diagram introduced the base system, and later parts showed only the component being changed.

The consistency also helped editing because I could check whether every part had a working artifact, a number, and an explicit limit. If one of those was missing, the part was incomplete.

## Series status

The published plan held through all five articles. Median drafting time fell from about fourteen hours for part one to around nine hours for part four. The recurring example and the stable review checklist accounted for most of the savings.

The published plan exposed two weaknesses. The Q&A archive is synthetic and cleaner than a real ticket system, so the text can understate extraction work. I also need a better on-ramp for readers who only care about operations because they currently have to skim two implementation parts first.

## Lessons Learned

A series is easier to plan as a set of dependencies than as a list of topics. The promise tells the reader why to start, and the running example keeps the middle from drifting.

I would now write the last article's title before publishing the first one. If I can't describe its outcome clearly, the earlier parts probably promise too much.

I plan to reuse this method for a shorter course on agent evaluation. Subscribe if you want to see how that series develops.
