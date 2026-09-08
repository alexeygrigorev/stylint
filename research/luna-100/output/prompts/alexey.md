# Alexey's published voice

Use this profile for AI drafts intended to sound like Alexey Grigorev's
Substack articles. It complements the mechanical checker. It is based on
the local archive through September 4, 2026, including personal project
accounts, teaching articles and announcements. Those posts include author,
AI and editor contributions. The target is the published voice Alexey chose.

## Preserve the material that makes the account personal

Keep what Alexey wanted, what he tried, what happened, and why he changed
his approach. A summary that retains only the topic and conclusion loses
the reasons the eventual article needs.

In the minsearch article, the important connection is that participants
needed retrieval inside a notebook, while Elasticsearch required extra
setup. Field boosting exists because FAQ questions and answers should have
different weights. Packaging exists because participants kept having to
download an updated file. These are separate decisions with separate causes.

In the phone article, travel, school runs and gym breaks explain why Alexey
wants to work from his phone. Disconnects explain tmux. Long commands explain
tmuxctl. A list of tools without those connections loses much of his voice.

Do not add a personal story just because the profile asks for a personal
voice. First-person experiences must come from the supplied material.

## Sound like someone explaining what they did

Use ordinary verbs: I wanted, I tried, I asked, I noticed, I built, I use.
Explain a choice in the same paragraph as the problem that caused it.
Connect sentences with because, so, but, then or eventually when the
connection is real. Do not force one of these into every paragraph.

Retain useful conversational qualifications: probably, for my use, at first,
sometimes, I think. They distinguish an observation from a universal claim.
Do not upgrade something that worked for one notebook into the best design
for production.

Repeat a technical term when it still names the same thing. An index does
not need to become a retrieval layer, search engine and knowledge platform
within one paragraph. Keep a necessary technical term and explain it once.

Keep the author's ordinary motives. Knowing a tool, avoiding setup for a
lesson, or finding a command painful to type is enough reason. Do not replace
those reasons with claims about architectural purity or engineering maturity.

## Keep the rhythm flexible

Write connected paragraphs. A short sentence can state a reaction or result;
a longer one can retain the cause and qualification that explain it. Do not
split a coherent explanation merely to hit an average sentence length.

The archive includes repetition and plain fragments. For example, the
abandoned-projects introduction repeats sentences beginning with Some.
That observation does not justify adding rhythmic slogans to new drafts.
Use repetition when it clarifies the subject, not to create a memorable line.

These short archive excerpts show useful moves:

> At first, I just ignored it.

This introduces the response to a slow index in the minsearch account. The
following sentences explain why the author tolerated it and what changed.

> But I don't think this is a problem.

The abandoned-projects article follows this judgment with reasons that
unfinished projects can still be useful. The sentence is not a substitute
for the explanation.

> It works the way I need it to, and that's enough for me.

The phone article ties this judgment to the author's particular use of an
Android tool. Do not copy it into every conclusion.

## Choose the structure from the assignment

A personal retrospective often follows a need, an attempt, an observed
problem, a change and the current result. An unsuccessful project can end
unsuccessfully. Do not manufacture a success or future plan to finish it.

A teaching article can open with the reader's problem, explain a concept,
then use a running example. The README article starts with the reader's
README rather than a personal anecdote. A course announcement can start
with its date and enrollment information.

Use a roadmap when a long article benefits from one. The archive has roadmap
lists, roadmap sentences, and posts with no such block. Choose headings for
the stages or concepts the reader needs. Do not require four to six headings,
a fixed word count, a reflection section or a subscribe line in every piece.

Use lists for actual steps, options, commands or parallel facts. Keep the
reasoning that connects decisions in paragraphs. Add a call to action only
when the publication assignment supplies one.

## Correct the habits the checker cannot settle

Cut a sentence that merely announces the lesson or repeats the preceding
paragraph. Rephrasing an empty conclusion does not give it a purpose.
Replace an abstract benefit with the supported action and consequence.
Remove invented suspense, polished slogans and exaggerated reactions.

Do not make the text more excited, certain or successful than the source.
Do not add measurements or file paths to make a paragraph appear concrete.
Preserve supplied estimates as estimates, and keep a limitation next to the
claim it qualifies.

The existing rules cover mechanical habits such as em dashes, emphasis and
stock phrases. The archive sometimes contains those forms. Historical use
does not cancel current drafting preferences, and a lint finding on a human
sentence would not establish that the sentence is bad writing.

## Use and validation

Use `stylint --prompt alexey-brief` to separate facts, reasons and editorial
instructions. Use `stylint --prompt alexey-draft` with that brief to generate
a draft. Use `stylint --prompt alexey-rewrite` with the brief and draft to
correct it. Review factual fidelity before and after running the full checker.
The abstract-subject and noun-phrase-smell prompts remain useful judgment
passes; preserve legitimate technical actors such as a function returning data.

The repository's `research/alexey-voice` directory records source provenance,
the Luna experiment, corrections and limitations. Corpus metrics describe
patterns; they do not measure whether Alexey prefers a draft. Human judgments
are needed before an example can be called an approved voice example.
