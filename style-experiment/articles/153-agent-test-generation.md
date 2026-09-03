# Using an Agent to Generate Tests from a Specification

Last month I asked Claude Code to add tests for a fictional invoice service. The service had a 180-line specification, 14 endpoints and almost no tests. I wanted to know whether an agent could turn that specification into useful checks without inventing behavior.

This synthetic style exercise reports on that experiment. The invoice service, dates and metrics are fictional, and I reviewed every generated test before it entered the repository.

In this post, I'll share:

- how I prepared the specification
- how I asked for the golden path first
- how we added boundary cases
- what the review caught
- how I would run the next experiment

## Prepare The Specification

I stored the original document in `docs/invoice-api.md`. It mixed requirements with implementation notes, old decisions and one retired retry rule. That mixture made it hard for either a person or an agent to tell current behavior from history.

I first asked Claude to write tests directly from that file. It produced 22 tests in a few minutes. Eleven were plausible, but three asserted behavior that only appeared in a deprecated paragraph, and one expected a 409 response for a validation error. The specification was the problem, so I stopped and rewrote it.

The cleaned specification had four sections:

- endpoint, method and path
- request fields and validation limits
- response status and body
- failure conditions and identifiers

Each section described current behavior only. I removed deployment notes and moved the old retry rule into a separate decision record. I also wrote a short paragraph saying that the API returns validation errors with status 422.

## Generate The Golden Path

I started with the golden path, meaning the simplest successful request for an endpoint. I wanted that behavior locked down before we discussed edge cases.

I used this prompt:

```text
Read docs/invoice-api.md. For endpoint POST /invoices, write pytest tests
for the successful path only. Use the fixtures in tests/conftest.py.
Do not invent fields, headers or status codes. If the specification is
ambiguous, add a TODO comment instead of guessing.
```

Claude generated seven tests, and six passed immediately. The seventh used a customer ID from another test instead of the fixture, so it failed in isolation but passed in the original file order.

I liked the result enough to continue, but I didn't merge those tests yet. Passing tests can encode a bug. I compared each assertion with the specification and found one useful omission: the agent checked the invoice status but didn't assert that `created_at` used UTC.

## Add Boundary Cases

After the golden path passed review, I expanded the task to limits and failure conditions. The invoice endpoint accepts an amount between 0.01 and 999,999.99, requires a customer ID and rejects duplicate idempotency keys.

I asked for a table of cases first:

```text
Using the same specification, list boundary and failure cases for
POST /invoices. Include the input, expected status and reason. Do not
write test code yet.
```

The list contained 17 cases. Nine covered validation limits, five covered required fields and three covered duplicate requests. I deleted a case about a database timeout because the specification didn't define that behavior, and I combined two nearly identical missing-field cases.

The revised list had 14 cases. I then asked the agent to turn them into tests in batches of five. Smaller batches made every diff easy to read and kept failing cases connected to their source line in the specification.

That produced 14 tests, and nine passed without changes. The other five exposed either fixture gaps or genuine ambiguities, which was the outcome I wanted.

## Review The Generated Tests

For every test, I had to answer one question: each assertion had to come from the specification.

I read each generated diff, then marked every line with its specification source.

Four problems appeared repeatedly:

- tests asserted implementation details, such as internal error text
- tests reused objects created by another test
- tests named a case after its input, but not its expected outcome
- TODO comments disappeared when Claude rewrote a test

The first issue was the most dangerous. The specification said the response body includes a user-facing message, but it didn't fix the exact wording. I kept one test that checked for a stable identifier in the error body and removed assertions about full sentences.

I also added a rule to the repository's agent instructions: generated tests must be independent and must clean up database rows. That rule came directly from the review failures, so it's easy for future contributors to understand.

## Measure The Result

The experiment took one working day. Writing the specification by hand took 3.5 hours, and generating, reviewing and fixing tests took another 3.5 hours. That total included two conversations with the agent about ambiguous cases.

The final repository had 21 tests for the invoice endpoint: seven golden-path tests and 14 boundary tests. Two of the golden-path tests were rewritten by me, and nine of the boundary tests needed edits. I kept the other ten essentially as generated.

Those numbers need context because the endpoint is small and the specification was fresh. I worked on a favorable task. A legacy endpoint with implicit behavior would need much more human work, and the agent would have more chances to invent requirements.

Coverage improved from 4% to 71% for that module, but coverage is a side effect. I value the named source more because every test now references a line in the specification. I can find affected tests quickly when the document changes.

## Next Experiment

The next experiment will start with a specification checklist rather than a cleaned file. Before generation, I'll check that every response field has a type, every limit has a value and every failure has a status.

I'll also keep the case table as a separate artifact. Reviewing 17 plain cases took about ten minutes and prevented several bad tests. That step was cheaper than reviewing code that shouldn't exist.

Finally, I won't ask for a whole module in one prompt. Working endpoint by endpoint was slower on paper, but every diff stayed reviewable, and I never had to reverse engineer the agent's intent.

I'll write about the specification checklist in a future post. If you want to follow along, don't forget to subscribe.
