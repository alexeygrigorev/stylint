# Generating Release Notes Without Inventing Impact

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional.

On 8 September I released version 0.9.2 of `inventory-agent`, a fictional Python service that reconciles warehouse counts. The release contained 19 merged pull requests. The previous notes had said the changes would "improve performance and reliability", but neither sentence said what a user could now do.

The draft had been generated from commit messages. It listed every commit, including three revert commits and five commits that were parts of one feature. It also claimed a 30% speedup because the phrase appeared in one commit message.

I wanted notes that were useful, verifiable and quick to edit.

In this post, I'll share:

- how I grouped 19 pull requests into five user-facing changes
- how I linked each claim to its issue or diff
- which generated sentences I removed
- how a human editing pass changed the tone
- what the final workflow looks like

## Starting From Pull Requests

The first change was the input. A commit message describes an engineering step, while a pull request describes the intended change and its review. The repository requires every merge to reference an issue, so I started from the 19 merged pull requests.

I exported the basic fields with `gh`, the GitHub command-line interface:

```bash
gh pr list --state merged --limit 50 --json number,title,body,files
```

The JSON gave me 19 titles, descriptions, changed files and linked issue numbers. It contained no performance claims. Those lived in one pull-request comment and one commit message, and both referenced an unfinished benchmark.

Reading the file lists gave the first grouping. Nine pull requests changed the reconciliation engine, four changed the API, three changed documentation, and three changed continuous integration. The remaining pull requests were two user-visible fixes and one dependency update.

## Grouping Changes For Readers

My first grouping mirrored the code layout, so it produced headings such as "engine changes" and "API updates". Users think in tasks, and a reader cares whether the nightly reconciliation resumes after a failed upload.

I therefore grouped by user-visible behavior:

- resume the nightly reconciliation after a failed upload
- show unexplained count differences in the API
- reduce the memory required by large inventory files
- correct timezone handling for stores outside UTC
- update the configuration reference

Continuous-integration and refactoring went into one "internal changes" section. Three pull requests formed one behavior change because they shared issue #418 and shipped as a single sequence.

That process cut 19 pull requests to five user-facing changes and two smaller sections. It also exposed a gap: the memory change had no issue. I created issue #451 so the release note had a canonical place to record the claim.

## Linking Claims To Evidence

Every bullet follows the same structure. It states what changed, then links the pull request or issue that contains the evidence. If a claim has no matching issue, the release notes omit it or mark it as unresolved.

The first bullet in the draft looked like this:

```text
- Nightly reconciliation now resumes after a failed upload (#402, #407).
```

That sentence is testable because issue #402 reports the original failure. Pull request #407 contains the acceptance test. For the memory improvement, I added the measured condition instead of a percentage. The loader peaked at 610 MB instead of 940 MB on a synthetic file with 1.2 million rows.

The generated draft had contained this sentence: "Performance is improved by 30%". The linked pull request showed the benchmark was run on a 10,000-row file, while the reported customer problem involved more than one million rows. I removed the claim and left the memory measurement with its file size.

The rule I took from that review: a generated release note may report what a diff changed, and a human must decide what it means.

## Removing Invented Impact

I gave Claude Code the grouped pull-request data and a prompt with explicit constraints.

The goal was clear phrasing, not interpretation:

```text
Write release-note bullets from these pull-request summaries. Use only facts in the input. Link issue numbers. Do not add benefits, percentages, adjectives, or recommendations. If the input does not explain user impact, write "Change:" followed by the observable behavior.
```

The model produced five usable bullet skeletons and 11 sentences I deleted. They included "significantly improves stability", "streamlines the developer experience" and a recommendation to upgrade immediately. None had support in the pull requests.

Three generated bullets stayed close to the diff. They named the changed command, the returned field and the corrected timezone. I kept their structure and replaced two verbs with the words used in the issue reports.

The result mixed generated structure with human judgment, and the model arranged repeated structures. I supplied the boundary between observable behavior and claimed benefit.

## The Human Editing Pass

The editing pass took 35 minutes for the entire release. I read each bullet against its linked issue, then read the five user-facing bullets as one sequence. Two bullets started with the same noun, so I rewrote one around the user task instead.

I also added a short upgrade note because version 0.9.2 renames one configuration field. The notes needed to say the old field continues to work until version 1.0. That fact came from pull request #433 and was absent from the generated draft.

Finally, I ran the docs check. Every code identifier in the notes appears in the configuration reference, and every issue number resolves. The release notes contain 610 words, five user-facing bullets, six internal-change bullets and 14 links.

## The Final Release Workflow

The workflow now runs in four stages:

- the release manager collects merged pull requests and groups them by user-visible behavior
- the coding agent turns those groups into constrained bullet skeletons
- the release manager verifies each claim against its issue or diff
- a second person reads the notes before publication

The reusable prompt lives in the repository at `scripts/release_notes_prompt.txt`, and it contains the no-impact rule and the "Change:" fallback. Because the prompt is versioned, the 0.9.2 notes can be reproduced from the same input.

The system still depends on good issues. The memory improvement became reliable only after someone recorded the row count, memory ceiling and benchmark date. My next change is a pull-request template field for measured impact.

I'll write about that template after one more release. If you want to follow along, don't forget to subscribe.
