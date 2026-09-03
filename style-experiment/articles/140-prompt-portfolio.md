# Keeping a Portfolio of Prompts Instead of One Giant Prompt

I used one 3,100-word prompt for my fictional writing assistant, DraftDesk, for
eight months. I invented its versions, costs, and test results for this
synthetic style exercise. The prompt contained project and tone rules, four
article templates, citation rules, and instructions for three different review
modes.

The assistant often produced usable paragraphs, but review took longer than
drafting. A request for a structure review could also reformat citations. A
request for a title change could remove a caveat required by the template. The
prompt had become a set of instructions that fought each other.

In this post, I'll share:

- why I split the prompt,
- how I designed one prompt per task,
- how the prompts compose,
- how I test changes,
- what I gave up.

## Reasons for splitting it

I started with an inventory of DraftDesk actions, and it supported outlining
articles, drafting sections, and creating titles. It also supported structure
review and citation checking. The giant prompt described every action on every
request, and only the citation instructions were genuinely shared.

I also counted failures over four weeks. Of 76 rejected responses, 41 came from
instructions that didn't belong to the requested task. Nineteen responses
changed formatting in the wrong section, 14 removed caveats, and eight applied
tone rewrites the user never requested.

That number changed the design question. I stopped asking how to make one prompt
clearer and started asking which instructions the task needed.

## Design one prompt per task

I gave each prompt one output schema. The outline prompt returns sections, while
the drafting prompt returns section text. The structure reviewer returns a
verdict, the citation checker returns findings, and the title prompt returns
candidate titles.

Every prompt uses the same four parts:

- task and audience,
- input fields,
- output fields,
- what the prompt must leave unchanged.

That fourth constraint reduced most regressions. For example, the title prompt
receives the article claim and audience. I allow it to suggest titles, but I
forbid it to rewrite body paragraphs or delete a limitation. I made that
constraint explicit even though it sounds obvious to a person.

The structure prompt is now 420 words instead of a 700-word section inside the
old file. It checks the promise, the evidence, the objections, and the ending. A
reviewer can read it in two minutes and explain a disagreement by naming one
check.

## Let the prompts compose

The composition rule is simple: each stage receives the minimum output of the
previous stage. The outline stage produces section titles and claims. The
drafting stage receives one section title and its claim. The review stage then
receives that draft and the claim.

The workflow looks like this:

```text
outline -> draft section -> structure review -> citation check -> title
```

I put shared rules in one 180-word file called `draftdesk-rules.md`. It defines
the audience, the synthetic disclosure, banned phrasing, and the citation
format. The runner includes that file in every task prompt, while task-specific
rules stay in their task prompt.

The most useful change was a stable intermediate file, so the runner now writes
each draft section to `sections/03-audience.json` before review. A user can edit
that JSON file, and review uses the edited claim instead of silently
regenerating a different section.

## Test each prompt

The portfolio made evaluation smaller. I can test 18 title cases without
running the drafting model, and I can test citation behavior without asking for
new article text. That reduced the cost of a prompt-only regression run from
$4.80 to $0.85 in our fictional accounting.

Each prompt has a small evaluation set:

- outline: 12 briefs,
- drafting: 9 section requests,
- structure review: 14 drafts,
- citation check: 16 snippets,
- titles: 18 claims.

Each case has an expected output shape and one or two behavior checks. For the
title set, a pass requires a title under 12 words, the main noun phrase from the
claim, and no invented statistic. The tests don't judge writing quality, but
they catch schema failures before a human review.

When I change the shared rules, I run all five sets. It takes 19 minutes and
costs about $3.40. When I change only the title prompt, the run takes 90 seconds.
That quick result makes small changes much easier to review.

## Costs of the split

A single prompt made it easy to start a new variant. I could copy the file,
change two lines, and send a request. The portfolio requires me to name a task,
check its schema, and decide where a new rule belongs. That's more friction for
experiments.

It also produced one surprise. A drafting request once lacked the shared rules
because the runner failed to read `draftdesk-rules.md`. The old monolith would
have included the rules by accident. I added a startup check that verifies every
required file and fails before calling the model.

There's also a duplication tax. Four prompts mention "short sentences", but they
mean different thresholds. I use 18 words for titles, 20 for outlines, and 24
for drafts. I keep those differences because each task needs a different limit.

## Lessons from the migration

The portfolio is easier to reason about because each prompt has one job. It
makes failures local: a citation error references the citation prompt, and a
structure dispute references one check.

The rule I took from the migration: name the task before adding another
instruction to a prompt. I'll write more about the evaluation sets in another
synthetic article. Subscribe if you want to follow along.
