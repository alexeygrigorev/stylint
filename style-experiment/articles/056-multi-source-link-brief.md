# A Brief Format for Multi-Source Research

I wrote this how-to guide as a synthetic style exercise, and I invented every source name, measurement, and decision. I use the template when a technical question crosses libraries, vendor documentation, and my own project constraints.

The format came from a failed afternoon. I read 14 browser tabs about streaming responses and copied promising fragments into a document. I still couldn't decide whether to use server-sent events or chunked JSON.

In this post, I'll share:

- how to write the research question first
- how to record evidence with a decision test
- how to handle contradictions
- how to turn the brief into a decision
- a filled example from an invented project

## Write the Question First

Start with one decision rather than a topic. "Streaming" is a topic, while a decision asks whether the FastAPI chat endpoint should use server-sent events or chunked JSON for the first release.

Then write the constraints before you read. I usually record runtime, operating cost, and the client environment.

Finally, state the deadline and the cost of waiting. If a choice can be reversed later, say so, and record any external-interface impact as well.

## Record Evidence

Each source gets one row in a table or one block in Markdown. I record the source name and publication date, then the claim and evidence given.

The evidence field enforces discipline. Write what the source actually provides, whether that's a benchmark or an opinion.

"It says this is fast" isn't evidence. "The post reports 1,200 requests per second on four cores, with hardware listed" is.

Then add a relevance test. This is one sentence explaining how the claim would change your choice. A benchmark on four cores may not matter if your endpoint waits on a model for two seconds per response.

```text
source: FastAPI response documentation
date: 2026-03-18
claim: StreamingResponse can yield JSON lines incrementally.
evidence: code example and response headers
relevance test: supports chunked JSON without changing the client parser
```

I keep quotations short and link each source. If the source is private, record where the claim came from and who can verify it. The brief should work three months later, after everyone has forgotten the conversation.

## Handle Contradictions

Contradictions are useful, so don't smooth them over. Put conflicting claims near each other and name the discrepancy. One benchmark may measure time to first byte, while another measures total completion time on a slow network.

For each contradiction, classify the source mismatch:

- different metric
- different workload
- different version
- missing reproducibility details
- incompatible assumptions

Some contradictions resolve without more research. A library comparison from 2021 may not apply to version 4.2. Other contradictions become an experiment. If two sources disagree about memory use under 10,000 concurrent clients, run a small load test.

I write the resolution under both claims. If the evidence remains incomplete, write what test would settle it and how long the test should take. That turns disagreement into a task with a stopping condition.

## Decide and Record the Choice

End the brief with a decision section, even when the decision is to wait. I record the decision and reason first, then rejected options and the first review date.

The rejected options matter more than they first appear. They prevent a later reader from relitigating the choice without new evidence. They also record the conditions under which the losing choice would win.

I use this section:

```text
decision: ship chunked JSON
reason: no client parser change; model latency dominates transport
rejected: server-sent events, WebSockets
risks: no automatic reconnection; needs explicit retry logic
review: after the first 1,000 chat sessions or 2026-11-01
```

Then write one paragraph describing what would make you change the decision. This is the brief's memory. If the mobile client later requires background reconnects, the brief should show exactly which assumption broke.

## Filled Example

In the invented project, the team had three sources and one experiment. The FastAPI documentation showed both transport options were feasible. A vendor guide claimed server-sent events reduced client code, and an internal spike measured time to first byte.

The internal spike used 200 simulated chat sessions. It measured a median time to first byte of 310 milliseconds for chunked JSON, while server-sent events averaged 295 milliseconds.

The decisive evidence was client code. The existing React parser already consumed JSON lines, while server-sent events would add an event parser and a fallback for older internal browsers. That requirement came from a support request, and it outweighed 15 milliseconds.

The brief took 75 minutes to complete. Thirty minutes went to reading, 20 to the internal spike, and 25 to writing. Without it, we would probably have chosen server-sent events because two sources mentioned it more often.

## Practical Rules

Keep the brief under two pages. If it grows past that, split research from decision or narrow the question. A brief that becomes a literature review won't get read before the deadline.

Set a time budget before you begin. For reversible choices, 60 to 90 minutes is often enough. For external interfaces, give yourself time for one experiment, but write the stopping condition before you run it.

Use the same template across projects. The fields may feel repetitive, but repetition makes comparison possible. When you review three briefs from the last quarter, you can see which constraints actually changed outcomes.

The core rule is simple: write the decision before the sources. Then every link either changes the choice, strengthens an assumption, or gets left out.
