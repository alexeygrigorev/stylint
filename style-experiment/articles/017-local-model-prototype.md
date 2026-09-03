# Prototype with a Local Model or Switch to an API

I wrote this analysis as a synthetic style exercise. Although the usage logs, dates, and prices are fictional, the decision rules reflect how I compare local models with hosted APIs.

In May 2026, I ran a four-week experiment with two implementations of the same meeting-note helper. The local version used a 7-billion-parameter model on a laptop with 32 GB of memory. The hosted version used a mid-tier API and cost about €11 for the month.

In this post, I'll share:

- the privacy threshold that makes local models attractive

- how latency changed my prototype choices

- where local quality was good enough

- why three tasks moved back to an API

- the cost model I now use before building

## Privacy decides the first branch

My local-model experiments start with the data before I compare quality or price. If the input contains client contracts, health records, or unreleased financials, I start on hardware I control. The same rule applies to anything covered by a data-processing agreement.

That rule comes from a project with a fictional law firm. The first prototype summarized 180 engagement letters. The letters contained names, matter numbers, rates, and exceptions to the standard agreement. Sending that corpus to an external API would have required a review that the two-day prototype schedule didn't allow.

The local prototype was acceptable for that job. It ran on the laptop, wrote output to `/tmp/legal-notes`, and used a local embedding model. Nobody outside the device saw the letters.

Privacy still has a boundary. Local execution reduces exposure, but it doesn't create a compliance program. The law-firm scenario would still need retention rules, disk encryption, audit logging, and a formal review before production use.

## Latency changes the interaction

The second branch is interaction structure. Local models shine when I can accept a short wait or run work in the background. They become frustrating when I expect conversational immediacy.

On my laptop, the 7-billion model produced the first token in 0.9 seconds and completed a 500-word summary in 24 seconds. That delay was fine for a nightly batch job. It felt slow when I edited a prompt and waited for a new result.

The hosted API produced its first token in 0.4 seconds and completed the same summary in 11 seconds. More important, it stayed at that speed while my laptop ran a build and a browser full of tabs.

For the meeting helper, I settled on two paths. During prompt development, I used the hosted API because iteration speed mattered. In the private deployment, I used the local model because the notes could wait until the morning.

## Some tasks need only good-enough output

Quality matters, but every task has a threshold. I stopped asking which model was better in general and started asking which failures mattered.

The local model met the bar for three jobs:

- remove filler words from dictated notes

- propose five headings for a meeting transcript

- classify notes as action, decision, or background

I evaluated those jobs with 80 synthetic and 20 real-shaped meeting notes. The local model agreed with my labels on 92 of 100 classification decisions. Its headings were sometimes dull, but reviewers accepted 86% of them with minor edits.

The hosted model reached 97 agreements and 94% acceptance. For internal triage, the extra quality didn't justify sending every transcript to another service.

## Three tasks moved to an API

Three jobs failed the local threshold, and the first was legal clause extraction. The local model missed unusual limitation-of-liability language in 7 of 40 documents, and those omissions looked harmless in the output.

The second was multilingual question answering. Our test set contained 60 questions in German, English, and Spanish. The local model handled English well, but its German answers mixed registers and mistranslated two accounting terms.

The third was complex tool use. The task required the model to call a calendar API, resolve ambiguous times, and explain conflicts. The local version produced invalid JSON in 14% of 120 runs, even with a schema in the prompt.

For those jobs, we used a hosted model with logging and redaction. We removed client names and matter numbers before the request, stored only task metadata, and kept human review in the loop. That compromise worked because the remaining text no longer identified the client.

## Costs need the whole workflow

API pricing is easy to calculate. Local pricing is easy to underestimate because the laptop, electricity, memory pressure, and maintenance time hide in other budgets.

For the meeting helper, hosted inference cost €11 for 620 summaries in May. A small API deployment would add about €8 per month. The local version used hardware I already owned, but it required two days to tune prompts for a smaller model.

Over twelve months, the hosted option cost about €228. The local option had no inference bill and 16 hours of setup and maintenance. At a blended internal rate of €45 per hour, that work was worth €720. Local execution was therefore more expensive unless privacy made the hosted path unavailable.

That number changed my framing. Local models are best understood as a privacy and control option. Cost savings appear in high-volume workloads or on hardware already running for another reason.

## Lessons from the experiment

I now decide in this order: data sensitivity, interaction latency, quality threshold, then total cost. That order prevents an interesting benchmark from making the privacy decision for me.

The best setup usually combines both paths. I use hosted APIs to accelerate exploration and handle difficult multilingual or tool-use jobs. Local models hold the private, repetitive, background work.

I plan to publish a small checklist for recording these thresholds before a project starts. Subscribe if you want the follow-up.
