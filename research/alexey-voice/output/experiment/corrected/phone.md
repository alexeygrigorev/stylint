I want my projects to keep moving while I'm traveling or taking my son to school. I pick him up at 4 PM, and I also have short breaks between sets at the gym. I want to use some of that time to work from my phone.

I used to do this with GitHub Copilot and GitHub Actions. The remote environment went away when the task finished, so I couldn't keep it customized for myself.

Now I rent a dedicated Linux server available 24/7, with Claude Code, Codex and OpenCode running there. I connect to it from Android using Termius, an SSH client.

But SSH connections from a phone drop often when I'm traveling. When I ran an agent directly in the SSH shell, I lost its process along with the connection.

So I run the agents inside tmux sessions. Tmux stands for Terminal Multiplexer, and I use it to keep the processes running when the phone disconnects. I reconnect and continue the same session without restarting the agent.

Once I started using tmux, I had to type its commands and long session names on the phone. That was painful, so I built `tmuxctl` to make the commands shorter.

These are the commands I use:

- `t` lists the sessions
- `t 1` attaches to session 1
- `t -` creates or attaches to a session named after the current directory

I also use Makefiles for tasks that require more than a few typed characters. I keep the longer commands there so I can run them from the phone without typing the whole command each time.
