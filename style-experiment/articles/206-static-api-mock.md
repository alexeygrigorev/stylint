# Generating a Static Mock API from an OpenAPI File

This synthetic style exercise follows a fictional practitioner with invented numbers and events. Nothing here describes a real project. Last spring I agreed to build a small dashboard while the backend team still owed me three endpoints.

I had the OpenAPI file and a deadline in twelve days, and the file described fourteen routes with schemas, examples, and error codes. The running service didn't exist yet, so every frontend change waited on guesses.

I first hardcoded responses inside the React components. Each component returned a fixed object after a short timeout. That approach worked for two screens and then started to rot.

The fixtures lived in five different files with mismatched field names. One screen used `userName` while another used `username`. I fixed the same typo twice and still missed a third copy.

In this post, I'll share:

- why hardcoded fixtures stalled the frontend work
- how I turned the OpenAPI file into static mock routes
- how I covered error codes and response latency
- how the mock fit into daily frontend work
- what the setup costs and where it still falls short

## Hardcoded Fixtures Stall Fast

I liked hardcoded fixtures at first because the first screen rendered within an hour. I added three objects to a `fixtures.js` file and moved on. The second screen needed a list with pagination fields.

By day three the fixtures disagreed with the spec in four places. The spec said `created_at` held an RFC 3339 string. My fixture used a Unix integer because I typed it from memory.

I also faked errors with boolean flags inside nine components. A `fail=true` prop switched each fixture to an error object, and those flags drifted from the spec within days.

The rule I took from that week: fixtures must come from the spec file, and the spec file stays the only place I edit.

## Mock Routes From the Spec

The OpenAPI file already held everything the mock needed, and it named each path, method, and status code. I wrote Mockline, a small Python script for this task, to read that file and emit static JSON.

A route like `GET /users` becomes `mocks/get_users.json` with content taken from the first example in each schema. Missing fields get plain defaults from a lookup I keep in the script.

I run the generator with one command:

```bash
uv run python scripts/generate_mock.py
```

The command reads `openapi.yaml` and writes 14 JSON files in under a second. A missing example prints a warning line, so gaps show up right away.

I added a tiny FastAPI app with one file per route mounted under `/mock`. The app sets the content type to JSON and returns the file bytes unchanged.

The daily flow uses two commands in order:

- regenerate the JSON after any spec edit
- restart the mock server and reload the dashboard

That flow kept the mock honest because every fixture traced back to the spec. When the backend team renamed a field in May, I regenerated and saw the diff in git within a minute.

## Error Codes and Latency

Happy-path mocks hide the screens users see most, so empty states, permission errors, and timeouts need fixtures too. The spec listed five error codes across the fourteen routes, so I covered each one.

For every error code Mockline writes one extra file, so a `403` on `GET /reports` becomes `mocks/get_reports_403.json`. The content follows the error schema from the spec with a fixed message string.

Switching a route to its error file uses a query string:

```text
GET /mock/reports?mock=403
```

The mock server reads the `mock` value and returns the matching file. Without that value it returns the normal `200` file.

Latency needed the same treatment because instant responses lie. Real endpoints in this project answer in 120 to 400 milliseconds. A mock that answers in 4 milliseconds hides loading-state bugs.

I added a fixed 180 millisecond delay to every mock route. I verified the behavior with a short script that timed forty requests. The median sat at 184 milliseconds with no failures over forty requests.

## Daily Frontend Work With the Mock

The dashboard reads its API base URL from one environment variable. Pointing that variable at the mock took a single line in the `.env` file.

The mock server runs on port 8123 on my ThinkPad. Startup takes about two seconds and memory stays under 60 MB.

The repo layout for the mock stays small enough to read at a glance:

```text
mocks/get_users.json
mocks/get_users_403.json
mocks/post_reports.json
scripts/generate_mock.py
scripts/mock_server.py
```

Fourteen routes produced 19 JSON files totaling 41 KB, and the two scripts add another 210 lines of Python. Nobody on the team needed docs beyond the README section.

Two frontend developers used the mock for nine working days. They filed eleven bugs against loading states and empty screens that instant fixtures had hidden. That stability meant we quoted exact payloads in bug reports with line numbers from the JSON files.

## Lessons From the Mock Setup

The mock paid off the week the real backend arrived. Swapping the base URL took a minute and broke only two screens. Both breaks came from fields the backend team had renamed without updating the OpenAPI file.

That failure taught me the same lesson the fixtures taught me earlier. A mock is only as honest as the spec behind it, so the spec needs a freshness check. I now diff the spec date against the mock date in CI.

I generate fixtures from the spec instead of typing them by hand. I ship error files and a fixed delay with every mock route. I treat spec drift as a build failure instead of a surprise.

Six hours of building supported nine days of frontend work for two people. That trade looks fine to me, and I'd repeat it on the next project with a late backend.

I'll write more about spec testing against OpenAPI files in a future post. If you want to follow along, don't forget to subscribe.
