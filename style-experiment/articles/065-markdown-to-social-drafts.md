# Generating Social Drafts from a Finished Article

On July 2, I finished a fictional 1,840-word article about data quality checks. I needed one LinkedIn post, two tweets, and a newsletter teaser, and I didn't want each surface to invent a different argument. So I built a small pipeline that turned the article into four drafts and kept every claim traceable to the source.

I invented the article, metrics, and outputs for a synthetic style exercise. I used it to test a rule about compressed citations: a social draft should come from a sentence that already survived editing.

In this post, I'll share the workflow:

- how I prepared the source article
- the extraction and scoring steps
- how the tool adapted one claim for each surface
- the human review pass and prompts
- what the first drafts got wrong
- what I changed after four weeks

## Prepare one canonical article

I stored the article at `articles/2026-07-02-quality-checks.md` and treated it as the canonical version. If a social draft disagreed with that file, the draft was wrong, even when the new phrasing sounded better.

I added YAML frontmatter with the audience, core claim, and evidence list. The core claim was that automated checks catch known failure classes, while humans still choose which failures matter. Three supporting numbers came from the fictional experiment.

The front matter looked like this:

```yaml
audience: "data engineers and analytics developers"
core_claim: "automated checks catch known failures; humans decide which failures matter"
evidence:
  - "12 failure classes covered by the check suite"
  - "37 percent fewer silent bad loads"
  - "22 minutes median triage time saved per week"
```

This step took about 20 minutes, and it became the most useful part of the exercise. It forced me to choose one claim before I generated any shorter text.

## Extract candidate passages

I wrote a Python script called `social-extract.py`. It reads the Markdown, removes code fences and headings, splits paragraphs into sentences, and writes candidate rows to `output/candidates.csv`.

The first version kept every sentence and produced 94 candidates for a 1,840-word article, so I added these filters:

- reject sentences longer than 28 words
- require a number, named tool, or explicit claim
- skip sentences that depend on an earlier pronoun

The filters reduced the list to 31 candidates. For each row, the script stored the article heading and evidence status alongside the text and character count. That made review easy by section instead of rereading the whole article.

The mistake in this pass was mechanical extraction. One candidate read, "We ran the suite nightly, which was enough for the first month". It looked useful, but it lacked the context that later data had changed. I marked it rejected and added a rule: candidates must make sense as the first sentence a reader sees.

## Score for reuse

I used three categories, and each candidate got one mark:

- direct: the sentence can move to another surface unchanged
- adapt: it needs a new opening or a platform-specific phrasing
- source-only: it supports the article, but lacks context elsewhere

Eleven candidates were direct, 14 needed adaptation, and 6 were source-only. I reviewed all 31 by hand. This exercise used a small model to suggest a category, but I overruled it on nine rows because it preferred numbers over claims.

The best candidate was the core claim. It was 14 words, used no pronouns, and contained the contrast that made the article coherent. Two evidence sentences also scored well because each named a specific number and consequence.

## Adapt for each surface

The generator produced one draft per target in `output/drafts/`. It received the canonical claim, the selected evidence, the audience, and a surface profile. The profiles defined length, tone, and the link style.

LinkedIn got a 112-word draft. It opened with the core claim, gave all three numbers, and ended with a question that invited examples. Twitter got two drafts: one 246-character claim post and one 265-character evidence post. The newsletter teaser used 41 words and explicitly linked to the article's opening problem.

The prompt was deliberately narrow:

```text
Use only the supplied claim and evidence. Do not add new facts.
Return one draft for LinkedIn. Keep the claim in the first sentence.
End with one question about the reader's current quality checks.
```

The generator followed the factual boundary well and didn't invent a new statistic. It did add a fairly generic closing question, which I replaced with a more specific request for examples of silent failures.

## Review the generated drafts

I reviewed the four drafts in a single pass with the article open. For each draft, I checked claim accuracy, evidence use, and whether the first line made sense without the article.

The first Twitter draft was too compressed. It said checks reduced "silent bad loads" by 37 percent, but it omitted that the check suite covered only 12 known classes. That omission made the result sound broader than the fictional experiment. I restored the class count and accepted a longer draft.

The LinkedIn draft repeated the word "quality" seven times. That repetition came from the source title and evidence labels, so I varied two instances while keeping the term in the main claim. The newsletter teaser was the cleanest output and needed only a punctuation change.

The final drafts kept one discipline: no claim appeared unless it existed in the article. When I wanted a sharper line, I edited the article first, regenerated the candidates, and only then changed the social draft.

## Four weeks later

I used the same workflow on six fictional articles. The preparation time stayed around 15 to 25 minutes per article, and generation took under two minutes. Human review was the real cost, usually 20 to 35 minutes.

The value changed over time. Direct extraction worked for articles with explicit claims, while adaptation worked better for narrative articles. In those cases, the interesting sentence often depended on the preceding paragraph, and source-only candidates still served as notes.

I added one rule after the fourth article: generate no drafts until the article has a single-sentence core claim. That prevented several tempting excerpts from becoming standalone arguments without a point.

The pipeline doesn't make publication automatic. It shortens the path from a finished article to a matching summary, while a person still chooses the claim and checks the evidence. If I extend the exercise, I'll compare the drafts against engagement data in the fictional environment. Subscribe if you want that follow-up.
