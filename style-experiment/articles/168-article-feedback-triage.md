# Triaging Feedback on a Draft Without Losing the Argument

This synthetic style exercise invents the draft, reviewers, and feedback counts. On May 9, 2026, I sent a 2,300-word draft about model routing to four reviewers. By May 11, it had 37 comments: 9 about structure, 13 about evidence, and 15 about wording.

My first response was to start at the top and edit every comment. Two hours later, the ending contradicted the new introduction. That was my mistake, and it cost another three hours.

In this post, I'll share:

- why I now group comments before editing
- how I decide the order of structural fixes
- what belongs in an evidence pass
- how I handle line edits without sanding off voice
- the one-page review summary I keep

## Group First, Edit Later

The draft argued that a small classifier should route between a local model and a larger hosted model. Reviewer A wanted a stronger opening. Reviewer B wanted cost data. Reviewer C liked the ending but found section three repetitive. Reviewer D made mostly sentence-level changes.

I copied every comment into a plain markdown file with four columns: comment ID, reviewer, section, and quote. Then I added one decision column. Reading without editing took 35 minutes.

The grouping looked like this:

- argument: 8 comments
- missing evidence: 13 comments
- repetition: 5 comments
- wording and citations: 11 comments

Five comments referred to the same paragraph. Three others asked for a definition in different words. Seeing them together turned 16 possible edits into seven decisions.

## Order the Structural Fixes

I rank structural comments by what they change downstream. The order has four passes:

- clarify the claim
- define the scope and audience
- choose the evidence
- adjust section order

The claim came first. Two reviewers thought I recommended local models in general. I meant this specific case: requests under 300 tokens, with a 2-second latency target and public data. I rewrote the first three paragraphs to say that exactly.

Scope came next because it removed an argument I didn't need. Reviewer A wanted a comparison with enterprise gateways. That is a different article, so I added one sentence naming it out of scope. That choice saved roughly 500 words.

Section order changed only once. I moved the failure cases before the benchmark table. Readers needed to see the 14 misrouted samples before they could care about the 6% cost reduction. Every later section became easier to write.

I leave a structural comment unresolved until the draft has a new pass. Changing the opening, the evidence, and the transitions in one sitting produced the contradiction I mentioned earlier.

## Evidence Pass

The evidence comments fell into three groups:

- numbers that lacked a method
- claims that needed a limitation
- examples that did not match the audience

I made a table of every number in the draft. For each, I recorded its source file, query date, sample size, and the sentence that used it. The fictional routing dataset had 4,180 requests, but only 3,944 survived filtering. The original draft said 4,180 in one section and 3,944 in another.

Reviewer B asked why the hosted model cost $11.40 per 1,000 completed tasks. That number combined prompt tokens, output tokens, and 4% retries. I added those components and the date of the price list.

Reviewer C challenged the statement that the local model handled "most requests". After grouping the data, "most" meant 72%, but only 64% met the latency target. The final sentence reports both numbers.

For missing evidence, I choose one of three actions: add the number, soften the claim, or cut the sentence. Cutting feels uncomfortable, but it's faster than defending a sentence the draft doesn't need.

## Line Edits

Only after structure and evidence do I read wording comments. By then, 11 of the 15 line edits had disappeared because their paragraphs were gone or rewritten.

I separate reviewer preferences from readability problems. Reviewer D wanted shorter sentences throughout. The draft's median sentence length was 18 words, and several longer sentences carried the reasoning. I split three sentences above 30 words and ignored the blanket instruction.

Real clarity problems got priority. One paragraph used "router", "classifier", and "policy" for the same component. I chose "classifier" and repeated it. Another used the passive voice across four sentences, so I named the service and the request.

I also read the draft aloud after accepting line edits. That took 14 minutes and found two places where punctuation made the sentence technically correct but hard to hear. I fixed both by deleting a subordinate clause.

## The Review Summary

After the final revision, I write a one-page summary for the reviewers. It has three short lists:

- accepted changes
- rejected suggestions and reasons
- questions for the next draft

The accepted list names sections rather than every sentence. For this draft, it recorded a revised claim, moved failure cases, corrected sample counts, and two cost breakdowns.

The rejected list is more useful. It shows that the enterprise-gateway comparison is out of scope and that the blanket sentence-length rule conflicted with the reasoning in two sections. Reviewers can push back while the reason is still visible.

The next-draft questions keep momentum. Mine asked whether a 30-day cost example would be clearer than the per-1,000-task number. Reviewer B offered a simpler accounting method the next day.

## What I've Learned

Feedback triage works like dependency ordering. Structure changes invalidate wording, and evidence changes can invalidate structure. Doing them in the wrong order creates extra work.

The summary matters as much as the edits. It keeps the argument accountable to the reviewers without turning the article into a compromise.

I'll write more about turning reviewer questions into an article outline in a future post. Subscribe if you want to see that workflow.
