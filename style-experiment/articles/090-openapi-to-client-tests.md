# Generating Client Tests from an API Contract

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. In March our API gained three endpoints, and the Python client broke silently for a week before anyone noticed.

The server spec listed the new fields. The client targeted an older schema, and no test covered the gap between them. A user reported the missing data, and the fix took 20 minutes against a week of quiet breakage.

In this post, I'll share:

- how I read request examples from the spec
- how I encode status rules as tests
- how I cover failure cases systematically
- how I keep generated tests readable
- what the generated suite catches monthly

## A Week Of Silent Breakage

The March endpoints served billing history with pagination. The server returned a `next_cursor` field, the old client ignored unknown fields by default, and users saw only the first page.

Nobody owned the client-server boundary explicitly. The server team merged the spec change on Monday without telling the client team. The client team read the changelog on Friday, and the gap sat open for four working days.

The rule I took from March is simple. I generate client tests from the spec on every change, and I treat a red generated test as a release blocker.

## 1. Read Request Examples From The Spec

The generator starts from the machine-readable spec file, not from docs text. Our spec lives at `api/openapi.yaml`, and it defines 23 endpoints with request and response schemas.

Each endpoint declares a request example at minimum, and I require examples in review. The spec linter rejects any endpoint that ships without one, using a ten-line Python rule that already caught three violations.

The extraction command lists the covered endpoints:

```bash
uv run python scripts/spec_examples.py --spec api/openapi.yaml --list
```

That script found 21 endpoints with examples and two without. I wrote the missing two examples with the server team in 30 minutes, since guessing examples defeats the purpose.

## 2. Encode Status Rules As Tests

Every endpoint maps status codes to meanings, and each mapping becomes one test. A 200 returns the schema, a 400 names the bad field, and a 404 repeats the missing identifier.

The billing history endpoint produced five status tests:

- 200 returns a page with items and a cursor
- 400 names the offending query parameter
- 401 returns no body beyond the error code
- 404 echoes the unknown customer identifier
- 429 includes a retry delay in seconds

I write those rules once in a table inside the generator config. The table holds 58 rows today, and each row names an endpoint, a status and the expected body fields. I review the table with the server team quarterly, and stale rows surface within one session.

## 3. Cover Failure Cases Systematically

Failure coverage comes from mutating valid requests along fixed axes. The generator varies auth headers, content types, required fields and value ranges, one axis at a time.

The mutation axes fit on four lines:

- missing or expired auth tokens
- wrong content type on the request body
- each required field dropped in turn
- boundary values for dates and amounts

That sweep produced 140 failure tests from 23 endpoints in April. Eleven of those tests failed against the live server, and eight failures traced to real server bugs.

The remaining three failures traced to spec mistakes. The spec promised a 400 where the server returned 422, and fixing the spec took one line each time.

## 4. Keep Generated Tests Readable

I distrust generated tests that read as dumps. Each test gets a human name, a short comment citing the spec section, and exactly one assertion block.

A generated test reads like this:

```python
def test_billing_history_empty_page(client):
    # spec 4.2: empty result still returns a cursor
    page = client.get_history(customer="c_001")
    assert page.items == []
```

I regenerate the suite on every spec change and diff the output. The diff shows which tests the spec change added or altered, and I review that diff like any other code. Regeneration takes 40 seconds, and the diff review takes about ten minutes per spec change.

## 5. Run The Suite In CI

The suite runs against a disposable server on every pull request. CI boots the API from the same commit, waits for health, and runs the 200 generated tests.

The CI job definition fits on five lines:

```yaml
- run: compose up -d api
- run: wait-for http://localhost:8000/health
- run: pytest tests/generated/ -q
- run: compose down
```

That job takes six minutes, dominated by the server boot. It has blocked four merges since April, and each block named a real mismatch.

## Four Blocks Since April

The generated suite now holds 204 tests across 23 endpoints. It runs in six minutes, it needs no maintenance beyond spec edits, and it caught four mismatches before release.

The mismatches split evenly between sides. Two were server regressions against a frozen spec, and two were spec edits that forgot the client implications.

The suite works because it tests the boundary both teams share. I spend about an hour monthly reviewing generator diffs, and neither team writes client tests by hand anymore.

I'll cover the mutation-axis design in detail in a future post. If you want to follow along, don't forget to subscribe.
