# Five Small Utilities, Five Ways to Start

I built five small utilities to remove recurring annoyances:

* `dirdotenv`
* `ssh-auto-forward`
* `nobook`
* Microphone Booster
* Bot Master

Each starts with a concrete workflow, and an AI coding assistant handles the unfamiliar technical area.

`dirdotenv` solves a mismatch between directory-based environment loading and the formats I already use. `direnv` is built around `.envrc`, while Docker Compose and VS Code use `.env`, as do `uv` and many Python projects.

It supports both formats on Windows, Linux, and macOS. Bash and zsh work with it, and so do fish and PowerShell.

I wrote it in Python because it runs on my machines, including Windows ARM64. Installation works with `uv` or `uvx`.

Start with the formats and machines you actually have. Copilot's browser-based Jumpstart feature produced the first version, and I continued with Claude Code.

I hadn't worked with shell hooks before, so the project also gave me a practical reason to learn them.

For `ssh-auto-forward`, the starting point was different. VS Code Remote SSH forwards ports conveniently, but my terminal workflow didn't.

The tool connects to a remote server and scans listening ports. It tries to reuse the same local port and resolves conflicts when that's impossible. Its dashboard shows active ports, process names, and logs. A command-line mode works without an interactive interface.

`nobook` addresses a format problem for interactive work. Jupyter notebooks are convenient, while `.ipynb` files are JSON and awkward to diff. AI tools therefore spend more effort looking at them.

Nobook keeps a normal Python file and marks cells with `# @block=name`. A Jupyter contents manager converts those blocks into notebook cells and converts them back when saving.

The command-line mode executes blocks and writes outputs as comments in `.out.py`. The resulting file remains valid Python.

Microphone Booster came from quiet USB-C microphones on Windows, especially Apple earbuds, and two early attempts weren't usable.

The third attempt rewrote the application around native Windows APIs. OpenCode with GLM-5 chose Rust, Tauri 2, and Svelte.

The goal was a focused tool for one Windows limitation, while learning enough about a new desktop stack to understand the result.

Bot Master handles a failure that's easy to miss. It runs Telegram bots under a background daemon, starts them through systemd so they survive reboots, and restarts crashed processes with exponential backoff.

A separate terminal interface displays status and streams logs. It sends start, stop, or restart commands, while the bots keep running if it disconnects.

Across all five projects, the workflow is the same: describe a specific behavior, look at the first implementation in real use, then correct what's missing. AI lowers the cost of trying an unfamiliar area, but the useful requirements still come from the workflow.
