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
