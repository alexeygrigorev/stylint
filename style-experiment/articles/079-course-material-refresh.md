# Refreshing Course Material Without Rewriting Everything

This synthetic style exercise follows a fictional practitioner. The course, tools, and counts are fictional and illustrate a refresh routine. Last January I owned a six-module Python course with 320 enrolled learners and 41 code samples.

Three samples used retired library versions and two assignments referenced a closed API. Learners filed 23 issues in one month. I had four weeks before the next cohort and no time for a full rewrite.

In this post, I'll share:

- how I listed stale tools and dates
- how I preserved assignments that still worked
- how I updated tests before slides
- how I re-recorded only failing sections
- how I published changes with a changelog

## 1. List Stale Tools And Dates

I started by listing every tool, version, and date in the material. I scanned slides, notebooks, and starter code for version pins and screenshots. The scan covered 41 samples, 18 notebooks, and 96 slides.

I tracked findings in a small Markdown table replacement file called `refresh.md` with one bullet per issue. I used bullets because they diff cleanly in Git and render in any editor. Each bullet named the file, the stale item, and the replacement.

The audit command was simple:

```bash
uv run python scripts/scan_versions.py --course course-v3 --output refresh.md
```

The command prints version strings, screenshot dates, and linked API endpoints. It found 14 stale pins, nine outdated screenshots, and two dead endpoints. The full scan took 11 seconds on my laptop.

I ranked issues by learner impact rather than file order. Broken installs came first, while outdated screenshots came last. That ranking kept the refresh focused on failures that blocked progress.

## 2. Preserve Assignments That Still Worked

Four of six assignments needed no changes beyond version bumps. Their learning goals remained sound and their datasets still loaded. I kept those assignments intact and said so in the changelog.

I ran each assignment fresh in a clean virtual environment. The check used Python 3.12, fresh installs, and the starter code learners download. Three assignments passed in under six minutes each.

One assignment failed on a changed CSV header. The dataset owner had renamed two columns in December. I updated the loader and added a header check, which took 40 minutes including a rerun.

The rule I took from that day: preserve anything that still teaches, and change only what blocks learners. Rewrites feel productive, but they introduce new errors into material that already works.

I also kept the assignment IDs stable across the refresh. Past forum answers reference those IDs, and renaming would have broken 60 linked threads. Stability mattered more than tidier names.

## 3. Update Tests Before Slides

I updated the automated checks before touching any slide. The course has 112 checks that verify installs, imports, outputs, and file layout. Those checks define done more precisely than prose.

I ran the suite first to record failures:

```bash
uv run pytest tests/course --tb=short -q
```

The command reported 19 failures across five modules. Twelve came from version pins, while five came from changed output strings. Two failures traced to the renamed CSV columns I had already fixed.

I fixed tests one module at a time and committed after each module. That gave me five small diffs instead of one large rewrite. Review took 25 minutes per module with a teaching assistant.

Only after tests passed did I update slides and transcripts. The slides then described behavior the checks enforced. That order prevented the common drift where slides promise one thing and code does another.

## 4. Re-record Only Failing Sections

Video made up 7.5 hours across 42 lessons. Re-recording everything would have taken two weeks I didn't have. I re-recorded only lessons where commands or outputs changed.

I identified nine lessons with behavioral changes. Each needed new terminal output, a new explanation, or both. The other 33 lessons kept their recordings with updated captions where version numbers appeared.

My recording setup uses OBS with a 1080p canvas and a USB microphone. I record in the morning, edit in the afternoon, and publish at night. One lesson takes about 90 minutes from script to upload.

The nine re-recorded lessons totaled 94 minutes of new video. I reused intro and outro segments to keep the style consistent. Learners noticed the fixes and didn't comment on mixed recording dates.

I also added errata markers to three lessons with minor wording issues. The markers link to the changelog entry with the correction. That avoided re-recording for small clarifications.

## 5. Publish Changes With A Changelog

I published a one-page changelog with the refreshed material. The page lists changed files, new versions, and assignment status. It also names two known issues I chose to defer.

The changelog groups entries for quick scanning:

- updated library pins across 14 samples
- fixed CSV loader and added header checks
- refreshed nine videos totaling 94 minutes
- deferred two optional API lessons to summer

I linked the changelog from the course homepage and the first lesson. Support questions about versions dropped from 23 to six in the next cohort. The page took 50 minutes to write and saved several hours of forum replies.

The refresh took 38 hours across four weeks. Full rewrite estimates had ranged from 120 to 160 hours, so the targeted pass saved about three weeks. Learner completion rose from 54 to 61 percent, though the cohort differed in other ways.

I'll repeat this audit before every cohort and keep the scan script alongside the course. If you want to follow along, don't forget to subscribe.
