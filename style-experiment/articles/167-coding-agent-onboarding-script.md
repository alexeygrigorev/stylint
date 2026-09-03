# Creating an Onboarding Script for a New Coding Agent

This synthetic style exercise invents the repository, commands, and timings. In February 2026, I started a fictional client project called Ledgerpulse, an expense-review dashboard. Its README had installation steps, but they had drifted from the actual service setup. A coding agent made that drift obvious because it followed the instructions without assuming the missing parts.

In this post, I'll share:

- how I reduced onboarding to one command
- what the script verifies before it runs
- how I give the agent a first task
- where I look when the output looks wrong
- what I'd change for a larger team

## 1. Write the Minimum Contract

The repository had three services: a FastAPI backend, a PostgreSQL database, and a Vite frontend. The README said to run Docker Compose, but it omitted the `.env` file, database migration command, and seeded user.

I stopped adding prose to the README and wrote the contract first:

- Python 3.12
- Docker Engine 27
- `uv` for Python packages
- Node 22 for the frontend
- one `.env` file with 11 variables

Each item has a version because "current" changes too quickly. The contract lives at the top of `onboarding.sh` and in a short section of the README.

The first version of the script tried to install everything itself. That made it harder to tell whether a failure came from the machine, the script, or the project. I changed it to check for required tools and stop with the exact missing item.

## 2. Verify Before Installing

The final script has three modes: `check`, `install`, and `reset`. `check` is read-only, so I can run it before explaining anything to an agent.

Here is the useful part of the command flow:

```bash
./scripts/onboarding.sh check
./scripts/onboarding.sh install
./scripts/onboarding.sh reset --with-data
```

The check phase verifies tool versions, free disk space, available ports, and Docker permission. It prints one line per requirement and exits on the first blocker. On my laptop, that takes about 900 milliseconds.

The install phase copies `.env.example` to `.env` only when `.env` doesn't exist. It starts Postgres, applies migrations, loads 2,400 sample transactions, and installs frontend packages. The complete install took 2 minutes and 40 seconds on a 2024 laptop.

The reset mode removes generated containers and local data. It refuses to run unless `LEDGERPULSE_CONFIRM_RESET=yes` is set. That one guard has prevented me from deleting a real database twice.

## 3. Run a Small Task

After installation, the agent gets a task that proves it can edit, test, and observe the full loop. I don't start with architecture work. The first task is to add a nullable `reviewed_at` field to the expense table and expose it in one API response.

I put the task in `agent-tasks/001-first-change.md`. The file contains the user-visible behavior, acceptance checks, files to touch, and commands to run. The acceptance section has four items:

- the migration applies on an empty database
- the API response includes `reviewed_at` as null
- the frontend displays an em dash when the field is null
- backend and frontend tests pass

This is deliberately dull. It crosses the migration, serializer, UI, and test layers, so a missing service shows up early. It usually takes the agent 6 to 12 minutes.

The prompt tells the agent to run `./scripts/onboarding.sh check` first. If that fails, it should stop and report the missing requirement. That rule keeps the model from improvising around a broken environment.

## 4. Inspect the Output

I don't read the final diff first. I read the command log, because it shows whether the agent actually followed the loop. The useful log has a migration command, backend tests, frontend tests, and a short summary.

Then I run the same commands myself:

```bash
uv run pytest tests/api -q
npm test -- --run
```

The first task should leave 34 backend tests and 19 frontend tests passing. I also open the dashboard and create one expense. The field should show as empty until the review endpoint is called.

Three output problems appear most often. The agent adds documentation for an unrequested feature. It puts configuration in two places. Or it improves unrelated code in the same commit. For each case, I reject the unrelated part and leave the small vertical slice intact.

The log is also a learning artifact. On Ledgerpulse, the first run showed that the frontend test command had no coverage of the serializer. I added that test to the starter branch after seeing the gap.

## 5. Make It Repeatable

Once the first task passes, I save the whole exchange as a fixture. The repository now has five such tasks, covering an API endpoint, a report query, a CSV export, a permissions rule, and a bug fix. Each one has known commands and a known test count.

When I upgrade a dependency or add a service, I rerun all five tasks. That takes about 45 minutes on the fictional project and has caught two breaking changes before client work started.

For a larger team, I'd add role-specific seeds. A reviewer shouldn't need sample financial data from every organization, and a frontend designer shouldn't need to run database migrations by hand. The shared script should stay boring and compose smaller scripts.

## What I Learned

The onboarding script isn't a convenience layer; it's the first test of the project. If a coding agent can't reach a passing task in one command, a new teammate will have the same problem.

Keeping the first task small matters just as much. It gives the agent a complete loop and gives me a stable way to review its output.

I plan to write more about task fixtures for coding agents. Subscribe if that's useful to you.
