# stylint

Voice, formatting, and code-style rules for technical write-ups, plus a
mechanical checker that catches the worst offenders.

## Install

Install from PyPI.

```bash
uv tool install stylint
```

Or install from a local clone.

```bash
git clone https://github.com/alexeygrigorev/stylint ~/git/stylint
uv tool install --from ~/git/stylint stylint
```

For a local checkout you edit often, add this repo's virtualenv binaries to
`~/.bashrc`:

```bash
./install.sh
```

These are the common commands.

```bash
stylint docs/
stylint --list-tags
stylint --ignore tables docs/
stylint --exclude _docs docs/
stylint --agents
stylint --style-guide
stylint --style-guide voice
stylint --prompt abstract-subject
```

## Files

The package has these main files:

- `stylint/style_guide/voice.md` - tone, voice rules, content rules
  (include/leave out). Print it with `stylint --style-guide voice`.
- `stylint/style_guide/formatting.md` - markdown mechanics: headings, code blocks,
  lists, links, asides. Print it with `stylint --style-guide formatting`.
- `stylint/style_guide/code-style.md` - educational code style inside example blocks
  (no defensive `try/except`, no chained `.get()`, one blank line
  between definitions). Print it with `stylint --style-guide code-style`.
- `stylint/style_guide/polish.md` - judgment-level text patterns the script can't detect
  (plain words over abstractions, banned-but-context-sensitive words).
  Print it with `stylint --style-guide polish`.
- `stylint/style_guide/agents.md` - short agent-facing checklist for which
  guide to read at each editing stage. Print it with `stylint --agents`.
- `stylint/style_guide/prompt-abstract-subject.md` - required final-pass
  prompt for abstract nouns used as sentence subjects. Print it with
  `stylint --prompt abstract-subject`.
These style guide docs are bundled in the Python package.

Print their installed paths:

```bash
stylint --style-guide
```

Print one guide directly.

```bash
stylint --style-guide voice
stylint --style-guide formatting
stylint --style-guide code-style
stylint --style-guide polish
stylint --prompt abstract-subject
```

- `stylint/` - mechanical checker package. Edit `BANNED_WORDS`,
  `BANNED_PHRASES`, `BANNED_OPENERS` in `stylint/patterns.py` to
  extend the enforced list.
- `check_style.py` - compatibility wrapper for direct script usage.

## Run the checker

Scan the current directory.

```bash
stylint
```

Scan one file or a specific folder.

```bash
stylint path/to/post.md
stylint docs/
```

Suppress specific rules with `--ignore`.

```bash
stylint --ignore tables docs/
stylint --ignore tables,long-clause-likely docs/
stylint --list-tags
```

Exclude files or folders with `--exclude`.

```bash
stylint --exclude _docs --exclude AGENTS.md docs/
stylint --exclude _docs,AGENTS.md docs/
```

Do not use `--ignore` as a verification check after editing. It is only
for local investigation.

Before calling work done, run the full checker without ignored tags:

```bash
stylint path/to/docs
```

To skip files, drop a `.prose-style-ignore` at the scan root.

Use one fnmatch pattern per line:

```text
# build outputs
_site/*
node_modules/*
# generated docs
docs/api/*
```

Stylint also skips common generated and vendor directories by default. This
includes virtualenvs, caches, build folders, and dependency folders.

## Rule tags

Every finding starts with a `[tag]`. Run `stylint --list-tags` for the current
list. The finding text includes the fix guidance, so the README does not repeat
the rule catalog.

## Reading order for a write-up

Run `stylint --agents` first when an agent edits text.

Use the full guides in this order:

1. `voice.md` while drafting.
2. `formatting.md` for any markdown syntax question.
3. `code-style.md` for example code blocks.
4. Run `stylint` and fix every reported finding.
5. `polish.md` for a final judgment-level pass.
6. `stylint --prompt abstract-subject` as a required final pass for abstract
   nouns used as sentence subjects.

## Hooking it into a project

Add a pre-commit hook from the target project root.

```bash
ln -s ~/git/stylint/check_style.py .git/hooks/post-add-style-check
```

Or run it from CI.

```yaml
- run: stylint docs/
```

## Checks vs judgment

`stylint` prints the mechanical findings. The bundled guides cover tone,
structure, source material, and other judgment calls.

## Drafting in Alexey's voice

The author profile uses the Substack archive to guide AI drafts.

Start with source notes that preserve facts and reasons for decisions:

```bash
stylint --style-guide alexey
stylint --prompt alexey-brief
stylint --prompt alexey-draft
```

Give the brief prompt and your notes to the writing agent. Then give the
resulting brief to the agent with the draft prompt.

For an existing AI draft, use the source brief with the rewrite prompt:

```bash
stylint --prompt alexey-rewrite
stylint path/to/draft.md
```

Use these commands to print prompts, then pass them to your writing agent.
Review the draft against the source after editing. A clean lint result
doesn't establish that the wording sounds like you.

The [archive analysis and Luna experiment](research/alexey-voice/README.md)
include source evidence, original drafts, corrections and observed limits.
The [comparison tool](tools/README.md#voice-comparison) measures reference text
without changing it and runs stylint on AI candidates.

The [100-article Luna experiment](research/luna-100/README.md) extends that
work with two treatments of each of 50 archive articles. It preserves the
drafts and revisions so you can compare the edits.

Two checks came from recurring differences between those drafts and the
reference articles:

- `dense-paragraph-run` flags four consecutive paragraphs with at least
  three sentences and 50 words each, prompting a review of where the
  subject changes.
- `evaluative-framing` flags lead-ins such as "The useful part is" and
  "That was the point", prompting you to state the observation or remove
  the redundant recap.

Print the reasoning and exceptions for either check:

```bash
stylint --explain dense-paragraph-run
stylint --explain evaluative-framing
```

These checks express drafting preferences without attempting to identify
AI authorship.
