# Review prompt: simplify

Make the text easier to read for a developer whose first language may not be
English. Most technical drafts already use short sentences, so length is rarely
the problem. The reader slows down on idioms, framing sentences, terms that
arrive before their definition, and points made twice. Fix those.

This is a line edit, not a rewrite. When a sentence is already plain, leave it
alone. Many paragraphs come out unchanged.

## Never change

- Frontmatter, fenced code, command output, inline code, URLs, link targets,
  and image paths.
- Numbers, prices, dates, versions, and tool or API names.
- Quoted prompts (text the author typed into an agent) and quoted speech.
- Facts, reasons, steps, gotchas, and caveats. Don't invent a new reason.

Don't use find-and-replace across a whole file. It edits code blocks too. Edit
one paragraph at a time.

## What to fix

Work through the text in this order.

1. Replace idioms and metaphors with literal words.
   - `the model is a passenger ... let it drive` -> `the model can't search
     again ... let the model call search itself`
   - `would blow up the token bill` -> `would cost many tokens`
   - `shortcuts creep in` -> `the agent skips steps`
   - `had no second move` -> `couldn't try again`
   - `a Hetzner box` -> `a Hetzner server`
   - `grooming` -> `planning`
2. Replace cleft and "where" framings with the direct claim.
   - `X is what stops Y` -> `X stops Y`
   - `This is where RAG helps most` -> `RAG helps most here`
   - `What matters is that you narrow the field` -> `Narrow the field`
3. Use the common word when the meaning is the same.
   - `conveys` -> `says`, `evaluates` -> `checks`, `demands` -> `needs`
   - `mirrors` -> `matches`, `synthesizes` -> `writes`, `consume` -> `read`
   - Keep precise technical terms such as `latency`, `idempotent`, and
     `embedding`. Those are the subject of the text, not jargon.
4. Define a term on first use, in plain words.
   - `the trajectory` -> `the trajectory (the sequence of tool calls the
     agent made)`
   - `hot loading` -> `hot loading (picking up new files without a restart)`
   - If the definition comes later on the page, move it up.
5. Split a sentence that stacks an appositive, a subordinate clause, and a
   result.
   - `Both reach the same answer, but the trajectory, the way the agent got
     there, is different.` -> `Both reach the same answer. The sequence of
     tool calls is different.`
6. Put the point first. If a long condition comes before the main action,
   flip the sentence when that reads better.
7. Turn stacked nouns into a phrase with a verb.
   - `two reusable behavior layers` -> `two reusable ways to add behavior`
   - `a more OpenCode-shaped tool set` -> `a tool set closer to OpenCode`
8. Cut meta-narration.
   - Cut `Here we make the case for posting` and `Next, we cover where to
     post`. Headings already say what comes next.
   - Keep a lead-in sentence right before a list or code block. Stylint
     requires one.
9. Cut the second copy of a repeated point. Look for these cases:
   - a README bullet restated in the next paragraph
   - a sentence that repeats the one before it
   - a closing line that repeats the page intro
10. Name vague pointers. When `that path`, `this piece`, or `it` refers to
    something two or more sentences back, name the thing.
11. Use first person for the author's own experience, but check who the
    speaker is first. In a co-presented workshop, `I` may be a different
    person. There, keep the third-person name instead of claiming someone
    else's story.

## Don't

- Pad. The result should be the same length or shorter.
- Turn text into bullet lists, or add headings.
- Chop every sentence into five-word pieces. Stylint's `choppy-rhythm` flags
  two very short sentences (6 words or fewer) or three short ones (9 words or
  fewer) in a row. A split that leaves each half at 8-15 words is fine. When a
  split trips the rule, join the two halves with `because`, `so`, `but`, or
  `when` instead of undoing the split.
- Swap plain words for "better" synonyms. `simple`, `works`, and `like` stay.
- Add em dashes. Use a period, a comma, or parentheses.

## Output

Edit the file in place. Then run `stylint` on it and fix every finding. If a
stylint fix makes a sentence worse, say which rule and which sentence in your
report. Don't work around the rule by making the text vaguer.

Report the changes as `original -> rewrite`, grouped by the numbered item
above. List facts you found wrong but left alone, such as a count that
doesn't match its list, or a link to the wrong page.
