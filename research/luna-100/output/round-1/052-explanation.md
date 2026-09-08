# Using retrieval to maintain an FAQ

Retrieval augmented generation is often introduced as a way to answer questions over documents. The DataTalks.Club FAQ shows another use: retrieval can help decide how a new contribution should change the knowledge base.

The workflow begins with a GitHub Issue. A student fills in the course, question, and answer. The automation loads the existing FAQ entries and course metadata, then builds a minsearch index with section, question, and answer as text fields. Course and section identifiers are keyword fields. The proposal is searched before it reaches the model, so the model receives comparable entries rather than an isolated suggestion.

The prompt contains three parts: the new proposal, the closest existing FAQ records, and metadata describing the course section. The model returns a structured Pydantic object called `FAQDecision`. Its action is `NEW`, `UPDATE`, or `DUPLICATE`. It also identifies the document and section, explains the choice, chooses an order, writes normalized question and answer text, proposes a filename slug, and can include warnings.

The workflow then acts on that decision. A new entry becomes a Markdown file. An update changes an existing file. A duplicate closes the issue with feedback. If a file must change, GitHub Actions opens a pull request. A human reviews and merges it. The student uses a form while the repository receives a reviewable change.

This only became practical after the FAQ moved from Google Docs to Git. Google Docs had made contribution easy, but it was difficult to moderate and became unwieldy at around 1,300 entries. The Git repository stores separate Markdown files with frontmatter and generates a static website. A custom Python generator was used because Jekyll interpreted dbt’s Jinja syntax as its own Liquid templates. The generator also exports JSON, so the same records can feed search systems.

Retrieval helps at several points. It finds related entries, identifies possible duplicates, suggests an update target, and provides context for choosing the correct module. That last part matters because surface similarity can be misleading. A question about Kestra may look general but belong in workflow orchestration. The model can make that mistake, so the system keeps a human gate.

The review loop is deliberately simple. I list open pull requests, ask Claude Code to inspect one branch, describe the correction, and review the edited result before merging. This is faster than building every edge case into the GitHub Actions workflow. It also produces examples of failure: wrong section, wrong merge target, or an undetected duplicate. Those examples can later be included in the prompt.

The system uses a small model, gpt-5-nano, for routine triage and a stronger model only during review. That keeps the automation inexpensive while preserving a person’s judgment for changes to the source of truth. The pattern is useful beyond FAQs: retrieve existing records, ask for a structured decision, create a reversible change, and keep human review where classification can affect the whole collection.
