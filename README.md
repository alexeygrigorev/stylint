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
stylint --workflow
stylint --workflow final docs/
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
- `stylint/style_guide/agents.md` - the agent workflow (draft, edit, final)
  as a readable document. `stylint --workflow STAGE PATHS` prints the same
  steps with your file names filled in.
- `stylint/style_guide/prompt-abstract-subject.md` - required final-pass
  prompt for abstract nouns used as sentence subjects. Print it with
  `stylint --prompt abstract-subject`.
- `stylint/style_guide/prompt-empty-rhetoric.md` - required final-pass
  prompt for sentences that sound punchy but carry no content:
  throat-clearing announcements, mirrored short-aphorism pairs,
  manufactured decisiveness, and redundant recaps. Print it with
  `stylint --prompt empty-rhetoric`.
- `stylint/style_guide/prompt-simplify.md` - required final-pass prompt that
  makes text easier to read for readers whose first language may not be
  English: literal words over idioms, direct claims over clefts, terms
  defined on first use. Print it with `stylint --prompt simplify`.
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

A passing check covers the mechanical rules only. Every run ends with a
`Next:` footer that lists the remaining steps. Hide it with `--no-next` or
`STYLINT_NO_NEXT=1`, for example in CI.

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

## Agent workflow

Agents tend to run the static check, fix the findings, and stop before the
LLM smell passes and the final re-check.

`stylint --workflow` prints the ordered steps for each stage:

```bash
stylint --workflow                  # overview of the three stages
stylint --workflow draft docs/      # guides, then a fix-verify loop per file
stylint --workflow edit docs/       # the same loop for changes to existing text
stylint --workflow final docs/      # smell passes, re-check, repo checks
```

With paths, the commands name your files and end with the current static
status. The final stage lists every smell prompt from `stylint --prompt` and
asks for one subagent per prompt. Then it lists a re-check, a polish read, and
the repo's own checks. `stylint --agents` prints the overview.

The exit codes don't change. A static run exits 0 when it passes, 1 with
findings, and 2 on bad usage. The footer says "Not done yet" on a pass, so a
clean check doesn't read as the end of the job.

## Configuration

Stylint reads `[tool.stylint]` from the nearest `pyproject.toml` that has
one, or from the nearest `.stylint.toml`. It searches upward from the first
path, or from the current directory.

```toml
[tool.stylint]
author_name = "Alexey"     # default for --author-name
profile = "alexey"         # adds the alexey-brief/draft step to the draft stage
exclude = ["_docs", "AGENTS.md"]

[tool.stylint.workflow]
smell_prompts = ["abstract-subject", "noun-phrase-smell", "empty-rhetoric", "simplify"]
final_steps = [
  "uv run python scripts/check_workshops.py",
  "Walk _docs/05-01-checklist.md",
]
```

CLI flags override the config, and `--exclude` adds to the configured
patterns. In `.stylint.toml`, put the keys at the top level and the workflow
keys under `[workflow]`.

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
