# Noun-smell calibration tools

These are calibration tools (not linters) for building good/bad example sets
for the noun-smell review prompts. The pipeline is: **scan → review → merge →
label**.

## Pipeline

1. **Scan** the corpora for candidate lines (over-collects on purpose):

   ```bash
   python3 tools/noun_smell_scan.py --root <corpus-dir> --out /tmp/noun-smell-candidates.json
   ```

2. **Review** — subagents classify each candidate (keep/bad + reason +
   rewrite), writing one review JSON per source/smell slice.

3. **Merge** the subagent review files back into the candidate set:

   ```bash
   python3 tools/noun_smell_merge_reviews.py \
     --review /tmp/noun-smell-review-workshop-abstract.json \
     --review /tmp/noun-smell-review-telegram-concrete.json \
     --out /tmp/noun-smell-reviewed.json
   ```

4. **Label** — a human marks each phrase Good / Bad / Skip in the review app
   (below). Labels save into the `human_label` field of the data file.

## Labeling app

`noun_smell_review_app.py` is a tiny local HTTP server that serves the merged
dataset for human labeling.

```bash
python3 tools/noun_smell_review_app.py --data .tmp/noun-smell-reviewed.json --port 8765
# then open http://127.0.0.1:8765
```

- **Good / Bad / Skip** buttons plus a free-text note per item.
- The **Status** filter defaults to `unlabeled`; use Source / Smell to narrow.
- Every label writes straight back into the `--data` file (the `human_label`
  and `human_note` fields), so commit that file to save your work.

## Data

The current labeling dataset lives at `.tmp/noun-smell-reviewed.json` (256
phrases, each with an agent classifier label). It is committed so it survives
across machines — re-commit it after labeling to preserve human labels.

## Voice comparison

`voice_compare.py` measures paragraphs in a reference corpus and an AI
candidate corpus. It runs the current default stylint checks on candidates
only. It never edits either corpus or lints the reference text.

Run it from the stylint checkout:

```bash
uv run python tools/voice_compare.py \
  --reference ../telegram-writing-assistant/reference/substack \
  --candidate research/alexey-voice/output/experiment/corrected \
  --output /tmp/voice-comparison.json
```

The JSON includes per-file SHA-256 hashes, descriptive features, corpus
medians, and candidate findings by tag and line. Findings don't set the
tool's exit code because this tool generates a report. Use the regular stylint command
for a pass/fail verification of generated drafts.

The parser measures paragraph text after removing structural Markdown
blocks and standalone links. It retains inline code identifiers
and link labels, along with captions and newsletter backmatter. It's an
approximate parser, so abbreviations and unusual Markdown can affect sentence
counts. Aggregation uses an unweighted median of document features,
excluding empty documents.

Compare similar genres and lengths when interpreting the measurements.
There's no combined voice score, and similarity doesn't establish human
preference. The [experiment report](../research/alexey-voice/README.md) records
the tested prompts and the limits of the current examples.

## Mining generated drafts

`voice_mine.py` compares an assigned generation round with its source
articles. It reads the experiment manifest and keeps development and
reserved sources separate. It also reports full stylint findings on drafts.

```bash
uv run python tools/voice_mine.py \
  --manifest research/luna-100/output/manifest.json \
  --round round-1 --split development \
  --output /tmp/luna-development.json
```

Use `--split holdout` after freezing rule choices, or `--split all` to
compare completed revision rounds. Missing assigned drafts cause an error
unless you pass `--allow-partial` for a progress report.

The report includes phrase prevalence and sentence shapes for review.
It lists exact source sentence overlaps of at least 12 words, plus sentences
shared by at least three drafts. Read matches before deciding whether
they represent copying or an unwanted writing habit.

The tool never adds rules or edits articles, and phrase frequency alone
doesn't justify a ban. Two drafts from one source are related observations, and
article length affects comparisons with the references. The
[100-article report](../research/luna-100/README.md) records those limits.
