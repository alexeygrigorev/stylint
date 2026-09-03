# Testing the Seams in an AI-Assisted Application

I wrote this synthetic style exercise as a how-to guide. CourseMetrics, its users and all measurements are fictional.

CourseMetrics is a fictional homework service with a FastAPI backend and a React frontend. A coding agent wrote about 70% of the current code across 34 pull requests. The service accepts ZIP files, extracts student notebooks, runs five checks and returns a review.

The first two agent-generated releases looked correct in a demo. Then a valid submission failed because the upload service changed one response field. The tests passed, because they mocked the response used by the old code.

In this post, I'll share:

- how I decide which interfaces deserve tests
- how I write integration tests for model calls
- how I protect one complete user path
- how I keep generated fixtures honest
- what the final test suite looks like

## 1. Name The Stable Seams

Each seam marks where software components exchange a promise. In CourseMetrics, the important seams are upload-to-extraction, extraction-to-rules, rules-to-database and backend-to-frontend. The local helper functions between them are usually easier to review by reading.

List those boundaries before opening the coding agent. For each one, write the input type, the output type, the failure status and the retry behavior. A short interface file gives the agent a definition of done.

I keep this in `tests/contracts.md`:

```text
- /uploads accepts multipart/form-data and returns upload_id, file_hash, status
- extraction accepts upload_id and returns cells, images, notebook_version
- rules accept cells and return findings, score, elapsed_ms
```

The file is 19 lines long. It has prevented more arguments than any prompt I've written, because the agent can reference the agreement before it changes code.

## 2. Write Interface Tests First

Interface tests describe what one side must receive from another. They run against a real instance of the producer whenever that producer is cheap to start. In CourseMetrics, the extraction worker starts in under two seconds, so its tests use SQLite, a temporary directory and three checked-in notebooks.

For a new endpoint, I ask for the failing test first. The agent then adds only enough implementation to make that test pass. This keeps the review focused on behavior rather than on naming.

Each interface has three cases at minimum:

- a valid input with the smallest useful payload
- a malformed input that must return status 422
- an empty result that must still use the documented schema

The extraction interface has nine tests and runs in 1.4 seconds. Four are happy paths, three cover malformed files and two cover large files. That balance is small enough to run on every save.

## 3. Test Model Calls At Integration Boundaries

Unit tests can verify that the application sent a prompt and parsed a JSON object. They can't prove that the model response is useful. CourseMetrics separates those concerns, so parser failures are unit tests and answer quality is an integration test.

The grading assistant reads the notebook summary and writes two comments. Its integration test uses Ollama with Llama 3.2 3B Instruct. I chose a local model because the test doesn't need the production model's best answer. It needs a response that clears the parser and meets the rubric.

The test supplies one notebook with an obvious division-by-zero error. It fails when the response omits the error, uses an undocumented JSON field or writes more than 180 words. A real review can still be poor, but these checks catch failures that violate the documented API.

The full model check takes 9 seconds on my fictional laptop. It runs before every pull request, while a broader 32-case set runs nightly.

## 4. Protect One User Path

One complete path catches coordination mistakes that component tests miss.

The CourseMetrics path covers several stages:

- upload a submission
- extract the notebook
- run the checks
- save a review
- load that review in the browser

I use Playwright for that path. The test signs in as a fictional teacher, uploads a 240 KB notebook and waits for the review page. It checks three visible elements: filename, score and first comment. It doesn't try to review every screen.

The path runs against the FastAPI server, the extraction worker and a built frontend bundle. SQLite is the only service replaced. This costs about 35 seconds and has caught two CORS settings, one mismatched identifier and one frontend error that unit tests missed.

If the path fails, the browser screenshot, the server log and the request identifier appear in the CI artifact. Those three files usually make the cause obvious before I open a terminal.

## 5. Keep Fixtures Honest

I found that generated fixtures drift into idealized data. They may omit malformed Unicode, empty sections, old notebook versions and long file names. Those cases are exactly where the CourseMetrics agent made incorrect assumptions.

I built the main fixtures from 18 synthetic student notebooks. Six are clean, six contain common mistakes and six are deliberately awkward. The awkward set has a 4 MB image, cells in reverse order, a notebook with version 3 and one file named `final final (1).ipynb`.

Every fixture has a sidecar file with its expected structure. The expectations stay coarse: required keys, acceptable ranges, error classes and the number of findings. They don't encode every sentence the model should produce.

When a production-like case exposes a bug, I reduce it to the smallest fixture and add it to the folder. The folder now has 18 cases, and every one maps to a named issue.

## Closing Notes

The suite now contains 84 tests: 61 unit tests, 14 interface tests, 8 integration tests and one browser path. It runs in about 4 minutes. The agent can change implementation freely when the tests stay green.

The difficult work was choosing promises, not writing assertions. Once I named the four seams, reviewing generated code became much easier. Rubric quality is the remaining risk, and no test can decide it for me.

I'll write more about the 32-case model set in another synthetic article. Subscribe if you want to follow along.
