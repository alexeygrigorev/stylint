# Building a Minimal Time Tracking Tool I Actually Use

I have tried at least seven time tracking systems since 2019. Three were spreadsheets, two were commercial apps and two were CLI tools. Every system lasted between two and five weeks. The reason was always the same: recording time felt like another job.

This synthetic style exercise describes a fictional tool called "seven", a small time tracker I designed around one command. It stores events in SQLite, shows a weekly summary and refuses to become a project management system.

In this post, I'll share:

- why the previous trackers failed
- how the one-command interface works
- what the local storage contains
- how the weekly report is built
- what still doesn't work

## The Failed Trackers

The spreadsheet required me to reconstruct the day at 6 p.m. I usually forgot lunch breaks, small debugging sessions and context switches. After two weeks, the sheet contained confident-looking rows with wrong numbers.

The commercial apps were better at reminders, but they wanted a project, client and tag for every entry. That classification work was useful for an agency. I work on courses, articles and a few personal systems, so I needed a different tradeoff.

The CLI tools came closer. One had a beautiful terminal chart and a config file with 180 lines. I stopped using it when I couldn't remember whether "resume" resumed the previous task or opened an editor. Another stored time in JSON files, but its start command asked for a category.

The rule I took from those attempts: the tracker has to capture one fact in less time than I spend deciding whether to capture it.

## One Command

The entire interface uses one command named `seven`.

Running it records the current time and the shell's working directory:

```bash
seven
```

I run that command when I switch work, and it reads the project from the current directory. If I'm in `~/code/course Exercises`, I don't type a project name because the directory already identifies the location. If I'm in `~/writing/newsletter`, the report calls the work "newsletter".

For a task that spans two directories, I can pass one optional label:

```bash
seven --label "course launch"
```

That label overrides the directory for the event, and there's no stop command. When I run `seven` again, the previous event ends and the new one begins. The tracker doesn't try to know whether I spent the intervening 20 minutes on the task.

## Local Storage

The tracker writes to `~/.local/share/seven/events.db` with SQLite. I chose SQLite because it's a single file, I can query it directly, and I've used it often enough to review the SQL.

The schema has one table:

```text
events
  id INTEGER PRIMARY KEY
  started_at TEXT
  ended_at TEXT
  directory TEXT
  label TEXT
```

The first event of a day gets `started_at` but no `ended_at` until I run the next command. If I shut the laptop at 18:40, that event remains open. The weekly report treats an open event as ending at its next event, or leaves it out after 14 hours.

This design misses breaks and distractions: a 45-minute event may include coffee, a phone call and 12 minutes of actual work. I accept that error because I use the report to find blocks of attention, while a billing system would need exact task durations.

## The Weekly Report

The `week` subcommand prints a summary for Monday through Sunday:

```bash
seven week
```

It groups events by the final path component, combines labels with directories and rounds each group to five minutes.

A typical fictional week shows the result:

```text
course Exercises   9h 55m
newsletter         4h 15m
seven              2h 40m
course launch      1h 20m
admin              0h 45m
```

The directory `~/code/course Exercises` produced the awkward two-word name. I left it in the output because it reminds me to stop renaming projects. Renaming directories for a report would turn the tracker back into an administrative task.

The report also prints the number of events per group. "seven" often has 34 short events during a busy development week, while "admin" has four. That count helps me distinguish sustained work from scattered interruptions.

The report changed one decision in the fictional project. For three weeks, "course Exercises" had 12 hours while "newsletter" had only 95 minutes. I had planned to write two articles during that period, so I moved the writing block to Tuesday morning and protected it on my calendar. The next week, "newsletter" reached three hours and 20 minutes.

I also stopped pretending that Friday afternoon was suitable for course development. The report showed only 35 minutes of course work across four Fridays, with most of that time spent on setup. I now use Friday afternoons for admin and short reviews.

## Maintenance And Limits

The tool is 290 lines of Python. It uses the standard library, SQLite and Rich for terminal tables. I don't run a background daemon, sync service or mobile client because `restic` already copies my home directory every night.

The known limitations are clear:

- a forgotten command leaves an open event
- two overlapping sessions are impossible
- the report can't distinguish deep work from waiting
- directory names become categories

Forgotten commands remain the largest gap. On three fictional days in May, I switched work at a whiteboard and recorded nothing until lunch. The report showed a six-hour gap, which was closer to the truth than a guessed entry would have been.

## Daily Use And Limits

After eight fictional weeks, I still run `seven` several times each day. The weekly report is accurate enough to decide whether a project got real attention, even though it's useless for billing and doesn't measure productivity.

That limitation is deliberate: the tool replaces a weekly reconstruction with a sequence of timestamps. It gives me a map of attention blocks, and it costs less than one second per switch.

My next small change is a "review" command that shows days with fewer than three events. I don't want reminders while I work, but I do want a gentle check when I forget the system.

I'll describe the report queries in more detail in a future newsletter. If you want to follow along, don't forget to subscribe.
