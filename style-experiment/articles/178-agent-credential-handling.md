# Keeping Credentials Away from Agent Logs

I wrote this synthetic style exercise as a how-to guide. The project, dates and numbers are fictional. On 3 December 2025 I found a live staging password in an agent session log inside a git repo.

The credential opened a Postgres staging database, and the coding agent had echoed an exported variable into its own transcript. I revoked the password within the hour and spent the next two weekends on the setup in this guide.

The setup has four parts, and it takes about half a day to apply to one machine.

In this post, I'll share:

- how I store secrets as references
- how session logs get masked
- how rotation works without a weekend of work
- how the audit file records who used what
- which caveats come with the setup
- what the setup looks like today

## 1. Store Secrets As References

An agent should see the name of a secret, and it should never see the value. I keep values in the system keyring and pass references like `STAGING_DB_PASSWORD` into prompts and config files.

A small wrapper script called `run-safe` loads the keyring entry at launch, so the working environment of the agent never sees the value.

The wrapper takes the project name and the command:

```bash
run-safe staging -- claude "refactor the invoice module"
```

The script reads `staging/db-password` from the keyring, exports it for the child process and scrubs the environment when the session ends. The agent works with `STAGING_DB_PASSWORD` as a name. If it prints the name into its transcript, the transcript holds nothing usable.

Config files follow the same rule, so `config/staging.env` in the repo lists names only. A repo-wide grep for credential values is part of my Friday review now, and it reuses the same matching rules as the mask filter.

## 2. Mask Secrets In Session Logs

References fail when a tool prints a value anyway, so the logs need a second layer. A filter called `log-mask` watches the session directory and rewrites anything that looks like a credential before the file is one minute old.

It catches three line types, and each type has a test file in the repo:

- assignments like PASSWORD=value on any line
- connection strings with a password before the @ sign
- long tokens that match a keyring value

Masking turns a leaked line into a safe one:

```text
before: connect=postgres://admin:Hunter2-2026@10.0.0.14/staging
after:  connect=postgres://admin:[MASKED:db-password]@10.0.0.14/staging
```

The filter keeps the last four characters visible, which is enough to tell two staging passwords apart. A full mask made rotation checks harder, so I traded a little exposure for that check. The first version of the filter ran once per hour, and a test session showed a value sitting in a log for 40 minutes. The watch loop now runs every 30 seconds, which is where the 60-second guarantee comes from.

## 3. Rotate On A Fixed Schedule

Rotation turns a leaked secret into a short problem instead of a permanent one. Every secret in the keyring has a set-date label, and a cron job prints anything older than 90 days on the 1st of each month.

The cron entry for the age report looks like this:

```bash
0 9 1 * * /home/dev/bin/key-ages.py --older-than 90d
```

The report arrives in the same Telegram chat as my other cron output. I rotate about four secrets per quarter now, and each rotation takes under ten minutes with the keyring CLI. One rotation means a keyring write on each machine that uses the secret, and my staging setup uses two.

## 4. Record Who Used What

The fourth piece answers a question that shows up after an incident. It records which agent touched which secret, and when. `run-safe` appends one line to `~/.local/secret-audit.log` for every launch. The line holds the date, the project, the secret name and the command.

The file is plain text. A leak drill in February used it, and one grep answered "which agents saw staging credentials this quarter" in 8 seconds.

That drill is now a quarterly habit. I plant a fake password in the keyring and ask an agent to print it. The mask filter and the audit file should both catch it within the minute.

## Caveats And Limits

The setup covers two machines and about 30 minutes per month of attention.

It has gaps I already know about:

- the mask filter reads after the agent writes, so a value can sit in a log for up to 60 seconds
- the audit log records projects, so it can't separate two people on one machine
- the keyring backup is a printed recovery sheet in a drawer

The 60-second window bothers me most. The fix, a file-watcher daemon, sits on the later list next to a hosted vault.

## My Setup Today

Four months after the December leak, the same four parts run on two machines. Session logs hold references and masked lines, rotation happens four times per quarter, and the audit file answered its first real question in February.

The biggest remaining cost is trust in the mask filter. It matches the three line types I taught it, and a fourth type would slip straight past, so the quarterly drill stays on the calendar.

I'll write about moving the staging secrets into a hosted vault in a future post. If you want to follow along, don't forget to subscribe.
