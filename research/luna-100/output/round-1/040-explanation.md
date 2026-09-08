# A practical pattern for building personal utilities

Small utilities are often useful precisely because they fit one person’s workflow. The starting point is usually a recurring inconvenience: a format does not match, a command requires too much setup, or an existing tool assumes a different environment. AI coding assistants make it easier to explore these ideas, but the workflow still needs a clear requirement and real testing.

Take environment variables. `direnv` loads them by directory, but it expects `.envrc`. If the rest of your tools use `.env`, adding another format creates needless friction. A small alternative can support `.env` and `.envrc`, choose a portable implementation, and expose the shells you actually use. In my case, `dirdotenv` uses Python because it runs across Windows, Linux, and macOS, including several Windows machines. It supports bash, zsh, fish, and PowerShell, and can run through `uv` or `uvx`.

The same reasoning applies to remote development. If an editor forwards remote ports automatically but terminal work does not, build around the missing behavior. `ssh-auto-forward` connects to a remote machine, finds listening services, and tries to reuse local port numbers. When there is a conflict, it resolves it and shows the process and logs. A dashboard helps during interactive work, while a CLI mode supports scripts.

For notebooks, separate the interactive interface from the storage format. Nobook keeps ordinary Python files with block markers and lets standard JupyterLab present them as cells. The contents manager translates on load and save. This gives interactive execution while preserving readable diffs and files that can be tested like normal code. A command-line runner writes outputs as comments, keeping the result valid Python.

Hardware problems may require a different kind of iteration. The Microphone Booster exists because USB-C microphones can be quiet on Windows and the normal boost controls are not sufficient. The first two generated implementations were not usable. The requirement had to stay specific: solve the microphone problem, rather than grow into a generic audio application. The third attempt used native Windows APIs with Rust, Tauri, and Svelte.

Operational utilities benefit from separating supervision from control. Bot Master uses a background daemon to run Telegram bots, restart crashes with exponential backoff, and survive reboots through systemd. A separate text interface displays status and logs and sends commands. If the interface fails, the daemon continues to manage the processes. That boundary protects the main responsibility from an optional monitoring tool.

For this kind of project, the steps are straightforward:

1. Describe the repeated problem and the behavior you want.
2. Ask an assistant for a small first implementation.
3. Use it in the actual workflow.
4. Record the cases it misses and revise the design.

The assistant lowers the cost of entering unfamiliar areas, but it does not remove the need to check behavior. A tool becomes useful when it removes the original interruption and remains small enough to adapt when the workflow changes.
