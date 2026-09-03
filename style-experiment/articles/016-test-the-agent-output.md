# Test the Output, Not the Prompt

I wrote this analysis as a synthetic style exercise. Although the project details are fictional, the argument reflects how I make agent-assisted code maintainable.

In February 2026, I inherited an internal reporting tool whose prompt was 8,900 tokens long. The prompt contained customer rules, date rules, output examples, and six paragraphs of warnings. The coding agent often produced plausible Python, and the tests passed even when the report was wrong.

In this post, I'll share:

- why prompt review failed us

- how I defined four behavior checks

- what the first evaluation run exposed

- how those checks changed the prompt and code

- the limits I still accept

## Prompt review found the wrong defects

For two weeks, we reviewed the prompt the way we reviewed a legal document. We debated whether "recent quarter" was clear, whether the agent should ask before inventing a fiscal calendar, and whether the warnings sounded strong enough.

Those debates found two real ambiguities, but no evidence about which ambiguities mattered. A prompt is an instruction whose effect depends on the model and available tools. It also depends on repository state and supplied examples.

I copied three prompts into a document and showed them to two engineers. They preferred different versions, and both preferences were defensible. Neither engineer could tell me what output would change.

That was the moment I stopped grading the prompt, because we needed to grade observable behavior.

Our checks examined three kinds of evidence:

- database writes

- edited files

- a generated report against a known case

## Define checks before examples

I started with four reports the finance team had already accepted. Each report had an input file, an expected total, a known timezone adjustment, and a named owner who could answer questions.

Those reports gave us four checks:

- totals match the accepted report to two decimal places

- date boundaries use Europe/Berlin rather than server time

- SQL reads only tables listed in the access manifest

- generated files go to `/tmp/reports`, never to the project root

The checks deliberately covered correctness, time handling, permissions, and side effects. Together they expressed what the tool must do and what it must avoid. They also gave us a way to reject a run even when the code looked clean.

Each check returns a stable JSON record. The record includes the case ID, expected value, observed value, and the evidence path. A run can produce beautiful code and still fail because the agent wrote to the wrong directory.

## The first run was humbling

We ran the agent on all four cases and asked it to update the quarterly report. The Python tests passed, and the agent said the work was complete. The behavior checks said otherwise.

The totals matched in three cases, but the date boundaries were wrong in all four. The agent had used UTC because the database driver returned timestamps without timezone information. One report differed by €14,286.

The access check exposed the third failure. The generated SQL included `marketing.contacts`, a table absent from the access manifest. The agent used it to enrich the report with campaign names. That addition was useful, and it violated the tool's permission boundary.

Finally, one run created `report_2026Q1_draft.csv` in the repository root. A code reviewer might have caught that file, but the behavior check caught it immediately and printed the path.

## Fix the system, then the wording

We fixed the timezone issue in the code, not only in the prompt. Every query now passes an explicit timezone argument, and a helper function converts database timestamps before aggregation. The prompt says "use Europe/Berlin", and the code enforces it before data reaches aggregation.

We made the permission fix structural. I added a read-only database role for the reporting job, and its grants cover only the tables in `access.yaml`. The job runs under that role, so the prompt can't grant it a new table.

The draft-file issue got a filesystem check and an explicit output directory. The agent may write only inside `/tmp/reports`. Before merge, a test compares files in that directory against the accepted artifact.

Only after those fixes did we revise the prompt. We removed 2,100 tokens of repeated warnings and added two short examples. Warnings became descriptions of enforced constraints.

## Keep the checks in CI

The four checks run on every pull request that touches the reporting code or prompt. The job takes 4 minutes and 20 seconds, mostly because it builds a small fixture database.

We added five more cases over the next month. One covers leap years, another covers a customer with no revenue, and three cover malformed input files. The evaluation set now contains 9 cases and lives beside the code.

When we changed models in April, the checks gave us a baseline. The new model passed all 9 cases on the first run, but it took 38% more tokens. That trade was acceptable for this tool, and we could see it instead of debating it.

The checks don't prove the agent will handle every future request. They prove that our known, expensive failures stay fixed.

## Lessons from the checks

Prompt review is useful after the behavior is defined because it explains requirements to a model. Before that, it's an argument about words with no evidence attached.

The prompt got shorter after we added enforcement, a result that surprised me at first. A constraint in code, permissions, or a test does more work than another warning.

I plan to write separately about the JSON result format for these checks. Subscribe if you want to see how the evaluation set grows as the tool changes.
