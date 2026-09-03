# Making Long Agent Runs Recoverable

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional. In April I launched an overnight agent run to migrate 60 notebook tutorials, and I woke up to a dead process with nothing saved.

The run had worked for five hours before the laptop suspended. It had converted 41 notebooks, and every conversion vanished with the process memory because nothing had touched disk.

In this post, I'll share:

- what the overnight run lost
- how I checkpoint each unit of work
- how I log progress for restarts
- how I store artifacts between runs
- how I write restart instructions
- what recovery looks like today

## Five Hours With Nothing Saved

The April job converted teaching notebooks into a small Python library. Each notebook took four to seven minutes, and the full set needed about six hours of model time.

I started the run at midnight with the laptop plugged in and the lid open. The building power flickered at 5 AM, the machine suspended for two minutes, and the agent process died without writing a single file.

The rule I took from April is simple. I treat every long run as interruptible, and I design the checkpointing before I design the work.

## The First Version

My first fix wrote each converted module to disk immediately after conversion. That change took 20 minutes, and the next run survived a manual stop with 12 modules saved.

The second failure exposed the gap in that fix. The run crashed on notebook 30 with a malformed table. It restarted from the top and reconverted the same 12 modules before failing again at the same place.

Blind resume wastes the exact hours checkpointing was meant to save. The run needs to know what finished, what failed and what never started, and it needs that state on disk.

I added a state file after that crash. Every notebook now moves through three states, and the runner reads the file before picking up work.

## Checkpoints For Each Unit

The state file lives at `runs/migration_state.json`, and it holds one record per notebook. Each record names the source file, the current state and the timestamp of the last attempt.

The runner updates the state after every unit completes:

```bash
uv run python scripts/migrate_one.py --notebook 031 --state runs/migration_state.json
```

That script converts one notebook, writes the module, and flips the record from pending to done in a single transaction. A crash between units loses at most one unit of work.

I move failed units to a third state instead of blocking the run. The runner logs the error, marks the record as failed, and continues with the next pending notebook.

## Logs That Support Restarts

Checkpoint state tells the runner where to resume, and logs tell me why it stopped. I write two logs per run, and each serves a different reader.

The event log records one JSON line per state change:

```text
runs/logs/migration_events.jsonl
```

That file answers the restart question directly. I read the last 20 lines, and I know exactly which notebook failed and what the error said.

The human log records my own decisions alongside the run. When I skip a notebook deliberately or change a prompt mid-run, I append a dated line explaining why.

Both logs rotate per run directory, and I never delete a run directory before the quarter ends. Old logs have settled two arguments about what actually happened during a failed night.

## Artifacts Between Runs

Each finished unit produces one module in `library/`, and the runner writes it immediately after conversion. The runner writes partial outputs to `runs/scratch/` with the notebook number in the filename.

When a conversion fails halfway, I open its scratch file to see how far the output got before the error.

My artifact rules fit on four lines:

- finished modules go to `library/` immediately
- partial output goes to `runs/scratch/` with a numbered name
- the state file updates only after the write succeeds
- no artifact is ever overwritten without a backup copy

That last rule saved a full evening in May. A rerun produced a worse module for a finished notebook, and the backup copy restored the better version in seconds.

## Restart Instructions

Every run directory holds a `RESUME.md` file with the exact commands to continue. I write it before the first launch, and I update it whenever the procedure changes.

The May version reads in full:

```bash
uv run python scripts/migrate_all.py --state runs/may_batch/migration_state.json --skip-failed
```

One command resumes the run, skips known failures and picks up where the state file says. A second command retries only the failed units after I fix their inputs.

I tested those instructions on a cold checkout on another machine. The run resumed with zero questions asked, which is the entire point of writing them down.

## Recovery In Practice

Since May I have run 11 long jobs totaling 74 hours of model time. Four were interrupted by network drops, one by a full disk, and six finished without incident.

Each interruption cost under ten minutes. I read the event log, fixed the cause, ran the resume command, and watched the state file advance past the failure point.

The full-disk case taught me to check capacity before launching. The resume file now starts with a disk-space check, and the runner refuses to start with under 5 GB free.

Recovery works because the run state lives outside the process. I spend about half an hour setting up each run directory, and I stopped losing nights of compute to silent crashes.

I'll cover the state-file schema in detail in a future post. If you want to follow along, don't forget to subscribe.
