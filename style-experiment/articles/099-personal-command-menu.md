# Creating a Personal Command Menu for Repeated Work

I wrote this synthetic style exercise as a build log, and the commands, numbers and file names in it are fictional. In February 2026 I counted 42 one-off scripts and aliases across my dotfiles, and I could name about 15 from memory.

The rest surfaced only when a task reminded me they existed, usually after I had already rebuilt the same thing by hand. Twice in January I rewrote a report script that I had written back in November. That was the trigger for a weekend project I now use about ten times a day.

In this post, I'll share:

- 42 scripts and a memory that held 15
- aliases and a notes file that both went stale
- a history scan that proposed command candidates
- how the menu file groups tasks
- defaults written next to the commands
- the menu today and its limits

## Forty Commands And A Bad Memory

My working day runs through a terminal, and repeated work collects scripts. Site deploys, database copies, and log tails live in `~/bin`, along with a dozen report generators. In February I counted them: 42 commands across four projects.

Being able to run a command starts with being able to name it. I could name about 15 from memory, and the rest surfaced only when a task reminded me they existed. Rewriting a script always felt faster than searching for one, which is how the collection kept growing.

## Two Systems That Went Stale

My first fix was aliases. I had collected about 30 of them in `.bashrc` over the years, and the list worked until it grew past one screen. An alias remembers nothing beyond the command name, so arguments, default hosts, and when-to-use notes stayed in my head.

A notes file called `commands.md` came next, a markdown list I started in 2025. It went stale within five weeks, because nothing updated it when a flag changed. I trusted it once, typed a command from it, and used a flag that no longer existed.

My mistake was keeping documentation that no command executes. The rule I took from it: the command list has to be the thing the terminal runs.

## Scanning History For Candidates

Before writing anything new, I wanted to know what I actually repeat. In late February I wrote `menu-scan`, a 60-line Python script that reads my shell history and proposes candidates.

The scan covers about 8,000 history lines, the 30 aliases, and the README files in `~/bin`.

It strips arguments, counts identical prefixes, and prints commands I ran more than five times in 90 days:

```bash
python menu_scan.py --history ~/.zsh_history --min-count 5
```

The scan proposed 27 candidates, and I kept 14 for the menu. Six proposals were one-off migrations that ran exactly once, which is the noise I wanted the count filter to remove. Rerunning the scan monthly gives me a number I now trust, namely how much of my terminal work is repeated work.

## Grouping Tasks In One Text File

The menu lives in `menu.txt`, a plain text file with a group per task area. Groups came before names, because my first version kept one flat list of 14 commands and I stopped opening it within two weeks. The rule I took from that failed draft: group first, then name.

Four groups cover the work at the moment:

- deploy, for building and pushing the static sites
- database, for dumps, restores, and copies
- writing, for drafts, word counts, and the newsletter
- ops, for log tails and disk checks

A 25-line bash script called `menu` prints the file with line numbers and executes the line you pick:

```bash
menu database
```

Typing a group name filters the list to that group, and pressing Enter runs the command. The interaction costs two keystrokes more than remembering the command, and it costs nothing when I forget it.

## Defaults Written Next To Commands

Each line in `menu.txt` documents its default arguments in plain text, on the same line as the command. The database group lists which of the 12 tables `db-copy` skips, and the deploy group names the VPS a push targets. Since the file is what executes, the documentation can't drift from the behavior.

In April the defaults caught a real mistake before it happened. `db-restore` defaults to the scratch database, and I nearly overrode it with the staging host. The comment line stopped me for the ten seconds that check needed. Writing a default next to its command takes seconds, and it removed a lookup step from every task.

## The Menu Today

Three months in, the menu holds 14 commands in four groups, and I run about ten menu calls a day. The scan runs monthly now, and it has proposed only two new commands since March. Total build time was two evenings, about three hours including the failed flat list. That failed draft stays in the git history of my dotfiles, where it reminds me that structure matters more than quantity.

Two limits stay open in the current setup. Commands that need per-run arguments don't fit the file format, so those stay as plain aliases. The menu can't chain commands either, so long jobs still run as small scripts.

I'll write about how I manage the dotfiles repo in a future post. If you want to follow along, don't forget to subscribe.
