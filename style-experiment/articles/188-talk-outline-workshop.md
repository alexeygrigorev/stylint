# Using an Agent to Workshop a Conference Talk Outline

This synthetic style exercise follows a fictional talk prep with invented numbers and dates. Last June I workshopped a 25 minute conference talk with a coding agent. No detail here describes real events or real audience data.

The talk covers agent evals for 220 attendees with mixed Python experience. I had 14 pages of raw notes and no clear promise line.

The request asked for audience, promise, examples and time budget in one outline. I wanted that structure without generic advice or filler stories.

In this post, I'll share:

- how I briefed the agent
- how I fixed the promise line
- how I picked three examples
- how I enforced time budget
- what one workshop run taught

## Audience Notes Guide Cuts

I started with 38 attendee notes pulled from last year with names removed. Each note keeps role, Python level and one pain quote.

I keep notes in `audience.md` and I feed them to the agent in chunks. TalkPack, a small set of prompts that draft outline versions, sits beside the notes.

I chose small chunks because I know limits well enough to avoid overflow at midnight without extra tools. The downside is slower passes, and that trade has stayed manageable for 38 notes.

I counted 22 backend engineers early and I grouped the rest by data roles. That manual tally took 27 minutes and it forced me to cut two academic asides.

I split the audience across three groups I used in June:

- backend engineers shipping agent features
- data scientists running evals weekly
- team leads buying tooling time

I kept all 38 notes so the outline stays grounded across the talk.

One brief looks like this inside the plain input file:

```text
role: backend engineer
level: mid Python
pain: evals take too long
```

I don't trust memory so I reread that brief before every single draft.

## Promise Line Keeps Focus

I asked the agent for five promise lines with concrete outcomes each time. The drafts named the takeaway, the method and the time saved.

The top line promises a 20 case eval routine in under an hour. At talk pace that line fills ten seconds with room for a pause.

The next lines promise cost tables, latency checks and review gates on stage. Its total came to five options, which fits one slide without crowding.

I chose the first line because I pay attention to builder time each week. The downside is narrow scope, and I added a caveat slide.

The five options share four traits I read in June:

- concrete numbers tied to live runs
- method names tied to repo files
- time bounds tied to talk demos
- no jargon without quick gloss

I don't keep clever lines when clarity lacks numbers or verbs.

I draft promise lines with one short command before every review:

```bash
uv run python scripts/draft_promises.py --audience audience.md --count 5
```

That command lists options so I can pick one without rewriting all slides.

## Examples That Fill Time

I picked three examples from June logs and I timed each at six minutes. The old outline listed six ideas where two people guessed different depths.

Both overruns came from live demos run without timers during rehearsal in June. I had left transitions implicit in review, which turned out to be a mistake.

The rule I took from it: examples need timers before any full rehearsal run. I keep the timer sheet in Git so I can confirm splits without guessing.

I chose three examples because I already time them in practice and they fit. The downside is fewer stories, and I move extras to backup slides.

The three examples passed three checks in the June sample:

- each example shows one live run
- each example names one file path
- each example ends with one takeaway

I added timer checks for each block and the outline stayed tight.

I time examples with one repeatable pass each evening:

```bash
uv run python scripts/time_blocks.py --outline outline.md --per-example 360
```

That output lists long blocks first so I trim fat without cutting proof.

## Time Budget Enforces Choices

I gave the 25 minutes clear splits across intro, examples and close. The intro takes three minutes, each example takes six and close takes four.

I recorded the splits and I kept photos of each timer for reference. A strict cap cut one example, yet the talk still covers the promise.

I watch pace and slide counts during rehearsals with a phone timer. I skipped the timer once on a Friday run, which turned out to be a mistake.

The rule I took from it: budgets stay fixed before any slide polish starts. I chose fixed splits because I can explain them in seconds to organizers.

The downside is cut material, and I document removed slides in backup notes.

The budget splits into four blocks I use in July:

- intro and promise in three minutes
- two core examples in twelve minutes
- live numbers demo in six minutes
- close and links in four minutes

I rehearsed the full talk in staging and the run took 24 minutes. The timed run felt calm - the budget removed guesswork under stage pressure.

## Lessons From One Workshop Run

I produced 11 outline drafts in the workshop and the work took 94 minutes total. Those numbers matter less than the promise line that survived all cuts.

I don't add slides after lock now and I keep the outline frozen for one week. That freeze caught one late example swap in June logs.

I chose freeze because I prepare talks alone without coach help. The downside is stale jokes, and that pause has saved two rushed rewrites.

I'll keep the three-example limit and I'll refresh numbers with fresh runs each month. I'll write about the stage run after one more conference delivery. If you want to follow along, don't forget to subscribe.
