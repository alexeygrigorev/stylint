# Converting a Bug Report into a Test Case

I wrote this synthetic style exercise as a how-to guide. The tool, the report and the dates are fictional. On 3 March 2026 a user of InvoiceKit, my small invoicing side project, filed report #412. The title was "Invoices show the wrong date at month end", and the report held one screenshot with no reproduction steps.

Reports like that used to sit in my tracker for weeks. The screenshot made no sense to me, and fixing some vague date bug felt bigger than the report deserved. In this guide I show the conversion I now run on every report the day it arrives.

The conversion takes 30 to 60 minutes for most reports. It earns its keep the first time someone reintroduces an old bug.

In this post, I'll share:

- how I shrink a report to minimal input
- how I write the expected failure first
- how a fixed test becomes a regression test
- how I label and link everything
- which mistakes I made with my first conversions

## 1. Reproduce With Minimal Input

Start by cutting the report down to the smallest input that still shows the bug. The screenshot in #412 showed a due date of 28.02 instead of 01.03, so I built one invoice through my dev API. Everything unrelated to the date stayed out. The API path also beats clicking through the interface, because the interface changes and the input stays stable.

The minimal case fit in six lines:

```python
invoice = make_invoice(
    issued_on="2026-03-01",
    timezone="Europe/Berlin",
)
print(invoice.due_date_label())  # 28.02.2026, expected 01.03.2026
```

Six lines beat the original screenshot, because they name the two ingredients that matter. The date sits at a month boundary, and the user sits in a non-UTC timezone. Every later step builds on this input.

## 2. Write The Expected Failure

Turn the minimal input into a test that fails for the reported reason. I write the test before I touch any code, because a failing test proves I understood the bug. A test written after the fix only proves the fix passes its own check.

The test for #412 looks like this:

```python
def test_month_edge_stays_in_march():
    invoice = make_invoice(
        issued_on="2026-03-01",
        timezone="Europe/Berlin",
    )
    assert invoice.due_date_label() == "01.03.2026"
```

One command runs it against the current build:

```bash
uv run pytest tests/test_dates.py -k month_edge
```

The failure printed 28.02.2026 against the expected 01.03.2026, exactly what the reporter saw in the screenshot. That match matters, because a test that fails for a different reason describes a different bug. On my first attempt the test failed with a validation error, which meant the input was still too big.

## 3. Turn The Fix Into A Regression Test

The bug sat in a formatter that converted dates to UTC before printing. I removed the conversion, ran the test, and it passed in under a second. The tempting next move is to close the ticket, and that move throws away the value.

A regression test is the same expected-failure test, kept after the fix, with a name that states the expected behavior. It joins the normal suite and runs on every push through GitHub Actions. If someone reintroduces the conversion next quarter, the suite fails with a message about invoice dates. That message reads like a user complaint, which makes the failure easy to judge.

The rename matters more than it sounds. A test called `test_utc_conversion_removed` describes my edit, while `test_month_edge_stays_in_march` describes the promise the user cares about.

## 4. Label And Link Everything

The last step connects the test to the report, so the history needs no memory. Each regression test gets a comment with the report number. The tracker entry gets the label `regression` and a link to the test file.

One tracker entry from March shows the whole chain:

```text
#412 wrong dates at month end
status: closed
label: regression
test: tests/test_dates.py::test_month_edge_stays_in_march
```

The label also changed my release process. Any failing test marked `regression` now blocks a release until someone rereads the linked report. Since March, that rule has stopped one bad release and produced two useful postponements.

## 5. Mistakes From My First Conversions

My first conversion skipped the minimal-input step, and the test I wrote reproduced a different bug. I fixed that other bug, closed #412 as done, and the reporter reopened it two days later. The rule I took from it: a test that never failed the reported way proves nothing about the report.

A second mistake involved scope. I once converted a vague report into an end-to-end test with about 40 lines of setup, and the suite still pays for that run time. Keep conversions small, and leave broad coverage to planned work.

## 6. Running The Habit Since March

The tracker holds 14 reports with the `regression` label since March, and each one links to a test that failed first. The habit also changed how I read reports, because minimal input forces understanding before fixing. The conversion settled at about 40 minutes per report in April, down from a whole afternoon in February. Half of that time goes into the reply to the reporter, which the test link now makes easy.

It still fails on visual reports. Layout glitches need a screenshot-comparison setup to become tests, and I haven't built one yet. Those reports wait in the tracker with a `visual` label and a note about the missing tooling.

I'll write about the screenshot-comparison setup in a future post. If you want to follow along, don't forget to subscribe.
