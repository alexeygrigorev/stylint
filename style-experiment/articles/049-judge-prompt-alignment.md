# Aligning a Judge Prompt with Human Review

In July 2026 I built an LLM judge to score 240 customer-email drafts for a course support bot. The judge agreed with my scores on only 58% of the set. The mismatch started with a specification problem hidden inside one long prompt, not with the model.

I wrote this as a synthetic style exercise with invented drafts, raters, and scores. I would still use this alignment workflow before trusting a judge at scale.

In this post, I'll share:

- how I chose a small disagreement sample
- how I turned review comments into a rubric
- how I revised the judge prompt in layers
- which threshold I set for automatic acceptance
- what changed after the second review round

## Start with Disagreements

My first judge prompt contained the task, a quality scale from 1 to 5, and a long instruction to reward helpfulness. It returned plausible explanations, so I initially trusted the score.

The plausible explanations were exactly the danger. On a 60-draft sample, I had marked 39 drafts acceptable, while the judge marked 47. Nine drafts received a 4 or 5 even though they missed the refund deadline rule entirely.

I stopped collecting new scores and selected 30 drafts for disagreement review.

The sample had three groups:

- 12 drafts where I approved and the judge rejected
- 12 drafts where the judge approved and I rejected
- 6 drafts where both used extreme scores of 1 or 5

I included the extremes because a wide gap often reveals a missing criterion. I deliberately left out cases where both raters agreed, because they couldn't explain the mismatch.

## Turn Comments into a Rubric

For each disagreement, I wrote why I made my decision in one sentence. After 30 reviews, I grouped those sentences by cause.

From those sentences, I derived five criteria:

- correctness of the support policy
- direct answer in the first two sentences
- absence of invented customer details
- tone appropriate for a frustrated adult
- one concrete next action

The first three could be checked from the draft and source policy. Tone needed a judgment call. The next action had to match the customer's original request.

I gave each criterion a separate weight:

```text
policy correctness: fail or pass
direct answer: 0-2 points
no invented details: 0-2 points
tone: 0-1 points
next action: 0-1 points
```

After the policy check passed, a draft could receive a score of 6. The structure mattered because a friendly draft with an invented refund rule should still fail. The original prompt had allowed tone to compensate for a factual mistake.

## Revise the Prompt in Layers

I rewrote the judge prompt in three passes. I supplied only the rubric and source policy in the first pass. I added two positive and two negative examples in the second. I required JSON output with a reason for every criterion in the third.

The output format looked like this:

```json
{
  "policy_correctness": "pass",
  "direct_answer": 2,
  "no_invented_details": 1,
  "tone": 1,
  "next_action": 0,
  "total": 4
}
```

The required fields slowed the judge down slightly, from 1.4 to 1.9 seconds per draft. They made debugging much faster because I could see which criterion caused each low score.

On the 30-draft disagreement sample, exact agreement with me rose from 18 of 30 to 25 of 30. The remaining disagreements were all tone judgments or borderline invented details.

## Set the Acceptance Threshold

Next, I needed a decision rule. A judge score alone doesn't publish an email, so a threshold determines which drafts can go out without another human review.

I used these bands:

- 0 to 3 points: revise or reject
- 4 points: human review
- 5 to 6 points: automatic acceptance

I tested this rule on 180 fresh drafts. The judge auto-accepted 71 drafts, sent 88 to human review, and rejected 21. A second rater, Ilona Marsh, reviewed the accepted set and found 4 problematic drafts.

That gave a 5.6% miss rate among auto-accepted drafts. It was too high for customer support, so I moved automatic acceptance to 6 points. Only 22 drafts then bypassed review, and Ilona found no problems in that smaller set.

The stricter threshold shifted work back to people. Still, 88 drafts arrived with criterion-level explanations, so the reviewers could make a decision in about 25 seconds instead of writing a reply from scratch.

## Run a Second Review Round

After two weeks, I sampled 50 accepted drafts and 50 human-reviewed drafts for a second round. I asked Ilona to use the same rubric and mark any criterion she would change.

She changed 9 criterion scores. Five involved tone, two involved the direct-answer boundary, and two involved next actions that were correct but delayed until the final sentence. I turned those notes into three new examples and one sentence in the rubric.

The updated judge stayed within one criterion of Ilona on 46 of the 50 drafts. Exact agreement reached 39 of 50. That number is useful for tuning, but it isn't a universal accuracy claim.

I kept a weekly sample of 20 drafts for drift review. Support policies change, so the judge's source policy and human sample need to age together.

## Final State

The judge prompt now contains a rubric, policy text, examples, and a strict output schema. The score is only one input. The threshold and weekly human sample determine what the system actually accepts.

Aligning the judge took three working sessions. The savings came afterward: reviewers spent less time rewriting drafts, and their feedback had a stable vocabulary.

I plan to show how I version the rubric with the evaluation set. Subscribe for that follow-up.
