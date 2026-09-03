# Moving a Teaching Notebook into a Small Python Library

I wrote this piece as a synthetic style exercise. The project details are invented, while the workflow mirrors my real extraction process.

In February 2026, I taught a four-week retrieval course with one 940-cell Jupyter notebook. Students liked the examples, but the notebook was already overloaded by then. By the third cohort it served as the syllabus, demonstration, exercise set, and grading script. I extracted the reusable pieces into `retrypipeline`, an internal library for loading, chunking, and evaluating small text collections.

In this post, I'll share:

- how I chose the boundary for the library

- how tests exposed hidden assumptions in the notebook

- the release and documentation steps

- why I kept the notebook after publishing the package

- what I would change in the next extraction

## Find the reusable path

My first instinct was to move all 940 cells into modules. That idea lasted about 20 minutes. I had mixed course narrative, dead experiments, demo data, and four genuinely repeatable operations in one file. Moving everything would have published my teaching scaffolding as an API.

So I counted cell purposes across the notebook:

- 340 cells contained course text and transitions

- 280 cells were demonstrations with hard-coded examples

- 188 cells were student exercises

- 132 cells defined functions with no interface to a lesson

The useful boundary was the final group. Those functions loaded JSONL records, split long documents, built a simple inverted index, and ran retrieval. A separate helper calculated hit rate and mean reciprocal rank. Students had copied the functions into two homework templates, and that reuse convinced me to extract them.

## Extract with tests first

I started with a 14-case characterisation test suite. A characterisation test records current behavior before I change the code. It didn't express the ideal design, but it stopped me from accidentally changing course results while I moved files.

I found a chunking function with an argument called `overlap`. It silently allowed an overlap larger than the chunk size. I wrote two tests that reproduced the behavior, and the resulting chunks were nearly empty. I changed the library to raise `ValueError` with a short message instead.

That decision changed one exercise. Three students had used the bad configuration as an accidental edge-case demo. In the next cohort, I turned their discovery into an explicit lesson about validating inputs. A silent failure in teaching material becomes a future debugging lesson.

The load function also assumed every record had fields named `id` and `body`. Tests with a 2,000-row synthetic corpus made that assumption obvious. I added optional field-name arguments, and the public surface became five functions plus one `SearchResult` dataclass.

## Package and document

Once tests passed, I moved the code into `src/retrypipeline/` and created a `pyproject.toml` file. I kept the dependency list intentionally small. `numpy` handles score calculations, while `pydantic` handles input validation.

I wrote a 25-line README example and explained the evaluation metrics in six sentences. I also added a `CHANGELOG.md` file because the course exercises reference exact behavior. For version 0.1.0, I didn't promise long-term compatibility.

The build command produces both distribution formats:

```bash
uv build
```

The wheel and source archive went into `dist/`. A check with `twine` caught a malformed project description on the first attempt. I fixed the metadata and published version 0.1.0 to our internal package index that evening. Total extraction time was 17 hours across six days, including tests and documentation.

I spent another hour deciding whether to rename `run_search` to `retrieve`. I changed it back after reading the homework prompts because the lesson used "retrieve" throughout. Consistency with the course mattered more than my preference.

Documentation took longer than the code. I wrote the metrics section four times before I could explain mean reciprocal rank without hiding the ranking step. Each version used a smaller example, and the final one lists the retrieved document IDs before it calculates the score.

I also asked two teaching assistants to install the package from a clean directory. Their first attempt failed because the README omitted one environment variable. Adding that line prevented the same ten-minute confusion for every student.

## Keep the notebook

Some engineers treat the notebook as something to eliminate, but I kept it and changed its role. It's now a course companion and integration example, with 410 cells instead of 940.

At the top, I import `retrypipeline` and use only public functions in notebook cells. When I want to demonstrate an idea, I can still modify a variable and see the output beside the explanation. That feedback loop is valuable in teaching, and a plain function call doesn't replace it.

I added one guardrail to catch broken notebook cells. A 30-line script runs through the notebook with `nbconvert`, executes every non-exercise cell, and fails if output contains a traceback. The guardrail runs in GitHub Actions and takes 72 seconds.

This setup keeps both artifacts useful. The library owns reusable behavior, while the notebook owns the narrative and demonstration.

## Lessons from the extraction

The useful extraction was smaller than the original idea. Five functions covered the repeated work, and 132 notebook cells produced a library with a stable enough surface for two courses.

Tests weren't overhead because they found the silent overlap bug and the rigid field names. They also exposed one inconsistent metric calculation before students did. The 14 initial tests grew to 47 after release.

The package boundary also made course maintenance easier. When we changed the demo dataset, I updated one loader and 12 test fixtures. Before extraction, the same change touched 31 notebook cells.

The rule I took from the project: extract the path students copy, and leave the story in the notebook. I plan to write about the retrieval exercises separately next month. Subscribe if you want to see how the course material changes.
