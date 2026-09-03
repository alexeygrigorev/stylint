# The API Contract Workflow That Keeps Generated APIs Usable

I wrote this synthetic style exercise as a how-to guide with fictional details, not real events. In January I let a coding agent build a FastAPI service from two sentences. The agent returned nine files with working routes and no usable error format.

The service ran and passed a smoke test on my laptop. It accepted new users and stored them in SQLite. It rejected bad input with a stack trace and exposed internal field names.

That failure pushed me to write the API contract first in OpenAPI. I now spend 30 minutes on the schema before the agent writes implementation code. The extra time replaced two-hour cleanup sessions after each generation.

In this post, I'll share:

- how I write the API contract before code
- how I generate server stubs from the schema
- how I add tests for each endpoint
- how I fill implementation behind the schema
- how I review drift before merging

## 1. Write the API Contract First

I start with one OpenAPI file and no implementation words beyond field names. The file names each route, its inputs and its responses with status codes. For a user service, I listed registration, login and profile fetch with explicit error shapes.

The first version took 28 minutes for three endpoints with shared error objects. I defined `UserCreate` with email, password and display name. I defined `ErrorResponse` with code, message and offending field for every 400 response.

The schema file lives at `api/openapi.yaml` and stays under 220 lines for small services. I keep descriptions short and focus only on required fields.

An early version missed pagination on the list route and caused a later rewrite. The rule I took from that miss: the API contract must show list limits before any code exists.

I review the schema by rendering docs locally before proceeding:

```bash
uv run python scripts/render_docs.py api/openapi.yaml
```

That command builds a preview in 6 seconds on my ThinkPad. I click each route, check examples and confirm error responses look consistent across endpoints.

## 2. Generate Server Stubs from the Schema

Stubs give the agent a fixed target instead of open choices. I generate FastAPI route shells from the OpenAPI file with types and status codes already set. The agent fills logic inside those shells without changing signatures.

Generation takes about 9 seconds for three endpoints with Pydantic models included. I run the generator after every schema edit so stubs never drift from the declared shapes. The output goes to `app/routes` with one file per resource.

The generator command is short and I run it from the repo root:

```bash
uv run python scripts/gen_stubs.py api/openapi.yaml app/routes
```

The command overwrites route signatures and leaves handler bodies marked for manual fill. It preserves my earlier logic when only descriptions change, so repeated runs stay safe.

Stub files include response models for success and error cases from the start. When the schema says 400 returns `ErrorResponse`, the stub already declares that return type. The agent doesn't invent a different error format later.

## 3. Add Tests for Each Endpoint

Tests lock the API contract in place before implementation starts. I write one test file per resource with cases for success, validation failure and missing auth. Each test calls the stub through FastAPI TestClient.

The first suite for three endpoints had 18 tests and ran in 4.2 seconds. Six tests covered happy paths with valid payloads and expected 200 or 201. Twelve tests covered bad email formats, short passwords and missing tokens with expected 400 or 401.

I keep test data small and explicit in `tests/test_users.py`. Each case builds its payload inline so failures show the exact input. No fixtures hide required fields or default values from the reader.

A typical validation test looks like this in plain Python:

```python
def test_create_user_rejects_bad_email(client):
    payload = {"email": "nope", "password": "secret123", "name": "Sam"}
    response = client.post("/users", json=payload)
    assert response.status_code == 400
    assert response.json()["code"] == "bad_email"
```

That test checks the status code and the error code from the API contract. When the agent changes validation messages, the test still passes if codes stay stable.

## 4. Fill Implementation Behind the Schema

Implementation happens only after stubs and tests exist in the repo. I give the coding agent the API contract, the stub files and the failing tests in one prompt. I forbid signature changes and new dependencies in that prompt.

The agent implemented three endpoints in 22 minutes across two passes in my trial. The first pass added SQLite queries and password hashing with bcrypt. The second pass fixed two error codes that didn't match the declared `ErrorResponse` format.

I review the diff with attention to queries and auth checks only. I check that every 400 response includes code, message and field name.

Common issues I catch at this stage fall into a short list I keep in review notes:

- missing 401 check on one route after copy-paste
- password hash compared with plain equality in one branch
- list endpoint ignoring the 50-item limit from the schema
- error message leaking an internal column name

Each fix takes five to ten minutes and gets its own test run. I don't let the agent refactor the schema to fit its implementation. The schema stays fixed while logic adapts to meet the declared shapes.

## 5. Review Drift Before Merging

Drift means the code accepts or returns something the API contract doesn't describe. I check for drift with a diff between the schema and the running app before every merge. The check runs generated requests against every declared route.

The drift script starts the app on port 8123 and sends 34 requests in 11 seconds. It compares status codes, required fields and error codes with the OpenAPI file. Mismatches print as one line per route with expected and actual values.

I run the drift check from the repo root after tests pass:

```text
drift check: 34 requests, 2 mismatches
POST /users 400 missing field in ErrorResponse
GET /users limit default differs from schema
```

That report tells me exactly which handler needs adjustment before merge. I fix the handler, rerun tests and run drift again until the report shows zero mismatches.

The workflow has one limit I accept openly. It fits services with three to ten endpoints and clear CRUD shapes.

This method taught me a simple lesson about generated code. A declared API contract turns review into comparison, and comparison takes minutes instead of hours.

I'll extend the same flow to a larger billing service next quarter. If you want to follow along, don't forget to subscribe.
