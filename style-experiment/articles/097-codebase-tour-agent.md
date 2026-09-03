# Building an Agent That Gives a Guided Tour of a Repository

I wrote this synthetic style exercise as a build log, and the repository, tools and numbers in it are fictional. In February 2026 a new engineer joined my team of five, and our main repository held about 3,400 Python files across 60 packages.

Onboarding ran on a wiki page last updated in 2024 and on my time in direct messages. The last engineer we hired had needed about five weeks for a first merged change. I wanted a better path for the next one.

In this post, I'll share:

- the repository and the slow ramp it caused
- a naive prompt that produced a generic tour
- how the script finds the real entry points
- the import graph and its depth cap
- worked examples and the limits I accept
- where the tour runs in our week now

## A Monorepo And A Slow Ramp

We keep two API services, one worker fleet, and a CLI in the repo, and most teammates touch the CLI daily. Sixty packages share one `src/` tree, and the wiki described three of them. Every question about the rest came to me in a direct message, usually while I was in a review.

I measured the problem instead of trusting my memory. The engineer hired in 2024 had sent me 61 questions over five weeks, and 40 of them asked where some behavior lived in the code. That number convinced me to spend a weekend on the problem.

## A Generic Tour From A Naive Prompt

The first attempt took one prompt. I asked Claude Code, a coding assistant, to write a guided tour from the repository file map it already had in context. The response arrived in about a minute and read like a restyled README.

It listed the directory tree, called four packages core without evidence, and never mentioned the CLI that handles most of our daily jobs. Two of the four packages it praised were half-migrated experiments from 2023.

My mistake was asking for a tour without letting the agent run or test anything. The rule I took from it: a tour needs observed entry points. Observation means running code or reading tests, never listing files.

## Finding The Real Entry Points

The first component was a finder script that scans for startup code.

Our code starts through a `__main__` guard, a FastAPI factory, or a click command group, and the finder greps for all three:

```bash
grep -rln "def create_app\|__main__\|@cli.group" src/ | sort
```

The grep returns 23 candidate files, which is too many for any tour. A second pass asks the agent to open each candidate and write one line about what starts there. Nine of the 23 turned out to be real entry points, and the rest were dead experiments that we deleted in March.

The nine survivors go into a candidates file that the tour treats as its table of contents. Each line names the file, the function that starts, and the team that owns it.

## Mapping Dependencies With A Depth Cap

Entry points say where to start, and the graph says what each start touches.

I build that graph with grimp, a Python library that maps imports between modules without executing any code:

```python
import grimp

graph = grimp.build_graph("billing")
imports = graph.find_modules_directly_imported_by("billing.api")
print(len(imports), "modules imported by the API layer")
```

The tour follows the graph breadth-first from each entry point and stops at depth two. The cap keeps one tour under 40 modules. My first version had no cap, the billing tour alone covered 190 modules, and nobody read past the second page.

The rule I took from that draft: keep a tour under one screen per entry point. A full run now takes about four minutes and about 60,000 tokens, which comes to roughly $0.30 with the model I use.

## Worked Examples And Known Limits

Descriptions drift, so the tour quotes working code instead of characterizing modules. For each core module it finds one test that exercises the public interface and embeds 10 to 15 lines from it. Tests beat written examples because they fail loudly when the code changes.

An excerpt from the billing section shows the format:

```text
## Start here: billing
Entry: src/billing/api.py - create_app() wires 9 routes
Core: src/billing/service.py - ChargeService, 240 lines, no I/O
Test: tests/billing/test_refunds.py - read test_refund_flow first
```

Three gaps stay open in the current design. Dynamic imports hide whole plugins from the graph, cross-repository calls appear as opaque names, and the Celery workers sat outside every tour until April. That worker gap surfaced when a new engineer changed a shared module and broke a nightly job the tour never mentioned.

The rule from that incident: a tour covers only what the graph can see, and the team document has to say so at the top.

## The Tour In Daily Use

Since April a scheduled GitHub Actions job regenerates the tour every Monday morning, and the file lives at `TOUR.md` in the repo root. The engineer hired in May read it as her first task. She made her first merged change in week three, about two weeks faster than the 2024 baseline. The codebase also got simpler over the winter, so the number deserves some discount.

The tour works because it stays small and fully regenerated. The wiki keeps our opinions, and the tour keeps only what the code proves. The moment I let hand-written sections accumulate, it will rot like the 2024 wiki page did.

I'll write about the onboarding checklist in a future post. If you want to follow along, don't forget to subscribe.
