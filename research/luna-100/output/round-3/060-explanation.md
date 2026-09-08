# Working with remote agents during short breaks

I use my phone to communicate with coding agents that run on a dedicated Linux server. That gives me a permanent environment I can customize, unlike the GitHub Actions environment that disappeared after each Copilot task.

I connect through Termius on Android and run Claude Code, Codex, and OpenCode inside tmux. The connection can drop while I'm travelling without stopping the agent's work. I reconnect and return to the session when the network is available again.

Long terminal commands are difficult to type on a phone, so I use tmuxctl for session management. The `t` command lists sessions, and `t 1` attaches to the first one. With `t -`, I create or attach to a session named after the current folder.

For other long commands, I use Makefiles to reduce the number of keystrokes. I also launch agents through aliases, using `csp` for Claude with skipped permissions and `cy` for Codex in YOLO mode. OpenCode has the `oc` alias.

I use those shortcuts on a remote machine without production access. AWS access is limited to a sandbox account through a temporary one-hour session. Real deployments go through CI, and I can rebuild the server from my bootstrap scripts.

For previews, I need access to the ports agents open on the server. Configuring each port manually in an Android SSH client interrupted the work, so I asked an agent to port my Python ssh-auto-forward tool to Android.

The Kotlin application detects remote ports and forwards them. I tap Connect to see the list, then tap a port to open the corresponding localhost page in my browser.

Typing prompts is still awkward even with short commands. I use Typeless to turn dictation into cleaned-up terminal input. When its free quota runs out, I use Android's built-in voice recognition, which produces messier text but usually gets the instructions across.

For a longer explanation, I record in Google Recorder and share the link with an agent. It uses a skill to download and transcribe the recording, then works from those instructions.

On a plane, I can review code or run the project on my laptop while recording feedback offline on my phone. I send the recording to the agents after the flight.

Visual decisions need a different interface. For 30 banner variants, Codex built a temporary HTML page where I could mark preferences and add comments. I reviewed them in five minutes, exported the choices, and sent the file back to the agent.

For articles, I send voice notes and other material to the Telegram writing assistant, then use `/process` to create a draft. I record feedback with Google Recorder while commuting or between gym sets. Valeriia does an editing pass, we review the article together, and she finishes it.
