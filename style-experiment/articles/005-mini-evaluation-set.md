# Building a Mini Evaluation Set Before Touching a Prompt

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. In April I changed a support-email classifier to reduce false positives. The change looked good on ten examples I had in my head and pushed two legitimate refund requests into the wrong folder.

I had skipped the boring step. Since then, I build a 20-case evaluation set before editing any prompt. It takes 25 to 45 minutes for a narrow task, and it has caught three regressions in the last month.

This isn't a full evaluation framework, but it's a small artifact I can read, run and change. For a task with one model call and one observable outcome, twenty cases are enough to reveal obvious damage.

In this post, I'll share:

- where the real cases come from
- how I label and balance the set
- how I define a pass rule
- how I run the checks
- when the mini set is insufficient

## The Cases Come From Real Use

The set needs cases from real use. I start with the artifact that produced the failure, then add neighboring examples from logs, tickets or my inbox. For the support classifier, I copied 20 messages from the previous 30 days.

I don't generate all examples with a model. Synthetic examples can help later, but they tend to encode my assumptions. My first ten real messages included a Dutch invoice, a message with no subject and one customer who put the refund request in an attachment.

Each case lives in a JSON object with an ID, input, expected result and source. The source field records whether the case came from a production sample or a later regression.

Here's one case from the set:

```json
{
  "id": "refund-004",
  "input": "I was charged twice for order 2043.",
  "expected": "refund",
  "source": "production sample"
}
```

That message is short and obvious to a person. It's useful precisely because the old prompt handled it correctly and the new one didn't.

## Label And Balance The Set

Twenty cases split into categories in this project:

- billing questions
- refund requests
- bug reports
- spam

I kept five examples in each category. The balance is artificial, but it prevents the set from becoming a billing-only test.

I also include two hard examples per category. A hard example is one where the category depends on a phrase, a date or a nearby message.

The bug-report set contains a message that mentions a billing page but describes a JavaScript error.

The labels stay coarse, and I don't score tone or urgency yet, because the production decision only routes email. When the application changes, I build a new set rather than stretching an old one beyond its purpose.

## Define The Pass Rule

Before running anything, I define what "pass" means. For each case, the classifier must return the expected category and a confidence above 0.60. The threshold comes from the current routing rule, and I record it beside the test data.

I also set a minimum for the whole set: 19 of 20 correct. One miss can show that a case is ambiguous. Two misses in the same category stop the prompt change. If the failures differ, I look at the examples and decide whether they reveal a real boundary.

The pass rule goes into `README.md` next to `cases.jsonl`. That makes the criterion part of the artifact instead of a private standard in my head.

## Run The Checks

The runner is deliberately small. It reads cases, calls the model and writes a JSON report.

The command fits in one line:

```bash
uv run python eval/run_classifier.py --cases eval/cases.jsonl
```

The report includes the case ID, expected result, actual result and confidence, and failed cases appear first. For a 20-case set, the model call took 31 seconds with a small API model and cost about $0.04.

I run the set three times when a decision is close. Model responses can vary, and it's misleading when a single run makes a boundary look more stable. The report records the date, prompt version and run number.

The latest report from 21 April showed 18 correct cases. Both failures were refund messages written as billing questions. That was enough to reject the prompt change and add two regression cases to the set.

## The Limits Of The Mini Set

The mini set has clear limits. It can't estimate accuracy across thousands of messages, measure bias across customer groups or replace monitoring after deployment. It only answers whether a change damages a small set of known cases.

It also ages, because production language changes and a set kept too long starts testing last quarter's questions. I review the 20 cases every six weeks, retire three to five items and add fresh samples.

For multi-step agents, the same idea needs more structure. A final answer can be correct after several bad intermediate actions. In that situation I log each step and evaluate the route as well as the result. The set may still contain 20 tasks, but each record becomes richer.

## Lessons From The Mini Set

The evaluation set changed the conversation with the model, and I no longer ask whether a prompt reads better. I ask whether it preserves the behavior represented by 20 examples and which boundary it moves.

The artifact also improves review. A coding agent can run the same command, and a colleague can see the pass rule without reading my prompt history. The small data file makes the decision public inside the repository.

My next change is a weekly job that samples ten live classifications for review. That won't replace the mini set. It will help me notice when the set no longer represents the input.

I'll write more about that monitoring workflow after it runs for a month. If you want to follow along, don't forget to subscribe.
