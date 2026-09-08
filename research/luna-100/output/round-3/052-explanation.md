# Using Retrieval to Maintain an FAQ

A retrieval workflow can help maintain a knowledge base, not only answer questions from it. The FAQ Automation Bot starts with a simple contribution: a student opens a GitHub Issue and provides a course, question and answer. GitHub Actions then turns that proposal into a structured review process around the existing FAQ.

## Retrieve before deciding

The agent first loads the current FAQ entries and course metadata from the repository. It builds a minsearch index using `section`, `question` and `answer` as text fields, with `course` and `section_id` as keyword fields.

When a proposal arrives, the model doesn't receive it in isolation. The agent searches the current FAQ for similar entries and keeps the relevant matches. It then builds the prompt from three parts: the new proposal, the matching FAQ entries and the section metadata for that course. Retrieval gives the model the local context needed to decide how the proposal fits the existing knowledge base.

This step supports several maintenance decisions. A similar entry may already answer the question, and a proposal may add information to an existing answer. A new question may need a different section from the one suggested by its wording. Searching the current records gives the decision model concrete material to compare.

## Return a structured decision

The model returns a Pydantic object called `FAQDecision` instead of free-form text, and its `action` is `NEW`, `UPDATE` or `DUPLICATE`. The object can also contain rationale, document and section IDs, section rationale and order. It can include normalized question text, proposed content, a filename slug and warnings.

The workflow uses that decision to change the repository. A `NEW` action can create a FAQ file, an `UPDATE` can modify an existing entry and a `DUPLICATE` can close the issue with feedback. When a file change is needed, GitHub Actions opens a pull request for review.

The student therefore fills out a short issue form, while the automation handles searching, section selection and repetitive repository work. The FAQ remains a collection of Markdown files under version control, so the generated website and other consumers still use the same maintained records.

## Keep a person in the loop

The agent can make mistakes. A proposal about Kestra may land in the general section instead of the workflow orchestration module. A retrieved match may look similar while describing a different problem, leading the agent to merge the proposal into the wrong FAQ.

The default triage model is gpt-5-nano, which keeps routine classification inexpensive. That doesn't make automatic merging safe. I review batches of pull requests with Claude Code. I explain a correction, Claude edits the branch, and I review and merge the result.

This workflow separates the jobs cleanly. Retrieval finds relevant existing material, and the structured decision records what the model wants to do. GitHub Actions prepares the repository change. Human review decides whether the proposed change is actually correct.

Students get an easy contribution path while the FAQ's maintained version stays under review.
