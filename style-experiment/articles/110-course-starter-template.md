# Designing a Course Starter Template Students Can Extend

Two cohorts ago, 21 of 68 students spent the first homework session fighting project setup instead of writing code. I counted 34 distinct questions about missing dependencies and file locations.

I wrote this course story as a synthetic style exercise. I invented the enrollment numbers, tool versions, test counts, and student feedback so I could explore template design.

In this post, I'll share:

- why my first starter template failed
- the files I now include and exclude
- how I make the first command predictable
- how a small test suite guides the assignment
- how students extend the template without breaking it

## The First Template

My original template contained a complete sample project. It had authentication, a database, a Docker setup (a tool for running applications in containers), and 42 tests copied from my own service.

Students could run it after installation. They often couldn't tell which files were part of the assignment. The sample code answered questions they didn't have yet and hid the three decisions they did need to make.

One student removed the authentication module, broke four shared fixtures, and lost two evenings. Another submitted the example endpoint with a new name because the assignment boundary wasn't visible.

The failure was mine because I had optimized the template for my demo and made students navigate my project instead of starting theirs.

## Keep the Starting Set Small

The current template has 11 files, including the license and this README:

```text
README.md
pyproject.toml
.gitignore
Makefile
app/main.py
app/config.py
app/models.py
tests/test_health.py
tests/test_students.py
data/sample.csv
.devcontainer/devcontainer.json
```

Each file has one job. I define two routes in `app/main.py` and read environment variables in `app/config.py`. I included 20 rows in `data/sample.csv`, with the same fields as the assignment dataset.

I removed Docker for the first assignment. The course uses Python 3.12, a virtual environment, and SQLite (a small embedded database). Those choices are less realistic and much easier to debug during a live session.

The template also contains no solution code. It has a health route and one working route for the `students` table, and those examples show naming, status codes, and error responses.

Students extend that route or add one beside it. They don't have to reverse-engineer a larger system before they write their first endpoint.

## Make the First Command Predictable

I list four steps in the README before any course theory:

- copy the template repository
- install Python 3.12 and create a virtual environment
- run `make install`
- run `make test`

The install command uses only standard tooling:

```bash
uv sync
uv run pytest -q
```

On the fictional cohort, the median setup time dropped from 38 minutes to 9 minutes. Nine students still needed help, and seven of those had an old Python version or a conflicting global package.

That improvement changed the first class. I now use the recovered 25 minutes for a short tour of the request lifecycle and a demonstration of the two tests.

I state the expected output after `make test`:

```text
2 passed in 0.18s
```

If a student sees a different result, the troubleshooting section names the three most common causes. It doesn't try to diagnose every possible machine.

## Use Tests as Assignment Boundaries

The starter suite has only two tests. Their purpose is to explain the expected API behavior, and the grading suite adds 11 cases later.

`test_health.py` checks that the service responds with HTTP 200. `test_students.py` checks that a POST request creates one row and returns the stored fields.

The test names use student vocabulary:

```python
def test_create_student_returns_saved_fields(client):
    response = client.post("/students", json={"name": "Ada"})
    assert response.status_code == 201
    assert response.json()["name"] == "Ada"
```

Students can read this test before they understand fixtures. The visible assertions define one acceptance rule without a rubric document.

For the graded assignment, I publish the categories, and I don't publish every case:

- create a student and return the saved fields
- reject a missing name with HTTP 422
- reject a duplicate email with HTTP 409
- return an empty list before records exist

That balance gives students enough information to test locally and leaves some implementation choices open.

## Support Extension Without Chaos

A starter should make the next step obvious. My README ends with three extension paths, and the student can add a field, add a route, or replace the sample dataset.

Each path names the files to touch and the tests to update. That detail is more useful than a generic instruction to "explore the code".

For example, adding a `course` field requires changes in `app/models.py`, the student route, and the test fixtures. I ask the student to run the tests after each change.

Students can also delete the sample route once their own endpoint works. The template doesn't depend on that route, and I say so explicitly.

The course forum confirmed the effect. Questions about file locations dropped from 34 in the earlier cohort to 7 in the latest fictional cohort. Questions about validation rules rose, which was the goal.

## Lessons From Two Cohorts

A starter template works as a teaching interface. It should make one working path obvious and leave enough room for the student's own design.

The rule I use now is to include the smallest code that demonstrates the assignment API and to explain every included file.

I'll write more about assignment rubrics in a future article. Subscribe if you want to follow along.
