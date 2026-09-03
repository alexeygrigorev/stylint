# Auditing Generated Articles Before They Touch a Blog

I wrote this synthetic style exercise as a how-to guide. The blog, the drafts and the numbers are fictional. In February 2026 I started generating first drafts for my 14-post blog with Claude Code. The tenth draft invented a Postgres default, and I caught it two minutes before publishing.

That near miss became a fixed audit with 22 checks in four groups. The audit takes about 35 minutes for a 1,000-word draft. It has kept three fabricated facts and two dead links out of the blog since February.

In this post, I'll share:

- how I verify every fact against a source
- how I compare structure with the brief
- how I read for voice and banned habits
- how I test links and add the disclosure
- which catches keep the audit honest
- how the audit fits my publishing flow

## 1. Verify Every Fact Against a Source

The drafts state numbers with total confidence, which is why the fact check comes first. I list every claim that includes a number, a version or a default, and each claim gets a source or gets cut. The February draft claimed that autovacuum waits 10 minutes between runs, and the manual says 1 minute, so the sentence got cut.

The check follows a simple rule: a number without a named source is a rumor. Tool defaults get checked against the official docs, and benchmark numbers get checked against the cited post. Claims about pricing get checked in the vendor's own pages.

I also keep a fact log for each draft, a plain text file with one line per claim and one link per source. The log holds about 15 claims for a 1,000-word draft, and writing it takes 10 of the 35 audit minutes. When a regeneration reuses the draft, the log tells me which claims to recheck. It saved one argument in March, when a regeneration changed a benchmark number and the log exposed the change in 2 minutes.

## 2. Check Structure Against the Brief

The brief for each draft states the audience, the promise and the section list. I reread the brief, then compare it with the draft section by section. The February draft buried its fourth step inside a paragraph about configuration, and moving it into its own heading took 5 minutes.

Most drift shows up in the same places, so I compare the draft against the brief with a short checklist:

- the roadmap bullets map to real headings
- the step count matches the brief
- the opening promise matches the body

The checklist runs in about 6 minutes, and it catches reordering before I waste time line editing. A draft that fails two or more bullets gets sent back for regeneration first.

## 3. Read for Voice and Banned Habits

Voice problems survive a silent read, so I read every draft aloud. Rambling sentences, missing contractions and a flat opener all become obvious in about 4 minutes of reading. My first drafts read like documentation until I started doing this.

Then a mechanical pass catches what reading misses:

```bash
grep -rniE "delve|leverage|seamless|game-changer|supercharge" drafts/february/
```

The grep finds hype words, and a second pass with stylint, a small style linter I wrote, catches long sentences and missing list lead-ins. The linter also flags contrastive formulas that define an idea by what it isn't, which generated drafts produce constantly. I run the grep across the whole drafts folder, so a recurring offender shows up in every draft that shares the habit. Two drafts failed the read-aloud test for a missing roadmap, and both were fixed by adding one.

## 4. Follow Links and Add the Disclosure

Every link gets clicked, every time. The February batch held 31 links, and 2 of them were dead. One led to a blog post that had moved, and one used a docs URL that changed in a release. Dead links get replaced with the current page, or the sentence gets cut.

The last check is disclosure, and each published draft includes one line at the top:

```text
This post was drafted with Claude Code and audited by me before publishing.
```

The line costs 12 words, and it tells readers how the piece was made. The checklist won't clear a draft without it.

## Caveats From Ten Audits

The audit scales badly, and 35 minutes per draft would drown a daily publishing schedule. The checklist also drifts toward what's easy to check, and a fact check can't tell me whether an article is dull. A dry draft passes all 22 checks and still shouldn't always ship.

I still miss things, and a March draft used the same transition in four sections without me noticing it until after publishing. The audit reduces the error rate, and it doesn't reduce it to zero. The time split is roughly 10 minutes for facts, 10 for structure and voice, and 15 for links plus the write-up.

## The Audit in My Publishing Flow

Ten drafts have gone through the audit since February. Three published after fixes, four went back to Claude Code for a regeneration with notes, and three got abandoned as unsalvageable. The regeneration notes are becoming their own checklist, which I didn't plan.

What still doesn't work is tone, and no grep can catch a boring explanation. I'll write about the regeneration notes in a future post. If you want to follow along, don't forget to subscribe.
