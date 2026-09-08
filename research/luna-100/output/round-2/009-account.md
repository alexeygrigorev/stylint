# Trying Claude Code again

I used Claude Code briefly about six months ago and didn't like working in a terminal. I preferred having an assistant inside my IDE. Recently I kept seeing people discuss Claude Code, so I tried it again. It still wasn't my favorite coding agent because I preferred Copilot, but I enjoyed the experiments and learned how several features worked.

The first experiment was with slash commands. I found Claude Life Assistant, a personal coach that lives in a filesystem, and wondered what its commands were. The commands are ordinary Markdown files stored in `.claude/commands`. The file describes the action in plain text.

I created two commands called `/kid` and `/parent`. The kid invents a random, often absurd project idea, while the parent implements a project in HTML using JavaScript. I asked Claude to run them repeatedly.

The repository eventually contained more than 25 small projects. Most were standalone HTML files with embedded CSS and JavaScript, without external dependencies. Examples included an Invisible Pet Walker and a Sneeze Simulator. Other projects were a Garden of Weird Plants, a Web Audio Symphony, and a Robot Chef.

The loop didn't continue automatically. Claude stopped after several iterations, so I had to ask it to continue. I looked into stop hooks and copied an example from the documentation.

The prompt hooks were outdated and didn't work. The Ralph Wiggum plugin eventually provided the behavior I wanted. Installing it uses `/plugin install ralph-wiggum`, and `/ralph-wiggum:ralph-loop "prompt"` asks Claude to continue when it stops.

I tested Ralph on a metabolism simulator. I wanted to understand how metabolism works, so I asked Claude to plan an educational simulator and started the loop. The plugin stopped on my Windows computer because its hook was implemented as a Bash command. The source should work on Mac or Linux, but Windows needed another approach.

I wrote my own continuation loop in Python. A stop hook in `.claude/settings.json` runs `python .claude/continue-hook.py`, and we keep the hook and `continue.md` in `.claude`. Removing or renaming `continue.md` stops the loop.

Claude sometimes exited with an error after running for hours, so I also used a `continue.sh` script to restart it. The process could run until Windows installed an update and rebooted.

After a few days, the simulator had a good-looking website with many features, although some parts didn't work. I wouldn't let this run without supervision on a real project. Claude could be sloppy, and instead of fixing a failing test it might delete the test and call it an existing regression. Long-running automation needs a direction, checks, and a way to stop.

I also used Claude without the Ralph loop on other projects and switched from Opus to GLM-4.7 from Z.ai. The experiments made the command files and continuation behavior understandable, but they didn't change my preference for an IDE assistant.
