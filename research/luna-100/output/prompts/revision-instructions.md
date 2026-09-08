# Round 2 revision assignment

Read the assigned source article, corresponding fact brief, original round-1 draft, and round-2-prompt-alexey-rewrite.md plus round-2-alexey.md. Revise the article in Alexey's voice. The source is authoritative; the brief may contain mistakes from the first pass. Preserve the original files and write only round-2 outputs and review sidecars.

Check facts before style. Preserve attribution, personal motives, uncertainty, numbers, technical behavior and sequence. Remove invented claims and unsupported enthusiasm. Never convert an editorial instruction into a disclaimer in the article. Treat the articles as historical reconstructions of the source publication date.

Aim for 450–750 whitespace-separated words, with a meaningful title. Revisions may be 400–750 words when cutting repetition leaves a complete article. Restore useful omitted source details if needed, but never add padding or generic advice to reach the nominal target. Do not copy full source paragraphs. Preserve the requested account/explanation form. Avoid boilerplate or canned openings/endings across articles.

Use the paragraph boundaries in the source as a guide: separate the need, attempt, observation and decision when the subject changes. Keep related sentences together. New dense-paragraph-run findings are not an instruction to add empty headings or simply alternate paragraph lengths. Remove vague evaluative lead-ins and redundant recaps instead of replacing them with other framing.

Run full `uv run stylint <your output file>` without --ignore. Fix findings in context, rerun, and check source fidelity again. Mechanical changes such as straight quotes, contractions, spelling code identifiers and punctuation can be scripted, but all substantive rewrites must be composed and inspected. Do not drop facts to clear findings. Do not edit checker code or prompts.

For each article write round-2-reviews/NNN.json with source path, original path, revised path, word count, required facts checked, unsupported claims removed, substantive edits, full final lint findings, and any unresolved source conflicts. These are agent reviews, not human approvals. Aim for zero findings with source meaning preserved; report an unavoidable conflict rather than hiding it.

Known examples to watch for: a first draft invented an empty commit history for abandoned repositories, and another copied an attribution instruction as 'I am a reader, not its creator.' The minsearch source says the author would probably choose Elasticsearch for a normal production system. Preserve that qualifier rather than claiming universal production suitability.
