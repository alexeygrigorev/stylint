# Making a Small CLI Tool Pleasant Enough to Keep Using

I wrote this build log as a synthetic style exercise, and the tool name, usage counts, and release notes are fictional. In the invented project, I spent three weekends improving `invoiceq`, a command-line tool that turns CSV invoices into summary reports.

The core transformation already worked. It processed a 4,200-row file in 0.8 seconds and wrote both output formats.

The problem was that I avoided the tool unless I had its README open.

In this post, I'll share:

- the first command and its bad defaults
- how I reduced flags to two modes
- the errors I rewrote first
- how shell completion changed usage
- what the three-week measurements showed

## First Command

The original command looked reasonable to me and hostile to future me. It required five arguments, used short flag names inconsistently, and wrote its output to a hidden directory if no path was given.

```bash
invoiceq -i ./data/2026-08.csv -o ~/reports -f md -c EUR -p
```

I had to remember that `-p` meant "include per-client rows". If I forgot `-c EUR`, the tool used dollars without saying so. If the output folder didn't exist, it printed a Python traceback and exited with status 1.

My first instinct was to add a config file. I sketched a YAML schema with currency, locale, output directory, and report sections. Then I looked at the actual invocations in my shell history: 38 of 42 used the same three settings.

I made those settings defaults instead, and I left the exceptions on the command line. Configuration would have centralized choices I rarely changed.

## Two Modes

I reduced the interface to `report` and `check`. The `report` command reads one CSV file and writes a Markdown summary.

The `check` command validates required columns, date formats, and duplicate invoice numbers. It then prints a short problem list.

```bash
invoiceq report data/2026-08.csv
invoiceq report data/2026-08.csv --per-client
invoiceq check data/2026-08.csv
```

I kept the currency default in the project-local `.invoiceq.toml` file, so this wasn't another global configuration layer.

I preserved `--output` for scripting, but the default became `reports/2026-08.md` next to the input file. Predictable naming mattered more than flexibility, so I could find last month's report without opening shell history.

Before writing anything, the tool now prints the source file, row count, and output path. That one preview caught two mistakes in the first week.

## Helpful Failures

I rewrote errors in the order they appeared in my own sessions. The first was a missing input file, and the old traceback said `FileNotFoundError`.

In the new message, I show the checked path with a command the reader can run next. That next command is `invoiceq check` on a sibling CSV.

```text
error: input file not found: data/2026-09.csv
checked: /home/me/work/invoices/data
try: invoiceq list data
```

The second was a schema error. Instead of reporting the first bad cell, `check` now reports all issues by row number and column, with a maximum of 20 findings per run. In the original 4,200-row test file, this turned five repair cycles into one.

```text
data/2026-08.csv: 6 issues
row 14: amount "1.234,56" does not match decimal format
row 22: missing invoice_number
row 22: currency "US" is not ISO alpha-3
```

I also changed the exit codes. Zero means the command succeeded, while 1 means validation failed. Status 2 means the tool couldn't run.

## Shell Completion

Adding completion did more for daily use than I expected. Typer, the CLI framework, generated its completion scripts for common shells such as Bash and Fish.

I added a `--install-completion` command and documented it first in the README.

```bash
invoiceq --install-completion
```

After installation, `invoiceq <TAB>` showed `check` and `report`, while `--<TAB>` showed only valid flags for the active subcommand.

I also added `invoiceq list`, which prints CSV files and row counts in the current folder. It solved a small but repeated question: I could see which monthly file was correct before running a report. The command took 45 lines of code and became the second most used subcommand.

For six weeks, I logged shell invocations with shell history timestamps. Before completion, 15 invocations used `--help`. After completion, that dropped to 3, while total invocations rose from 42 to 61.

## Measured Improvements

I tracked command success rate for three weeks. I also tracked the time from invoice CSV to finished report and the number of validation cycles per bad file.

Command success rose from 31 of 42 to 57 of 61. Median time to a monthly report fell from 2 minutes 40 seconds to 48 seconds. Bad files needed 1.4 validation cycles, down from 3.2.

The most useful change was less measurable because I stopped keeping a note with example commands.

I did find one limit. A new user still needed a sample file and a description of expected columns. Ergonomics can't remove domain rules. It can only expose them before the tool fails.

## Lessons

The best interface changes removed choices. Two modes, four project-local settings, and predictable output names made the tool easier to remember than a configuration file.

Error messages are part of the interface. Good messages name the checked path, show the offending rows, and suggest the next command. Bad messages turn a small data problem into a debugging session.

I plan to write about the validation rule set in more detail in a future article. Subscribe if you want to see how it handles more invoice formats.
