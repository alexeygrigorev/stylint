# Five small tools that removed recurring annoyances

Over the last few months I built several small utilities with AI coding assistants, mostly Claude Code. None began as a large product idea. Each came from a problem that kept appearing in my daily work, and the existing workflow did not fit quite well enough.

The first was `dirdotenv`. I wanted environment variables to load when I entered a project directory, but I also wanted to keep using ordinary `.env` files. `direnv` uses `.envrc`, while Docker Compose, VS Code, `uv`, and many Python projects already use `.env`. I did not want another format. Because I work across Windows machines, including an ARM64 tablet, Python was a practical choice for a cross-platform tool. `dirdotenv` supports Windows, Linux, and macOS, as well as bash, zsh, fish, and PowerShell.

`ssh-auto-forward` came from remote development. My code and services run on a Hetzner server through VS Code Remote SSH. VS Code forwards ports, but I wanted an equivalent terminal workflow. The utility connects over SSH, finds listening ports, reuses the same local number when possible, and resolves conflicts. Its dashboard shows active ports, process names, and logs, while a command-line mode works without an interactive screen.

I built `nobook` because Jupyter notebooks create both technical and editorial friction. The `.ipynb` format is JSON, which makes it awkward to diff and less convenient for AI tools. Nobook keeps the source as a plain Python file and uses `# @block=name` markers to define cells. JupyterLab and IPython remain standard. A contents manager converts blocks to cells on load and back to Python on save. The command-line mode can run a file and write outputs as comments in `.out.py`, so examples stay testable and version-control friendly.

The Microphone Booster addressed a Windows hardware limitation. USB-C microphones, including Apple earbuds, were sometimes too quiet, and Windows did not offer the same useful boost controls. OpenCode with GLM-5 chose Rust, Tauri 2.0, and Svelte. The first two attempts missed the requirement or became too heavy. Rewriting the application on the third attempt produced a tool using native Windows APIs.

Finally, Bot Master solves an operational problem. I run several Telegram bots, and a crash could go unnoticed. The daemon starts through systemd, manages subprocesses, restarts failures with exponential backoff, and survives reboots. A separate terminal interface shows status, streams logs, and accepts start, stop, and restart commands. If the interface disconnects, the bots continue running.

The common pattern is simple: notice a repeated inconvenience, describe the behavior, let an assistant make a first version, then use it and correct what is missing. AI made it easier for me to explore shell hooks, SSH tunneling, notebook internals, native Windows APIs, and background daemons that I would probably have postponed otherwise.
