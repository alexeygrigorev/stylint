# Building a Tiny Tool for Naming Side Projects

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional. In April I spent most of a Sunday afternoon trying to name a small backup utility, and every candidate failed a domain or repo search.

The finalists all collided with existing tools. Two names matched PyPI packages, one matched a VS Code extension, and my favorite matched a Jira plugin with 40,000 installs.

In this post, I'll share:

- how I collected word lists
- how I generate candidate names
- how I check collisions automatically
- how I keep the final choice human
- where the naming tool lives now

## An Afternoon Lost To Naming

The April utility syncs dotfiles across three machines. The code took six hours, the README took one hour, and the name took four hours spread across a frustrated Sunday.

My process was a text file with 30 candidates and 30 browser tabs. Each candidate needed a PyPI check, a GitHub check and a domain check, and I repeated that gauntlet for every new idea.

The rule I took from April is simple. I generate many candidates from word lists, I check collisions with a script, and I choose with my own taste at the end.

## The First Version

My first generator combined random syllables into pronounceable strings. It produced names like "veltrix" and "qubelo" that passed every collision check and meant nothing to anyone.

I used one of those names for a week. Every conversation about the project started with spelling the name, and nobody remembered it between calls.

Pronounceable isn't memorable, and unique isn't evocative. Random strings optimize the checks while failing the human purpose of a name, so I deleted the syllable combiner.

The replacement builds names from real words. Two-word combinations of concrete nouns hold meaning on first hearing, and the collision script keeps them honest.

## Collecting Word Lists

The generator reads three plain word files from a `words/` directory. Each file holds one word per line, reviewed by hand once and rarely touched after.

The current lists hold curated counts:

- 220 short concrete nouns like river, anchor and watch tower
- 140 verbs of motion and making like ferry, stitch and carve
- 90 place and weather words like harbor, monsoon and ridge

I collected the nouns from my own project history first. Then I added words from release notes I liked, stopping whenever a word needed explanation.

The lists exclude anything coined after 2020. Trendy suffixes age fast, and a name should survive at least as long as the side project it labels.

## Generating Candidates

The generator pairs one word from each of two lists with a separator. Noun-plus-noun pairs form the default pool, and verb-plus-noun pairs form the second pool.

The generation command prints 40 candidates:

```bash
uv run python namegen.py --style noun-noun --count 40
```

That run takes under a second and writes the candidates to stdout. I pipe the output into the collision checker directly, so generation and checking form one motion.

Seeds keep the output reproducible across runs. I pass `--seed 7` during development, and the same seed returns the same 40 names on any machine.

## Checking Collisions Automatically

The checker tests each candidate against four registries in parallel. It queries PyPI, GitHub search, a domain registrar API and the local filesystem for directory clashes.

The check command reads candidates from stdin:

```bash
uv run python namegen.py --style noun-noun --count 40 | uv run python check_names.py
```

That pipeline takes about 25 seconds for 40 names, dominated by the registrar API latency. Each surviving name prints with the four green checks beside it.

Roughly one candidate in twelve survives all four checks. A 40-name batch yields three or four viable options, which is exactly the right number for a human to consider.

## Keeping The Final Choice Human

The script never picks a winner, and that boundary is deliberate. It ranks survivors by length and readability score, then prints the ranked shortlist for me to read aloud.

Reading aloud kills most survivors within seconds. Names that look clever on screen often stumble in speech, and a project name gets spoken in every demo and standup.

My choice checklist fits on three lines, and I apply it to the shortlist only:

- I can spell it over a bad phone connection
- it hints at what the tool does
- no existing tool with 1,000-plus users shares it

The backup utility became Harbor Stitch after two batches. The name hints at syncing across harbors, it survived all four checks, and nobody has misspelled it since May.

## Naming In Minutes Now

The tool has named six projects since April. Each naming session took under 20 minutes, and every chosen name survived its first public mention without spelling trouble.

Total maintenance across four months is near zero. I added 12 words to the lists once, and the checker needed one update when the registrar API changed its response format.

The tool works because it splits the job at the right joint. The script handles volume and verification, and I handle the one judgment scripts perform poorly. That split survived six naming sessions without adjustment.

I'll cover the readability scoring in detail in a future post. If you want to follow along, don't forget to subscribe.
