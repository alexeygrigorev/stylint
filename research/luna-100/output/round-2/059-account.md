# Keeping projects moving from my phone

I've recently been to conferences in Darmstadt, Amsterdam, and Porto, alongside trips with my child. My normal week also has school runs and gym visits, with short gaps between them. I want to use that time to keep my projects moving, including the AI Shipping Labs site.

I previously used GitHub Copilot through GitHub Actions. It gave me a remote environment, but that environment disappeared when the task ended. I wanted a permanent setup I could customize, so I rented a dedicated Linux server.

Claude Code, Codex, and OpenCode run there. I connect from Android using Termius and keep the agents inside tmux sessions. When the connection drops during travel, the work continues and I can reconnect to the same session.

Typing long tmux commands from a phone was painful, so I built tmuxctl.

The shortcuts cover the actions I use most:

- `t` lists the sessions
- `t 1` attaches to session number one
- `t -` creates or attaches to a session named after the current folder

I put longer commands in Makefiles. Agent launch commands have aliases too, including `csp` for Claude with skipped permissions and `cy` for Codex in YOLO mode. I use `oc` for OpenCode.

That machine has no access to production. Agents can reach a sandbox AWS account through a temporary one-hour session, while real deployments run through CI. I can rebuild the remote environment from bootstrap scripts if it breaks.

Previewing a server from the phone introduced another problem. Android SSH clients made me configure forwarded ports manually whenever an agent started something new.

I already had a Python tool called ssh-auto-forward on my laptop. I gave its source to an agent and asked for an Android version, which it built in Kotlin. I open the app and tap Connect, then select a forwarded port to open localhost in the browser.

I understand a little Kotlin because I used to work with Java, but I don't plan to read this application's code. It does what I need, just as the Python version does.

For prompts, I mostly dictate through Typeless. It cleans up what I say and inserts the text into the terminal. When I hit the free usage limit, I fall back to Android's voice recognition. The input is messier, but the agents usually understand me.

Longer instructions go into Google Recorder. I share a link with the agent, which downloads and transcribes the recording. Recorder works offline too, so on planes I can review code on my laptop and dictate feedback to share after the flight.

For visual work, I ask agents for small review tools. Codex built an HTML picker for 30 banner variants so I could choose and comment from my phone. I exported the selections and sent them back to the agent, finishing the review in five minutes.

I used the Telegram writing assistant for this article too. The initial notes took about 40 minutes during my trip to the gym. I recorded another 30 to 40 minutes of feedback between sets and on the way home.

Valeriia then does the initial edit, we review it together, and she finishes the article. We complete it in four to five hours instead of the days it used to take me to sit down and write.
