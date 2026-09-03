# Indexing Ten Years of Teaching Notes

I wrote this build log as a synthetic style exercise, and all archive details are fictional. In January 2026, I finally processed 1,842 teaching notes from a folder called `teaching-archive`, spanning courses I taught from 2016 through 2025.

The folder had become unusable. Some files lived in year folders, some lived in course folders, and 237 were named `notes-final.txt` or `notes-final-2.txt`.

In this post, I'll share:

- how I normalized the folder without deleting anything
- how I extracted topics, examples, and exercises
- how I reviewed the generated metadata
- how I built a small search index
- what the archive looks like after one term

## Normalize the Folder

The first rule was preservation. I copied the archive to `teaching-archive-processed` and left the old folder read-only. Every later script wrote into the copy.

The normalization script created one directory per course, then one directory per year inside it. It preserved the original relative path in a YAML header so every derived file could point back to its source.

For a file called `sql-window-functions.txt`, the header looked like this:

```yaml
source: 2018/data-engineering/notes-final-2.txt
course: Data Engineering
year: 2018
language: en
sha256: 9f14c8d2
```

The checksum let me prove that normalization changed whitespace and encoding only. A diff report initially showed 611 modified files, mostly line endings and smart quotes.

I also split 412 long notes at headings or blank-line boundaries. Each fragment kept the source path and an offset, so no sentence lost its position. The target size was 300 to 900 words because that fit both search results and later review.

After two evenings, the copy had 3,118 normalized fragments and no duplicate filenames.

## Extract Structure

Next, I used a local model to classify each fragment. The prompt asked for topic, audience, examples, and exercises. I supplied 30 manually labeled fragments for reference.

The prompt set stable labels with this instruction:

```text
Return JSON with keys topic, audience, examples, exercises.
	topic must be one of the labels in topics.txt.
Use empty lists when a field is absent.
Do not invent content that is absent from the note.
```

The classifier labeled 2,905 of 3,118 fragments on the first run. I reviewed all 213 low-confidence cases, plus 150 randomly selected confident cases, over three sessions.

Fourteen confident labels were wrong, mostly because a note about SQL execution plans also discussed visualization. That gave a measured accuracy of about 91% on the sample. I corrected the prompt, reran only those 164 files, and stored every model version in the metadata.

Examples and exercises were harder than topics. The model found 1,744 examples and 886 exercises, but it initially treated every command as an exercise. I added a rule that an exercise had to ask the learner to produce something.

## Review Metadata

Manual review stayed in the loop because a teaching archive fails quietly. A wrong label makes useful material disappear from a future search.

I generated a review queue as CSV with one row per uncertain file. The columns showed the topic, confidence, source path, and the first 240 characters. I marked each row accept, edit, or reject.

The review script then wrote only the accepted changes:

```bash
python scripts/apply_reviews.py reviews/2026-02-11.csv
```

It created an undo file before modifying metadata and refused to run if the CSV referenced a checksum that no longer matched. That prevented me from applying decisions to a file I had already edited.

After the first full pass, 61 topics remained ambiguous, so I created two new labels: `career-advice` and `course-logistics`. The archive improved because the labels followed the material instead of forcing every note into the first taxonomy.

The final metadata file is 1.1 MB and plain YAML. I can read it with standard tools, diff it in Git, and regenerate the index without retaining the model. That was the outcome I wanted from extraction.

## Build Search

The search index combines lexical and semantic search. SQLite with FTS5 handles exact words and course names, while a 384-dimensional embedding model handles natural-language questions.

I kept the implementation boring. A Python script reads each YAML file, inserts the fields into SQLite, computes one embedding, and stores it as a compact binary blob. The complete rebuild takes 9 minutes on my laptop.

The query path first runs FTS5. If it returns fewer than five results, it runs semantic search and merges the two lists. Each result displays the topic, year, source path, and a highlighted fragment.

The first useful query was practical:

```bash
python teach.py search "pandas groupby exercise" --topic python --after 2020
```

It returned seven fragments from three courses and showed that I had reused the same airline-delay dataset in 2020, 2022, and 2024. That repetition was invisible in the old folder.

## After One Term

I used the index while preparing an eight-week data engineering course. It replaced about six hours of manual searching across ten weeks with perhaps 90 minutes of indexed lookup and review.

I found 27 old exercises I had forgotten, including three that fit the new cohort better than anything in the current slides. I didn't only save time.

The system still has limits. Handwritten scans from 2016 and 2017 are indexed only by filename. Two old course folders use inconsistent module names, so their topic labels need another review pass.

My rule from the project: extract enough structure to retrieve an idea, and preserve enough source detail to distrust the extraction when needed.

I'll write separately about the merge query and the exercise reviewer. Subscribe if you want the next article in this teaching-archive series.
