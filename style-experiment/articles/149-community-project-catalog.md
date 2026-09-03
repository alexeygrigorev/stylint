# Creating a Catalog of Community Projects

Our 24,000-member course community produces dozens of portfolio projects every
cohort, and they were scattered across 1,412 Slack threads. In April, I built a
catalog so learners could browse finished work before choosing their own. I
wrote this synthetic style exercise with a fictional community name, counts,
dates, and submissions.

The first version was a spreadsheet with 30 rows. It worked for two weeks, then
links expired, screenshots disappeared, and nobody could tell which projects
had a working demo. A catalog needs status fields, not just a pile of links.

In this post, I'll share:

- how submissions enter the catalog,
- how I normalized project metadata,
- how I review entries,
- how the public catalog works,
- what I changed after the first month.

## Collect submissions

I didn't want another form people fill out once and forget. The submission flow
starts in Slack with a shortcut on any thread.

It opens a modal that asks for five things:

- project name and one-sentence description,
- public repository URL,
- demo URL or a short screen recording,
- course module,
- permission to publish the builder's name.

The shortcut sends a JSON payload to a FastAPI service and replies with the
submission ID. If the thread contains a message with an attached image, the
service stores a copy immediately. That fixed the expired-link problem.

During the first month, 68 builders used the shortcut. Eleven submissions were
private repositories, and 6 asked us to list the project anonymously. I kept
those entries in review state rather than rejecting them.

## Normalize the metadata

Free-text descriptions produced unusable categories. One project described "a
chatbot for PDFs", another said "RAG assistant", and a third said "document
question answering". They belonged in the same catalog group.

I created a small canonical vocabulary in the service. The fields are project
type, domain, primary model access, and deployment status. Builders choose from
lists, and the form allows one optional free-text note.

The current groups are:

- retrieval assistant,
- structured data extractor,
- prediction dashboard,
- automation workflow,
- teaching or practice tool.

Each project also gets status values:

- whether a reader can run it today,
- whether tests provide evidence,
- whether the README explains installation.

A separate `needs-help` flag marks projects looking for collaborators.

Normalization is deliberately shallow because I don't try to infer quality from
keywords or stars. Those fields make browsing possible, while human review makes
the catalog trustworthy.

## Review entries

Two volunteer reviewers, Priya Nair and Daniel Ortiz, spend about 45 minutes per
week on new entries.

Their checklist has four checks:

- public links resolve,
- the README explains how to run the project,
- the demo matches the description,
- the builder's permission is recorded.

Reviewers don't judge ambition or design. A modest command-line tool that runs
clearly is more useful to a learner than a beautiful page with no reproducible
demo. If something fails, the reviewer sends the builder a short private note.

I put the review queue in a PostgreSQL table with one row per submission.

Each state change records the reviewer, timestamp, and reason:

```json
{
  "submission_id": 418,
  "state": "changes-requested",
  "reviewer": "priya",
  "reason": "README has no command for loading the sample data"
}
```

In May, 54 entries reached the published state, 9 needed changes, and 5 stayed
private. The median time from submission to publication was 2.4 days.

## Serve the catalog

I generate the public page as a static site with a Python script. I chose that
over another web application because the data changes only after review and the
site needs no login. The generator runs after every approved submission.

I added filters for project type, deployment status, and course module.

Each card contains these fields:

- project name
- creator
- one-sentence description
- repository link
- demo link

If the builder supplied a screenshot, they see a 480-pixel-wide image with
descriptive alt text.

The generator adds three fixed sections to every project page:

- what it does,
- how to run it,
- known limitations.

It extracts those headings from each project's README. When a heading is absent,
the catalog marks the section as missing rather than inventing text.

The site also exposes a JSON feed. Twelve learners used it to build their own
filters in the first month. That was an accident I want to keep: the catalog is
data, and the website is one view of it.

## Improve after use

Feedback from the first month changed two defaults. First, submission now asks
for sample input when the project is a document assistant. Second, the review
checklist requires a limitation line. Almost every useful project had one, but
builders rarely wrote it down.

The most popular filter turned out to be "runs without a paid API key". Twenty
learners selected it in the first week. I hadn't treated that as a first-class
field, so I promoted it from a note into deployment status.

Six builders never answered reviewer questions, so their projects are still
queued. Links decay despite local screenshots. The catalog also omits the amount
of help a project received from a coding agent, which several learners asked
about.

## First-month findings

A catalog succeeds when builders and reviewers pay little to submit and maintain
entries. Canonical fields make the collection browsable, while evidence links
make it credible.

The rule I took from the first month: publish the limitations beside the demo.
That single field made the projects easier to learn from. Next, I plan to add a
quarterly review that marks dead links and invites builders to refresh entries.
Subscribe if you want to see the updated submission form.
