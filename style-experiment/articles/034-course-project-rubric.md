# Designing a Rubric That Students Can Self-Apply

This synthetic style exercise uses a fictional project and invented details.

I review about 90 final projects per cohort in a fictional data engineering course. Last term I spent 12 minutes on the first project and 4 minutes on the last one. The comments also drifted: the first submissions got detailed suggestions, while the last ones got short scores.

The problem wasn't effort but buried context. I had a checklist in my head, so I turned the review into a rubric.

The cohort numbers in this article are invented examples for this exercise.

In this post, I'll share:

- the four rubric categories and pass rules
- how I tested the rubric with student reviewers
- what changed after one cohort used it
- how I handle edge cases and partial credit
- what I changed in my own review process

## Four Categories

The rubric has four pass/fail categories:

1. functioning demo
2. automated tests
3. README and reproduction steps
4. stated limitations

I ask students to run the demo with two commands and produce visible output. I require tests that include one happy-path example and one boundary-case example. Students document inputs, outputs, and setup in the README, then name at least two unsupported cases.

The binary rule matters because a student can tell whether "the demo runs with two commands" passed. They can't tell what "good design" means at the end of a long course.

## Testing with Student Reviewers

I tested a draft with 11 volunteer students before the term started. Each person reviewed the same two fictional submissions and filled the rubric without seeing my notes.

The agreement was uneven:

- functioning demo: 11 of 11 matched my judgment
- automated tests: 9 of 11 matched
- README: 8 of 11 matched
- limitations: 5 of 11 matched

Their comments explained the numbers. Most students knew how to run a script, but they disagreed about what counted as a limitation. Some wrote "no Kubernetes", which wasn't relevant. Others wrote "slow for 10 million rows", which was relevant and testable.

I rewrote the limitations rule around three questions:

1. What input volume did you test?
2. What data did you exclude?
3. Which component would fail first under heavier load?

After that change, agreement on limitations rose to 9 of 11 reviewers.

## One Cohort of Results

The next cohort submitted 87 projects. Before the deadline, 71 students used the rubric and recorded a self-score. The other 16 submitted without a completed rubric.

The self-scores were optimistic, but useful. Students predicted pass on all four categories for 58 of the 71 rubric users. My review confirmed 49 of those predictions. Eight failed on tests, and three failed on limitations.

More importantly, 22 students fixed their projects before submission after filling the rubric. Several told me they discovered missing setup commands when they followed their own README from a clean environment.

My review time dropped from an average of 9.4 minutes to 5.1 minutes per project. The comments became more consistent because we used the same vocabulary.

## Edge Cases and Partial Credit

Some projects don't fit the standard form. A data pipeline may produce a file instead of a web demo. A model assignment may need a notebook for exploratory charts. The rubric allows an equivalent demo if the student states the substitution in the README.

I also added three explicit partial-credit rules:

- one missing command in the README: revise and resubmit
- no boundary test: 80% credit for that category
- irrelevant limitations: revise the limitations section

The rules remove negotiation during grading. They also make it safe to fail the first submission, because revision is a normal path.

For late or broken projects, I still review the repository before applying penalties. A student may have a working local version and a broken upload. The rubric reviews the artifact, while I review the situation.

## Changes to My Review

My review now runs in three passes:

1. run the demo from a clean container
2. read the tests and README while the data job runs
3. compare the submitted rubric with the actual result

The first pass is mechanical, while the second pass looks for reasons behind failures. The third pass records disagreements between the student's prediction and the artifact.

Those disagreements became teaching material. In one project, the student marked tests as passed because "they all ran green". The test asserted only that a file existed. We discussed how to assert row counts and schema types.

The rubric didn't remove my judgment. It moved judgment to interpretation and left checking to the student. That made the course scale without lowering the bar.

I'll publish the next revision after the coming cohort. If you want to follow along, don't forget to subscribe.
