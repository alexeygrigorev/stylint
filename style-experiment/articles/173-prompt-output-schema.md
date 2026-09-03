# Constraining Prompt Output with a Simple Schema

This synthetic style exercise describes a fictional prompt project with invented field names. All names, counts and dates below are fictional, and no real events are reported.

Last November I asked a coding agent to draft release notes from 40 commit messages. The output arrived as chatty paragraphs with version numbers buried in prose, and my parser extracted the wrong date from three releases. I spent an hour fixing notes that should have taken ten minutes.

I first tried a longer prompt with formatting instructions in bold caps. That approach reduced chatty openers while leaving version strings unpredictable, and two releases still shipped with swapped fields. After the second bad release I stopped tuning words and added a schema with validation.

The schema pass took one afternoon and cut field errors to zero across the next 30 releases. Every output now arrives as JSON with fixed fields, and a validator rejects bad drafts before they reach the notes. The steps below show the exact setup.

In this post, I'll share:

- how I name fields and types before writing the prompt
- how I show two examples the model can copy
- how I validate output and retry failures
- how I build a fallback for invalid drafts
- what the setup costs and where it still falls short

## 1. Name Fields And Types First

I start by listing the fields the release notes need, with one type per field. For my notes, I chose version as a string, date as a YYYY-MM-DD string, changes as a list of strings and breaking as a boolean. Four fields cover the notes, and no extra keys are allowed.

I store that list in a JSON Schema file so both the prompt and the validator read the same source. I keep the file at `schemas/release.json` in the repo root:

```json
{
  "type": "object",
  "required": ["version", "date", "changes", "breaking"],
  "properties": {
    "version": {"type": "string"},
    "date": {"type": "string"},
    "changes": {"type": "array"},
    "breaking": {"type": "boolean"}
  }
}
```

I show the schema to the model inside the prompt rather than describing it in prose. Descriptions drift between prompt and validator, while a shared file stays identical. That single read step removed a whole class of mismatches.

Skipping this step caused my original mess. I had described fields in sentences, so the model returned `release_date` once and `date` the next time. Fixed names in a shared file ended that variation in one edit.

## 2. Show Two Copyable Examples

With fields fixed, I add two full examples of correct output to the prompt. One example shows a routine release with three changes, and the other shows a breaking release with a migration note. Both examples use the exact keys from the schema file.

I keep examples short so they fit the context window without crowding the task. Each example stays under 15 lines, and both use fictional versions that never match real releases:

```text
{"version": "0.4.0", "date": "2026-02-10", "changes": ["add CSV export", "fix date sort"], "breaking": false}
{"version": "0.5.0", "date": "2026-03-02", "changes": ["rename date_col"], "breaking": true}
```

I place the examples after the schema and before the commit list in the prompt. That order matters because the model copies the last structure it sees, and the commits come last as raw data. Swapping the order once produced chatty output again, so I keep examples adjacent to the task.

Two examples beat five in my tests. Five examples pushed the prompt past 2,000 tokens and slowed responses by 40 percent, while two examples held the same accuracy across 30 trial runs.

## 3. Validate Output And Retry

I never trust model output without a validation pass in code. A ten-line Python check, a function that loads JSON and checks keys, runs on every draft before it reaches the notes. It uses the same schema file the prompt references.

The check runs from one command after each generation:

```bash
uv run python scripts/validate_notes.py --draft /tmp/draft.json
```

The command prints `ok` plus the version string, or it prints the first failed rule. Across the last 30 releases, 24 drafts passed on the first try and six needed one retry. No draft needed more than two tries after I added the second example.

I retry with the error message appended to the prompt rather than starting over. The retry prompt includes the failed draft plus one line naming the broken rule, and the model usually repairs that rule alone. That targeted retry costs fewer tokens than a fresh generation.

## 4. Build A Fallback Path

Six retries still leave the chance of a stubborn draft, so I added a fallback that never calls the model. The fallback writes a minimal notes file with the version, the date and the raw commit subjects as bullets. It cannot produce wrong fields because it copies strings without interpretation.

The fallback runs automatically after two failed validations. I wired it into the same script that validates, so no manual step decides between retry and fallback:

```python
if errors and attempts >= 2:
    write_minimal_notes(version, date, subjects)
```

That branch ran twice in 30 releases, and both notes needed only light editing. The minimal file reached reviewers on time, which beats a clever draft that arrives late. I review fallback notes first because raw subjects sometimes include typos from commits.

I log every fallback with the failed rule attached. Both fallbacks failed on the date format, which told me the date example needed emphasis. I bolded nothing and instead added a comment line above the example showing the format.

## 5. Keeping The Working Parts

The setup now runs in about four minutes per release. Generation takes two minutes, validation takes seconds and the changelog edit takes the rest. Field errors dropped from five per 40 releases to zero per 30 releases, and no bad notes reached users since November.

The work taught me a narrower lesson than "constrain every prompt". Schemas pay off for outputs that code must read, while free prose still suits summaries that humans read once. I now add a schema only when a parser or a template consumes the output.

Gaps remain around long commit lists and vague messages. Lists past 60 commits overflow the window, and one-line messages like "fix stuff" produce thin notes. My next addition splits long lists into chunks with one draft per chunk.

I'll write about that chunking step in a future post. If you want to follow along, don't forget to subscribe.
