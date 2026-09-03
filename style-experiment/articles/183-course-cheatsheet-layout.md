# Designing a Cheatsheet Students Print and Use

This synthetic style exercise follows a fictional course project with invented numbers and dates. Last February I built a two-page cheatsheet for 128 students in a weekend Python course. No detail here describes real events or real classroom data.

The course runs four live sessions with one coding agent and many terminal commands. I had watched students retype long flags from slides and lose ten minutes each time.

The request asked for commands, decisions, warnings and links on two printable pages. I wanted that density without tiny fonts or clipped margins in print.

In this post, I'll share:

- how I picked commands for print
- how I grouped decisions by task
- how I wrote warnings that stick
- how I kept links printable
- what two print runs cost

## Print Limits Guide Early Choices

I started with A4 paper, 10 point type and 12 millimeter margins on both sides. The printer in the venue clips outer edges, so I kept critical text inside a safe frame.

I keep the source in `cheatsheet.md` and I render it with a small Python script. PrintPack, a small set of markdown files that render the two-page PDF, sits beside the source.

I chose Markdown because I know it well enough to fix layout at midnight without extra tools. The downside is manual spacing, and that trade has stayed manageable for two pages.

I measured the capacity early and I counted 48 command lines per page with readable spacing. That manual count took 34 minutes and it forced me to cut three nice extras.

I split the jobs across two pages I tested in January:

- setup and environment checks for day one
- daily commands for running and tests
- Git steps for commit and review
- debug flags and log locations

I kept 24 entries per page so the text stays above 10 points.

One entry looks like this inside the plain source file:

```text
pytest -q : run tests quietly, show dots only
ruff check . : lint changed files fast
```

I don't trust memory so I reread that file before every single print.

## Commands Students Copy Most

I pulled 62 candidate commands from January session logs with student names removed. The script counts frequency, flags long flags and sorts by daily use.

The top 24 commands cover setup, test runs and Git sync for the course repo. At print size those 24 lines fill one page with room for short notes.

The next 24 commands cover Docker rebuilds, log tails and env checks on Linux. Its total came to 48 lines, which fits the two-page limit without crowding.

I chose frequency order because I pay attention to minutes lost retyping flags. The downside is rare commands missing, and I added a small overflow box.

The overflow box lists six extras I saw twice in February:

- rebuild container without cache drain
- tail last 200 log lines
- export env from template file
- reset local database safely
- run single test by name
- show Git status short

I don't include admin commands when students lack production access in class.

I render the draft with one short command before every review:

```bash
uv run python scripts/render_sheet.py --input cheatsheet.md --pages 2
```

That command writes a PDF so I can check margins without opening an editor.

## Warnings That Prevent Mistakes

I collected 18 warnings from February chats and I kept the nine that caused data loss. The old draft buried warnings inside paragraphs where tired eyes missed them.

Both print tests showed students skip grey boxes and read bold-adjacent lines first. I had placed the database reset warning in grey, which turned out to be a mistake.

The rule I took from it: warnings need high contrast placement near the related command. I keep each warning on one line beside the command it guards.

I chose one-line warnings because I already use them in slides and they scan fast. The downside is short wording, and I link longer notes by short codes.

The nine warnings share clear traits in the March sample:

- destructive commands flagged with red left border
- irreversible deletes paired with backup reminder
- network steps paired with offline fallback

I added short codes like W3 to each warning and the recall stayed strong.

I check warning contrast with one repeatable pass each morning:

```bash
uv run python scripts/check_contrast.py --input cheatsheet.md --min-ratio 4.5
```

That output lists low contrast lines first so I fix glare without reading all pages.

## Links That Survive Printing

I wrote 22 links in the first draft before testing print on venue paper. The URLs broke across lines and three QR codes scanned poorly under warm light.

I recorded the failed codes and I kept photos of each scan attempt for reference. A short link service cut length, yet two codes still needed larger quiet zones.

I watch scan rates and print darkness during tests with an old iPhone camera. I skipped the second paper test on a Friday run, which turned out to be a mistake.

The rule I took from it: links stay testable on paper before any large print run. I chose short URLs because I can read them aloud in class without spelling pain.

The downside is link rot, and I document the target date in the source file.

The link list shows four groups I use in March:

- setup guides for Python and Docker
- course repo and branch naming notes
- test docs and lint config samples
- office hours form and chat archive

I rehearsed link reading aloud and the full pass took 96 seconds. The classroom run felt calm - the short codes removed spelling delays under time pressure.

## Lessons From Two Print Runs

The first run printed 140 copies for $18.40 and it took 22 minutes at the venue. Those numbers matter less than the nine warnings that prevented two risky deletes.

I don't add new commands after freeze now and I keep the source locked for one week. That freeze caught one late Docker flag change in March logs.

I chose freeze because I maintain the course alone without print shop help. The downside is stale tips, and that delay has saved two reprint orders.

I'll keep the 48-line limit and I'll refresh links with fresh scans each cohort. I'll write about the next cohort after one more weekend session. If you want to follow along, don't forget to subscribe.
