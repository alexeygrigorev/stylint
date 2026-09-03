# Write an Onboarding Context File a New Agent Can Use

I wrote this guide as a synthetic style exercise. Although the repository and measurements are fictional, the method reflects how I prepare an unfamiliar codebase for agent work.

In January 2026, I gave a coding agent a small FastAPI repository with 14,200 lines of Python. The initial task looked narrow: add a filter to one reporting endpoint. After 40 minutes, the agent had changed the endpoint, invented a database migration, and edited two unrelated tests.

In this post, I'll share:

- how to map commands before granting edit access

- what belongs in an architecture map

- how to document risks and forbidden paths

- which review rules keep changes small

- how I measure whether the context file works

## 1. Map the commands first

In the first section, I explain how a developer runs, tests, and resets the project. Until that section exists, every agent session invents its own workflow.

Start with the commands you use after a fresh clone. Include package installation, database setup, and seed data. Also explain local server startup, test execution, and command order.

For the FastAPI repository, the file began with four commands:

```bash
uv sync
uv run alembic upgrade head
uv run python scripts/seed_demo_data.py
uv run pytest
```

The seed command mattered because my first agent saw an empty SQLite file and assumed the schema was incomplete. It generated a migration for a table that already existed in `alembic/versions/`.

I also record expected runtime and output. Tests take 48 seconds, print one deprecation warning, and write a temporary report to `/tmp/report-tests`. Without that note, an agent may try to fix harmless output.

## 2. Draw the architecture in the application's own words

An architecture map should describe the moving parts, their owners, and their boundaries. Keep it short enough that a new engineer can read it before the first cup of coffee.

The FastAPI file used five entries:

- `app/api/` contains HTTP handlers and request models

- `app/services/` contains business rules and no database sessions

- `app/repositories/` owns all SQL queries

- `app/workers/` runs asynchronous export jobs

- `alembic/versions/` stores ordered database migrations

Each entry names the responsibility and the boundary. The line "services contain business rules and no database sessions" prevented a later agent from putting a query in the middle of a pricing rule.

I add one data-flow paragraph for the main request. In this repository, a request entered `api/reports.py`, called `services/report_builder.py`, and read through `repositories/report_queries.py`. The service returned a serialized Pydantic model.

## 3. Document risks and paths

Every repository has areas where a small edit creates a large problem. The onboarding file should name them plainly, with reasons rather than vague warnings.

Our file listed high-risk areas alongside the reason for each rule. New migrations in `alembic/versions/` had to follow the existing naming scheme and include a tested downgrade. We guarded `services/billing.py` because it fed a monthly invoice process. We also flagged `scripts/delete_demo_data.py` because it could erase shared staging records.

I also wrote an explicit forbidden list:

- don't edit generated clients under `generated/`

- don't add dependencies without discussion

- don't run destructive database commands

- don't widen database grants or API scopes

The reasons matter as much as the rules. The build overwrites generated clients with `make generate-client`, while dependencies affect a deployment image. Destructive commands once cost the fictional team four hours of recovery.

## 4. Set review gates

A review gate is a required check before work is considered complete. It turns taste into a repeatable process, especially for an agent that can't infer team habits from hallway conversations.

The repository used three gates:

- all 214 tests pass

- database changes include an upgrade and downgrade path

- API changes update the OpenAPI examples

I added a change budget for ordinary tasks. A bug fix could touch 150 lines, while a feature could touch 400 lines across at most 12 files. If the agent exceeded the budget, it stopped and submitted a plan.

That rule caught the original endpoint problem early. The reporting change needed 90 lines, while the agent's first attempt had reached 260 lines across seven files. The extra edits were plausible, but they belonged in separate proposals.

## 5. Include task examples

Abstract instructions degrade under pressure. A new agent also needs examples of completed work in the repository's own vocabulary.

I include examples of accepted task descriptions in the context file. Each one states the outcome and the allowed paths. It also states the evidence and the stop condition. The best examples come from recent requests that a human reviewer accepted.

One good example read:

```text
Add `status` to the report filter.
Allowed paths: app/api/reports.py, tests/api/test_reports.py.
Evidence: three pytest cases for active, archived, and invalid input.
Stop when: tests pass and OpenAPI examples include status.
```

The example is deliberately narrow. It shows that a small feature still needs tests and OpenAPI updates. It also shows what doesn't need to change.

## 6. Measure the onboarding file

An onboarding file is useful only if it changes the outcome. After writing it, I run the same task three times in clean sessions and record the edits, failures, and review time.

For the reporting filter, the first unguided run produced 260 changed lines and needed 55 minutes of human correction. After the context file, three runs averaged 95 lines and needed 14 minutes of correction. The sample is small, but the difference matched what reviewers noticed.

I also count questions the agent asks. In the unguided run, it asked for the test command and database setup. With the file, it asked one question about invoice rounding. That remaining question exposed a real ambiguity, so I added one sentence about rounding to two decimal places.

The measurement needn't be elaborate. I record runs, changed files, review minutes, and rollback events in a comparison table. Those numbers reveal whether the context file helps.

## Lessons from the file

Most bad agent work comes from missing local context. The agent fills the gap with reasonable habits from other repositories, and reasonable habits are still a risk when they conflict with team rules.

A good onboarding file makes the ordinary path explicit. Commands, boundaries, risks, and examples let the agent spend effort on the requested change. Review gates then decide whether the result can merge.

I plan to write next about turning these files into reusable project templates. Subscribe if you want the follow-up.
