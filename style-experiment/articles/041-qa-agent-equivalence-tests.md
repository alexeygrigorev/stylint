# Writing Equivalence Tests for a QA Agent

In June 2026 I built a QA agent for a course platform with 112 support questions. The first run looked useful and gave the wrong answer to 17 of them. I stopped shipping answers and spent three days turning the same questions into equivalence classes.

I wrote this as a synthetic style exercise with fictional users and measurements. I would still reuse the workflow with a real assistant.

In this post, I'll share:

- why question examples hid several behaviors
- how I grouped inputs by expected behavior
- how I wrote a compact test manifest
- how I compared the agent with human answers
- what I changed after the first results

## The First Run

The obvious approach was to save 112 questions as one test list. I put them in `tests/questions.jsonl` and asked the agent to answer each one. The agent answered 95 questions acceptably.

That number felt strong until I looked at the failures. The errors clustered around refunds, deadline extensions, and certificate names. Meanwhile, the 95 passing cases were mostly ordinary login and video playback questions.

The headline score rewarded the easiest cases. It gave me almost no information about the risky branches.

## Grouping by Behavior

I printed every question and sorted them into groups by the outcome a student expected.

The eight classes were:

- account access
- playback
- assignment submission
- deadline extension
- refund
- certificate
- course access
- human escalation

Deadline extension split into three subclasses. The agent should grant a documented illness a maximum of 14 days automatically. It should refer longer or paid-course cases to a person and refuse a completed course.

Each class got a short behavior schema.

The extension schema said:

```text
Input: student asks for a deadline extension.
Evidence needed: course ID, original deadline, and reason.
Automatic approval: illness with a date, maximum 14 days.
Human review: paid course, extension over 14 days, or second request.
Refusal: completed course or missing course ID.
Output: decision plus the policy sentence used.
```

Writing the schema exposed two unwritten rules in our support policy. We had never defined documented evidence, and we had never decided whether a second request reset the first review decision.

## Building the Compact Set

The full set was still useful for regression runs, but 112 cases made iteration slow. A local run took 38 minutes and cost about $4 with the hosted model.

I chose 42 representative cases. They included every class, boundary dates, mixed evidence, and 12 known hard cases. The compact set ran in 9 minutes and cost roughly $1.20.

Each row had four fields.

The extension example showed the minimum I needed:

```json
{
  "id": "extension-07",
  "class": "deadline-extension",
  "input": "Can you move my deadline? I was sick last week.",
  "expected": "human-review"
}
```

I deliberately left out the expected explanation. The agent could phrase that part in many ways, so the test only checked the decision and the cited policy.

## Comparing with Human Review

For the next check, I needed a human baseline. A colleague, Maren Keller, reviewed the same 42 decisions without seeing the agent output. She marked 39 cases as clear and left 3 for policy discussion.

We compared the agent output, Maren's decision, and my original label for every case. A short Python script summarized agreements and printed every disagreement.

```python
results = load_results("runs/2026-06-14.jsonl")
report = compare(results, keys=["agent", "human", "expected"])
print(report.conflicts())
```

The script found 11 conflicts. Seven came from label mistakes in my manifest, two came from an acceptable alternative policy sentence, and only two marked genuine quality failures.

This disagreement review was the most useful part of the exercise. It took longer than reading a score, but it made the expected behavior sharper.

## Revising the Behavior Schema

I changed the deadline schema after the review. Missing course IDs now trigger one clarifying question, and second requests always go to a person even when the first request was approved. The agent also has to quote the policy sentence it used.

The revised version answered 39 of 42 compact cases correctly. On the full set, it handled 104 of 112. The remaining 8 failures sat in certificate wording and one refund boundary.

That score looks smaller than the original 95, but it's more useful. The failures now map to named classes, and ordinary cases no longer dominate the result.

I also added a test for output shape. Each answer had to contain a decision, an evidence list, and a next action. Six technically correct answers failed because they skipped the next action.

## Final State

Equivalence tests forced me to define behavior before judging the agent. A pile of real examples showed which questions were common, while classes showed which decisions mattered.

The compact set didn't replace the full set. I could edit and check faster with it, while the full set caught regressions after each schema change. I now run the compact set after edits and the full set before deployment.

The stored artifacts also made handoff easier. The classes live in `tests/classes.md`, the compact rows live in `tests/compact.jsonl`, and the full run results use the date as a filename. A new reviewer can trace a failure from the row ID to the schema and the raw answer.

This approach doesn't solve open-ended conversation. It works best when the assistant should make a small number of predictable decisions. In that setting, classes turn a vague quality debate into a reviewable change.

I expect to reuse this approach for a retrieval assistant next. If you want the follow-up, subscribe to the newsletter.
