# Deciding Who Owns AI-Generated Code

I wrote this synthetic style exercise as an analysis piece. The project, dates and numbers are fictional. Between January and April 2026 a coding agent wrote 61% of the lines in my invoicing side project, about 4,200 of 6,900 lines.

When a date format broke in March, I realized I could explain maybe half of the code in my own repository. That mismatch between merged work and understanding pushed me to write down an ownership rule, and this post is the result.

In this post, I'll share:

- why the person who reviews the behavior owns the code
- how I review behavior before reading lines
- why small diffs keep the review honest
- what I write down after each accepted change
- how the duty transfers in a handoff

## 1. Review Makes The Author

Authorship in the git sense stayed with me from the first commit, because every commit had my name on it. Useful ownership meant something else: being able to explain, defend and change the behavior.

In February I merged an agent's 300-line export module in one commit without running it against real invoices. The agent wrote the code in 11 minutes, and my review pass took four minutes of scrolling. Two rounding bugs in the tax logic cost me a full weekend, and I couldn't have written either line myself.

The asymmetry was the whole problem: generation got faster, and my side of the commit stayed slow. The commit had a co-authored-by trailer, and the understanding was missing on my side anyway.

The mistake was counting merged lines as understanding. The rule I took from it: the author is the person who reviews the behavior, whoever typed the code.

## 2. Review Behavior Before Lines

Reviewing behavior means checking outputs against fixed cases instead of reading lines for style. I also keep a fixture file with 12 invoice cases for the export module, including two rounding edge cases from March.

A change passes review when all 12 outputs match, and only then do I look at the diff. Reading the lines comes second, and on a 300-line module it takes about 25 minutes. The fixtures take ten minutes to run, so behavior review costs less than line review.

I keep input CSVs and expected output lines in the fixture folder, and a single `pytest` command runs all 12.

One caveat applies to this too. Fixtures cover the behavior I thought to freeze, and the March bug came from a case nobody had frozen. New production incidents become new fixture cases, which is how the file grew from 6 cases in February to 12 in April.

## 3. Small Diffs Keep Review Possible

Diff size decides whether review can happen at all. The February merge put 300 lines in front of me in one sitting, and I reviewed almost none of them.

Since March, agent tasks follow a simple rule: a single behavior, under 120 changed lines. Across 31 tasks since March the median diff is 60 lines, and I read every one of them. The same work split over five small changes takes longer to type, and the review actually happens.

Small diffs have a cost too: some refactors genuinely need 400 moved lines, and I let those through with a slower, explicit review. The 120-line budget is a default, never a hard wall. Each task description also names the fixture cases up front, so the agent runs them before claiming done.

## 4. Record What You Checked

Memory of a review fades within days, so the repository keeps the record. Every accepted change adds three lines to `review-log.md`, a file at the repo root. Each entry lists the cases I ran, the outputs I compared and what I refused.

The log helped in April, when the same rounding question came back and the entry showed exactly which cases I had checked. Skipping the entry feels faster in the moment, and it erased the evidence twice in March. The entry takes about three minutes to write, which is cheaper than reconstructing a review a month later.

## 5. Handoffs Transfer The Duty

Ownership transfers with the review duty, and it never transfers with the repository. In May I gave the invoicing project to a friend for one month of maintenance while I traveled.

My handoff note listed the 12 fixture cases, the review log and the diff-size rule. She accepted ownership by running the fixtures, and her first change arrived with a review entry of her own.

The repository never owned anything, and the duty sits with people. A team can copy the same three artifacts, and each reviewer still has to sign the behavior with their own run.

## Closing Notes

The arc went from a blind 300-line merge to a written ownership rule: review the behavior, keep diffs small, record what you checked. Ownership stopped being about who typed the lines and became a duty I can schedule.

The numbers come from one solo project with no deadline pressure, so treat them as a diary entry rather than a study. Prototypes and throw-away scripts stay outside the rule. For those I still skip fixtures and merge agent code I haven't read line by line. The blast radius is one weekend script, and I accept that trade.

I'll write about the fixture file format in a future post. If you want to follow along, don't forget to subscribe.
