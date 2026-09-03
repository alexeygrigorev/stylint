# Keeping Local Development and Production Containers Close

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. In March my checkout passed all tests locally, and the same commit failed in production within four minutes of deploy.

The failure came from a minor image difference. My laptop ran Postgres 15.2 from a compose file I had edited by hand. Production ran Postgres 14.9, and one query behaved differently across the two versions.

In this post, I'll share:

- how I unified the compose files
- how I check the environment before tests
- how I keep image versions aligned
- how I handle secrets across environments
- what parity removed from my deploy routine

## Drift Between Laptop And Server

The March setup had grown organically across eight months. My compose file defined five services, the production cluster defined seven, and three shared services used different image tags on each side.

Local Redis ran version 7.0, production ran 6.2, and a stream command I used in development didn't exist in the older version. The tests passed locally because they never touched that command path directly.

The rule I took from March is simple. I keep one compose definition that both my laptop and the server derive from, and I verify the derivation in CI.

## 1. Unify The Compose Files

I merged the two compose files into one base file plus two small override files. The base file at `compose.yaml` defines every shared service, and the overrides add only what differs.

The production override holds three settings:

```yaml
services:
  api:
    replicas: 3
    restart: always
```

The development override mounts source volumes and opens debug ports. It changes no image tags, no environment defaults and no service names.

That split removed an entire failure class in one move. When I rename a service or bump a version, I edit the base file once, and both environments inherit the change.

## 2. Check The Environment Before Tests

Unification helps only while the files stay unified, so CI verifies the derivation on every pull request. A check script compares the resolved development and production configurations field by field.

The check runs as the first CI job:

```bash
uv run python scripts/check_compose_parity.py
```

That script resolves both override chains and compares image tags, port mappings and volume mounts. It ignores replica counts and restart policies, since those differ by design.

The check failed four times in April, and each failure named a real divergence. Twice I had bumped a local image without touching the base file, and twice a teammate had added a volume to one override only.

## 3. Keep Image Versions Aligned

Every image tag in the base file names an exact version, and a weekly job proposes updates as pull requests. I never use floating tags in shared services, since a floating tag reintroduces silent drift.

The base file currently locks seven images:

- Postgres 15.4 with the pgvector extension
- Redis 7.2 with persistence enabled
- Python 3.12 slim for the API service
- Nginx 1.25 as the static frontend
- Grafana 10.2 for dashboards
- Prometheus 2.49 for metrics
- Certbot 2.8 for certificate renewal

I review the weekly update PR on Mondays, and it takes about ten minutes. The PR shows the version diff, the upstream changelog links and the CI result against the new tags.

## 4. Handle Secrets Across Environments

Parity stops at secrets, because development and production must never share credentials. I keep the variable names identical and the values strictly separate.

Each environment reads from its own file:

```text
.env.development
.env.production
```

Both files define the same 14 variable names, and the parity script verifies the name sets match. It never reads the values, so secrets stay out of logs and diffs.

Development values live in the repo with safe defaults, and production values live in the server vault. A missing variable fails fast at container start with the variable name printed.

## 5. Verify Before Deploy

The deploy script runs the parity check, the test suite and a smoke migration before pushing anything. Each stage gates the next, and a failure stops the run with a named cause.

My deploy checklist fits on four lines:

- parity check passes on the release commit
- full test suite passes against compose services
- migration dry run completes without errors
- image digests match the tested versions

That last line matters because tags can move between test and deploy. I record the digest after tests pass, and the deploy refuses any image with a different digest.

Since April I have shipped 19 releases without an environment-divergence failure. The March incident remains the last one, and the fix for it took one evening against months of background anxiety.

## Deploys Without Surprises

Parity didn't remove deploy failures, and I don't claim otherwise. Two releases since April failed on migration locks, and one failed on a third-party API change.

What disappeared is the specific dread of environment differences. When a release fails now, I debug the change rather than the setup, and that focus cuts diagnosis time roughly in half.

The routine costs me the Monday update review plus the minute CI spends on the parity job. Against that I stopped paying the random tax of works-on-my-laptop incidents.

I'll cover the parity script internals in a future post. If you want to follow along, don't forget to subscribe.
