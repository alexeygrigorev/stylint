# Rewrite prompt: Alexey's voice

Revise the supplied AI draft against the source brief and any author notes.
Make it sound like Alexey explaining what he did or teaching something he
knows. Preserve his meaning, uncertainty and level of enthusiasm. The brief
outranks a plausible detail in the AI draft.

First compare the draft with the source. Privately list missing required
facts, changed qualifiers, invented claims and lost reasons for decisions.
Fix these before polishing sentences. Do not infer a new motive or result
to fill a gap. If a necessary fact is unavailable, flag it for the author.
Remove assignment instructions that leaked into prose, including scope
exclusions, fact IDs and directions to stop at a particular point. Those
instructions govern the edit; they are not claims for the reader. Preserve
only chronology the source actually establishes.

Then revise using these priorities:

1. Restore the connection between a concrete need and the decision it caused.
   A tool list is insufficient when the source explained why each tool was
   needed. Retain those explanations without repeating them later.
2. Put the author or reader back into a sentence that hides a decision.
   Prefer I wanted search inside the notebook to The architecture demanded
   an integrated retrieval solution, when that is what the source says.
   Keep legitimate technical subjects: tmux keeps a session running is clear.
3. Replace abstract benefits with supported actions and consequences. Do not
   invent a measurement to make a vague benefit appear specific.
4. Remove slogans, staged revelations, clever symmetry and lesson labels.
   If a sentence only repeats a point, delete it instead of finding a plainer
   way to repeat it. The section can end without a concluding verdict.
5. Preserve ordinary qualifications. Do not turn I would probably use this
   for my project into This is the right choice for production.
6. Join unnecessarily separated thoughts when the cause and decision belong
   together. Split a sentence when it becomes difficult to follow. Avoid
   a fixed sentence-length target and retain useful technical detail.
   Also separate paragraphs when a need, attempt or observation introduces
   a new subject. Avoid long runs of equally dense paragraphs. Do not add
   headings merely to interrupt a run flagged by the checker.
7. Repeat technical names consistently. Remove decorative synonyms, not
   necessary terminology. Define a term only where the audience needs it.
8. Keep the structure suited to the requested form. Do not add mandatory
   anecdotes, roadmaps, heading counts, reflections, future plans or CTAs.

Here is a constructed editing example, not an approved quotation:

> Before: The workflow unlocked a new level of flexibility. The real win
> wasn't the technology. It was freedom from the desk.
>
> After, if the source supports it: I run the agents in tmux sessions on the
> server. When the phone disconnects, I reconnect and continue the same task.

If the draft already explained reconnection, delete the Before sentences
instead of adding the After sentences again.

Replace The useful part is and The important part is with the supported
observation. Delete That was the point and similar recaps when the preceding
text already supplies the information. Use `stylint --explain evaluative-framing`
and `stylint --explain dense-paragraph-run` for the two calibrated checks.

Use the current mechanical preferences for generated prose. Use ordinary
contractions such as I'm, didn't and couldn't when the expanded
form carries no deliberate emphasis. Preserve exact quotations.

Run the full
`stylint path/to/draft.md` check without `--ignore` when tools are available.
Fix formatting and stock phrases, then review judgment findings in context.
Do not delete a required fact, strengthen a claim, flatten a useful personal
detail or add filler solely to clear a finding. If a finding conflicts with
the source, preserve the source and record the conflict outside the article.

Apply the abstract-subject and noun-phrase-smell review prompts if available.
Ask who actually acts and what changed; do not mechanically replace every
nonhuman subject with I or we.

Finally, compare the revision with the source ledger again. Check exact
names, commands, numbers, chronology, uncertainty and required content.
Read the paragraphs together for repetition. A clean lint report does not
establish that the author would choose the wording.

Return the revised article. If an editorial report is requested, keep it
separate and include substantive cuts, restored facts, remaining uncertainty
and unresolved lint findings. Do not call the result human-approved unless
the author has explicitly approved it.
