# Generating Course Exercises from Existing Material

I teach a fictional 14-lesson course on data quality at DataPrep School. My notes total 43,000 words and include 61 datasets and 180 recorded troubleshooting questions. Students kept asking for more practice work, while writing exercises by hand took me most of a weekend.

I wrote this synthetic style exercise for a writing series. The school, lesson counts, measurements and student outcomes are fictional.

In this post, I'll share:

- how I tied every exercise to a learning goal
- how I turned lesson material into a generation dataset
- how I constrained the generated tasks
- how I scored drafts with a rubric
- what the student trial changed

## Start With Learning Goals

My first attempt was exactly what I should have avoided. I asked a model to create five exercises from each lesson and received 70 tasks in 20 minutes. Most were grammatically clean, but several asked students to use functions from another lesson.

The problem wasn't the model. I hadn't said what a student should be able to do after each lesson. So I wrote three objectives per lesson and mapped them to the existing assignment. That process took four hours and made the later work much easier.

For the lesson on duplicate detection, the objectives were to:

- choose a blocking strategy for a one-million-row table
- compare similarity thresholds and measure precision
- explain when a human reviewer should resolve a match

Each objective now has an identifier, such as `DQ-4.2`, and an assessment level. Some require the student to run code, while others require a short written judgment. I don't generate an exercise unless the objective can be assessed.

## Build a Generation Dataset

The course repository has one directory per lesson. I wrote a script that reads lesson notes, datasets, assignment solutions and student questions, then writes a normalized JSON object for each lesson. The object records the objective IDs, code snippets, dataset schemas and vocabulary that a generator may use.

The per-lesson record includes:

- lesson number and learning objectives
- acceptable dataset names and column schemas
- tested code snippets
- vocabulary the course has introduced
- common student mistakes

Cleaning was the largest task. I removed 214 broken notebook outputs, resolved 17 duplicate function definitions and marked 38 snippets as illustrative rather than runnable. I also excluded solution code so the model couldn't reveal an answer inside an exercise.

I reviewed the generated dataset by sampling three lessons. In one case, the record listed a `customer_email` column that no longer existed in the current SQLite schema. That would have produced a plausible and unusable exercise.

## Constrain the Generated Tasks

The prompt gives the model one objective, one dataset and one exercise format. It must use only supplied schemas and functions. It can't introduce tools, package versions or business rules absent from the lesson.

Each generated item has this structure:

```json
{
  "objective": "DQ-4.2",
  "format": "notebook",
  "dataset": "supplier_shipments_v2",
  "prompt": "Compare two blocking strategies and report precision for each.",
  "constraints": ["use the provided threshold grid", "report precision to two decimals"],
  "estimated_minutes": 35
}
```

The generator returns three candidate exercises per objective, and I set separate time budgets:

- single-method work gets 10 to 20 minutes
- a comparison gets 30 to 45 minutes
- a mini-project gets up to 90 minutes

Anything longer becomes a separate assignment. Notebook exercises can use a supplied dataset, while written exercises can reference a chart or a short scenario. Multiple-choice questions may only test definitions or decisions that have a defensible answer.

## Score With a Rubric

A fluent exercise can still be a bad exercise, so I scored every generated task against the same rubric. I created the rubric before reading the candidates, which kept me from drifting toward tasks that merely looked impressive.

The rubric has five checks:

- objective match
- schema consistency
- unambiguous instructions
- expected answer or acceptance test
- realistic completion time

Two checks can be automated. Schema consistency compares every table and column name to the lesson record. The acceptance-test check requires either a reference solution or a written answer key with observable conditions.

I judged the remaining checks in a spreadsheet for the first batch of 210 exercises. I accepted 116 outright, edited 67 and rejected 27. Most edits shortened instructions and removed unnecessary context. Most rejections failed objective match because the generated task tested an adjacent concept rather than the stated objective.

## Run a Student Trial

I released 24 exercises to a fictional pilot group of 38 students. Every exercise had a feedback link, and students could report an error without leaving the notebook. The trial lasted two weeks.

The pilot produced these results:

- 73% of students attempted at least six exercises
- median completion time was 18% above my estimate
- 12 error reports involved missing prerequisites
- 5 reports found ambiguous wording

Completion time was the most useful result. Comparison exercises took longer than expected because students spent time reading the schema, so I raised their estimates from 35 to 45 minutes. Two notebook exercises also needed starter cells that loaded the data and printed the column types.

Missing prerequisites were the second useful result. A duplicate-detection exercise assumed knowledge of string similarity functions from an optional lesson. I moved that prerequisite into the exercise and added a two-paragraph explanation with a runnable example.

## Changes After the Trial

The workflow now has an automated stage and a human stage. First, the generator produces candidates and the automated rubric rejects schema failures. Then I review objective match, clarity and difficulty before release.

I also added a version field to each exercise. When the course data changes, the generator can list affected exercises instead of regenerating all 210 tasks. That matters because students download notebooks and continue working after the course ends.

The remaining weakness is creative transfer. The generator can vary column names and contexts, but it rarely invents a realistic data-quality failure beyond the examples in the lesson. For those tasks, I still write the scenario by hand.

## Closing Notes

The learning objective governed every other step. Once I had objective IDs, schemas and assessment levels, generation became manageable and review became concrete.

I plan to test an acceptance-test generator for code exercises. A generated task only scales if we can grade it reliably without adding hours to each cohort.

If you want to follow along, don't forget to subscribe.
