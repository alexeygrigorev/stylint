# Readme-First Development for Tiny Projects

Last month I abandoned a 240-line CSV splitter because I couldn't remember which flag produced the audit file. The code worked, but the project failed because its interface lived only in my memory and a pile of shell history.

I wrote this as a synthetic style exercise with an invented tool and history. I would still use the readme-first workflow on a weekend project.

In this post, I'll share:

- why I now write the README before the implementation
- the six sections I include in a tiny tool
- how I turn the first example into a test
- how I automate the promised command
- what I check before calling the tool usable

## The Abandoned Splitter

The tool read a 48,000-row donor export and split it into monthly files. It also created a `summary.csv` with row counts and a `rejects.csv` for malformed records. I built the useful path in one evening and shipped it to myself.

Three weeks later, I needed the same split for a smaller export. I opened the repository and found four flags, two environment variables, and no README. I ran the wrong command twice before the output revealed my mistake.

The failure wasn't technical because the script did its job every time I gave it the right arguments. I had failed to describe the job at the command line where future me would enter.

That experience gave me a new starting rule for tiny projects: promise the command before writing the internals.

## Promise Before Implementation

I now create a repository and write a README stub before adding code. It can be incomplete, but it has to show the command I intend to run and the output I expect.

For the rebuilt splitter, the first promise looked like this:

```bash
python -m donor_split donors.csv --date-column joined_at --outdir monthly
```

Under that command, I wrote the expected result in three sentences. The tool should create one CSV per month, preserve the input column order, and write rejected rows with their original line numbers. It shouldn't modify `donors.csv`.

That promise immediately exposed a decision I had skipped in the first version. If a row had an invalid date, the tool needed a rule. I chose rejection over guessing because the audit file was the reason I wanted the tool.

## A Minimal README Layout

I keep the finished README short. I don't need a full documentation site for a 300-line script.

I do need six stable sections:

- one-sentence purpose
- supported input format
- installation command
- first useful example
- expected output
- known limitations

I write one sentence about the intended user, then list the required columns and accepted date format. I also state the largest file I tested and whether duplicate donor IDs pass through unchanged.

I use the same layout with a coding agent. When I ask it to change the splitter, it can read the promised interface instead of inferring behavior from four flags.

## Test and Automate the Example

After the README draft, I turn its first example into an integration test. This keeps the documentation honest and gives me a quick regression check.

I put a 12-row fixture in `tests/fixtures/donors.csv`:

```text
donor_id,name,joined_at,amount
1001,Ada North,2026-01-14,25.00
1002,Ben Ortiz,2026-01-31,40.00
bad,Invalid Row,2026-13-02,10.00
```

The test runs the CLI with the README command and checks four facts. It expects two monthly files, one summary row for each month, one rejected row, and no change to the fixture file's checksum.

I wrote the test before the new implementation. That order mattered because it forced me to choose the exact filenames and output columns while the interface was still cheap to change.

## Automate the Promised Command

Once the test passes, I add a small Makefile target.

The command is deliberately boring:

```bash
make example
```

The target creates a temporary directory, runs the fixture, compares generated files with checked snapshots, and prints a short diff on failure. The whole check takes under two seconds.

I also add the same target to GitHub Actions. The workflow uses Python 3.12, installs the package with `uv`, and runs `make example` before unit tests. A README change that breaks the example now fails in about 45 seconds.

This setup removes the most common drift problem. I can change the code, see the output diff, and decide whether to update the README and snapshots together.

Before I consider a tiny tool usable, I run a short review. I read the README as a fresh user, copy every command into a clean shell, and compare the visible output with the promised output.

I also ask a coding agent to use only the README. During the rebuilt splitter, it asked whether `monthly` should exist first and whether an existing file should be overwritten.

Both questions led to documentation changes. I now say that the tool creates the directory when needed and overwrites generated files, while refusing to overwrite the input path.

The final review takes about 15 minutes, which is cheaper than rediscovering the tool after three weeks.

## Final State

I rebuilt the splitter in 310 lines with 14 tests. It reads a 50,000-row file in 2.8 seconds, and I kept the README to 86 lines.

I can scale this method down without losing its point. A tiny project doesn't need elaborate documentation. It needs one honest command, an expected result, and a test that keeps them together.

I plan to use this README-first pass on a small charting utility next. Subscribe if you want to see how that experiment goes.
