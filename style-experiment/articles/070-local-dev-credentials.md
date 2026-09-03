# Managing Local Credentials Without Spreading Dotfiles Everywhere

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional. In March I counted the credential files on my laptop, and 11 repositories held 14 copies of the same API key.

Three of those copies were expired, and two belonged to a revoked test account. One sat in a shell history file from a January debugging session. Nobody knew which copy was current, so every new checkout added one more.

In this post, I'll share:

- how the copies multiplied across repos
- how I built one loader for all projects
- how I scoped each secret to its project
- how I redacted secrets from logs
- where the credential setup stands today

## Fourteen Copies Of One Key

The March count started as a ten-minute cleanup and turned into an inventory exercise. I searched home directories for files named `.env` and found 23 matches across personal and client projects.

Fourteen of those files held variants of one analytics API key. The values differed by creation date, and the newest copy lived in the repo I touched least. I had pasted it there during onboarding and never rotated the older ones.

The rule I took from March is simple. I keep one loader that reads from one vault directory, and no project stores a secret in its own files.

## The First Version

My first attempt was a shared shell script that exported variables from a central file. I sourced it from `.bashrc`, and every terminal inherited 30 variables for all projects in one go.

That approach leaked across project boundaries within a week. A staging script read a production key because both lived in the same environment. A dry run then sent 200 test events to the live analytics pipeline.

Global exports ignore project scope by construction. Every process sees every secret, and a wrong default in one script spends real money in another account.

I deleted the global script after that incident. The terminals went back to empty environments while I built a loader that respects project directories.

## One Loader For All Projects

I replaced it with `credload`, a small Python tool that runs at the project root. It reads the current directory name, loads only that project's secrets, and prints the export commands for copy-paste.

The loader runs as one command:

```bash
credload --project billfetch
```

That command reads `~/.vault/billfetch.env`, validates the 12 expected names, and prints shell exports to stdout. I review the names before evaluating the output in the current terminal.

Nothing persists between terminals unless I ask for it. Each new shell starts clean, and I load exactly one project scope per working session. That default took a week to get used to, and it has prevented two near-misses since April.

## Scoped Secrets Per Project

The vault directory holds one file per project, and each file defines only the variables that project needs. The `billfetch` file defines 12 names, and the newsletter file defines seven. No name appears with a value in two files.

The vault layout stays flat and explicit:

```text
~/.vault/billfetch.env
~/.vault/newsletter.env
~/.vault/client-acme.env
```

I back up that directory with an encrypted archive monthly. The archive lives on an external drive, and the encryption passphrase lives on paper in a drawer.

Rotation now touches exactly one file per project. When the analytics key rotated in May, I updated one line in one vault file. All three checkouts picked it up on the next load. The old global script would have required hunting down every copy first.

## Redacted Logs From Day One

I load exactly one project scope per terminal, which stops cross-project leaks. A logging filter masks secret values before they reach disk, which stops accidental exposure. Every project logs API calls during development, and raw logs used to include full bearer tokens.

I added a logging filter that replaces secret values before they reach disk. The filter loads the same 12 names from the vault file and masks each value wherever it appears.

The filter code fits in 40 lines:

```python
def redact(text, secrets):
    for value in secrets.values():
        text = text.replace(value, "***")
    return text
```

I call that filter in the shared HTTP helper every project imports. Since May the debug logs have contained zero raw tokens across roughly 300 recorded sessions.

One habit supports the filter. I never print secrets to the terminal during debugging, and I grep new log files for key prefixes before attaching them to any issue.

## Three Checkouts, One Key

The May rotation proved the design. I changed the analytics key in the vault at 9 AM, reloaded it in three terminals, and every checkout used the fresh value before lunch.

Total credential files on the laptop dropped from 23 to zero tracked secrets. The vault holds five project files, and no repo contains anything beyond variable names and safe defaults.

New machine setup takes 20 minutes now. I copy the encrypted archive, decrypt it into `~/.vault`, install `credload` from a gist, and each project loads on first use.

The setup works because scope is structural rather than disciplined. I don't rely on remembering which terminal holds which keys, since each terminal holds exactly one project.

I'll cover the vault backup routine in a future post. If you want to follow along, don't forget to subscribe.
