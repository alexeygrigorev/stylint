Use this before and after editing technical text.

1. Run `stylint --style-guide voice` before rewriting paragraphs: tone, cuts,
   and how personal the writing should be.
2. Run `stylint --style-guide formatting` when changing headings, lists, code
   blocks, links, captions, or callouts.
3. Run `stylint --style-guide code-style` when editing example code or command
   snippets.
4. Run `stylint --style-guide polish` for the final pass: fluff, abstractions,
   bridges, redundant setup, and topic-introducer sentences.
5. Run `stylint --prompt abstract-subject` and apply it to the edited files.
   This required judgment pass catches abstract nouns used as sentence
   subjects, which the mechanical checker can't catch reliably.
6. Run `stylint --prompt noun-phrase-smell` and apply it to the edited files.
   This required judgment pass catches concrete noun phrases that hide the
   person, decision, sequence, or design constraint.
7. After editing, run the full `stylint` check without `--ignore`.

Use `--ignore` only for investigation because it isn't a verification pass.
