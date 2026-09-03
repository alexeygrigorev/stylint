# Routing Requests Between a Small Model and a Larger One

Last November I added a fictional support assistant named `replykit` to a small invoicing product. Its 9,200 monthly questions ranged from password resets to questions about broken recurring invoices. The first version sent every request to a large hosted model, and the monthly bill reached EUR 214.

I wrote this piece as a synthetic style exercise. Every product, model, request count, latency and cost figure in this article is fictional.

The cost wasn't the only concern. Password questions usually waited 2.8 seconds for a response, while a small local model already answered them correctly during testing. We needed a way to choose the model per task without sending simple requests to the expensive path.

In this post, I'll share:

- how I grouped requests into task classes
- how the router estimates confidence
- how it chooses a fallback path
- how we track cost and quality
- what changed after eight weeks

## Group Requests Into Task Classes

The first useful step was classification, and the labels came from support categories rather than model names. We already knew which workflows required account access, invoice data or a free-form answer.

We started with four classes:

- account actions such as password resets and email changes
- invoice questions that require retrieval from billing records
- template questions that repeat every month
- complex complaints involving multiple messages and a human decision

For two weeks, I labeled 1,000 sampled requests by hand. Account actions made up 41% of the sample, invoice questions 27%, template questions 19% and complex complaints 13%. That exercise changed the design before I wrote any router code.

Complex complaints needed a human and a larger model, while account actions needed strict validation and a small model. The initial classifier was therefore simple: a support form provided the class when available, and a logistic-regression classifier filled the gap for chat messages.

## Estimate Confidence Before Routing

The router doesn't decide based on the prompt alone.

It combines three scores:

- classifier probability for the predicted task class
- retrieval score when the request needs a document
- historical answer acceptance for that class and model

Each score has a purpose. The classifier probability tells us whether the request matches a known workflow. Retrieval score tells us whether the assistant found relevant evidence. Historical acceptance reflects whether users needed to rephrase or open a ticket after an answer.

For the small model path, `replykit` requires a combined confidence of at least 0.82. If confidence falls below that threshold, the request enters the larger-model queue. The threshold came from 400 validation requests, where the small model answered 94% of high-confidence cases correctly but only 61% of the remaining cases correctly.

Confidence measures fit between a request and a known path. That distinction matters most for account actions, where validation and permissions matter more than model confidence.

## Choose a Fallback That Preserves Context

The first fallback design passed only the user's latest message to the larger model. That produced answers that ignored earlier clarifications, so users had to repeat themselves.

We changed the handoff to include a compact context object. It contains the conversation summary, extracted fields, retrieval results and permission checks.

The large model receives this context:

```text
task_class: invoice_question
conversation_summary: customer changed plans and asks about proration
extracted_fields:
  invoice_id: inv_88213
  plan_changed_at: 2026-02-11
retrieval_ids: ["billing-cycle-04", "proration-02"]
permission_check: passed
```

This format keeps the large model from repeating retrieval work. It also makes every handoff auditable, because the object shows which permissions and documents entered the request.

When the large model still can't answer confidently, `replykit` escalates to a human. The escalation includes the same object, so the support engineer doesn't need to reconstruct the conversation.

## Track Cost and Quality Together

The router writes one event per request with the task class, chosen model, confidence, latency and result. We aggregate those events hourly. The important comparison includes model quality, cost and latency for the same class.

Our dashboard shows five measures:

- answer acceptance rate by class
- rate of escalation to a human
- median and 95th-percentile latency
- tokens and hosted-model cost
- percentage of requests answered locally

After the first month, local requests averaged 210 milliseconds, while larger-model requests averaged 2.4 seconds. The small model handled 52% of all requests. Monthly model spending fell from EUR 214 to EUR 138, even though the local server added about EUR 18 in electricity and depreciation.

The acceptance rate required a more honest look. Template questions stayed at 91%, but invoice questions fell from 87% to 83%, so we raised their confidence threshold to 0.89. That change pushed more requests to the larger model and brought acceptance back to 86%, at an extra EUR 7 per month.

## Handle Model Updates Carefully

A router tuned to one small model can break after an upgrade. We therefore treat the router as part of the evaluation surface.

Before replacing a model, we replay 600 saved requests. The replay uses recorded context and expected outcomes, but it calls the candidate model live. We compare acceptance, escalation, token use and latency by class.

The rollout has three stages:

- shadow mode for 5% of requests
- limited release for one task class
- full release after seven days of stable measurements

In March we tested a newer 7B local model. It matched the older model's acceptance rate, but its p95 latency rose from 520 milliseconds to 1.1 seconds on invoice questions. We kept the older model for that class and used the newer model only for template questions.

## Status After Eight Weeks

The final setup answers 58% of requests locally. Hosted-model costs remain at EUR 145 per month, and the support team accepts 87% of assistant answers across all classes. Human escalations take 11 minutes at the median, down from 17 minutes before the router stored handoff context.

The remaining problems are clear:

- the classifier needs more non-English messages
- invoice questions still depend heavily on retrieval quality
- confidence scores drift when customers invent new workflow names
- our cost model excludes support engineers' time

The next iteration will improve the non-English classifier and add per-customer opt-outs. I'll write about that after the opt-outs complete one billing cycle. If you want to follow along, don't forget to subscribe.
