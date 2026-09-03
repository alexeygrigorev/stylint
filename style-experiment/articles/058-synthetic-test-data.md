# Rules for Synthetic Test Data in Agent Evaluations

I wrote this analysis as a synthetic style exercise, and the datasets, metrics, and project outcomes are fictional. It covers three invented projects that used synthetic data to evaluate assistants answering questions about customer invoices and shipping records.

Synthetic data earned its place in those projects. It let me test boundaries before I had production access and reproduce a crash from a rare date.

In this post, I'll share:

- when synthetic cases are most useful
- how to design a coverage matrix
- where realism matters more than volume
- how I compare synthetic and real samples
- the rules I now apply before trusting a score

## Useful Cases

Synthetic cases work best when you know the rule and want to test whether the system applies it. A fabricated invoice with a 19% tax rate, a 0% tax rate, and a negative credit line can cover three branches in one small fixture.

They also work for rare boundaries. In one project, no real invoice arrived from a leap-day billing period, but the assistant still had to answer questions about one. I created 11 such dates and verified that date arithmetic stayed correct.

A third use is failure reproduction. When a generated SQL query timed out on 90,000 rows, I reduced the fixture to 1,200 rows while preserving its join order.

The least useful use is proving demand. Synthetic questions can show whether the system can answer a question type. They can't show that customers actually ask it, so they shouldn't decide the product roadmap by themselves.

## Coverage Matrix

I now start with a matrix rather than a list of examples. One axis contains lookup, comparison, aggregation, and refusal questions.

That gives 25 cells before any cleverness. I aim for at least two cases in each cell, though some cells need more. Permission restrictions and aggregations get four because a permission leak is more expensive than a wrong count.

The matrix also exposes gaps. In the first invoice project, 38 of 56 cases tested lookup questions. Only 4 tested a refusal, so the assistant confidently answered questions about invoices belonging to another subsidiary. Synthetic data found the gap because I had drawn it deliberately.

I keep the matrix in `evals/coverage.md`, next to each generated case. Every case has an ID, input, expected answer, and source rule.

```text
case: inv-agg-014
input: total tax for customer 8841 in 2026-Q2
expected: 431.20 EUR across 7 invoices
rule: tax is per line and rounded per invoice
pass: exact amount and invoice count
```

## Realism

Random volume can't replace realism. Generating 10,000 random invoices may exercise code paths, but random names and dates can create a distribution that no customer produces.

Realistic synthetic data starts from business rules. A legitimate invoice has a customer and line items, with currency and tax treatment.

Some combinations are invalid because a cancelled invoice shouldn't have a paid-at timestamp. A credit invoice should also point at the original invoice.

I encode those constraints before generation. For the shipping project, I used a small schema with 18 fields and 23 validation rules. The generator produced 3,400 records, and the validator rejected 412 on the first run. Those rejections were more useful than the accepted records.

Free text needs separate care. Fake customer questions sound artificial when every request contains perfect grammar and exact product names. I wrote 40 real-shaped questions by hand, then added 60 variants with abbreviations, vague dates, and two languages.

## Compare With Real Samples

Synthetic results need a calibration set. In each project, I reserved a sample of real interactions, even if it was small.

I report synthetic and real scores separately. The invoice assistant answered 94% of synthetic lookup cases correctly but only 78% of comparable real questions. The difference came from vague dates and customer-entered text that the generator had never produced.

The comparison also revealed a case where synthetic data looked worse. On aggregation questions, the real sample scored 69% while synthetic scored 71%. The real sample had only 16 cases, so the two-point difference was well within sampling noise. I labeled it inconclusive instead of inventing an explanation.

My current rule is to treat synthetic data as a development tool and real data as the acceptance test. A large synthetic gain can justify development time. Only the real sample can justify a claim about production readiness.

## Trust Rules

Before I trust a score, I run four checks. First, every synthetic case must trace to a written rule or a real incident. Second, the coverage matrix must show the mix of question types and data conditions.

Third, I sample failures, not just successes. After one run, I reviewed 30 wrong answers and found 19 came from one ambiguous date format. That single fix raised the overall score by 6 percentage points.

Fourth, I record the generator version with the results. When we changed the shipping generator from version 3 to version 4, scores moved from 86% to 91%. The data had changed as much as the model, so comparing those numbers directly would have misled us.

## Lessons

Synthetic data is best at making assumptions explicit. It creates controlled conditions, exposes missing branches, and gives failing cases a stable record.

It proves less than it appears to prove. A score on generated records describes those records and the generator behind them. Production claims still need a real sample, a caveat about its size, and a review of errors.

I plan to write separately about the schema validator and the case ID format. Subscribe if you want the next part of this evaluation workflow.
