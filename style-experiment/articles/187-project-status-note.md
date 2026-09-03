# A Weekly Project Status Note That Fits on One Screen

This synthetic style exercise follows a fictional team routine with invented numbers and dates. Last March I wrote Friday status notes for a team of six engineers. No detail here describes real events or real workplace data.

The team ships one agent feature per week across three repos with many reviews. I had posted long updates in Slack and nobody read past line ten.

The request asked for done, learned, next, blocked and help needed on one screen. I wanted that brevity without losing decisions or owners in threads.

In this post, I'll share:

- how I capture done items
- how I note what I learned
- how I list next steps clearly
- how I flag blocks early
- what eight Friday notes changed

## 1. Done In Five Lines

I started with five bullet slots pulled from merged pull requests each Friday. Each line keeps a verb, a file area and a result number.

I keep notes in `status.md` and I draft them in a plain text editor. FridayNote, a small template that formats the five sections, sits beside the drafts.

I chose five lines because I know limits well enough to cut fluff at midnight without extra tools. The downside is omitted context, and that trade has stayed manageable for six readers.

I counted 34 merged requests early and I picked five with user impact. That manual pick took 22 minutes and it forced me to read diffs twice.

I split done work across three groups I used in March:

- shipped features behind flags
- fixes with test coverage added
- docs and examples refreshed

I kept all 34 links so the note stays honest across the week.

One done line looks like this inside the plain note file:

```text
shipped retry queue UI, 43 tasks unblocked
added CSV export, 12 users tried it
```

I don't trust memory so I reread that note before every single send.

## 2. Learned From Last Week

I write two learned lines from incidents, reviews and support pings each week. The lines name the surprise, the cause and the new check.

I grouped top lessons around queue delays, flaky tests and unclear error copy. At one screen size those lines fill six rows with room for links.

The next set holds process notes about review speed and meeting load on Thursdays. Its total came to 14 lessons in March, which fits without scrolling.

I chose two lines because I pay for attention from a busy team each Friday. The downside is dropped nuance, and I link longer writeups by short codes.

I sort March lessons into four buckets I reuse each Friday:

- latency lessons from slow endpoints
- test lessons from flaky suites
- copy lessons from support tickets
- scope lessons from slipped dates

I don't record vague takes when facts lack numbers or owners.

I draft lessons with one short command before every review:

```bash
uv run python scripts/collect_lessons.py --week 2026-03-14 --out lessons.md
```

That command groups notes so I can pick two without reading chat all morning.

## 3. Next Steps With Owners

I list four next steps with a name and a date beside each item. The old notes named tasks where three people guessed different owners.

Both slips came from steps written without dates during a busy sprint in March. I had left owners implicit in review, which turned out to be a mistake.

The rule I took from it: steps need names and dates before any Friday send. I keep the owner map in Git so I can confirm assignments without asking around.

I chose named owners because I already track them in issues and it reads fast. The downside is public pressure, and I confirm dates by chat first.

The four steps passed three checks in the March sample:

- each step names one owner only
- each step has one due date
- each step links one issue thread

I added date checks for each line and the list stayed clean.

I verify owners with one repeatable pass each Friday:

```bash
uv run python scripts/check_owners.py --note status.md --team team.json
```

That output lists missing owners first so I fix gaps without reading all threads.

## 4. Blocked Items And Help Needed

I tried to surface two blocks early across six March notes with clear asks. The blocks named the waiter, the blocker and the needed reply.

I recorded the wait times and I kept copies of each ask for reference. A direct request cut wait from three days to one, yet one block still needed escalation.

I watch block age and reply times during reviews with Grafana boards. I skipped the ask line once on a Friday note, which turned out to be a mistake.

The rule I took from it: blocks stay visible with asks before any weekend gap. I chose explicit asks because I can answer them in seconds from context.

The downside is frequent pings, and I document each ask in the team channel.

The blocks fall into four kinds I use in April:

- waiting on review from one teammate
- waiting on data access approval
- waiting on design copy signoff
- waiting on staging deploy window

I rehearsed the ask format in staging and the full note took 84 seconds to scan. The Friday send felt calm - the format removed guesswork under time pressure.

## Lessons From Eight Friday Notes

The eight notes averaged 118 words and they took 24 minutes each to write. Those numbers matter less than the reply rate that rose from two to five.

I don't write long updates now and I keep each note under one screen. That limit caught one late scope creep mention in March logs.

I chose brevity because I write for six busy peers without manager help. The downside is fewer details, and that limit has saved two long threads.

I'll keep the five-section template and I'll refresh examples with fresh wins each week. I'll write about the next month after four more Friday sends. If you want to follow along, don't forget to subscribe.
