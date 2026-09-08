# Trying Claude Code Again



I want to describe what happened, because the sequence of small decisions is more useful than a polished summary. 

I chose Claude Code briefly half a year ago. I didn’t like the terminal experience and preferred to have

an AI assistant in my IDE. But recently a lot of people have been talking about Claude Code on social

media, so I decided to give it another try. it’s still Copilot, I actually enjoyed using it. Here and in

the next posts I’ll share with you what I did and what I learned. My Experiments: Claude Commands Claude

commands are /slash commands that you execute in Claude Code.

https://github.com/lout33/claudelifeassistant/tree/5dbef44d6f860bb7d477c4000b1ce88bc31464e0, “a personal

coach that lives in your filesystem”. I looked at the Quick Start and wondered, “What are these

commands?” So I decided to figure it out. Kid and Parent commands I discovered that these commands are

defined in a very simple way: you add a markdown file to the .claude/commands folder and describe what

the command should do, in plain text. Out of curiosity, I created a new project two commands: /kid and

/parent. https://raw.githubusercontent.com/alexeygrigorev/claude-code-kid-parent/refs/heads/main/.claude/

commands/kid.mdhttps://raw.githubusercontent.com/alexeygrigorev/claude-code-kid-parent/refs/heads/main/.c

laude/commands/parent.md takes that idea and implements it in HTML+JavaScript. Then the process repeats:

kid asks, parent builds. https://github.com/alexeygrigorev/claude-code-kid-parent with the code.

https://alexeygrigorev.com/claude-code-kid-parent/projects/judgy-crystal-ball.html. Other projects:

Invisible Pet Walker with awkwardness meters, a Sneeze Simulator with randomized power levels, a Garden

of Weird Plants with personalities, a Silly Symphony built on the Web Audio API, and a Robot Chef that

invents bizarre dishes. Ralph Wiggum: Running Claude Code Forever I asked Claude to run the /kid and

/parent commands forever. But it didn’t. After a few iterations, it stopped, so I had to ask it to

continue repeatedly. https://code.claude.com/docs/en/hookshttps://github.com/anthropics/claude-code/issue

s/11786issuecomment-3543716217. https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/

README.mdthe son of the police chief who’s “persistent despite setbacks”. It automatically prompts

Claude to continue when it stops. I haven’t checked the video though Use the /plugin command to install

it: /plugin install ralph-wiggum And now you run it: /ralph-wiggum:ralph-loop "prompt" I tested on

another project: a metabolism simulator. I want to know how metabolism in the human body works, so I

thought a simulator would help me understand this topic better. I gave it an initial prompt, asked it to

plan the app, and then activated the loop: https://github.com/anthropics/claude-code/blob/main/plugins/ra

lph-wiggum/hooks/hooks.jsonL9without prefixing it with “bash”, and it wouldn’t execute properly on

Windows. Claude saying that the Ralph loop will continue - but it’s not doing anything But if you’re on

Mac or Linux - it should work. My Own Ralph with Python But I thought “what if I implemented it with

Python?” Nano Banana made Ralph pet a python And it worked! Steps: Create a stop hook in

.claude/settings.json with type command and command python .claude/continue-hook.py Add continue-hook.py

and continue.md to the .claude folder If you want to stop the loop, remove or rename continue.md

https://github.com/alexeygrigorev/metabolism-simulator/tree/master/.claude. Another problem: Claude Code

sometimes fails and exits with an error. I don’t know why it happens. Claude Code exiting with error

after almost 6 hours of non-stop working https://github.com/alexeygrigorev/metabolism-simulator/blob/mast

er/continue.shuntil my Windows decides to install an update and reboot. After a few days it created a

nice-looking website with a lot of features. Not everything worked but I’m sure it’s fixable. Here’s

what it created: It’s a fun idea, but I wouldn’t let it run loose on any



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
