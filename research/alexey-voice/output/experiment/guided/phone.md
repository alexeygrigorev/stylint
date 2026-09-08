I want projects to progress during travel, school runs and the periods between gym sets. I take my son to school and pick him up at 4 PM, so having work available in short gaps matters to me.

My earlier phone workflow used GitHub Copilot with GitHub Actions. The remote environment went away when the task finished, so I could not keep it customized for myself. Now I rent a dedicated Linux server that is available 24/7. It runs Claude Code, Codex and OpenCode, and I connect to it from Android using the Termius SSH client.

There is one practical problem with this setup. Mobile SSH connections frequently disconnect while I am traveling. When I ran an agent directly in the SSH shell, losing the connection also meant losing its process. I now run agents in tmux sessions. Tmux, or Terminal Multiplexer, keeps the processes running across disconnects. I can reconnect and resume the session afterward.

Typing tmux commands and long session names on a phone is painful, so I built tmuxctl to shorten them. The command `t` lists sessions. `t 1` attaches to session 1. `t -` creates or attaches to a session named after the current directory.

For tasks that require more than a few typed characters, I use Makefiles. This setup is about keeping work accessible and reducing typing from a phone. It does not cover deployment permissions, port forwarding or voice transcription.
