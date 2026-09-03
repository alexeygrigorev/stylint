# Documenting API Timeouts and Quota Limits Before They Happen

Last quarter I inherited a Python service with 23 endpoints, no failure documentation, and three on-call engineers. Every outage taught us something, but we kept learning the same lesson at 2 a.m.

I wrote this article as a synthetic style exercise. I invented the service, the quota numbers, the error catalog, and the payment provider so I could show a repeatable documentation method.

In this post, I'll share:

- how to inventory timeouts, quotas, and validation errors
- why timeout and quota behavior need explicit examples
- how to describe recovery without promising too much
- how to test the documentation against real endpoints
- how to keep the document useful after release

## Start With an Incident Inventory

I started with a reference page that listed success responses. It covered eight endpoints and showed JSON examples. It said almost nothing about the states that actually woke us up.

The problem wasn't the formatting. The problem was selection: the guide described the happy path and left the operational behavior to memory.

I changed the input and collected 18 incidents from our issue tracker. I grouped them by cause, and most were boring and repeatable.

The groups looked like this:

- four timeouts between the service and the payment provider
- six malformed requests rejected by our validation layer
- three quota limits on the provider account
- two stale database connections after a deploy
- three ambiguous responses that returned the correct HTTP status

That list became the outline. It also showed that the reference guide should begin with the eight endpoints involved in those incidents.

## Define One Failure at a Time

For each mode, I wrote four fields on a page. The fields were trigger, response, user action, and engineering action. Keeping them separate stopped me from turning a guess into a procedure.

A timeout entry looked like this in the working file:

```text
Trigger: no provider response within 2 seconds
Response: HTTP 504 and request ID
User action: retry once after 10 seconds
Engineering action: inspect provider metrics and request ID
```

The trigger line forced a measurable number into the document. Before this pass, three engineers described the same timeout as "sometimes slow", and their assumptions about the threshold differed by several seconds.

Quota failures needed the same precision. The provider returned HTTP 429, a short retry window, and an account usage URL. We recorded all three and wrote down the rule against retrying immediately, because that made the waiting period longer.

Some modes had no automatic recovery, and the documentation said so directly. A reader needs to know when a retry is reasonable and when it will only repeat the failure.

## Describe the Recovery Path

The first recovery instructions were written for engineers, but support staff read them during the first customer escalations. I revised the document for that audience.

Each recovery section now tells the caller what they see, what they should try, and when they should contact us. The wording stays plain and avoids internal nicknames.

I wrote the shared request ID section in three short lines for support staff:

```text
Every failed response includes a request ID.
Include that ID in your support message.
We use it to find the log line and provider call.
```

The provider call is often the slow part. With the ID, an engineer can go directly to the relevant line instead of searching by email address and approximate time.

For customer-visible errors, we added an example message beside the technical response.

The message says what data was accepted, what failed, and what to change. Its wording doesn't promise that a retry will succeed.

## Test the Documentation

A failure guide is a set of claims, so I treated it like code under test. I wrote a small pytest suite (a Python test framework) that exercised the six documented failure classes against a mock provider.

The test commands mirrored the document entries:

```bash
uv run pytest tests/failures/test_timeout.py
uv run pytest tests/failures/test_quota.py
uv run pytest tests/failures/test_validation.py
```

Our tests caught two mismatches immediately. The documentation said the service returned HTTP 504 after 2 seconds, while the staging service waited 5 seconds. We also found one validation path that omitted a response field the guide described as always present.

We fixed the code and the document together. The timeout became 2 seconds, and the optional response field moved into a separate row. Neither change was difficult, and the value came from comparing the written claim with the actual behavior.

After that pass, a new engineer reviewed the document using only the endpoint and a test script. She identified one unclear instruction and one missing link. Both edits took less than an hour.

## Keep It Current

We keep the document in the repository beside the endpoint definitions. Each timeout, quota, and validation entry includes a source link to its incident or test, so a future editor can see why it exists.

We review the guide when an endpoint changes and during a quarterly on-call audit. The reviewer runs the error tests, confirms the recovery action, and removes entries that no longer apply.

The latest version covers 21 modes. Four entries were removed after we retired an old provider client, and seven were added when we split payments into two services.

The remaining gap is documentation for the mobile client. Its retry behavior differs, and the current guide mentions that only in a footnote.

## Lessons From the Catalog

A useful error guide is narrow, testable, and written while people still remember the incident. It doesn't need to explain every possible error. It needs to explain the errors that repeat.

The rule I took from the project: document failure behavior with the same care as the success response.

I plan to publish the four-field template in a future article. Subscribe to stay updated.
