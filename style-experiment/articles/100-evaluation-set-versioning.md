# Versioning Evaluation Sets with the Code That Uses Them

I wrote this synthetic style exercise as a how-to guide, and the repository, scores and dates in it are fictional. In January 2026 a release review at my workplace fell apart because an eval set had changed silently two days earlier. The 92 percent pass rate from the previous week was no longer reproducible.

We didn't need a better metric. We moved the eval sets into the same repository as the code, and we started versioning them like any other artifact. You can copy this setup in about an hour, and it has held for six months.

In this post, I'll share:

- freezing every case into an immutable version
- writing a change note for each new version
- comparing scores inside one version, with a bridge subset
- the mistakes we made in the first month
- where the setup stands after six months

## 1. Freeze Each Case Into An Immutable Version

An evaluation case is one input with one expected behavior, and ours live in `evals/cases/` next to the code that scores them. A frozen case never changes, no matter how small the flaw. When a case turns out to be wrong, you write a new case file and retire the old one.

A case file holds the input question, the expected behavior, and two grouping tags. Ours average about 15 lines of JSON, and the tags give us subsets such as timeouts or refunds without extra tooling. Each case also records the prompt format version it was written for.

The layout keeps versions, notes, and results apart:

```text
evals/
  cases/
    v3/
      case-001-retries.json
      case-002-timeout.json
  notes/
    v3.md
  results/
    v3-2026-06-12.json
```

The version lives in the folder name, and a result file always names the set it came from. Nothing edits a file under `cases/v3/` once that folder has a result in `results/`.

Freezing a new version is a copy plus a check:

```bash
cp -r evals/cases/v3 evals/cases/v4 && python evals/lint_cases.py evals/cases/v4
```

Here the helper script `lint_cases.py` verifies case ids and the JSON schema. A full copy costs about 60 KB for 126 cases, so we don't bother with fancier storage.

## 2. Write A Change Note Per Version

Every new version gets a short note in `evals/notes/`, written the same day the version is frozen. The note lists which cases were added, which were retired, and why the new version needed to exist at all.

Our notes follow one template:

```text
# v4 - 2026-05-02
Added: 6 timeout cases from the March incident (INC-114).
Retired: case-041, its expected answer cited a removed endpoint.
Reason: v3 under-tested timeouts before the retry change.
```

A note takes about ten minutes to write and saves an hour of archaeology later. The template lives in `evals/notes/TEMPLATE.md`, and the freeze command prints its path as a reminder. When someone asks why a pass rate moved, the note answers before anyone opens a diff.

## 3. Compare Scores Across Versions

Scores are only comparable within one version, because the cases define the test. The pipeline stores every result next to its set version, and our compare script refuses to mix folders from different versions.

To measure code changes across a set change, we run a bridge subset.

It scores the 40 cases that exist in both versions under both code versions:

```bash
python evals/compare.py --base v3 --head v4 --bridge
```

The June comparison printed:

```text
v3: 92.4% (115 of 118 cases, run 2026-06-12)
v4: 94.1% (119 of 126 cases, run 2026-06-12)
bridge: v3 90.0% vs v4 93.7% on 40 shared cases
```

The full-set numbers moved by 1.7 percent, and the bridge moved by 3.7 percent. That gap told us the code had improved, while the new cases were harder than the old ones. Without the bridge, we would have read the smaller number as the whole story. We run the full set before every release and after any prompt change, which works out to about six runs a month. The compare script is about 80 lines of Python and lives in the same folder as the cases it reads.

## Common Mistakes

We made three mistakes in the first month:

- editing a case in place to make a failing test pass
- comparing a v2 result with a v3 result and calling it progress
- letting case formats drift from the prompt format they test

Editing a case to turn a failing test green feels efficient, and it silently moves the target. We handle a bad case by cutting a new version with a note, and the note becomes the receipt for why the score moved. Format drift was the quietest mistake of the three. In February a prompt refactor changed the input shape, and 11 old cases failed for formatting reasons before we noticed the mismatch.

## Six Months With Versioned Sets

The whole setup fits in three folders, one lint script, and a note habit, and adopting it took about an hour. Release reviews stopped arguing about whether a score was real, because every score now names its set and its date.

The notes don't scale on their own. They depend on someone writing them the same day, and a two-week backlog in April left one version hard to explain at review time. Automating first drafts of the notes is the obvious next step.

I'll write about how we turn incidents into new cases in a future post. If you want to follow along, don't forget to subscribe.
