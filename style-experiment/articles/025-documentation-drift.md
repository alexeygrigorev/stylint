# Finding Documentation Drift Before Users Find It

I wrote this synthetic style exercise as a how-to guide. The project, dates and measurements are fictional. In February I renamed a CLI flag in a data validation tool, and the old flag lived in the README for another six weeks.

Nobody on the team noticed, because everyone runs the new flag from muscle memory. A new user filed an issue after copying the stale example on a Friday evening. That report took longer to answer than the rename had taken to make.

In this post, I'll share:

- how I link commands to tests
- how I audit examples on a schedule
- how I verify output blocks automatically
- how I handle screenshots and diagrams
- what the audit routine costs each month

## Stale Examples And Their Cost

The February rename changed `--validate-all` to `--check-all` across 12 files. I updated the code, the tests and the changelog in one commit, and I forgot the README example on line 44.

The issue arrived 43 days later from a user who had installed version 2.4 that morning. The reporter had copied the documented flag, watched it fail, and spent an hour checking the local install before filing the report.

The rule I took from February is simple. I treat every documented command as a claim, and I verify each claim the way I verify code.

## 1. Link Commands To Tests

I started by collecting every command the docs promise. A short script walks the `docs` folder, extracts fenced `bash` blocks, and writes each block into a generated test file.

The extraction command runs from the repo root:

```bash
uv run python scripts/extract_doc_commands.py
```

That script found 34 fenced blocks across nine pages. It writes them into `tests/test_doc_commands.py`, and each generated test runs its block with a ten-second timeout.

Six blocks failed on the first run, and three of those failures were real drift. The other three needed network access, so I marked them with a local-only flag and kept them out of CI.

## 2. Audit Examples On A Schedule

The generated tests catch breakage after it merges, and a scheduled audit catches rot while it spreads. I run a monthly pass over every page that contains a command, a flag table or a configuration sample.

The audit lives in a checklist file the whole team can see:

- each fenced command matches the current CLI help
- each flag table matches the parser defaults
- each config sample parses with the current schema
- each version number matches the latest release tag
- each removed feature lost its section

The February audit took 50 minutes across 11 pages. It found two stale flags, one renamed environment variable and a config key that had gained a required suffix.

## 3. Verify Output Blocks Automatically

Commands drift, and outputs drift faster. Help text gains a line, error messages change wording, and table borders shift with new columns.

I snapshot the important outputs with a second script:

```bash
uv run python scripts/snapshot_cli_help.py
```

That script runs eight commands and stores their outputs under `tests/snapshots/`. The test suite compares fresh output against the snapshots, and a mismatch fails the build with a unified diff.

The snapshots caught a real regression in March. A refactor had dropped the `--format` option from the help text, and the snapshot diff showed the missing lines before any user reported them.

I update snapshots deliberately with a named flag, never by copying blind output. Each update gets its own commit, so the history shows which release changed which text.

## 4. Handle Screenshots And Diagrams

I can't verify screenshots automatically, so I keep their count low. I keep four screenshots in the docs, and I note the capture version inside each caption.

The caption rule fits on one line. Each screenshot caption names the app version and the screen it shows, and I retake all four during release week.

Diagrams get the same treatment with less effort. I author each diagram as a Mermaid fence in the docs source, and the fence renders at build time from the current file.

```text
docs/diagrams/validation-flow.mmd
```

That file holds the validation pipeline diagram, and I review it in the same monthly pass as the commands. A diagram that no longer matches the code gets redrawn before the release branch merges.

## 5. Keep The Routine Cheap

The whole routine costs me about 90 minutes per month. The generated tests run in CI in under a minute, the snapshot comparison adds 20 seconds, and the manual pass takes the rest.

The manual pass shrank as the docs shrank. I deleted three tutorial pages that duplicated the reference, and each deletion removed a future audit surface.

Two habits keep the cost flat as the project grows:

- every new documented command arrives with its generated test
- every release updates the screenshot captions first

New contributors follow the habits because the CI failure message tells them exactly what to run. The message prints the extraction command, the snapshot command and the checklist path.

## Eleven Cases Since February

Since February the routine has caught 11 drift cases across four releases. Eight were stale flags or renamed keys, two were outdated outputs, and one was a screenshot from two versions back.

No user has filed a docs-drift issue in three months. The February report remains the last one, and the fix for it took nine minutes against 43 days of staleness.

The routine works because it treats docs as behavior rather than commentary. I spend a small fixed amount monthly, and I stopped paying the large random cost of confused users.

I'll cover the snapshot tooling in detail in a future post. If you want to follow along, don't forget to subscribe.
