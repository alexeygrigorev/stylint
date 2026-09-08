# Assignment

Write a 250–400 word newsletter excerpt in Alexey's first person, explaining the remote setup and session shortcuts for working from a phone. Use only the facts below. This is a reconstruction of an archived account, not a new event. Do not add a subscribe line or a general introduction to AI. Headings are optional. Output only the article excerpt.

# Fact ledger

- P1: Alexey wants projects to progress during travel, school runs and rest periods between gym sets. He takes his son to school and picks him up at 4 PM.
- P2: His earlier phone workflow used GitHub Copilot with GitHub Actions. The remote environment went away when the task finished, so he could not keep it customized for himself.
- P3: He now rents a dedicated Linux server available 24/7, running Claude Code, Codex and OpenCode.
- P4: He connects from Android using the Termius SSH client.
- P5: Mobile SSH connections frequently disconnect while traveling. In his account, running an agent directly in the SSH shell meant losing its process when the connection dropped.
- P6: He runs agents in tmux (Terminal Multiplexer) sessions to keep processes running across disconnects, then reconnects and resumes.
- P7: Typing tmux commands and long session names on a phone is painful. He built tmuxctl to shorten them.
- P8: The command t lists sessions; t 1 attaches to session 1; t - creates or attaches to a session named after the current directory.
- P9: He uses Makefiles for tasks requiring more than a few typed characters.
- P10: This excerpt is only about keeping work accessible and reducing typing. It does not cover deployment permissions, port forwarding or voice transcription.

# Required content

Preserve P1 through P8, including why he changed the setup. P9 is optional. Preserve exact command behavior. Do not add prices, measured productivity gains, guarantees about security or reliability, new travel incidents or promises that the setup works for everyone.
