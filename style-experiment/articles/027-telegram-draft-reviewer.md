# Extending a Telegram Assistant with a Draft Review Step

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional. In May my Telegram writing assistant published a draft with two duplicated paragraphs, and I found the duplication only after posting.

The assistant had merged three voice notes into one article file. It kept both versions of the closing section, and the published post repeated the same four sentences with slightly different wording.

In this post, I'll share:

- how the assistant drafted before the review step
- what the duplicated-paragraph incident taught me
- how I added message context to each draft
- how I wrote the revision rules
- how the approval flow works now
- where the pipeline still needs attention

## Drafts Without A Safety Net

The assistant collects my Telegram messages and turns them into article drafts. It groups related notes, orders them into sections and writes transitions. It commits the result to a git repo.

That pipeline ran without any verification for four months. I read each draft before publishing, and my read was the only check between the model output and the readers.

The May incident broke that trust quietly, since the draft looked finished at 1,050 words. The duplicated paragraphs sat 600 words apart, and my skim read connected them into one idea instead of two copies.

The rule I took from May is simple. I never publish a model draft that no second pass has read, even when I wrote every source note myself.

## The First Version

The first attempt at a review step was a second model call with a vague instruction. I asked the assistant to "check the draft for issues" after writing it, and it returned a cheerful approval every time.

I tested that reviewer against five drafts with planted defects. It caught zero of the five, including a duplicated section I had copied verbatim, so the vague instruction earned no trust.

The failure taught me that a review step needs the same concrete inputs as the drafting step. A reviewer without the source notes can only admire the wording, and admiration misses duplicated paragraphs.

I deleted the vague reviewer after that test. The draft pipeline ran unreviewed for another two weeks while I designed a stricter version.

## Message Context For Each Draft

The stricter reviewer reads the draft alongside its sources. For each article file, the pipeline now assembles a context folder with the three to eight Telegram notes that fed it.

The assembly script runs after drafting:

```bash
uv run python scripts/assemble_review_context.py --draft queue-monitoring.md
```

That script copies each source note into `review/context/queue-monitoring/` and writes an index file. The index records the note timestamp, the message type and the character count.

The reviewer receives the draft plus that index, so every claim in the draft can be traced to a note. When the May draft runs through this reviewer, it flags the second closing section as unsupported by any source note ordering.

## Revision Rules The Reviewer Follows

The reviewer works from a rule file I wrote by hand after studying 20 of my own edits. Each rule names one defect class, shows a short failing excerpt and states the required fix.

The rule file lives at `review/rules.md` and holds six rules:

- duplicated content across sections gets merged into one place
- claims without a source note get flagged with the note index
- headers deeper than second level get flattened
- sentences above 25 words get split at a clause boundary
- uncited numbers get matched to a note or removed
- transitions that restate a heading get cut

I added the 25-word rule after counting my own published sentences. My archive median sits at 16 words, and anything above 25 reads as tangled in my voice.

The reviewer applies each rule in order and writes its findings to `review/findings/queue-monitoring.md`. I read that findings file before I open the draft, and it tells me where to look first.

## Approval Before Publishing

Findings alone changed nothing until I gated publishing on them. The pipeline now refuses to mark a draft as ready while any finding stays open.

The gate logic fits in one script:

```bash
uv run python scripts/check_findings.py --draft queue-monitoring.md
```

That script exits nonzero while open findings exist, and the publish command calls it before copying anything to the output folder. A nonzero exit stops the publish with the findings path printed.

My approval finishes the process after the fixes merge. I read the revised draft once, confirm the findings file is empty, and mark the draft ready with a dated sign-off line.

Since June the gate has blocked nine drafts with real defects. Six had duplicated or near-duplicated paragraphs, two had uncited numbers, and one had three levels of nested headers.

## The Pipeline Today

The review step adds about six minutes per draft on a local model endpoint. Assembly takes 20 seconds, the reviewer call takes five minutes, and the gate script finishes instantly.

False alarms happen at a steady low rate. Roughly one draft in eight gets a finding I dismiss, usually a transition the reviewer calls restated while I judge it earned.

I keep a log of dismissed findings under `review/dismissed.md`. When the same dismissal repeats three times, I rewrite the rule instead of blaming the reviewer.

The pipeline still can't judge taste, and I don't ask it to try. It catches structure, duplication and missing sources, and I keep the decisions about voice and emphasis for myself.

I'll cover the rule-tuning routine in a future post. If you want to follow along, don't forget to subscribe.
