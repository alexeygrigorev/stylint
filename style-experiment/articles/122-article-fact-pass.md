# Running a Fact Pass on a Technical Article

I wrote this synthetic style exercise as a how-to guide. The article, dates and numbers are fictional. On 22 April 2026 I published a post about Postgres connection pooling. A reader emailed me within an hour about a wrong version number.

The draft said the default `pool_mode` in PgBouncer was transaction. The 1.22 changelog said session, and my config example only worked because I had set the value explicitly. The same post linked to a blog that had moved, so the second link a reader could follow was dead.

Since May 2026 I run a fact pass on every technical draft. The pass takes 25 to 40 minutes per article. Across 9 drafts it has caught 2 to 5 problems in each one.

In this post, I'll share:

- how I dump every checkable claim
- how I verify names and versions
- how I run commands and test links
- how I fix the text and log the changes
- where the pass still needs judgment
- what changed in my editing time

## 1. Dump Every Checkable Claim

A claim is anything a reader can check against the world. For me that means tool names with versions, shell commands, and links. It also covers every number I present as a result.

The dump step uses `dump-claims.py`, a 60-line Python script that prints every sentence containing a number, a version-like token, or a URL. You can write this script in an evening, or you can ask a coding agent to write it for you.

I run it from the repo root:

```bash
uv run python dump-claims.py drafts/pooling.md
```

The script writes `claims/pooling.md` with one line per claim. The April draft produced 34 lines, and 6 of them were version strings I had typed from memory.

For claims the script can't parse, I ask Claude Code, a coding assistant, to sweep the rest of the draft:

```text
List every factual claim in this draft.
For each claim, give the line it came from.
Label it as a name, version, command, link, or number.
```

The sweep found 4 extra claims the script had missed. All of them were comparative claims, things like "about 3x faster under load", and those need a benchmark behind them.

## 2. Verify Names And Versions

The rule sounds boring: check the official docs, and never your memory. The April draft said the default `pool_mode` was transaction. The 1.22 changelog said session, and my memory had kept the value from an older project.

So each tool name in the claim file gets a docs check, and each version string gets a changelog check. Verification takes about 10 minutes for a typical draft of mine. The rule I took from the April mistake: defaults come from the changelog.

Numbers about my own results get a different treatment. I can't re-verify a timing from a benchmark I ran in March, so I open the notes from that run instead. If the notes don't hold the number, the claim gets hedged or cut.

## 3. Run Commands And Test Links

Every command in the draft goes into a clean shell. I use a throwaway container for this, so my laptop stays clean and missing package versions show up the way a reader would see them.

Link checking is one command with lychee, a link checker that reports moved and broken pages:

```bash
lychee drafts/pooling.md
```

The April draft had 9 links, and lychee flagged one redirect to a docs page that had moved. I updated the target and added the new path to the claim file. Running everything takes about 10 minutes, longer when a command needs credentials I have to fake first.

## 4. Fix The Text And Log The Changes

I fix everything in one editing pass, then write a short log entry beside the claim file. The entry records what changed and what I confirmed, so future me doesn't re-check the same facts twice.

```text
2026-05-14 - pooling draft fact pass
fixed: pgbouncer version 1.20 corrected to 1.22
fixed: moved docs link updated to the new path
kept: the 30-second statement_timeout, confirmed in the docs
```

The kept line matters as much as the fixed lines. When a reader questions a number months later, the log tells me whether I verified it or guessed it. Across the 9 drafts, the log has settled 3 such questions without a re-run.

## Caveats And Limits

A fact pass checks facts, and it can't check judgment. Every number can be correct and the advice can still be wrong for your workload, so the pass sits beside editing rather than replacing it.

The sweep also produces noise. It lists every number, including example values I invented on purpose, so I read the list and mark those as intentional. That reading step is where most of the pass's judgment lives.

And 25 to 40 minutes feels slow on the day I want to publish. I still run it, because one wrong default costs more reader trust than the pass will ever cost me.

## Changes In My Editing Time

Across 9 drafts since May 2026, the pass has found 27 problems, and 11 of them were version or number slips. Reader corrections dropped from about one per article to one across all 9 drafts.

The pass still misses claims only a domain expert would question. It approved a vacuum tuning claim in July that a Postgres consultant later qualified, so expert review stays a separate step.

I'll write about the claim dump script in a future post. If you want to follow along, don't forget to subscribe.
