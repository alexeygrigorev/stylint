# Turning a Browser Recording into a Reproducible Bug Report

I built this workflow as a synthetic style exercise around a fictional support queue. In February 2026, a tester sent me a 3 minute 40 second browser recording of a broken checkout page. The attached Brightshop ticket said only "coupon no work".

The video showed the symptom, but the ticket omitted important state.

In this post, I'll share:

- why screen recordings failed as bug reports
- how I structure a reproducible report
- how I capture browser state and console output
- how I reduce a recording to the shortest failing path
- what the review template looks like now

## Recordings Alone Failed

The first attempt was easy: ask every tester for a screen recording. Over five weeks we collected 38 recordings and fixed 9 of the reported problems.

The remaining reports sat in review. A recording showed the symptom, but it skipped the network requests, hidden form state, and feature flags that caused it. In the coupon case, the tester had applied a 15% discount after selecting a gift card, and the recording never showed the order summary.

I watched that video three times and still guessed the wrong cause. My mistake was treating the recording as complete evidence instead of treating it as one observation.

The rule I took from it: a bug report should let a new engineer reproduce the failure without interviewing the reporter.

## Report Structure

Brightshop now uses a short report form. It opens with a one-sentence title, then separates observed behavior from expected behavior.

The next fields contain these values, and the reporter adds numbered reproduction steps after them:

- exact URL
- account type
- browser version
- operating system
- timestamp in UTC

For the coupon ticket, the useful title was this:

```text
Checkout shows 10% gift-card discount after a 15% coupon is applied
```

That sentence names both discounts and points at the order summary. The body then stated the actual total of €87.30 and the expected total of €84.15.

Each report also has an evidence section. It accepts links to the recording, exported HAR file, console log, and screenshot. The recording remains useful as final confirmation, while the structured fields hold the reproducible facts.

## State and Console

The reproducible bundle starts from browser state. I ask for the URL with query parameters, selected shipping country, and local storage keys that affect pricing.

The tester doesn't need to know the internals.

A small bookmarklet copies the diagnostic fields and prints them in a `text` block:

```text
cart_id: c-88412
country: DE
coupon: SPRING15
gift_card: gc-307
experiment: checkout-summary-v3
```

The bookmarklet redacts names, addresses, and tokens before creating that block. It also includes the browser user agent and the page's build ID.

Console output goes into a separate file. We ask for all warnings and errors from page load through the failing click, with timestamps enabled. In the coupon case, line 221 in `pricing.js` warned that a percentage discount had replaced the gift-card adjustment instead of stacking with it.

That warning reduced my first investigation from an afternoon to about 20 minutes. It also gave us a stable search phrase for later regressions.

## Shortest Failing Path

After capture, I reduce the report to the smallest sequence that still fails. This often reveals that a long recording contains two unrelated issues.

For the coupon ticket, I removed steps until only four remained:

```text
1. Add one camera bag at EUR 99.00.
2. Apply coupon SPRING15.
3. Apply gift card gc-307.
4. Open the order summary.
```

The original 14 steps included a failed address lookup, a language switch, and an abandoned payment method. Those details mattered to the tester, but removing them made the pricing defect obvious.

Removing steps also exposed the boundary. A coupon alone worked, a gift card alone worked, and both together failed in the exact order above. Reversing the order worked, so the fix had to cover both paths.

I record that reduction as a "minimal case" comment. When the ticket closes, it becomes the first assertion in a Playwright test named `coupon-plus-gift-card.spec.ts`.

## Review Template

The current review has three checks:

- a new engineer must reproduce the bug from the written fields without watching the video
- every nonpublic value must be redacted or replaced by a fixture
- the report must state how we'll prove the fix

For pricing defects, proving the fix means checking the expected total, the currency, and a test that runs both discount paths.

The reporter fills the form in about five minutes. The triage engineer adds the minimal case, severity, and affected release. We keep the original recording linked so the customer-facing symptom stays visible.

Since March 2026, Brightshop has received 31 reports with this format. Twenty-six reproduced on the first attempt, three needed one clarification, and two involved environment-specific cache settings.

The improvement is real, though modest. Two reports still required a call because a partner integration changed its webhook payload between capture and review.

## Lessons

A recording preserves human context, and structured evidence preserves reproducibility. The combination works because each one answers a different question.

The coupon report became a template for later work. Capture state, preserve output, remove unrelated steps, and convert the minimal case into a test. The test now protects a real support case rather than an invented scenario.

I plan to write more about the HAR review and the redaction bookmarklet. Subscribe if you want to follow that debugging series.
