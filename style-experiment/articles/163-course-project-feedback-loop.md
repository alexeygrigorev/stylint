# Scaling Project Feedback with a Checklist and Short Recordings

I invented Applied Data Pipelines, its 54 learners, and every project result for this synthetic style exercise. In the fictional spring 2026 cohort, reviewing each final project took me 35 to 50 minutes. At that pace, feedback arrived too late to help anyone improve the work.

In this post, I'll share:

- how I wrote a definition of done learners could apply
- what evidence belongs in the submission
- how I used one review checklist
- why short recordings reduced written comments
- how I kept the loop honest across three cohorts

## 1. Define Done Before Projects Start

The first version of my rubric had 22 criteria. It looked thorough, and learners couldn't use it while building. They optimized for visible artifacts rather than for a working pipeline.

I reduced the definition of done to five checks:

- the pipeline runs with one documented command
- input and output schemas are explicit
- at least one data-quality test fails on bad input
- the README explains a business decision
- limitations and manual steps are listed

Every check had to be observable by another learner. I removed "good code quality" because it produced contradictory reviews. I kept "a failing quality test produces a clear error" because we could reproduce it.

I introduced the checklist in week 1 and used the same five items in the assignment, self-review, and final review. Learners still made design mistakes, but they stopped discovering the submission format after deployment.

The first cohort with this checklist submitted 48 of 54 projects with all commands working, compared with 31 in the previous fictional cohort.

## 2. Collect Evidence, Not Descriptions

Each submission now includes a short evidence section in the README. The evidence proves that the checks ran rather than asking a reviewer to trust a screenshot of success.

A project called Transitdelay, a fictional bus-delay dashboard, included these items:

- `make run` followed by the final seven log lines
- a 12-row output table and its row count
- one failing test that rejected negative travel times
- a link to the deployment URL and a test account
- a paragraph naming the missing route-refresh job

I capped evidence at one screen. If a learner needed more, the pipeline probably needed a smaller verification path. Three projects moved manual checks into scripts while preparing evidence, and that was the behavior I wanted.

Peer review also changed after learners added evidence, and reviewers stopped arguing about style and started reproducing results. In week 4, each project received two peer reviews. Eighty-two percent of their comments referenced a command, file, test, or output.

## 3. Review With the Same Checklist

My review follows the five checks in order. I reproduce the pipeline first, then look at schemas and tests, and read the README last. If the first check fails, I stop and write that as the project's next step.

The checklist file has one row per item and three possible states:

- passed
- passed with a caveat
- failed with the command or file to fix

A caveat must say its cost. For example, a pipeline can pass with a manually refreshed source file if the README names the manual step and the staleness that can result.

The ordering protects review time. In the spring cohort, 11 projects failed the first run command. Those learners got a reproducible answer within two days instead of comments about documentation they couldn't apply yet.

I allow 20 minutes for a normal project and 30 minutes for one with a deployment. A timer is unglamorous, and it forces me to write the smallest comment that unblocks the learner.

## 4. Record the Next Step

For every project, I record a two-minute screen capture. The recording walks through one failed or caveated check and demonstrates the next change. Written feedback still contains the checklist results.

The recording has a fixed sequence:

- show the command and its output
- name the rule that failed
- point to the file to change
- describe the passing result
- stop before redesigning the project

Two minutes is enough for one problem and too short for a lecture. If I need ten minutes, I create a course exercise instead of repeating it in individual feedback.

Learners watched the recordings more reliably than long written comments. In a post-course survey of 49 learners, 43 said they used the recording to make a change. Only 27 said they reread the full written review.

I keep recordings inside the course site and remove personal data from shared examples. When a project has a particularly useful failure, I ask permission before reusing that example in course material.

## 5. Keep the Loop Honest

A checklist can drift into a compliance ritual, so I track whether feedback leads to changes. Each learner submits one follow-up after receiving feedback, and it can be a commit, a corrected README, or a written decision to stop.

Across the three fictional cohorts, 86% of learners made at least one checklist-driven change. The remaining learners had mostly reached the end of the cohort, so I shortened the final scope this year rather than adding more criteria.

The checklist also gets pruned. If a check produces no changes in two cohorts, I either fold it into another check or remove it. The current list remains at five items despite pressure to add security and performance requirements.

Those topics still matter, so they now appear as module exercises. A final project can pass without covering every advanced concern. That trade-off keeps feedback focused on whether the core pipeline works.

The practical rule is to review the smallest claim a project makes. The pipeline should run, validate its data, and explain a decision. I'll write about the follow-up submission format in a future article. Subscribe to stay updated.
