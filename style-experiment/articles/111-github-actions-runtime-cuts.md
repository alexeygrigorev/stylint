# Cutting Runtime from a GitHub Actions Workflow

I wrote this synthetic style exercise as a build log. The repository, dates and measurements are fictional.

On 12 June I looked at a GitHub Actions run for a Python package called `ledger-tools`. The full workflow took 27 minutes, and I had already waited for it four times that day. The package had 18 test jobs, three dependency caches and a deployment job that ran after every merge.

The workflow was correct, but it was unpleasant to use. A one-line documentation change waited behind the same matrix as a change to the payment parser. I wanted faster feedback without hiding the tests that had caught two real bugs in April.

In this post, I'll share:

- how I measured where the 27 minutes went
- why my first cache change barely helped
- how I reduced the test matrix from 18 jobs to 10
- which workflow changes survived a week of normal use
- what the honest final number looks like

## Measuring The Slow Workflow

I added `workflow-run-id` notes to a spreadsheet and recorded ten runs from the previous week. The median total runtime was 26 minutes and 40 seconds. Six runs varied by less than two minutes, so one median run was a reasonable target.

The job timeline showed three large blocks. Dependency setup took 5 to 8 minutes, the test matrix took 14 to 17 minutes, and deployment took 2 minutes. The remaining time came from queueing and the final status check.

I also recorded each job separately. The slowest Ubuntu and Python 3.12 job took 16 minutes. The fastest Windows and Python 3.10 job took 8 minutes. That difference shaped the next decision.

## The First Cache Attempt

The obvious first move was to cache more aggressively. The existing workflow cached `pip` packages but installed browser binaries and a compiled `orjson` wheel on every job. I added a cache for the browser directory and another for the local virtual environment.

I tried this cache block first:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/ms-playwright
    key: playwright-${{ runner.os }}-chromium
```

That block reduced browser installation from 85 seconds to 11 seconds on a warm run. It looked like a clear win until I measured the whole job. The same job still took 15 minutes and 50 seconds, because dependency setup was only one part of the slow path.

The virtual-environment cache was worse. It saved about 70 seconds after a warm cache appeared, but it added 40 seconds of cache restoration and another 30 seconds of cleanup. Across 18 jobs, the total savings was smaller than the noise between runs.

The rule I took from that afternoon: measure one job end to end before adding another cache.

## Pruning The Matrix

The old matrix covered Ubuntu, macOS and Windows. It paired them with Python 3.10 through 3.13 and produced 12 combinations. Six additional jobs covered optional database backends, so the workflow scheduled 18 test jobs on every push.

On 14 June, I reread the test names and issue history, then made these changes:

- every operating system continued to run the current Python version
- only Ubuntu ran the three older Python versions and the optional database jobs

I stored the new matrix in two files, and the main list stays small:

```yaml
matrix:
  os: [ubuntu-latest, macos-latest, windows-latest]
  python-version: ["3.13"]
```

A second include block adds the older versions on Ubuntu only. That removed macOS and Python 3.10, a combination that had never found a unique issue during the repository's 14-month history.

I also removed two duplicated smoke tests from the optional database jobs. They ran the same HTTP checks as the main suite and existed because a copy-paste in January had survived two refactors. The project went from 18 test jobs to 10.

## Making The Remaining Jobs Faster

The next change targeted the slowest job. It installed four database servers, even though each run exercised only two of them. I split that job into two jobs with narrower dependency sets.

One job installs PostgreSQL and runs the SQL tests:

```bash
uv run pytest tests/sql -x
```

The other installs Redis and runs the cache tests. Each job now installs fewer system packages, starts one service instead of two and fails closer to the code that caused the problem. The two jobs run in parallel, and each takes 4 to 6 minutes.

I also changed the deployment trigger. It previously ran after every merge, including merges that touched only `docs/`. The new condition checks that at least one file under `ledger_tools/` or `tests/` changed. That removed about 90 seconds from documentation-only merges.

## Runtime After Five Runs

I ran the new workflow five times on 17 June. The median total runtime was 13 minutes and 20 seconds, so the headline improvement was close to 2x.

The breakdown is less dramatic because matrix pruning saved about 8 minutes of elapsed time. Cache changes saved 35 to 60 seconds per job, but their contribution to total runtime was only about 2 minutes. Queueing remained outside my control.

Three results from the week made me comfortable with the trade-off:

- 14 pushes produced green runs with no new operating-system failures
- one Windows-specific path bug still appeared on the current Python job
- documentation merges returned feedback in about 4 minutes

I gave up parallel coverage for older Python versions on macOS and Windows. The project releases a pure-Python wheel, and its C extension has one build path. That made the risk acceptable, but a package with compiled wheels for every combination shouldn't copy this matrix blindly.

## Reflections From The Runtime Work

The useful number wasn't the first cache hit. The workflow felt slow because 18 jobs started on every push and one job controlled the final answer. Reducing that fan-out mattered more than shaving individual setup steps.

I now keep a small runtime log in the repository. It records the date, commit, trigger, total time and slowest job. Five rows after a change are enough to separate a real improvement from a lucky run.

The workflow still takes 13 minutes, and the end-to-end deployment path still waits for Windows. My next target is test collection, which adds 45 seconds before the first test starts.

I'll write about that profiling work after another release cycle. If you want to follow along, don't forget to subscribe.
