# Review prompt: abstract noun as the subject

Review the text for abstract nouns used as grammatical subjects. A linter
can't catch this reliably, so use judgment. Fix only genuine offenders and
leave concrete, well-grounded sentences alone.

## Target

Look for a sentence whose subject is an abstraction instead of a person,
a tool, or a concrete thing.

Common abstract subjects include:

- feelings
- outcomes
- processes
- qualities
- principles
- ideas
- habits
- values

The determiner and number don't matter. Check subjects even when they start
with small words like `the` or `our`.

The verb may be a weak copula such as `is` or `was`. It may also be an
active verb the abstraction can't literally do, such as `keeps` or
`drives`.

Treat this as a covert passive because it hides the actor without using
passive grammar. We write in an active, personal voice, so keep a real
subject. Use `you` or `we`, or name a person, tool, or concrete thing.

These forms usually need a rewrite:

- `The growth followed.`
- `The hate was hard to sit with.`
- `A few rules keep the code clean.`
- `Two habits make you consistent.`
- `These steps build trust.`
- An abstraction "does" something it can't literally do:
  `The honest account taught them something.`
- A pseudo-cleft that inflates a plain cause: `X is what made it useful.`,
  `Consistency is what grows a LinkedIn account.`
- A document part as the actor: `This part turns that into a routine.`

## The test (generalize, don't pattern-match)

Don't match the examples literally.

Apply this rule to every sentence:

1. Find the grammatical subject (what the main verb is about).
2. Ask: can you point at it? If yes, leave it alone.
3. If the subject is an abstraction doing the verb, it's the smell. The
   determiner, number, and verb type don't matter.
4. Rewrite so a person or a concrete thing does the work.

## Fix

Rewrite with a real actor, a concrete cause, or a person. When the
sentence only announces what comes next, delete it.

- `The growth followed.` -> `Subscribers grew 9% that week.`
- `The honest account taught them something.` -> `People found it useful
  because a senior engineer admitted a mistake.`
- `The hate was hard to sit with.` -> `It wasn't easy to deal with all
  the hate.`
- `A senior engineer admitting a mistake is exactly what made it useful.`
  -> `People found it useful because a senior engineer admitted a
  mistake.`
- `The outcomes are concrete.` (followed by a list of the outcomes) ->
  delete it because the list already names them.
- `Consistency is what grows a LinkedIn account.` -> `To grow your
  LinkedIn account, you need consistency.` (or `you need to post
  consistently.`)
- `This part turns that into a routine.` -> `Next, you turn this into a
  routine.`
- `Two habits make you consistent.` -> `You stay consistent by keeping
  two habits.` (a person does the work, not the habits)

## Leave Alone

Leave these cases alone:

- Concrete subjects: `The agent calls the search tool.`,
  `The function returns a list.` Leave these alone.
- Sentences where the abstraction genuinely is the topic and the claim
  is specific: `The latency dropped from 800ms to 120ms.`
- Don't manufacture a cause the source never stated. If you don't know
  why, cut the claim rather than invent one.

## Output

Use this reporting format:

For each change, give the original line and your rewrite, then apply it.
If a page has no offenders, say so plainly and change nothing.
