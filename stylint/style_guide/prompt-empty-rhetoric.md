# Review prompt: empty rhetoric

Review the text for sentences that sound punchy but carry no content, and be
strict. A linter can't catch this reliably, so you must list every candidate
sentence first and only then judge each one. Delete genuine offenders or
replace them with the plain fact. Leave sentences that carry a fact alone.

## Target

Look for sentences that perform a rhetorical move instead of saying
something. AI drafts add them as scaffolding around real claims. A real
practitioner writing plainly doesn't make these moves.

There are four kinds.

1. Throat-clearing announcement. The sentence announces that a point is
   coming, or that a point deserves attention, instead of making it.
   - `The skeptics have a case, and it's worth stating plainly.`
   - `It's worth noting that ...`, `It's worth pausing on this.`
   - `Let's be clear: ...`, `To put it plainly, ...`, `Put simply, ...`
   - `Here's the thing.`, `This matters.`, `This deserves a closer look.`
   - `There's an important point here.`, `One thing stands out.`
   - Attention-directing imperatives that tell the reader where to look
     instead of saying what is there: `Pay most attention to the second
     half of the prompt.`, `Note the last line.`, `Look closely at ...`,
     `Keep an eye on ...`
2. Mirrored short-aphorism pair. Two short sentences (or two clauses around
   a colon or semicolon) built on the same template, contrasting two
   things for a punchy beat. The pair has no fact that the surrounding
   text doesn't already give.
   - `The star count is noise. The postmortems are signal.`
   - `The short version: the star count tells you nothing. The code tells
     you a lot.`
   - Templates to catch: `X is A. Y is B.`, `X tells you nothing. Y tells
     you everything.`, `X is the easy part. Y is the hard part.`, `Less X.
     More Y.`, `Not X. Y.`
3. Manufactured decisiveness. A plain action dressed up as a dramatic,
   singular, inevitable choice. It often uses a colon to stage a reveal.
   - `I did the only thing that settles an argument like that: I cloned it
     and read the code.`
   - Variants: `There was only one way to find out: ...`, `So I did what
     any engineer would do: ...`, `The answer was obvious: ...`, `I made a
     call: ...`, `There's only one honest test for this: ...`
4. Redundant recap. A sentence that restates a claim already made earlier
   in the paragraph, section, or piece, purely as a punchy close. It adds
   no new number, name, step, reason, or consequence. There's no reason
   for this sentence to exist.
   - A paragraph explains that the agent wrote tests before code, the tests
     caught two bugs, and then it ends with `Tests first, bugs caught.` or
     `That's the whole point of writing tests first.`
   - Common shapes: `That's the point.`, `That's the lesson.`, `That's what
     X is for.`, `In other words, ...`, `The short version: ...`,
     `Bottom line: ...`, `So yes, X works.`, a one-line paragraph that
     repeats the section's claim.

## Step 1: list every candidate

Don't judge while you read. First go through the whole text and write down
every sentence that matches any of these surface shapes:

- The last sentence of every paragraph.
- The last sentence of every section (before a heading or the end of the
  page).
- Every pair of adjacent short sentences (under about 10 words each), and
  every short sentence that sits alone as its own paragraph.
- Every sentence with a colon, dash, or semicolon that introduces a reveal,
  a verdict, or a second half.
- Every sentence that talks about the point instead of making it: words
  like `worth`, `plainly`, `clear`, `simply`, `short version`, `bottom
  line`, `the thing is`, `matters`, `important`, `only`, `in other words`,
  `that's the point`, `that's why`.

Number the candidates and quote each one exactly. Expect many. Most
closing sentences are fine, so the list will contain more fine sentences
than offenders. That's expected: the list makes sure you don't skip one.

## Step 2: judge each candidate

For each numbered candidate, ask these questions in order:

1. Delete the sentence. Does the reader lose a fact: a number, a name, a
   command, a step, a reason, a consequence, or a condition? If not, it's
   an offender.
2. Does it announce or rate a point (`worth stating`, `let's be clear`),
   or tell the reader where to look (`pay attention to`, `note the`)
   instead of making it? Offender (throat-clearing).
3. Is it two parallel halves on one template where the contrast is the
   whole content, and the facts behind it are already stated nearby?
   Offender (mirrored pair).
4. Does it frame an ordinary action as the only, obvious, or decisive move
   (`the only thing`, `only one way`, `what any engineer would do`)?
   Offender (manufactured decisiveness), even when the action after the
   colon is a real fact. Keep the fact, drop the staging.
5. Does it repeat something the text already said, with different words?
   Compare it with the earlier sentences, not only the previous one.
   Offender (redundant recap).

Label each candidate `offender (<kind>)` or `fine`, with a one-line reason.
When you mark it fine, name the new fact it carries.

## Fix

Usually delete the sentence. When it wraps a real fact, keep the plain fact
and drop the staging.

- `The skeptics have a case, and it's worth stating plainly.` -> delete it
  and start with the skeptics' case.
- `It's worth noting that the agent ignored the lint config.` -> `The agent
  ignored the lint config.`
- `Pay most attention to the second half of the prompt.` -> say what the
  second half does: `In the second half of the prompt, we ask Lovable to put
  every backend call in one services layer and to add a mock backend.`
- `The star count is noise. The postmortems are signal.` -> delete the pair
  if the paragraph already says why the postmortems matter. Otherwise state
  the fact: `The postmortems show how the team handles outages.`
- `I did the only thing that settles an argument like that: I cloned it and
  read the code.` -> `I cloned the repo and read the code.`
- A closing line that repeats the paragraph's claim -> delete it.

Don't replace an offender with another punchy line. Don't invent a fact to
make a sentence earn its place.

## Leave Alone

Leave these cases alone:

- A short contrast that carries a fact the reader didn't have: `The first
  run took 14 minutes. The cached run took 40 seconds.` Parallel shape
  alone isn't the smell. Empty contrast is.
- A closing sentence that adds a new number, name, step, consequence, or
  caveat: `After the change, the build passed on all 37 tests.`
- A colon that introduces a real list, a command, a definition, or a quoted
  prompt: `The spec has three parts: the data model, the API routes, and the
  acceptance tests.`
- A sentence that names a real choice between real options with the reason:
  `We picked SQLite over Postgres because the app runs on one machine.`
- A first-mention summary at the start of a section that the section then
  expands, when it isn't a repeat of something earlier.
- Quoted speech, quoted prompts, and code.

## Output

Use this reporting format:

1. The numbered candidate list from step 1, each with its label and reason
   from step 2.
2. For each offender, the original line and your fix (`delete` or the
   rewrite), then apply it.

If a page has no offenders, say so plainly and change nothing.
