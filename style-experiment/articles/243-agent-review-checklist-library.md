# Building a Library of Review Checklists for Agent Work

I wrote this piece as a synthetic style exercise, so I invented every session count and project name in it. Last February I let a coding agent merge 34 change sets across 4 side projects with only a quick glance. Two of those change sets broke production within a week, and both failures shared one trait I had never written down.

The reviews kept catching the same defects across projects. Migrations missed null checks, new endpoints skipped auth, and tests asserted new behavior without covering old paths. Each defect felt surprising in the moment, and each one matched an older defect I had already forgotten.

After the second production incident I started collecting the misses in one file. That file grew into a small library of review checklists sorted by task type. Six weeks later the checklists caught 19 defects before merge, and reviews took less time than before.

In this post, I'll share:

- how I sorted past failures into task types
- how each checklist item earns its place
- where the checklists live in my repos
- how a review run works on a fresh change set
- what six weeks of checklist reviews changed

## 1. Sort Past Failures by Task Type

I opened my git log from January and listed every agent-authored change that later needed a fix. The list held 23 entries, and I grouped them by the kind of work involved. Five groups covered nearly everything, and each group failed in its own repeatable way.

The groups stayed concrete and small:

- database migrations that touched existing rows
- new API endpoints with auth requirements
- refactors that moved logic between modules
- dependency upgrades with config side effects
- test files written alongside new features

Migration failures all involved backfills or missing defaults, and endpoint failures all involved auth or validation gaps. Refactor failures all involved callers I hadn't found in the first pass. Once I saw those clusters, writing checks became straightforward transcription instead of invention.

I keep the groups in a single index file. When a new failure fits no group, I add a group instead of forcing the fit. The library has gained exactly one group since February, which tells me the first five were close to right.

## 2. Write Checks From Real Failures

Every checklist item traces back to one specific incident with a date attached. The migration list opens with a null-check item from a February 12 backfill that set 214 notification rows to null. The endpoint list opens with an auth item from a February 19 route that shipped without login requirements.

Each item states one observable check in plain words:

```text
- The migration sets a default for every new non-nullable column.
- The backfill script runs on a staging copy before production.
- The rollback migration exists and was applied once in staging.
- The new route rejects anonymous requests with a 401 response.
- The new route validates every query argument and rejects unknowns.
```

Items stay under 20 words and name files, columns, or status codes. I delete any item that needs two sentences, because vague items never catch anything. Three early items died this way.

An item earns its place only after it catches a second defect. First-time items sit in a probationary section at the bottom of each list. Promotion takes one confirmed catch, and 11 items have earned promotion since March.

## 3. Store Checklists Beside the Code

The library lives in a docs folder inside each repo, not in a separate wiki. Each task type gets one markdown file with a short name, and the index links them together. The whole library is 6 files and about 180 lines, which keeps it readable in one sitting.

A coding agent can read the docs folder, so I point the agent at the relevant list before it starts. My kickoff prompt names the task type and asks for changes that already satisfy every item. That single sentence cut first-round defects nearly in half across 21 sessions.

I also keep a short changelog for the lists in the docs folder. Each entry records the date, the incident, and the item it added or changed. The changelog has 17 entries, and reading it shows exactly how the library learned what it knows.

Checklist edits travel through normal pull requests with the same review bar as code. A friend who reviews my repos rejected two of my edits, and both rejections improved the wording.

## 4. Run the List on Fresh Change Sets

A review run follows the same order every time, and the order matters. I read the change set first without the list, then I run the list item by item, then I read the diff once more. The first pass catches the odd surprise, and the list pass catches the known defects.

I run the checks with a small runner script:

```bash
uv run python scripts/review_run.py --type migration --diff HEAD~1
```

The script prints each checklist item beside the files it mentions. I mark every item as pass, fail, or not relevant, and the script stores the verdicts in a JSON log. The log now holds 58 runs, and fail verdicts cluster around backfills exactly as the history predicted.

A run takes 12 to 20 minutes for a typical change set of 200 to 400 lines. That time replaced longer debugging sessions, and the trade has paid off every week since March. Slow reviews beat fast rollbacks.

## 5. Lessons From Six Weeks of Use

The checklists changed my reviews last month in a visible way. An agent migration failed 4 of 9 items on the first pass, and the fixes took one evening instead of one incident. An endpoint change failed the anonymous-request item, and the fix was 3 lines added before merge.

This library taught me a narrower lesson than process worship. Checklists work when every item names a past defect with a date, and they rot when items describe hopes. My lists stay short because each item must keep earning its place.

The gaps are honest and I accept them for now. The lists cover only the 6 task types I have seen fail, and a new domain will need new items. Creative design choices still need human judgment, and no checklist replaces that reading.

I'll describe the runner script internals in a future post on this blog. If you want to follow along, don't forget to subscribe.
