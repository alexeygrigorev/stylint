# Alexey On Data Style Experiment

This folder contains 250 synthetic article drafts modeled on the voice of
[Alexey On Data](https://aishippingblog.com). The reference files are copied
from the Telegram writing assistant repository.

Every draft is explicitly synthetic. It may use plausible project names,
measurements, dates, costs, and tool choices, but it must not present those
details as real events or cite external facts. The first paragraph must say
that the piece is a synthetic style exercise.

## Generation rules

- Use the voice in `references/substack-writing-style.md`.
- Apply the drafting bans in `references/voice.md`.
- Write 900 to 1,100 words of article prose.
- Use `# Title`, four to six `##` headings, and no deeper heading levels.
- Include a bulleted roadmap after the opening.
- Keep paragraphs to one to three sentences.
- Prefer the spaced hyphen over the em dash.
- No bold, italics, tables, horizontal rules, rhetorical questions, hype words,
  emoji, or "not X, but Y" constructions.
- Use only well-known tool names and explain any invented internal name in
  apposition.
- End with a short reflective section and a generic subscribe line.
- Each file must pass `uv run stylint <file>` with zero findings.

## Layout

- `articles/` - one markdown file per generated article.
- `manifests/topics.tsv` - the complete numbered assignment list.
- `reports/` - worker completion reports.

The filename convention is `NNN-topic-slug.md`, using the three-digit topic ID
from `manifests/topics.tsv`.
