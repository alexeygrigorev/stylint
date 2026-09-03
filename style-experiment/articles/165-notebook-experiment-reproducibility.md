# Making a One-Off Notebook Reproducible Enough to Rerun

I invented Transitdelay, a bus-delay study, and every notebook result for this synthetic style exercise. In the fictional February 2026 setting, I needed to rerun notebook 03 for a meeting four days later. It had produced its charts six months earlier, and it now failed before the second cell.

In this post, I'll share:

- why a saved notebook wasn't a rerunnable result
- how I fixed the environment without freezing exploration
- how I separated inputs from generated outputs
- what belongs in runtime notes
- the rerun check I now use

## 1. Test the Claim, Not the Display

I trusted the notebook because every cell had stored output. The plots, row counts, and comments were all present. None of that proved I could produce them again from the current machine.

The first error was an unfixed plotting-library version. A newer version changed the date-axis behavior, and the notebook called a private helper that had disappeared. Later, a hard-coded `/Users/alexey/data/transit` path failed on the server.

I made a distinction that shaped the cleanup. Reproducibility for this project means a colleague can regenerate the final tables and figures from fixed inputs. It doesn't mean every discarded experiment must rerun.

With that scope, I could fix the useful path in one afternoon instead of turning a 74-cell notebook into a polished package.

## 2. Fix the Environment

I created a lock file for notebook 03 rather than upgrading the whole repository. The study used these packages:

- Python 3.11
- pandas
- DuckDB
- matplotlib
- `transitlib`, containing two internal utility functions

The relevant environment file records exact versions:

```text
python==3.11.8
pandas==2.2.1
duckdb==0.10.1
matplotlib==3.8.3
transitlib==0.4.2
```

`uv sync --locked` recreates that environment from the lock file. I kept a separate `requirements.in` file for future experimentation, but the meeting rerun uses the locked set.

This rule preserved the original behavior and let me improve other notebooks independently. When I later tested pandas 2.3, a failed new branch wouldn't invalidate the February result.

The system Python packages stayed out of the lock file. They weren't needed by the notebook, and including them made the first restore take 6 minutes instead of 45 seconds.

## 3. Separate Inputs and Outputs

The original notebook stored these file types together:

- downloaded schedules
- cleaned parquet files
- final charts

Several cells wrote into that directory, so rerunning could overwrite an input with a derived file.

I reorganized notebook 03 around four directories:

- `inputs/` for immutable downloaded files
- `work/` for intermediate tables
- `outputs/` for figures and result tables
- `logs/` for rerun records

Each downloaded file gets a `manifest.csv` row with its source name, download date, byte size, and SHA-256 checksum. The checksum is enough to tell whether a later export changed the study population.

I restricted notebook reads to `inputs/`. Intermediate cleanup writes to `work/`, and publication artifacts write to `outputs/`. A rerun may regenerate every derived file, but it can't modify the immutable directory.

For the meeting, I reran from the original 1.9 GB input set. The final output contained four CSV tables and nine PNG figures.

## 4. Write Runtime Notes

Code and a lock file weren't enough. I also added a runtime note. The note records the exact command, machine class, expected duration, and known nondeterminism.

The first note for notebook 03 has five lines:

```text
Command: uv run jupyter nbconvert --to notebook --execute notebooks/03-delay-by-route.ipynb
Machine: 4 CPU, 16 GB RAM
Duration: 3m40s to 4m10s on 1.9 GB inputs
Expected outputs: 4 CSV files, 9 PNG files
Known variation: route labels with the same delay percentile can swap order
```

The duration range matters more than a single precise number. It sets expectations and makes an unusually slow rerun obvious. The known-variation line prevents a false alarm when two tied routes switch positions.

I add one entry every time the environment, input manifest, or expected outputs change. Each entry explains its reason in one sentence. For example, the 0.4.2 release of `transitlib` fixed a timezone conversion and changed two totals by less than 0.1%.

The note lives next to the notebook, not in a separate wiki. A reader sees the operating instructions before trying to execute the file.

## 5. Add a Small Rerun Check

The final step compares the regenerated outputs with the February outputs. I don't require byte-for-byte equality, because PNG metadata can differ even when the image is equivalent.

For CSV files, the checker validates these properties:

- existence
- row count
- column names
- checksum

For PNG files, it checks dimensions and file size ranges.

```bash
uv run scripts/check-notebook-outputs notebooks/03
```

The script exits successfully when all 13 expected artifacts match their schemas. It reports a changed CSV checksum with the old and new SHA-256 values and the rows that differ most in numeric columns.

That failure report caught one real issue during testing. A filter used local time instead of the schedule timezone, so the row count changed from 412,806 to 413,114. Fixing it changed several chart points, and the meeting still used the corrected result.

The project is now reproducible enough for its purpose, and it's still a notebook. I'll write about promoting a stable notebook path into a small library in a future article. Subscribe for updates.
