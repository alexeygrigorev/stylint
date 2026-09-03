# Using an Agent to Upgrade Dependencies in Small Steps

This synthetic style exercise follows a fictional dependency upgrade I ran in April. My course demo app had 23 direct dependencies and 41 transitive ones. Three packages lagged more than a year behind current releases.

I maintain the app for workshops and I deploy it from a small VPS. I've postponed upgrades twice because I feared breaking the demo the night before class. The repo lives in GitHub and the test suite holds 118 tests.

I built DepBump, a Python helper that groups outdated packages and proposes upgrade batches. It reads the lockfile, checks release notes, and writes a short upgrade plan. The helper grew from a shell script I used in February.

In this post, I'll share:

- why bulk upgrades break workshop demos
- how the upgrade plan groups packages by risk
- what the agent changes in each small batch
- how test failures guide rollback choices
- where small-step upgrades still cost time

## Dependency Drift In A Small Project

The app started in 2023 with FastAPI, SQLAlchemy, and a handful of utilities. I updated packages when something broke and I ignored the rest for months. By April the gap felt risky because two security advisories mentioned old versions I still used.

I ran a full upgrade once in March on a Friday evening. The command updated 17 packages in one batch and the test suite failed with nine errors. I spent three hours untangling which package caused which failure and I reverted the whole branch at midnight.

The rule I took from that evening was simple. Upgrades run in small batches with a green test suite between batches.

I chose batch size of three to five packages because I can review that diff in about 20 minutes. Larger batches hide the cause of a failure and smaller batches waste time on repeated setup. That size keeps the review focused without slowing the week to a crawl.

My lockfile records exact versions for every install, and the CI workflow reinstalls from that file on each run. That setup gives me a working version I can return to - a known state with passing tests.

## Upgrade Plan And Safety Nets

The plan starts with a snapshot I can restore in minutes. I create a branch named `upgrade-april-batch` and I tag the last green commit with a date. That tag lets me compare behavior before and after each batch.

DepBump reads the outdated list and it sorts packages into three risk groups. Low-risk groups hold linters, formatters, and test helpers. Medium-risk groups hold web utilities and database drivers. High-risk groups hold FastAPI, SQLAlchemy, and Pydantic.

The grouping output looks like this:

```text
low: ruff, black, pytest, httpx
medium: alembic, asyncpg, redis
high: fastapi, sqlalchemy, pydantic
```

I review the groups and I move any package I don't trust into a higher group. That manual move takes five minutes and it prevents surprises from packages with a history of breaking changes.

The safety net includes a ten-minute smoke script I run after each batch. The script starts the server, creates a user, enrolls that user in a course, and deletes the test data. I wrote the script in March after a green test suite still shipped a broken signup flow.

## Running The Upgrades In Small Batches

Low-risk batches went first and they finished in one evening. The agent updated `ruff`, `black`, `pytest`, and `httpx` across four commits. Each commit changed the lockfile, the release notes reference, and nothing else.

I ask the coding agent with a narrow prompt for each batch:

```text
Upgrade ruff from 0.3.1 to 0.4.2. Update lockfile only. Run pytest -q. Report failures with file paths.
```

The agent edits the version pin, runs the test suite, and reports the result with file paths. I review the diff and I merge when the suite shows 118 passing tests. That loop takes about 12 minutes per low-risk batch.

Medium-risk batches needed more care. The `asyncpg` upgrade from 0.28 to 0.29 changed connection timeout defaults and two tests failed with timeout errors.

That boundary keeps judgment with me - the agent proposes edits and I approve behavior changes.

High-risk batches ran one package at a time. FastAPI moved from 0.109 to 0.115 and Pydantic moved from 2.5 to 2.7 in separate branches. Each upgrade took about 40 minutes including review, tests, and the smoke script.

## Test Failures And Rollback Decisions

Three failures taught me the most during the April run. The SQLAlchemy 2.0 upgrade broke five queries that used old session patterns. The agent suggested rewrites for all five and two suggestions missed a commit boundary.

I reverted those two files and I rewrote the queries by hand in about 30 minutes. The manual fix kept the transaction scope explicit and the tests passed on the next run. I don't trust generated rewrites for transaction code without reading every line.

The Redis client upgrade changed return types for missing keys from empty bytes to a null value. Four tests failed and the agent updated the assertions correctly in three files. I accepted those three and I fixed the fourth by hand because it covered a workshop example.

My rollback rule stays simple. I revert the batch when more than three tests fail or when the smoke script fails twice. That threshold triggered once in April and the revert took four minutes with the dated tag.

I record every decision in a short log next to the lockfile. Each entry holds the package, old version, and new version. It also records the test result and one line of reasoning. The April log holds 19 entries and it now guides the next upgrade round.

## Reflection And Next Steps

The small-step run finished in six evenings with 19 batches and zero workshop incidents. Total review time reached about nine hours and test runs added another three hours. The March bulk attempt had burned three hours and produced nothing usable.

I still spend too long reading release notes for low-risk packages. The notes rarely affect my code and I review them from habit. A shorter check for low-risk groups would save about an hour per round.

I plan a scheduled dry run that lists outdated packages every Monday with age and risk group. I'll store that report as JSON and review it with coffee before class. That habit should keep drift under three months.

I'll write about that Monday report format in a future post. If you want to follow along, don't forget to subscribe.
