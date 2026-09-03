# Publishing a Source Bundle for a Technical Article

I wrote this synthetic style exercise as a build log, and the article, data and numbers in it are fictional. In April 2026 I published an analysis of 4,812 rental listings from one mid-sized city. Three readers asked for the data within the first week, and my working folder answered that request with 1.9 GB of files.

I considered zipping the folder and emailing it. Then I found one API key in a settings file. I also found three notebooks of dead ends and 1.8 GB of raw scrapes with landlord names and street addresses.

The rule I took from that evening: a source bundle is an edited product, and the working folder never is.

In this post, I'll share:

- how I chose the data subset for the bundle
- what the scripts and README contain
- how I handled licenses for code and data
- how I tested reproduction on a clean machine
- where the bundle stands after two months

## The Data Subset

The full scrape held 31 columns, and the article used five. I wrote `subset.py`, a script that keeps those five columns, drops duplicate listings and samples 1,000 rows with the district mix preserved. The sample keeps every headline figure inside the margins the article quotes.

The subset came to 84 KB as CSV, small enough for an email attachment. Deciding what to leave out took longer than writing the script. Raw scrapes stay out entirely, because the listings contain landlord names and street addresses. District-level numbers stay in, because the article's argument needs them.

The cut also followed basic privacy lines from the start. Rent, size, district, room count and listing date survived. Contact names, phone numbers and exact addresses never left my machine. A `--check` run after sampling confirms the row count, the column list and the district distribution against stored values.

## Scripts And README

The bundle holds three scripts:

- `subset.py` builds the CSV from a raw export
- `figures.py` draws the four article charts
- `stats.py` computes the numbers in the summary table

Six steps in the README lead from download to the fourth chart.

Each step names its command and its expected runtime:

```text
uv sync                                  # about 1 minute
uv run python scripts/subset.py --check  # about 20 seconds
uv run python scripts/figures.py         # about 4 minutes
```

The `--check` flag compares the bundled CSV against a stored row count and column checksum, so a broken download shows up before any plotting. I also wrote one honest limit into the README: the figures regenerate exactly, while the table numbers stay within the article's stated margin.

Determinism turned out to matter as much as correctness. The figures script writes the same PNG bytes on every run, which I verified by hashing two runs on one evening. Readers compare their charts against the published ones, and a differing image would read as a broken bundle.

## License And Checksums

The code ships under an MIT license, and the data gets its own statement in `DATA-LICENSE.md`. The data statement allows reuse with attribution and asks for a link to the article. One license across both would have silently re-licensed data I don't own, so the split felt necessary.

The release zip publishes with a SHA-256 checksum beside the download link.

Generating it takes one command:

```bash
sha256sum rent-bundle-v1.2.zip > rent-bundle-v1.2.zip.sha256
```

That checksum earned its place in May, when a hosting migration moved the download to a new bucket. The hash before and after the move matched, which settled the migration in about two minutes. The license choice also took less time than I expected. MIT for the code was a default I had used on 11 earlier repos. Two other article bundles I read used the same attribution approach for their data.

## Reproducing On A Clean Machine

Instructions fail quietly, so I tested the bundle on a laptop with no project history. The first run stopped because `figures.py` needed matplotlib 3.9, and the README said nothing about it. I added the version to `pyproject.toml`, reran everything, and the fourth chart appeared in about four minutes.

The full reproduction took about 20 minutes, including that fix. A reader repeated the run a week later and reported 23 minutes with no fixes needed. That second number convinced me more than my own. The bundle check now reruns on the first Monday of each month, and it fits in the same 20 minutes.

## The Bundle After Two Months

The bundle has been downloaded about 140 times, and two readers found a rounding error in `stats.py` that the article had absorbed. Fixing it took an hour and produced version 1.3. I now link the bundle at the top of the article, and the README links back to the article. One reader also reused the district charts for a student project, with attribution, which is the outcome I hoped the license would enable.

The bundle has two limits after two months. The subset can't support questions beyond the article's five columns, and the raw data stays with me. The scripts also assume a raw export format the listings site can change without notice.

The rule I took from the whole exercise: publish the smallest bundle that still reproduces the claims. The bundle now also includes a small changelog file, and that file has already saved one reader from comparing the wrong versions.

I'll write about versioning the bundle after article updates in a future post. If you want to follow along, don't forget to subscribe.
