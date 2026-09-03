# Generating Architecture Diagrams from Structured Project Data

This synthetic style exercise follows a fictional practitioner. The repositories, scripts, and counts are fictional and illustrate a diagram workflow. Last April I maintained 11 small Python services and redrew their architecture diagrams by hand before each review.

Manual diagrams drifted within weeks. I renamed a queue in code and forgot the slide. A teammate added a cron job that never appeared in the overview. Reviews then debated outdated boxes instead of current behavior.

In this post, I'll share:

- the project data I started from
- how I listed components and edges on disk
- the validation step before rendering
- the render step with Mermaid
- limits of generated diagrams

## Project Data I Started From

Each fictional service used a short YAML file named `system.yaml` in its root. The file listed services, queues, cron jobs, and storage with one entry per component. I added the file during a cleanup sprint across 11 repositories.

A typical file held 14 to 22 entries. One search helper listed FastAPI, Postgres, Redis, a worker, and two cron jobs. Another listing service added SQLite for local runs and Postgres for deployed runs.

I chose YAML because I already edited it for Docker Compose and GitHub Actions. The team knew the syntax and the diffs stayed readable. I avoided a new database because the data changed only when the architecture changed.

The files lived beside code, so pull requests updated diagrams sources alongside logic. That placement mattered more than the format. When the source sits with the code, reviewers see drift in the same diff.

## Components And Edges On Disk

I defined four component kinds and two edge kinds for the first version. Components included service, worker, store, and schedule. Edges included calls and writes, which covered HTTP requests, queue publishes, and database updates.

The inventory script reads every `system.yaml` file and prints a summary:

```bash
uv run python scripts/inventory.py --root ~/services --output inventory.json
```

The command walks 11 directories, parses YAML, and writes one JSON file with 187 components and 243 edges. It runs in under two seconds on my ThinkPad. Failures print the file path and line number.

I call the checker `diagram-check`, a 160-line Python program that loads the inventory and reports gaps. It flags duplicate names, missing targets, and edges that point to removed components. The name describes its job in apposition and stays consistent across commands.

The first inventory run found 19 broken edges. Nine pointed to renamed queues, while six referenced a retired worker. Four edges used a service name with a typo that had survived three reviews.

## Validation Before Rendering

Validation runs before any image exists. I wanted broken references to fail fast with a file path, not a confusing diagram. The check became a required step in continuous integration for all 11 repositories.

The validation command is short:

```bash
uv run diagram-check --inventory inventory.json --strict
```

The command reports unknown targets, isolated components, and duplicate edges. In May it caught a renamed Postgres host that would have rendered as a disconnected box. Fixing the YAML took four minutes because the error named the file and line.

I added three rules after early mistakes. Names must use lowercase letters, numbers, and hyphens only. Every store needs at least one writer. Every schedule needs a target service that exists in the inventory.

The rule I took from those weeks: a generated diagram is only as honest as its input, so validation deserves the same care as rendering. I kept that check even after the diagrams looked polished.

## Render Step With Mermaid

Rendering turns the validated inventory into Mermaid flowcharts, a text format that Git can diff. I generate one file per service plus one overview for all 11. The generator is deterministic, so identical input yields identical output.

I render with one command:

```bash
uv run python scripts/render.py --inventory inventory.json --out diagrams/
```

The command writes 12 Mermaid files in about one second. Each file starts with a flowchart header, then lists nodes and labeled edges. I review the diff before committing, which takes about ten minutes for a typical change.

A small sample looks like this in the generated file:

```text
flowchart LR
    api[api] --> worker[worker]
    worker --> db[(postgres)]
    cron[cleanup] --> api
```

The text form makes reviews concrete. Reviewers comment on added edges and removed stores in the pull request. Rendered images come from the same files during site builds, so the published diagrams match the reviewed source.

I tried richer styling with colors and icons during the second week. Readers ignored the styling and asked about missing edges. I removed the styling and kept labels short, which improved comprehension without extra work.

## Limits Of Generated Diagrams

Generated diagrams show structure well and hide behavior by design. They list who calls whom, but they don't show retry rules, timeouts, or payload shapes. Three reviewers asked for latency numbers that the inventory never stored.

The inventory also lags during fast refactors. When I split one worker into two services, the YAML stayed stale for six days. The diagram looked clean and described a system that no longer existed.

I now treat the diagrams as an index rather than a manual. They answer where a component lives and what it touches. Detailed behavior still lives in code, logs, and runbooks that engineers read after the overview.

The workflow paid off despite those limits. Diagram review time dropped from 40 minutes to about 12 minutes per change. Drift reports fell from nine per month to two, according to my coarse review log.

I'll add optional timeout and owner fields next, then measure whether reviewers ask fewer follow-up questions. If you want to follow along, don't forget to subscribe.
