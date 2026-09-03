# Treating Server Configuration as Reviewable Data

I wrote this synthetic style exercise as a how-to guide. The server, dates and numbers are fictional. In January 2026 I edited /etc/nginx/nginx.conf over ssh, restarted Nginx, and took my demo site down for 25 minutes.

The file had 180 lines, and I had changed two of them without a diff, a test or a backup copy. That evening I moved every server config file into a git repo and added a schema plus a small validator. Setup took about two hours, and the same flow has run before every change since.

In this post, I'll share:

- how I moved server config into a small git repo
- how a schema file describes every allowed value
- how validation and review work before a change ships
- how I roll back a bad change in one command
- which gaps six months of use exposed
- how the setup stands after those six months

## 1. Copy Config Into a Repo

I keep the repo at `~/server-config` on my laptop, and I push it to a private GitHub repo as a second copy. It holds 12 files, from the Nginx config to two systemd units and the crontab. The server runs Ubuntu 24.04 on a small VPS that costs 4.50 euros per month.

You can pull the files down with scp and start the repo with two commands:

```bash
scp user@203.0.113.10:/etc/nginx/nginx.conf nginx.conf
git init && git add nginx.conf && git commit -m "import current config"
```

The first commit stores the before picture of every later change. I repeated the copy for the other 11 files until the repo matched the server exactly. Two files stayed out on purpose: the TLS private keys and the database password file. Secrets live in a password manager, and the config files reference them by path.

My January mistake was editing the live file directly. The rule I took from it: the repo is the editable version, and the server only receives reviewed files.

## 2. Write a Schema Per File

Git shows which lines changed, and a schema shows which values are allowed. So I wrote confval, a small Python script that reads a schema file and checks each config value against a range.

The schema for Nginx has 14 lines:

```text
worker_processes: integer, 1 to 16
worker_connections: integer, 64 to 4096
client_max_body_size: size, 1M to 100M
```

Each line names one directive, a type and a safe range. The checker rejects values that parse fine and still break the server. A timeout of 5 seconds and a timeout of 5 milliseconds are both valid syntax, and only the range knows which one makes sense here. Writing the schema took about an hour, mostly spent rereading the Nginx docs for real limits.

Anything outside the schema passes unchecked, and that's the trade-off I accepted. For my 12 files, the schema covers the 30 or so values I actually touch.

## 3. Validate and Review Every Change

The check runs locally before any file moves toward the server:

```bash
uv run confval check nginx.conf schema-nginx.txt
```

The script prints one line per value outside its range and exits with a nonzero status. The same check also runs in a GitHub Actions workflow on every push, and a full pass takes under a second.

Every change goes through a pull request, even though I'm the only committer. The diff shows old and new values side by side, and the description must say why the value moves. In March the review caught a typo: I had typed 409 as 4096 for worker_connections, and the schema range made it obvious. The check also fails the CI run, so a push with a broken value can't reach the server silently.

## 4. Roll Back in One Command

A bad change now reverts with a checkout and a copy:

```bash
git checkout 4f2c1a9 -- nginx.conf
scp nginx.conf user@203.0.113.10:/etc/nginx/nginx.conf
```

The two lines take about 30 seconds, and the site stays up while the file copies. I rehearsed the rollback twice on purpose, in February and in April, so the steps wouldn't be new during a real incident. The rehearsal also exposed a permissions issue with the systemd unit that I would have hit under pressure. Rolling forward is the other option, and the diff plus the schema check make that safe enough most weeks.

## Caveats From Six Months of Use

The schema checks ranges, and ranges don't prove a config is sensible. A value of 12 for worker_processes passes on my 2-core VPS, even though 2 is the sensible value on that machine.

The validator also understands only three file formats, so anything exotic still needs eyes. Drift is the last gap: an edit on the server makes the repo stale, so I re-run the import diff once a month. The monthly diff found 2 drifted lines in May, both from a package upgrade that had rewritten a unit file.

## The Setup After Six Months

The repo has 19 commits, and the schema has flagged 5 real errors and about 4 false alarms. The flow turned a 25-minute outage into a 30-second revert, and it forces me to think about a value before I type it. It still can't catch a wrong-but-valid value, and it says nothing about the database's internal state.

I'll write about the monthly import diff in a future post. If you want to follow along, don't forget to subscribe.
