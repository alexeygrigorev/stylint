# A Review Process for Portfolio READMEs

In March 2026 I reviewed 27 portfolio READMEs for a mentoring program. Nineteen projects could run, but only seven explained how to reproduce the result in under five minutes. The gap wasn't coding skill. It appeared at the exact moment a reviewer arrived.

I wrote this as a synthetic style exercise with invented applicants and measurements. I would still reuse the four-step review process.

In this post, I'll share:

- how I review the first screen before reading the code
- what a reproducible example needs
- how I check evidence behind the claimed results
- why limitations improve a portfolio
- the feedback format I now use

## The First Screen

I start with a 30-second first-screen test. I open the repository and read only what appears before scrolling.

I write down the purpose, the main output, and the runtime requirements.

In the strongest README, the first sentence named the task. It classified 12,000 support tickets into six categories and exposed the result through a FastAPI endpoint. A screenshot showed the request body, response label, and confidence score.

In the weakest READMEs, the opening section listed course names, model architecture, or technologies. I could often guess the domain from the repository name, but I couldn't describe the project's actual behavior.

This first screen matters because reviewers often have 30 to 40 repositories to look at. When they have to reconstruct the purpose, they usually move on before reading the code.

## Reproduction Before Description

After the first screen, I clone the project and try the README's first command. I use a clean container with Python 3.11, no cached model files, and no project-specific environment variables.

For a reproducible README, I expect three things:

- one command that starts the useful path
- expected output that I can compare
- a stated runtime and model-download size

Eight projects passed this test without a question, and their commands usually looked like `make demo` or `uv run python scripts/predict.py --input sample.csv`.

Six failed because a required file lived outside the repository. Three failed because the README assumed a database server without showing how to start it. Another four had no expected output, so I couldn't tell whether an empty response was correct.

When reproduction failed, I recorded the first error verbatim and the elapsed time. That detail turned vague feedback such as "setup was hard" into an actionable fix.

## Check the Evidence

Next, I compare the README's claims with the repository's evidence. A claim can be modest and still convincing if the artifact exists.

I look for four items:

- the dataset or a representative sample
- the evaluation script and its raw output
- a saved model or instructions for creating it
- at least one failed case with the reason

One applicant reported 94% accuracy on a 200-row validation set. She linked the split file, showed the confusion matrix, and explained that the class distribution differed from production. I found that score more credible than an unsupported 99% score elsewhere.

Another project claimed a two-second average response time. The repository included a benchmark script, but it ran against 20 cached requests. I suggested reporting the cache hit rate or removing the latency claim.

The evidence review takes 10 to 15 minutes per repository. It prevents me from rewarding confident text over reproducible work.

## Limitations as a Feature

I now treat the limitations section as a sign of engineering judgment. It tells me whether the applicant knows where the system would break first.

Useful limitations are specific:

- supported languages and known language failures
- maximum tested file size
- data period and known class imbalance
- infrastructure the project hasn't handled

One README said the model had only seen English and Spanish tickets, so it would likely route German requests to a fallback. Another said the queue used an in-memory store and would lose jobs after restart. Both applicants showed awareness without pretending to have solved the remaining work.

By contrast, "the project could be improved with more data" gives a reviewer no information. Every project could use more data, so the reviewer needs the specific gap.

## Feedback Format

I close each review with four short blocks.

The blocks cover:

- what works
- reproduction blockers
- evidence gaps
- the first two changes I would make

I keep praise attached to a concrete artifact, and I keep each suggested change small enough to finish in a weekend.

A typical high-priority comment looked like this: "The API starts with `make serve`, but `sample.csv` is missing. Add a 20-row sample and one expected response, then show both in the README".

Across the 27 reviews, reproduction fixes came first 19 times, evidence fixes came first 5 times, and presentation fixes came first 3 times. That distribution confirmed my order of operations.

I now use the same process for my own repositories before adding them to a portfolio page. It's uncomfortable, but it finds the missing sample file before an interviewer does.

The process doesn't judge a project's ambition. A small tool can pass every step if it states its scope honestly and reproduces its result. A large model project can fail if the only visible artifact is a training script and a number.

I also adjusted my own projects after the review round. I added a 25-row sample to a classifier. I reduced a claimed latency number to the tested cold-start path, and I documented that one parser had only been tested on English dates.

I plan to turn this review into a reusable checklist in a future article. Subscribe for that update.
