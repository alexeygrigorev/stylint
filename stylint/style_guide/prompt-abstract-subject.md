# Review prompt: abstract noun as the subject

Review the text for abstract nouns used as grammatical subjects, and be strict.
A linter can't catch this reliably, so you must scan for the surface patterns
in this prompt before using judgment. Fix genuine offenders and leave concrete,
well-grounded sentences alone.

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
- summary nouns that stand in for what the writer just described
- document parts that stand in for the author or reader

Scan for these nouns when they appear as the subject:

- `growth`, `impact`, `success`, `failure`, `result`, `outcome`
- `approach`, `process`, `workflow`, `flow`, `setup`, `pattern`
- `principle`, `idea`, `lesson`, `takeaway`, `insight`, `strategy`
- `habit`, `practice`, `routine`, `step`, `rule`
- `experience`, `struggle`, `challenge`, `problem`, `hurdle`
- `story`, `account`, `post`, `section`, `part`, `workshop`, `README`,
  `tutorial`, `guide`

The determiner and number don't matter. Check subjects even when they start
with small words like `the` or `our`.

The verb may be a weak copula such as `is` or `was`. It may also be an
active verb the abstraction can't literally do, such as `keeps` or
`drives`.

Scan especially for these verb families after an abstract subject:

- state verbs: `is`, `was`, `becomes`, `stays`, `remains`
- causation verbs: `makes`, `keeps`, `drives`, `forces`, `creates`, `builds`
- sequence verbs: `starts`, `continues`, `follows`, `ends`, `moves`
- explanation verbs: `shows`, `teaches`, `explains`, `proves`, `reminds`
- document-action verbs: `covers`, `walks through`, `introduces`, `turns`,
  `sets up`
- blocking or waiting verbs: `blocks`, `waits`, `hangs`

Treat this as a covert passive because it hides the actor without using
passive grammar. We write in an active, personal voice, so keep a real
subject. Use `you` or `we`, or name a person, tool, or concrete thing.

These forms usually need a rewrite:

- `The growth followed.`
- `The hate was hard to sit with.`
- `A few rules keep the code clean.`
- `Two habits make you consistent.`
- `These steps build trust.`
- `The same pattern works in three places.`
- An abstraction "does" something it can't literally do:
  `The honest account taught them something.`
- A pseudo-cleft that inflates a plain cause: `X is what made it useful.`,
  `Consistency is what grows a LinkedIn account.`
- A document part as the actor: `This part turns that into a routine.`

## Search checklist

Don't only read for the examples.

Make a deliberate pass for these patterns:

- `The <abstract noun> is/was...`
- `A/An <abstract noun> is/was...`
- `<Abstract noun> makes/keeps/drives/forces/creates/builds...`
- `<Abstract noun> followed/continues/starts/ends...`
- `This/That/These/Those <summary noun>...`
- `This section/part/workshop/README/tutorial <action verb>...`
- `The process/workflow/step <action verb>...`
- `<Abstract noun> is what made/makes...`
- `<Abstract noun> is why...`
- `<Abstract noun> means...`
- `<Abstract noun> lets/allows/enables...`

If the sentence starts with a determiner or number, slow down and find the real
subject:

- `the`
- `this`
- `that`
- `these`
- `those`
- `a`
- `an`
- `one`
- `two`
- a number

Many missed cases hide behind small determiners.

## The test (generalize, don't pattern-match)

Don't match the examples literally.

Apply this rule to every sentence:

1. Find the grammatical subject (what the main verb is about).
2. Ask whether the subject is a person, command, tool, file, endpoint, function,
   or another concrete actor, which may be fine.
3. Ask whether the subject is a summary label for previous text. That's likely
   the smell.
4. Ask whether the subject can literally do the verb. If not, rewrite it.
5. Rewrite the sentence so a person, command, concrete cause, or concrete thing
   does the work.

`pattern` is now a banned word (the static checker flags every use). Drop it
everywhere: for regex use `regex` or `regular expression`; otherwise name the
concrete approach, structure, or repeated action.

For `process`, keep only the literal operating-system sense. That means the
sentence talks about a PID, signal, worker, or runtime process. Otherwise treat
`process` as a workflow label and rewrite it. `The process blocks on long
polling` should become `The bot waits for messages with long polling` or `Long
polling keeps the bot waiting for messages`.

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
- `The same pattern works in three places.` -> `I now use the same AWS gate in
  three places.`
- `The process blocks on long polling.` -> `The bot waits for messages with
  long polling.`

## Leave Alone

Leave these cases alone:

- Concrete subjects: `The agent calls the search tool.`,
  `The function returns a list.` Leave these alone.
- Sentences where the abstraction genuinely is the topic and the claim
  is specific: `The latency dropped from 800ms to 120ms.`
- Precise technical nouns: `The data structure stores one entry per account.`
- Don't manufacture a cause the source never stated. If you don't know
  why, cut the claim rather than invent one.

## Output

Use this reporting format:

For each change, give the original line and your rewrite, then apply it.
If a page has no offenders, say so plainly and change nothing.
