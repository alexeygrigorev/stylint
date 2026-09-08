# Five small tools that removed recurring annoyances

Over several months I built small utilities with AI coding assistants, mostly Claude Code. They came from problems in my daily workflow rather than from a large product plan. Existing tools were close, but they didn't fit the way I worked.

`dirdotenv` loads environment variables when I enter a project directory while keeping ordinary `.env` files. It also supports `.envrc`, the format used by `direnv`. The other tools I use already read `.env` files.

I didn't want another format. I work across Windows machines, including an ARM64 tablet, so Python was a practical choice. It supports Windows, Linux, and macOS. It also supports bash, zsh, fish, and PowerShell.

My code and services run on a Hetzner server through VS Code Remote SSH. I wanted the same port-forwarding behavior from a terminal, so I built `ssh-auto-forward`. The utility connects over SSH and finds listening ports, then reuses the local number when possible and resolves conflicts. Its dashboard shows active ports and process names, logs, and a command-line mode that works without the dashboard.

I built `nobook` because Jupyter notebooks create technical and editorial friction. An `.ipynb` file is JSON, which makes diffs awkward and gives AI tools a less convenient source format. Nobook keeps Python as the source and uses `# @block=name` markers for cells.

A contents manager converts blocks to notebook cells on load and back to Python on save. Its command-line mode can write outputs as comments in `.out.py`, keeping examples testable and friendly to version control.

The Microphone Booster addressed a Windows limitation. USB-C microphones, including Apple earbuds, were sometimes too quiet, and Windows didn't expose the same useful boost controls. OpenCode with GLM-5 chose Rust, Tauri 2.0, and Svelte. The first two attempts missed the requirement or became too heavy. The third rewrite used native Windows APIs.

Bot Master manages several Telegram bots, so a crash doesn't go unnoticed. The daemon starts through systemd, manages subprocesses, restarts failures with exponential backoff, and survives reboots.

A separate terminal interface shows status and streams logs, and it accepts start, stop, and restart commands. If that interface disconnects, the bots keep running.

The common approach was to notice a repeated inconvenience, describe the desired behavior, try a first version, and correct what was missing. AI made it easier to explore shell hooks and SSH tunneling. It also helped with notebook internals and native Windows APIs.

Background daemons were another area I would probably have postponed.
