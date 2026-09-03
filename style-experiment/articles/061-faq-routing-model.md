# Adding a Simple Router in Front of a FAQ Assistant

Last March, my fictional `course-helper` assistant answered 412 questions in one week. Most were repeats from a FAQ corpus, but 74 needed course staff. The assistant was polite even when it should have stayed quiet, so I added a router in front of it.

I invented the course, messages, and measurements for a synthetic style exercise. I'm using that fiction to think through a common integration problem without describing a real deployment.

In this post, I'll share what changed:

- the routing classes I chose
- why confidence thresholds needed two rounds of tuning
- the fallback paths for unknown and mixed questions
- the logs I used to compare the versions
- what still fails after three weeks

## The first version answered everything

The obvious choice was to send every question to retrieval and answer whatever came back. I already had 380 curated answers in `faq/answers/*.md`, and retrieval usually found something plausible.

That "usually" was the problem. When a student asked about a broken lab environment, the assistant returned a FAQ answer about installation requirements. The text was technically related, and it didn't help the student.

I reviewed 50 sampled conversations with a colleague who helps moderate the fictional course forum. Nineteen needed a human, but only seven were routed to a contact form. The rule I took from that review: an assistant should be allowed to say that a question belongs elsewhere.

## Define the routing classes

I kept the taxonomy small enough to review by hand:

- `faq`: the question maps to a stable, approved answer.
- `coursework`: the question needs course-specific human judgment.
- `account`: the question involves login, billing, or access.
- `mixed`: the question contains more than one intent.
- `unknown`: the router can't choose a useful class.

The exact names matter less than the boundaries. `coursework` includes grading, extensions, and labs where the right answer depends on a student's submission. `account` was separate because it usually needs private data and should never be answered from public notes.

I wrote examples for each class in `router/examples.yaml`. They served as a smoke test and forced me to state the boundary cases. One example read, "I missed the deadline because my GPU sandbox stopped". That belongs in `coursework`, even though it mentions an infrastructure term.

## Build the smallest useful router

I used a small classifier model behind a plain Python function. The function accepts the message, returns a class, a confidence score, and a reason string. The router lives in `src/helper/router.py`, while the assistant lives in `src/helper/faq.py`.

The core flow takes five steps:

```text
message -> normalize -> router -> confidence check -> action
```

Normalization removes signatures, quoted earlier messages, and attachment names. Those fields increased token use and occasionally pulled the classifier toward the wrong class. The router then calls the model once.

For the first version, I asked the model to return JSON with these fields:

```json
{
  "class": "coursework",
  "confidence": 0.71,
  "reason": "asks about a deadline exception",
  "secondary_class": null
}
```

If parsing failed, the router returned `unknown`. That sounded conservative, and in practice it worked better than trying to repair malformed output. A broken response indicates a routing problem, so I didn't send a risky answer.

## Tune thresholds with a labeled sample

My initial threshold was 0.70 for `faq` and anything else. During the first two days, 12 percent of messages fell into `unknown`. That was too noisy, so I lowered the global threshold to 0.55.

It immediately routed two questions about assignment deadlines into `faq`. The retrieved answer explained the deadline policy, but the student had an approved extension. The mistake was mine: I had optimized volume instead of consequence.

I set `faq` to 0.78, while `account` and `coursework` routed at 0.60. In other words, an automatic public answer had to be clearly safe, and a route toward a human could tolerate more uncertainty. Over the next seven days, unknowns dropped to 6 percent and no sampled deadline case went to `faq`.

I found mixed questions harder. A message could ask for an extension and mention a payment error. I treated any strong secondary intent as a `mixed` route. The routing action then answered only the safe public part and asked the student to submit the private issue through the staff form.

## Add fallbacks and logs

Each routing decision produced a compact record. I keep the class, confidence, and action in `logs/router.jsonl`, plus retrieval score and answer ID. No message text is stored because this fictional setup handles private support traffic.

The router now selects one of four actions:

- answer directly from an approved FAQ entry
- show the staff contact form
- show both a public answer and the form
- show a short unknown-question response

The unknown response names what happened: the assistant couldn't identify the request confidently. It also offers three common categories. That added one interaction, and it reduced silent dead ends.

After three weeks, the router handled 468 messages, and the sampled results were directionally good:

- 58 percent answered from FAQ
- 27 percent routed to staff
- 9 percent used the mixed path
- 6 percent were unknown

I sampled 40 of those conversations. Two FAQ answers were technically correct and emotionally wrong, both about failed submissions. The response acknowledged the policy but didn't acknowledge the frustration. I added a human-approved empathy sentence to those two entries rather than giving the router free text control.

## Current limitations

The router is useful because its decisions are inspectable. For each message, I can answer why the assistant acted. The reason string is usually short and occasionally vague, but it's much better than a single opaque response.

The main limitation is drift. Course policies change every cohort, and new support topics appear during project season. I now review the logs weekly and label 30 sampled messages. Five minutes of labeling usually reveals one boundary case, and that case becomes an example in `examples.yaml`.

I'll add a per-category report next. Aggregate percentages hide a single new failure class until it grows. I want a table of new or rising clusters, even if a person still names the cluster.

Routing is a product decision. The model helps apply it consistently, but the classes, thresholds, and fallback actions encode who's allowed to answer and what happens when nobody knows. If I extend this exercise, I'll write about the escalation queue that receives the staff routes. Subscribe if you want to see where that experiment goes.
