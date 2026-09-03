# Drafting Support Answers with a Retrieval Assistant

I drafted this synthetic style exercise around Inboxbridge, an invented email-routing product. In the fictional January 2026 work, I answered about 40 support questions a week. Most answers already lived in our runbooks, changelogs, and old replies, so finding the current version was the hard part.

In this post, I'll share:

- why copy-paste retrieval wasn't enough
- how I prepared the answer sources
- the format I gave the retrieval assistant
- how confidence and citations fit into review
- what changed across four weeks of drafts

## Copying the Wrong Version

The obvious first attempt was a chat assistant pointed at every document. I pasted a customer message, asked for a friendly answer, and reviewed the result. The answer sounded good, which made the problem harder to notice.

On 14 January, the assistant quoted a retention setting that had changed in version 2.8. Our policy was 30 days, while the old answer said 90 days. I caught the mismatch because I remembered the release notes.

That experience produced my working rule: a support assistant should draft evidence with links, and a person should own the final claim.

The old process mixed three jobs into one step, and the model ran them together. When the answer failed, I couldn't tell whether retrieval, adaptation, or wording had caused the problem.

## Prepare the Answer Sources

I stopped indexing everything and let the retrieval assistant search a fixed set of sources that support owners already review.

The January index contained 1,874 chunks from these places:

- 43 operational runbooks
- 112 release notes
- 384 reviewed support replies
- the current pricing page

I removed marketing pages, old screenshots, and every reply older than the 2.8 release unless it had a review tag. This cut the index by 31% and removed two stale answer paths.

Each runbook section got stable metadata. I added a product area, supported version, and review date to its front matter. A section older than 180 days remains searchable, but the assistant labels it stale and refuses to present it as current policy.

The extra labeling took about six hours across a week. It changed retrieval more than a new embedding model would have. Questions about imports stopped retrieving onboarding essays and started returning the actual migration checklist.

## Draft Evidence Before Text

The assistant now returns structured results before it writes to the customer. I kept the response format deliberately small so I could review it in under a minute.

For every candidate answer, it fills this object:

```json
{
  "question_type": "retention",
  "answer": "In version 2.8 and later, deleted messages are removed after 30 days.",
  "sources": [
    {"title": "Message retention", "path": "runbooks/retention.md", "version": "2.8", "reviewed": "2026-01-09"}
  ],
  "missing_evidence": ["whether an admin can extend retention"],
  "confidence": "medium"
}
```

Only after that object passes my review does the assistant turn it into a short reply. It uses the customer's feature names, states the supported version, and adds one next action. It may not mention a source I removed from the object.

This split exposed another failure. The evidence might be correct while the first draft was overly apologetic or promised a feature change. I could fix the tone without second-guessing the facts.

The prompt asks for one answer, one limitation, and one next step. If a question has two plausible workflows, the assistant returns both in the evidence object and marks the choice unresolved.

## Make Review Cheap

Every draft goes into a review queue with the original ticket, the evidence object, and a short proposed reply. I can approve, edit, or reject it from one screen.

Approvals have three meanings:

- the answer is accurate for the customer's version
- the evidence links support the claim
- the tone matches our support guidelines

I tag failures as evidence, tone, scope, or stale source. Those tags feed a weekly review, and the most common failure decides what I fix next.

Confidence stayed useful after I defined it narrowly. High means all claims come from a current reviewed source and no required evidence is missing. Medium means one assumption is explicit. Low means the assistant found related sources but no direct answer.

I don't approve low-confidence drafts directly. They become either a short clarification question or a human-written reply, and their evidence remains in the queue. That boundary prevents the model from guessing about billing.

The queue also records the final edit. When my edit differs by more than 15 words, I add a note. Two recurring notes led to prompt changes: stop explaining internal queues, and use "workspace" exactly as the interface does.

## Results From Four Weeks

I ran the workflow for four fictional weeks on 164 tickets. Median drafting time fell from 14 minutes to 6 minutes, while the portion of answers accepted without edits rose from 44% to 63%.

That best number needs its caveat. More than one-third of drafts still required edits, and all billing drafts stayed fully human-written. The workflow reduced lookup work, but it didn't remove judgment about policy exceptions.

Most of the improvement came from source changes:

- We rewrote the import runbook after eight evidence failures.
- We added a compatibility matrix after four tickets asked the same upgrade question in different words.

Support quality also improved: customers received fewer replies that referenced deleted settings. The assistant's links also made it easier for another teammate to review an answer while I was offline.

I wouldn't describe this as autonomous support. It's a drafting tool with a narrow response format and a human gate. That limitation is why it stayed useful as volume grew.

The system works because the expensive step, deciding what's true, still has a person. I plan to write about the failure tags and weekly review in a future article. Subscribe for the next part.
