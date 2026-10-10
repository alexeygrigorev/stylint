Use this before and after editing technical text.

The static check (`stylint PATHS`) covers mechanical rules only. A passing
check is one step, not the finish line. Run `stylint --workflow STAGE PATHS`
to print the exact steps for your files. Put every numbered step in your
to-do list, one item each.

## Draft

For AI drafts in Alexey's Substack voice (`profile = "alexey"`), start with
`stylint --style-guide alexey`. Prepare source notes with
`stylint --prompt alexey-brief`, then draft with `stylint --prompt alexey-draft`.
Use `stylint --prompt alexey-rewrite` with the source to rewrite an existing AI
draft. Preserve facts and reasons for decisions before polishing. The author's
requested form takes priority over a fixed template.

Start a new text from the guides and a per-file fix loop.

1. Read `stylint --style-guide voice`, `stylint --style-guide formatting`, and
   `stylint --style-guide code-style` before writing.
2. Write one file.
3. Run `stylint --fix FILE` to fix contractions.
4. Run `stylint FILE`, fix every finding, and re-run it until it passes.
5. Repeat for each file, then go to the final stage.

## Edit

Changing existing text follows the same loop with a narrower reading list.

1. Read the guide for what you change. Use `voice` for paragraphs and
   `formatting` for headings, lists, code blocks, or links. Use `code-style`
   for example code and `polish` for cuts.
2. Make the edit, then run the same fix-verify loop as in the draft stage.
3. Go to the final stage.

## Final

The final stage runs the LLM review passes that no regex replaces.

1. Run each smell prompt as its own review in a subagent, one file or one
   small folder at a time, and don't rewrite inline. Each reviewer reports
   every change as `original -> rewrite`, or "no offenders" per file.
   - `stylint --prompt abstract-subject`
   - `stylint --prompt noun-phrase-smell PATHS`
   - `stylint --prompt empty-rhetoric`
   - `stylint --prompt simplify`
2. Re-run `stylint PATHS` without `--ignore` and fix anything the rewrites
   introduced.
3. Read the text again with `stylint --style-guide polish`.
4. Run the project's own checks, if any. Repos list them in
   `[tool.stylint.workflow] final_steps`.

Report the text as done only when every step has run. Use `--ignore` only for
investigation because it isn't a verification pass.
