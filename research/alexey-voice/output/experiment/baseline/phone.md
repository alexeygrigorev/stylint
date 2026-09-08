I want my projects to keep progressing while I am traveling, taking my son to school, picking him up at 4 PM, or resting between gym sets. My earlier phone workflow used GitHub Copilot with GitHub Actions. It was useful for running a task remotely, but the environment went away when the task finished, so I could not keep it customized for myself.

Now I rent a dedicated Linux server that is available 24/7. It runs Claude Code, Codex, and OpenCode. From Android, I connect to it using the Termius SSH client. This gives me a place I can return to, but mobile SSH connections frequently disconnect while I am traveling. When I ran an agent directly in the SSH shell, losing the connection also meant losing the agent's process.

I solved that part with tmux, the Terminal Multiplexer. I run agents inside tmux sessions, which keeps their processes running across disconnects. When the connection returns, I reconnect and resume the session. The work remains accessible even when the phone connection does not.

Typing tmux commands on a phone is painful, especially when the session names are long, so I built `tmuxctl` to shorten them. The command `t` lists the sessions. The command `t 1` attaches to session 1. The command `t -` creates or attaches to a session named after the current directory. These shortcuts make the common actions manageable from a small keyboard.

For tasks that require more than a few typed characters, I use Makefiles. I can keep the longer commands there and invoke them with a short command from the phone. This setup is about keeping work accessible and reducing typing while I am away from my usual computer.
