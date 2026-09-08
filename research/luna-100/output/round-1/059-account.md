# Building while moving between places

I have been traveling through conferences and family trips while continuing to work. Recently that meant Darmstadt, Amsterdam, Porto, Easter travel, a long weekend in Germany, and Stuttgart and the Schwarzwald. My daily schedule has the same gaps: taking my son to school, the gym, lunch meetings, and picking him up at four. I wanted to use the train, bus, gym rest periods, and even plane time to keep projects moving.

The setup starts with a dedicated Linux server that stays available around the clock. Earlier, GitHub Actions gave me a remote environment for Copilot tasks, but it disappeared after each task. Now Claude Code, Codex, and OpenCode run on the server, and I connect from Android with Termius.

Travel means the connection will drop. An agent running directly in an SSH shell dies when that happens, so I run everything in tmux. Reconnecting returns me to the same process. Typing ordinary tmux commands on a phone is awkward, which led me to build tmuxctl. `t` lists sessions, `t 1` attaches by index, and `t -` creates or attaches to a session named after the current folder. Makefiles handle commands that are still too long for a thumb keyboard.

Agent launch commands also became short aliases: `csp` for Claude with skipped permissions, `cy` for Codex in YOLO mode, and `oc` for OpenCode. The machine is isolated, with no production access. AWS access uses a sandbox account and a temporary one-hour session, while real deployments happen through CI. If something destructive happens, I can rebuild the server from bootstrap scripts.

Remote ports need their own solution. Agents start development servers and previews, but Android SSH clients require manual forwarding. I handed the Python logic from ssh-auto-forward to an agent and asked it to build a Kotlin Android version. I can tap Connect, see forwarded ports, and open a browser on localhost. I understand Kotlin enough to recognize the stack, but I use the app because it performs the needed job.

Typing prompts was still painful, so voice became the main interface. Typeless turns dictation into structured terminal input. When its free usage limit is reached, I use Android recognition. For longer thoughts I record in Google Recorder, share a link, and let the agent download and transcribe it. Recorder also works offline on planes.

Visual work needs another trick. To review 30 AI Shipping Labs banner variants, I asked Codex to create a temporary HTML picker. I marked like, neutral, or reject and added comments from my phone, then exported the choices. The review took five minutes. Writing works similarly through the Telegram assistant: voice notes become a draft, Google Recorder feedback supplies revisions, and Valeriia edits the result. An article can take four to five hours instead of days.
