# Writing a Validator for My Local Project Configurations

I wrote this synthetic style exercise after inventing 61 configuration files across 14 local projects. The fictional projects included Harborbook, a fleet-maintenance dashboard, a billing demo, and several throw-away tools. In the invented March 2026 work, I spent most of a Saturday fixing their configuration files and built a small validator the following week.

In this post, I'll share:

- why a YAML linter didn't catch my real failures
- the schema I started with
- how I improved the error messages
- where defaults belong
- how the check runs in CI
- what changed after I validated the projects

## The First Checker Was Too Broad

My first script looked for the keys I remembered and checked that every project had the required top-level sections. It accepted anything inside those sections, so a misspelled `ttl_seconds` key passed.

That omission mattered in one Harborbook report. The application read the misspelled cache value as missing and fell back to a 24-hour timeout. The service still ran, and the stale reports were easy to miss during a demo.

I also kept three conventions in my head:

- Staging services pointed at local development databases.
- Production URLs came from environment variables.
- Every cache had an explicit timeout.

The first checker encoded none of that context.

The rule I took from the stale demo was simple: a config check should test the decisions that make a project runnable, beyond syntax.

## Start With a Small Schema

I started with one service and wrote a schema for the fields Harborbook actually reads. JSON Schema was already familiar, so I used Pydantic to consume the schema and validate each file in Python.

The first Harborbook profile covered these fields:

- service name and environment
- database URL reference
- cache timeout in seconds
- allowed log level

A minimal Harborbook entry looked like this:

```yaml
service: harborbook
environment: staging
database:
  url: ${HARBORBOOK_DB_URL}
cache:
  ttl_seconds: 120
log_level: info
```

I resisted the urge to model every possible option. The schema covered the current application and one preview service. That let me find real mistakes before I invented rules for configurations nobody used.

Each project gets a `config-profile` field. The value selects a schema, so Harborbook can require cache settings while a static site can omit them. I kept the validator useful across projects with different directory structures.

## Make Errors Say Where to Go

The initial output said `database.url: required`, which was technically correct and didn't help me at 22:00 when I had four candidate problems. A useful message needed to name the file, the environment, and the intended fix.

I wrapped Pydantic's errors in a formatter that knows about local conventions.

The final text for the database problem reads:

```text
projects/harborbook/config.staging.yaml
  database.url must be an environment-variable reference.
  In staging, use ${HARBORBOOK_DB_URL} and put the value in .env.local.
  Example: url: ${HARBORBOOK_DB_URL}
```

For an unknown key, the formatter checks Levenshtein distance and suggests the closest schema field. It also prints the relevant section from the schema. This added about 60 lines of Python, and it removed most of the back-and-forth between editor and terminal.

I made one deliberate exception. Internal error output stays short because I only need it when the friendly formatter breaks. The friendly path is the default command, while `--format=json` remains available for scripts.

## Set Defaults Near the Config

At first, the validator inserted defaults into memory. That made validation pass while the running application still saw missing values. It also hid which fields were absent, so I stopped doing that.

The validator now reports a missing optional field and names the default it would use. A separate command writes an explicit block into the config file. That makes the setting visible in Git and keeps the application loader free of hidden behavior.

For example, `ttl_seconds` defaults to 300 in staging. The report says the value is missing, states the default, and offers a one-line patch. The patch command uses an anchor comment so the generated settings are easy to find later.

The validator gives secrets stricter treatment. It accepts only a reference such as `${HARBORBOOK_DB_URL}`, never a literal URL. It also scans the local `.env.example` file and confirms every referenced variable has an entry.

## Run It in CI

A local command only helps the person who remembers to run it. After I validated six repositories manually, I added a GitHub Actions job named `config-check`. It installs Python 3.12, runs `uv sync`, then calls one script.

```bash
uv run scripts/validate-config --all
```

The script discovers `config.*.yaml` files at the repository root and validates each one against its selected profile. It exits with a nonzero status after collecting every error, so one run shows all problems instead of stopping at the first file.

For Harborbook, I also made the deployment workflow call the same validator, so a deployment couldn't proceed with a missing cache timeout. The workflow duplicated no rules because both callers used the same Python package.

The local command and CI job print the same friendly output. I wanted consistency because I copy the CI error into my editor when a change fails on a clean machine.

## Measured Changes

The first full scan reported these issues in 14 projects:

- 9 misspelled keys
- 7 missing environment-variable references
- 7 forgotten defaults

I fixed them in small commits over two evenings.

The time cost also fell. Checking one project used to take five to ten minutes of manual review. The automated check takes about 1.2 seconds, and the six-project sweep takes 4.8 seconds.

The schema files still need care. When Harborbook added a queue section, I updated the schema, a fixture, and two error messages in one pull request. That was slower than editing YAML alone, but the next config change had a documented schema.

I wouldn't add this to every toy project. It earns its cost when several environments share a service, when deployment depends on local conventions, or when a silent default can change behavior.

The invented project taught me a practical rule: treat configuration as an interface. I'll write more about schema fixtures and error-message tests in a future article. Subscribe if you want to follow along.
