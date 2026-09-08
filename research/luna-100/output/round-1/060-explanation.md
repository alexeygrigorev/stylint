# A workable phone interface for coding agents

Phone-based development is possible when the expensive work stays on a persistent remote machine and the phone handles communication. The useful pieces are not one application but a chain: server, SSH, session persistence, short commands, voice input, port forwarding, and small interfaces for visual decisions.

Use a dedicated Linux server when a task must continue after the phone disconnects. An ephemeral GitHub Actions runner can execute work, but it disappears when the task finishes. A permanent server lets Claude Code, Codex, and OpenCode keep their environment. Termius provides the Android SSH connection.

SSH alone is not enough for travel. Network changes terminate shells, so run agents inside tmux. The multiplexer keeps processes alive and lets you reconnect later. Since commands such as `tmux attach -t long-session-name` are uncomfortable on a phone, a small wrapper can expose shorter operations. In this setup, `t` lists sessions, `t 1` attaches to one, and `t -` uses the current folder as a session name. Makefiles provide similar shortcuts for longer commands.

The same principle applies to agent startup. Short aliases launch Claude, Codex, or OpenCode in a few keystrokes. This convenience should sit inside an isolated environment. The remote machine has no production access, AWS uses a sandbox account with a temporary one-hour session, and deployments go through CI. Isolation makes fast commands recoverable because the machine can be rebuilt.

Development servers create a networking problem. A phone browser cannot see a port on the remote server unless it is forwarded. Automatic forwarding is better than manually entering every port. The Android version of ssh-auto-forward monitors remote ports and displays rows that open the corresponding localhost page.

Voice avoids the smallest keyboard in the system. Typeless turns speech into cleaned-up text for the terminal. Built-in Android dictation is a fallback when the free service limit is reached. Google Recorder handles longer instructions: record offline, share a link, let an agent fetch and transcribe it, and use the result as a task description.

Visual review needs a different interface. If a phone cannot conveniently compare screenshots or designs, ask an agent to build a temporary HTML picker. The picker can show variants, capture like or reject decisions, and export comments. That disposable tool is often cheaper than postponing the decision until a laptop is available.

The resulting workflow is suited to short intervals. Capture ideas by voice, keep the agent alive in tmux, inspect previews through forwarded ports, and use small review pages for visual work. The phone is the control surface; the server performs the long-running work. That boundary is what makes commuting, school runs, gym breaks, and travel usable for development.

The setup also keeps each inconvenience local. Disconnects are handled by tmux, long commands by aliases and Makefiles, speech by transcription, and visual review by a temporary page. The pieces work together because each one addresses a specific limit of the phone.
