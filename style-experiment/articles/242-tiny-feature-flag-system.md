# A Tiny Feature Flag System for Side Projects

I wrote this piece as a synthetic style exercise, so I invented every project name and number in it. Last March I maintained 16 small side projects and 9 of them used feature flags in some form. The flags lived in environment variables, config files, and one memorable hardcoded boolean named final2.

Each project had started with a single toggle for a half-ready page. Over six months the toggles multiplied into 23 flags across the 9 projects. I could no longer tell which flags guarded live behavior and which ones guarded code I had deleted in January.

The worst case sat in a URL shortener I run for friends. It held 6 flags, and 4 of them referenced endpoints that no longer existed.

In this post, I'll share:

- why plain environment variables stopped working for my flags
- how I name keys and choose default values
- how per-user overrides work without a dashboard
- how a cleanup pass removed 11 dead flags
- what the setup costs and where it still falls short

## Scattered Boolean Checks

Every project stored flags in a slightly different place. One FastAPI app read booleans from environment variables at startup. A Django side project kept them in settings with comments from October. A static site used a JSON file that I edited by hand.

None of these choices were wrong alone, and the trouble came from the spread across deploys. I once enabled an export page in staging and spent 40 minutes learning that production read a different variable name.

I counted the damage on a Saturday morning. The 9 projects held 23 flags, and my notes described only 14 of them. The rest had no owner, no date, and no comment.

That count forced a decision I had delayed for months. I needed one small system that fit every project without adding a service to maintain.

## The First Central Attempt

I first copied a shared Python module into each repo. I used it to read a flags dict from a YAML file through one is_enabled function. I wrote those 47 lines in one evening and felt good about the reuse.

The shared copy broke within three weeks. Two projects needed different defaults for the same flag name, and the module had no answer for that case. I patched it with an override argument, and the call sites turned into nested conditionals again.

I deleted the module from 7 of the 9 projects in April. The rule I took from that attempt: a shared helper must allow local differences, or every caller works around it within weeks.

## Key Names and Default Values

The convention starts with key names that state their own context. Each key has three parts joined by dots, starting with the project nickname. A key looks like shortener.export_csv, and the file groups keys by project without extra nesting.

I keep a short doc that records the naming rules:

```text
shortener.export_csv = false
shortener.retention_days = 30
dashboard.weekly_email = true
dashboard.max_rows = 200
```

Every key ships with a default value in code, so a missing entry never crashes a deploy. The default always selects the safer behavior, so new code paths stay off. A missing key once enabled an unfinished billing page for 11 hours.

Booleans stay booleans and numbers stay numbers. I stopped encoding three-state logic into strings after one flag cycled through on, off, and soon. Two boolean flags replaced it within a day.

## Overrides Without a Dashboard

Overrides live in a single local file that never reaches git. Each project reads flags.local.json at startup and falls back to defaults when the file is missing. The local file holds my testing overrides and nothing else.

Production overrides come from environment variables with a fixed prefix. The loader uppercases the key, replaces dots with underscores, and prepends FLAGS for the lookup. The variable FLAGS_SHORTENER_EXPORT_CSV overrides shortener.export_csv, and an empty variable counts as unset rather than false.

The loader fits in one small module:

```python
import json
import os

DEFAULTS = {
    "shortener.export_csv": False,
    "dashboard.weekly_email": True,
}

def is_enabled(key):
    env_name = "FLAGS_" + key.upper().replace(".", "_")
    raw = os.environ.get(env_name, "").strip().lower()
    if raw in ("1", "true", "yes"):
        return True
    if raw in ("0", "false", "no"):
        return False
    try:
        with open("flags.local.json") as handle:
            local = json.load(handle)
    except FileNotFoundError:
        local = {}
    return bool(local.get(key, DEFAULTS.get(key, False)))
```

I now run that module in all 9 projects, with only the DEFAULTS dict changed per repo. The per-project copy is deliberate, because a shared package would need releases for one-line default changes. Copying 30 lines beats versioning a package nobody else installs.

## The Cleanup Pass

In May I audited all 23 flags across the 9 projects in one sitting. The audit took 2 hours, and I marked each flag as keep, remove, or decide later. The 5 undecided flags each got a removal date 30 days out.

The removals followed a fixed sequence:

- flip the flag on in production and watch for one week
- delete the old code path once the week stays quiet
- delete the flag key, the default, and the override
- grep the repo for the key name before committing

That sequence removed 11 flags over five weeks. Two removals exposed dead endpoints I then deleted with about 600 surrounding lines. One removal broke a cron job, and I restored the job within 20 minutes.

The remaining 12 flags all have owners, dates, and one-line comments. Four of them have removal dates in July, and I review the list on the first Saturday of each month. The review takes 15 minutes with coffee, and it has caught 3 stale flags since May.

## Keeping the Flag List Short

The system worked last Tuesday when I shipped a new import page. I added one key with a false default, tested it through the local file, and enabled it in production with a single variable. The whole release took 25 minutes including the database migration.

Small projects need boring conventions with safe defaults, plus a monthly pass that deletes what nobody owns. A dashboard would add a service, an account, and a bill for 12 booleans.

The gaps are clear and I accept them for now. Gradual rollouts, percentage splits, and audit logs beyond git history are all missing here. If a project ever needs staged rollouts, I'll choose a hosted service instead of extending this loader.

I'll cover the hosted-service comparison in a future post on this blog. If you want to follow along, don't forget to subscribe.
