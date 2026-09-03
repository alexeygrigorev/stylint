# Making Assignment Dependencies Obvious to Students

This synthetic style exercise follows a fictional practitioner with invented numbers and events. Nothing here describes a real project. Last autumn I mentored a cohort of forty students through a four-week data project.

Week two brought a flood of setup questions in the course chat. Eighteen students couldn't run the starter code on their laptops. The failures traced back to hidden prerequisites nobody had named.

I first answered each question by hand in the chat. I asked for tracebacks, guessed the missing piece, and typed install steps from memory. That approach helped five students and exhausted me by Thursday.

The same three gaps kept appearing across machines. Students missed Python 3.12, lacked a C compiler for one package, and skipped the environment variable for the data path. I typed the same answers nine times in two days.

In this post, I'll share:

- why hidden prerequisites sank week two
- how I mapped every dependency before rewriting
- what the starter code checks at launch
- how students recover from a failed check
- what the setup costs now and where it still falls short

## Hidden Prerequisites Sank Week Two

The starter repo assumed a working Python setup with six packages pinned. I developed it on a ThinkPad where everything already existed. New machines missed pieces I no longer noticed.

I had written the install steps as paragraphs across two README pages. Students skimmed past the compiler note buried in step four. Windows users hit a different wall with path separators in the data loader.

I counted the damage on Friday from chat history. Eighteen students reported blocks, and eleven never finished the week-two task. Four of them wrote that the tooling felt harder than the coursework.

The rule I took from that week: prerequisites must announce themselves, and the announcement must happen before any coursework runs.

## Mapping Every Dependency First

I listed every external piece the project touched across a fresh Ubuntu install. The list held Python 3.12, `uv`, a C compiler, and Git. It also required 340 MB of disk for the dataset. Each item earned its place by breaking the run once.

I verified the list on two borrowed laptops over a weekend. One ran Windows 11 and the other ran macOS 14. Both failed in ways my ThinkPad never showed, and each failure added one line to the list.

The full prerequisite list lives in one file at the repo root:

```text
prerequisites.txt
starter/checks.py
starter/README.md
data/sample.csv
```

In that file I name each requirement with a version floor and a fix command. Students read that file first because the README points at it in the opening lines.

I also recorded install times on a clean machine for planning. Python plus packages took eleven minutes over course Wi-Fi. The dataset download added four more minutes at 340 MB.

## Starter Code With Built-In Checks

The starter code now opens with a check script that runs before anything. I wrote Checker, a small module for this task. It tests the interpreter version, imports, disk space, and data path. It prints one line per check with a pass mark.

Students run the check with one command:

```bash
uv run python starter/checks.py
```

The command finishes in under three seconds on a cold laptop. It exits nonzero on the first failure, so students fix problems in dependency order.

Each failure message names the missing piece and the exact fix. A missing compiler prints the install command for the detected platform. A bad data path prints the expected folder layout with an example.

The messages link to the course setup page for longer explanations:

- [Python setup guide](https://docs.python.org/3/using/index.html)
- [uv installer](https://docs.astral.sh/uv/getting-started/installation)

I tested every message by breaking a clean install eleven ways. Each break produced exactly one message with no traceback. That matrix took an afternoon and removed a whole class of chat questions.

## Recovery Without Mentor Help

A clear message means little without a fast retry path. Students needed a way to fix one item and recheck in seconds. The check script supports that loop by design.

Fixing follows the same three moves every time:

- read the one-line failure message
- run the printed fix command
- rerun the check script and confirm the pass mark

The script also writes a short log to `starter/check_log.txt`. Students paste that log into the chat when they stay stuck. The log holds versions and paths, so I diagnose without asking three follow-ups.

During the next cohort run, thirty-six of forty students passed all checks on day one. Three more passed on day two after one chat message each. One student needed a video call for an unusual antivirus block.

Median time from clone to first passing run dropped from three hours to twenty-two minutes. That number comes from self-reported times in the week-one survey. It overstates a little because fast students answer surveys first.

## Lessons From the Dependency Audit

The audit paid off across the whole four weeks of the course. Setup questions fell from forty-one messages to six between cohorts. I spent the saved hours reviewing projects instead of debugging installs.

One gap remains because I can't cover every machine. A student on a seven-year-old laptop failed the disk-space check with no room to free. We moved that student to a cloud notebook for the course.

I keep three habits from this audit for every new assignment. I install the starter code on a clean machine before publishing it. I print fix commands instead of bare error names. I log versions and paths so chat questions arrive with context.

Six hours of mapping and scripting saved roughly thirty mentor hours across one cohort. That trade looks fine to me, and I'd repeat it before any assignment with external tools.

I'll write more about designing starter repos for mixed-platform cohorts in a future post. If you want to follow along, don't forget to subscribe.
