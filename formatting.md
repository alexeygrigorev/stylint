# Formatting and markdown mechanics

Read this when adjusting markdown syntax, code blocks, headings, lists,
or links.

## Hard formatting rules

Apply these as you write. Items marked `(script)` are also enforced by
`check_style.py`; the rest are agent judgment.

- No bold, no italic, no horizontal rules `---`. Emphasis comes from
  sentence structure. (script)
- No tables. Use bullet points instead. (script)
- No em dashes. Use ` - ` (hyphen with spaces) or rewrite. (script)
- Use ` - ` with spaces around dashes, not `-`.
- Use straight quotes (`'` and `"`), never curly/smart quotes. (script)
- One dash per sentence. If you are reaching for two dashes to insert a
  parenthetical, split the sentence instead.
- Code ticks around every code-like identifier: filenames (`.env`,
  `app.py`), function names (`run_agent`), class names (`AsyncOpenAI`),
  env vars (`OPENAI_API_KEY`), module names (`minsearch`), regexes.
- No backticks inside link text - write `[search.py](url)`, never
  `` [`search.py`](url) ``. (script)
- No consecutive code blocks; every code block needs prose before or
  after it. (script)
- Block quotes (`>`) are allowed for asides and warnings.
- Leave a blank line between the closing `---` of YAML frontmatter and
  the body. The frontmatter should not look like it runs straight into
  the first paragraph. (script)

## Headings

- `#` once at the top for the title.
- `##` for every major section. This is the default.
- No `###` or deeper.
- No questions as headings: do not start with `Why`, `How`, `What`, `When`,
  `Where`, `Which`, `Who`, and do not end with `?`.
- No emoji prefixes on headings.
- Do not number headings (`## 3. Part 1...`) unless you have a table of
  contents that uses the same numbers - then the numbers must match.

Section sizing: each `##` section should be substantial - multiple code
blocks, multiple paragraphs of explanation. If a section has one code block
and two sentences, merge it with a sibling.

## Code blocks

- Always specify a language: ` ```python `, ` ```bash `, ` ```yaml `,
  ` ```dockerfile `, ` ```makefile `. For plain output, prompts, folder
  trees, and `.env` examples, use ` ```text `.
- Keep each block short (10-20 lines target, 40 hard max). Split longer
  code into multiple blocks with prose between each part. A 30-line
  dataclass that is read once is fine; a 30-line function that does four
  things should be four blocks.
- Never two code blocks in a row. Every code block needs at least one
  sentence of prose before or after it.
- Every code block and every list needs a lead-in sentence (often ending
  in `:`). Do not put a code block or list directly under a heading with
  no prose between.
- Import statements live in the block where the library is first used. Do
  not group imports in a separate cell at the top.
- Import each library once per write-up. If you need it again later, assume
  the reader already has it.

For shell commands shown as copy-paste instructions:

```bash
uv add fastapi uvicorn
```

For shell session transcripts where input and output matter, use
` ```console ` and a `$` prefix on the command, so syntax highlighting does
not color the output as code.

`check_style.py` enforces the language tag, the 40-line max,
no-consecutive-code-blocks, and the lead-in rule.

For code style inside example blocks (defensive coding, blank-line
spacing), see `code-style.md`.

### Block splitting for pacing

Separate a class or function definition from its instantiation or
first call. A block that ends with `class NotebookRenderer: ...` and
then has `renderer = NotebookRenderer()` on the last line forces the
reader to scan to the bottom of a long block to find the thing that
actually runs. Two blocks with one sentence between them read faster:

```python
class NotebookRenderer:
    async def handle_event(self, event_type, payload): ...
    # (handlers omitted)
```

Then:

```python
renderer = NotebookRenderer()
```

The same rule applies to a helper function you define and then
immediately call. Define once, show usage next.

## Links

- Relative links between files in the same folder are fine.
- Do not link into unrelated repos by relative path. For external
  references, use a full URL.
- External links use descriptive text, not `click here` or `link`.
- Readers see the published markdown pages, not the local source checkout
  used to prepare them. Do not say `local source`, `source material`, or
  `the source folder` as if the reader can browse your machine. If a reader
  needs a reference file, either include the relevant code inline or link to
  the public GitHub file or folder with a full external URL.
- Do not use local-repo authoring phrases like `in your checkout`, `inspect
  it in your checkout`, `local checkout`, `source checkout`, or `open it in
  the reference repo or...`. They sound like internal maintenance notes. Use a
  direct reader-facing sentence instead: `The reference implementation has two
  main files: [App.jsx](...) and [SnakeGame.jsx](...).`
- Prefer `look at` over `inspect` when talking to the reader. `Inspect`
  sounds like a tool trace or code-review command. `Look at the messages`
  reads like normal prose.
- Prefer `To learn more` over `For follow-up reading`. It is shorter,
  direct, and sounds like an invitation rather than a bibliography note.

## Lists

Unordered lists use `- ` (dash + space). Ordered lists use `1.`, `2.`, `3.`.

- Use bulleted lists when the reader wants to scan.
- Use numbered lists only for sequential steps.
- One item per line. No nested bullets unless the nesting is load-bearing.
- Keep item text short - one line each when possible. If one item needs a
  paragraph of explanation, pull it out into prose instead.

## Asides and warnings

Use block quotes for small warnings or asides that are worth pulling out of
the prose. Keep each one to one short paragraph - if the aside runs longer,
it is not an aside, it is a subsection.

```markdown
> The async Responses API expects `arguments` as the original JSON string,
> not as a parsed dict. If you re-serialize, OpenAI rejects the next request.
```
