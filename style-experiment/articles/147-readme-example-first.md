# Writing a README Around the First Useful Example

Last October I reviewed 38 portfolio projects for a hiring committee. Twenty-six
README files explained the author's goals in detail, while 17 left out the
commands needed to run the project. I wrote this synthetic style exercise with
fictional project names, counts, dates, and repository contents.

The review pushed me to rewrite the README for `outline-kit`, a small Python
library that turns meeting notes into an article outline. I had written an
ambitious introduction and buried the useful part on line 74. The rewrite took
three hours and made the project much easier to try.

In this post, I'll share:

- how I found the first useful path,
- how I ordered the opening sections,
- how I wrote runnable installation steps,
- how I documented the expected output,
- how I handled limitations and maintenance.

## Find the useful example

I started with the user's first successful moment. For `outline-kit`, that
moment is turning a plain text file of meeting notes into a numbered outline and
saving it as Markdown. Everything else comes after that.

Then I wrote the command I wanted a new user to run:

```bash
outline-kit notes.txt --format markdown --output outline.md
```

That command exposed three missing decisions:

- the supported Python versions,
- the accepted input formats,
- what the output contains.

Those were exactly the questions two reviewers had asked on the repository.

So I made the example smaller and more concrete, using a six-line input file
called `notes.txt`. The user can see the boundary between input and output
without reading the package internals.

## Put the promise first

I replaced the old paragraph about workflow automation with two sentences.
`outline-kit` turns unstructured meeting notes into an editable outline, and it
works locally with OpenAI-compatible APIs.

After the promise, I added a minimum status block:

- Python 3.11 or 3.12,
- an OpenAI-compatible endpoint,
- one text file of notes.

I resisted a feature list. The library has 14 command-line options, and 11 of
them are tuning choices. The first screen should tell readers what problem the
tool solves and what they need, so they can decide within 30 seconds.

I also moved the installation badge and test badge below the opening. Badges can
confirm a claim, but they don't replace the command a reader actually needs.

## Make installation runnable

The original installation section said "install from PyPI", followed by a
detailed development setup. A reader who only wanted to try the tool had to
guess whether both steps were required.

I wrote two paths into the rewritten section. The first uses `pipx`, a tool for
installing Python command-line applications in isolated environments. The second
shows a local development checkout for people who want to change the code.

The primary path is now three commands:

```bash
pipx install outline-kit
export OUTLINE_KIT_API_BASE="http://localhost:11434/v1"
export OUTLINE_KIT_API_KEY="local-key"
```

Every variable has a sentence beside it. The API base can use Ollama, a tool for
running local models, or another OpenAI-compatible service. The key is required
by the client even when the local server doesn't validate it.

I also added the uninstall command. It takes one line and answers a reasonable
question after someone tries a tool they don't want to keep.

```bash
pipx uninstall outline-kit
```

## Show the expected output

The most useful addition was the output file. Without it, readers had to install
the package to learn what it did. I added a complete example for a tiny input to
the README.

The input is:

```text
Team sync, 14 March
Maria: search latency doubled after the index update.
Sven: reproduce it with the staging corpus.
Decision: roll back this week and profile the new analyzer.
```

The output contains a one-line summary, three main points, and a next-actions
section. I copied an actual generated file into the README.

Then I changed the names:

```markdown
# Outline

## Summary
The team found a search latency regression and chose a rollback.

## Points
1. Search latency doubled after the index update.
2. Staging data can reproduce the regression.
3. The team will roll back and profile the new analyzer.

## Next actions
- Roll back the index this week.
- Profile the analyzer against the staging corpus.
```

Below the block, I state what varies. The model may phrase the summary
differently, and it may choose four points instead of three. The reader can
judge whether that variability is acceptable before installing anything.

## Keep limitations visible

I documented three limitations in the final section:

- `outline-kit` works best on notes under 2,000 words,
- it doesn't join separate meetings into one narrative,
- it requires an endpoint but never sends notes outside that endpoint.

Each limitation has a reason:

- the prompt and parser are tuned for one meeting,
- the output has no cross-meeting timeline,
- privacy depends on the endpoint the user selects.

I also added a short support policy. Bug reports should include the input file,
command, package version, and provider name. The maintainer responds to issues
on weekends, and the current version is supported until at least June 2027.

I also documented our maintenance rules. Breaking changes to the command-line
interface require a major version, while prompt improvements may change output
wording inside a minor release.

## Closing note

A README is a route into the project, and the route should start at the first
useful command. The opening promise earns attention, installation turns it into
a working program, and expected output lets someone decide without running
anything.

The rule I took from the rewrite: write the README around the path a reader can
finish in five minutes. I plan to use the same structure for my other small
tools this year. Subscribe if you want to see the updated template.
