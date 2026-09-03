# Budgeting Web Research for an Agent

I spent $38.20 in two days before I learned to budget agent research. I wrote
this synthetic style exercise with a fictional project, dates, prices, and tool
versions. The coding agent was comparing eight JSON logging libraries for
LedgerLab, a fictional subscription billing service.

The first prompt said "research the best option", and it did what I asked. The
agent opened 43 web pages, downloaded two comparison articles that required
JavaScript, summarized benchmarks from 2023, and returned eight paragraphs. I
still had to read the paragraphs and decide whether any benchmark matched our
service.

In this post, I'll share:

- how I scope the research question,
- how I cap sources and time,
- how I define the stopping condition,
- what I keep in the research brief,
- when I run the work myself.

## 1. Scope the question

I now write the decision first. "Choose a JSON logging library for FastAPI,
Python 3.12, and 200 requests per second" is research. "Tell me about logging"
is browsing. The narrow version tells the agent what evidence matters and what
it can ignore.

Before launching the agent, I write three lines:

- the decision it supports,
- the constraints I won't change,
- the evidence that could change my mind.

For LedgerLab, the decision was whether to keep the standard `logging` library.
The constraints were Python 3.12, JSON output, and support for request IDs.
Evidence that could change the decision included a maintained library with
structured context and clear configuration.

Performance comparisons stayed out of scope. Our peak traffic was 80 requests
per second, so a benchmark at 10,000 requests per second wouldn't decide
anything. That sentence in the brief saved the agent from its most attractive
pages.

## 2. Set source limits

The first run had no source cap, while the second run allowed 12 sources and 20
requests. I chose 12 because eight candidate libraries usually need a project
page, documentation, and release notes. Twenty requests covered those plus
enough room for one known issue.

I put the limits directly in the task:

```text
Use at most 12 unique web sources and 20 requests.
Prefer project documentation, changelogs, and issue threads.
Stop after you have one recommendation and two alternatives.
```

The cap made quality visible. On one run, the agent used all 20 requests and
found that a library's documentation referenced a version that hadn't been
released. On another run, it stopped after 6 sources because the standard
library met every constraint.

## 3. Define the stopping condition

I needed to define what "done" means, so I used a recommendation format with
exact fields. A source cap prevents runaway browsing, but it doesn't guarantee
a useful answer. With exact fields, the agent can't stop at a summary.

The output format has these parts:

- recommendation and version,
- constraints satisfied,
- two alternatives,
- evidence links,
- reasons to reject each alternative,
- unresolved questions.

"Unresolved questions" is the important field. It lets the agent admit that
two libraries support request IDs differently, or that a changelog doesn't say
whether Python 3.13 works. Those admissions make review much easier than
confident paragraphs.

I also give each unresolved question an action. The action can be "read the
issue", "write a ten-line test", or "accept the uncertainty". Without that
field, the next session often repeats the same search.

## 4. Keep the brief

Every research run writes `research/brief.md` in the LedgerLab repository. The
file records the prompt, the date, and the limits. It also records the resulting
recommendation and the token count. This setup took 10 minutes and has already
prevented three repeated debates.

A short brief looks like this:

```text
Date: 2026-05-14
Question: choose a JSON logging library
Limit: 12 sources, 20 requests
Recommendation: structlog 24.4.0
Token count: 41,200 input, 2,900 output
Unresolved: confirm async handler behavior under 200 requests/second
```

The token count is deliberately visible, and it keeps the cost beside the
conclusion. In April, a prompt revision reduced median input tokens from 38,000
to 17,500. Most of that reduction came from removing older search pages without
changing the recommendation.

I keep briefs for six months. After that, they're useful only if the question
comes back, so I archive each brief with the release that used its decision.

## 5. Know when to do it yourself

I run the research myself in three cases. I read legal terms directly, and I
search manually for evidence behind a login. I also verify published claims
before using them in a course or article.

Agent research is best when the result is internal and reversible. Choosing a
logging library, picking a retry interval, or checking whether a tool supports
a file format all fit that description. The agent narrows the field, and I make
the final call.

For LedgerLab, I still wrote a test before switching libraries. It emitted 500
log records from an async request handler. The test took 15 minutes and
answered the question no web page could answer.

## Lessons from the budget

Research budgets work because they turn curiosity into a bounded task. The
question names the decision, the caps name the cost, and the output names the
remaining uncertainty.

The rule from the expensive week is simple. If I can't define what counts as
done, I'm not ready to send the agent to the web. I plan to try the same brief
format on documentation research next month. Subscribe if you want to see the
updated template.
