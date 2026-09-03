# Turning Meeting Transcripts into Actions Without Losing Context

This synthetic style exercise uses a fictional project and invented details.

Last month I reviewed 42 meeting transcripts from a fictional logistics project, and they averaged 51 minutes. The action lists averaged 11 bullets, and I could trust only 6 without reopening the source.

The problem was obvious once I compared a task list with the meeting. A bullet said "Priya will fix the carrier timeout", but it omitted why we chose a 30-second timeout. It also omitted the owner of the upstream service and whether Priya had agreed to the change.

In this post, I'll share:

- why my first transcript summary failed during a sprint review
- how I changed the extraction fields so decisions kept their context
- how I linked each action to evidence in the source transcript
- what the workflow looks like after four project weeks
- what I still do manually before publishing an action list

## The First Extractor

I exported transcripts to plain text and asked an LLM to return title, owner, due date, and priority for every action.

The prompt worked well on tidy conversations. During a sprint review, Priya said the 30-second timeout had been proposed and rejected. The summary made it look approved.

That mistake taught me an important rule: an action always needs the nearby disagreement.

A smaller problem repeated because people used several names for the same colleague. The alias pair Priya and P. Nair referred to the same owner, as did "the carrier team". The extractor treated the first two as separate people and raised the action count from 9 to 12. My data model was too shallow to preserve the evidence.

## Keep the Decision Beside the Action

I rebuilt the extractor around four records. An action says what should happen, a decision says what the group agreed to, and a blocker names the condition that prevents work. An evidence link points back to the transcript.

I use this structure for each action:

```text
action:
  statement: "Priya will rerun the carrier timeout test at 45 seconds"
  owner: "Priya Nair"
  status: proposed
  depends_on: ["carrier API sandbox"]
  evidence:
    speaker: "Priya Nair"
    start: "00:31:18"
    end: "00:32:04"
    quote: "45 seconds may cover the reroute, but I need to test it."
  context:
    decision: "The team rejected 30 seconds."
    disagreement: "Jonas wanted 20 seconds for alerting."
    unresolved: ["test with reroute traffic"]
```

The statement stays short, while the context includes the parts that would otherwise become tribal knowledge. If Priya's task still exists three weeks later, the reviewer can see why the number moved and which condition remained untested.

I made one field mandatory. If the model can't identify a speaker and a timestamp, the item goes into a review queue and doesn't become an action.

## Turn Speech into Reviewable Intent

The second pass reads the transcript in windows. Each window contains 12 dialogue turns, with 2 turns before and after for overlap. For every window, the model proposes candidate records.

I ask for one of three labels on each candidate:

- agreed, when a person accepts responsibility out loud
- proposed, when someone suggests it without confirmation
- unclear, when pronouns or interruptions leave ownership unresolved

Marco said the routing service "probably needs a replay job", and Priya said "yes, eventually". That became a proposed idea, not an action owned by Priya. She agreed to the idea in principle, but she hadn't accepted delivery of a ticket.

I also preserve negative evidence. If the team rejects an idea, I keep it as a decision with a rejected status and leave it searchable. Those records don't enter the action list, but the rejected option often returns later under a new name.

The extraction output remains a draft.

## Attach Evidence People Can Open

Each record points into the transcript by speaker and timestamp. The internal tool resolves that reference to a URL in our meeting archive. The fictional example opens at 31:18 and highlights four sentences.

The reviewer sees three panels:

- the normalized action, decision, or blocker
- the evidence quote and the two preceding turns
- a diff against the previous action list

The diff matters more than I expected. In week two, 4 of 19 records changed after review, and in week four, 3 of 24 did. A reviewer corrected a name, changed "will migrate" to "will test migration", or marked an item proposed.

The model occasionally invented a due date from an ambiguous phrase: "before launch" became a calendar date. I now reject inferred dates unless the speaker says one or the notes define the launch window. The system leaves the field empty and adds a review flag.

Every accepted change becomes an example in a small regression set, which has 38 cases now. It doesn't prove the extractor is correct, but it catches the specific mistakes we already paid to find.

After four fictional project weeks, the daily flow is stable:

1. Import the transcript and identify speakers.
2. Extract candidate actions, decisions, and blockers in overlapping windows.
3. Require evidence for every action.
4. Show a reviewer the quote, surrounding turns, and diff.
5. Publish only records that pass review.

The average meeting now produces 7 actions instead of 11. Five of 7 recent items could be safely assigned in the tracker without reopening the transcript.

Review time is the main cost. It takes 8 to 14 minutes for a one-hour meeting, depending on disagreement volume. That's slower than pressing "accept all", and much faster than reconstructing intent after a task fails.

## Manual Review Steps

I keep three decisions manual:

- confirm that the speaker map identifies each person correctly
- choose which proposed ideas deserve tickets
- set priority after reading the evidence, because the transcript doesn't know the delivery plan

The biggest remaining weakness is cross-meeting state. If Priya discusses the same timeout twice, the extractor creates two records. A matching pass can group them, but a reviewer must decide whether the second conversation superseded the first.

I also don't use this for sensitive meetings. The fictional project has a data policy, and its archive limits access. The extraction fits inside that boundary, but expanding beyond it deserves a separate review.

The principle is narrower than "summarize meetings": preserve the disagreement and connect the claim to a place a reviewer can look at. An action can then leave the meeting without leaving its context behind.

I'll write next about matching repeated actions across meetings. If you want to follow along, don't forget to subscribe.
