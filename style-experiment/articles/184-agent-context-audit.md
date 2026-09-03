# Auditing What Context an Agent Actually Used

This synthetic style exercise follows a fictional audit with invented numbers and dates. Last April I traced what context a coding agent used across 46 completed tasks. No detail here describes real events or real customer data.

The agent runs inside Claude Code with file reads, shell calls and retrieval steps. I had saved full session logs for three weeks and the folder held 212 megabytes.

The request asked for prompts, retrievals, decisions and missing evidence in one review. I wanted that trace without replaying every session by eye.

In this post, I'll share:

- how I collect session logs
- how I map prompts to retrievals
- how I link decisions to evidence
- how I flag missing links
- what three audits showed

## Log Sources Show Real Use

I started with 46 session files pulled from March runs with secrets redacted. Each file keeps timestamps, tool calls, retrieved chunks and final diffs.

I keep the logs in `sessions/` and I parse them with a small Python script. TraceView, a small script that lists prompts beside retrievals, sits beside the data.

I chose JSON logs because I know them well enough to query at midnight without extra tools. The downside is large files, and that trade has stayed manageable for 46 runs.

I counted 1,204 tool calls early and I grouped them by file read, search and edit. That manual tally took 41 minutes and it forced me to see retrieval gaps.

I split the calls across three groups I checked in April:

- file reads with path and line ranges
- search calls with query text saved
- edits with diff and test result

I kept all 46 files so the audit stays complete across the month.

One log entry looks like this inside the plain export file:

```text
tool: search
query: retry queue delay
hits: 4 chunks from docs
used: 2 chunks in prompt
```

I don't trust memory so I reread that export before every single audit.

## Prompts And Retrieved Chunks

I pulled 182 prompts from the 46 sessions with duplicates kept for counts. The parser extracts system text, user text and chunk identifiers.

The top prompts reuse the same four chunks about queue config and retry rules. At full size those chunks fill 3,200 tokens with surrounding file context.

The next group pulls Docker logs, env samples and test output on Linux. Its total came to 410 retrieved chunks, which cost extra tokens without clear gains.

I chose exact identifiers because I pay for tokens from a small research budget. The downside is brittle joins, and I added a fallback match by filename.

The identifier match covers most links I need in March:

- prompt identifier matched to chunk store
- chunk store matched to file path
- file path matched to commit tag
- commit tag matched to test run

I don't drop near matches when identifiers drift across renames.

I join prompts to chunks with one short command before every review:

```bash
uv run python scripts/join_context.py --sessions sessions/ --out audit/joined.jsonl
```

That command writes joined rows so I can look at gaps without opening raw logs.

## Decisions Without Supporting Evidence

I mapped 132 file edits back to prompts and I kept the 28 with no linked chunk. The old review trusted edit messages where the agent claimed context it never read.

Both blind spots came from config edits made after a failed search with zero hits. I had trusted the summary line in review, which turned out to be a mistake.

The rule I took from it: edits need linked retrievals before any merge decision. I keep the link table in SQLite so I can query orphans without scanning logs.

I chose SQLite because I already use it for small audits and it answers fast. The downside is manual schema tweaks, and I version the file by date.

The 28 orphans shared clear traits in the April sample:

- config edits after empty search results
- test fixes citing files never opened
- import changes with no read event

I added source checks for each orphan and the gap stayed visible.

I list orphans with one repeatable pass each evening:

```bash
uv run python scripts/find_orphans.py --joined audit/joined.jsonl --min-hits 1
```

That output lists edits first so I see unsupported changes without scrolling far.

## Missing Evidence I Could Not Trace

I tried to trace 12 remaining edits across renamed files in late March. The paths had changed, the chunk store kept old names and two diffs referenced temp files.

I recorded the broken links and I kept screenshots of each lookup for reference. A filename fallback recovered seven cases, yet five still lacked source lines.

I watch rename rates and chunk freshness during audits with Postgres logs. I skipped the rename map once on a Friday run, which turned out to be a mistake.

The rule I took from it: renames stay mapped before any large audit pass. I chose filename maps because I can build them from Git history in seconds.

The downside is stale maps, and I document the build date in the audit notes.

The missing five share four traits I use in April:

- temp files deleted after run end
- renamed modules without redirect entry
- chunks from truncated log tails
- prompts pasted from chat without source

I rehearsed the rename build in staging and the full pass took 88 seconds. The lab run felt calm - the map removed guesswork under time pressure.

## Lessons From Three Audit Runs

The third run linked 1,104 of 1,204 calls and it flagged 28 orphan edits. Those numbers matter less than the five missing sources that exposed rename gaps.

I don't approve edits without linked chunks now and I keep the join output for two weeks. That hold caught one late config drift in April logs.

I chose strict links because I review agent work alone without second reviewer help. The downside is slower merges, and that delay has saved two bad deploys.

I'll keep the 46-file set and I'll refresh maps with fresh renames each week. I'll write about the next audit after one more release cycle. If you want to follow along, don't forget to subscribe.
