# Adding Browser Tests to an AI-Assisted Web App

I wrote this synthetic style exercise as a how-to guide. The app, dates and numbers are fictional. In May 2026 I shipped PantryLog, a small recipe tracker built with FastAPI and React. A coding agent had written roughly 6,000 of its lines.

Two days after launch, my son added the same pancake recipe twice, and the duplicate broke the weekly shopping list. Unit tests stayed green, because every endpoint returned correct JSON. The interface still failed at the flow a family touches most.

That gap is common in AI-assisted work. The agent tests the functions it wrote, and nobody tests what a person actually clicks. I added browser tests that week, and they have caught nine real bugs since.

In this post, I'll share:

- how I pick the user paths to test
- how I set up Playwright fixtures for the app
- how I test the critical paths
- how I capture screenshots on failure
- how I keep flaky tests under control
- which caveats apply before you copy the setup

## 1. Pick The User Paths To Test

Browser tests run slowly, so each one needs a job. I listed the flows that would cost me users if they broke, and I ignored everything else. The list came from one evening of clicking through my own app like a new user.

For PantryLog that produced three paths:

- add a recipe and see it on the weekly plan
- build the shopping list from the planned meals
- sign in and reach a private pantry

I kept the list in `docs/test-paths.md` so future tasks could point at it. Everything else stayed covered by unit tests. The rule is blunt: a browser test earns its place when a flow crosses two or more pages.

## 2. Set Up Playwright Fixtures

I use [Playwright](https://playwright.dev/python/docs/intro), a browser automation tool, together with pytest, because my backend tests already run there. Setup took about 20 to 30 minutes, and most of it was waiting for browser downloads.

The install needs two commands:

```bash
uv add pytest-playwright
uv run playwright install chromium
```

That gives you a `page` fixture, a live browser page your test code can drive. Tests also need known data, so I wrote a second fixture called `fresh_user`.

It registers a test account and seeds two recipes:

```python
@pytest.fixture
def fresh_user(page, live_server):
    page.goto(f"{live_server.url}/signup")
    page.get_by_label("Email").fill("tester@pantrylog.dev")
    page.get_by_label("Password").fill("test-password-1")
    page.get_by_role("button", name="Create account").click()
    seed_recipes(page, count=2)
    return page
```

The `live_server` fixture starts the real app against a scratch Postgres database, so no test touches production data. A test against mocks proves the mocks work, while a test against a scratch database proves the app works.

## 3. Test The Critical Paths

Each test follows the same three moves. The test opens a page, acts like a user, and asserts on what a user sees.

The shopping list test, the one my son broke, looks like this:

```python
def test_duplicate_recipe_appears_once(fresh_user):
    page = fresh_user
    page.get_by_text("Pancakes").click()
    page.get_by_text("Pancakes").click()
    page.get_by_role("button", name="Shopping list").click()
    rows = page.get_by_test_id("list-row").count()
    assert rows == 1, "a duplicated meal must appear once"
```

With the bug present, this test failed with two rows where the family expected one. It found the broken state update in the React code in about ten minutes. I fixed the update, reran the suite, and the same test turned green.

The other two paths followed the same template, and I wrote them in about an hour. The login test mattered more than I expected, because it caught a redirect loop that only appeared for accounts with no recipes yet.

## 4. Capture Screenshots On Failure

A red test with no context wastes time. Playwright can save a screenshot, a video, and a trace for every failed test, and I turn all three on.

One block in `pytest.ini` does it:

```text
[pytest]
addopts = --screenshot only-on-failure --video retain-on-failure --tracing retain-on-failure
```

After a failed run, I open the trace with `playwright show-trace` and watch every click. The trace from May 18 showed the add button rendering twice, which explained the duplicate in one view. I now read the trace before I read the test.

## 5. Control Flaky Tests

Flaky tests erode trust faster than failing tests. My first run had three tests that passed on retry and failed alone, all of them racing the app startup.

Three changes removed almost every flake:

- wait for visible text instead of fixed sleeps
- give every interactive element one test id
- start each test from its own scratch database

Sleeps with fixed waits were my worst habit from the first version. I replaced `page.wait_for_timeout(2000)` with `expect(...).to_be_visible()`, which waits only as long as needed. Flakes dropped from one failure in three runs to zero failures across forty runs.

The suite now holds 22 browser tests and finishes in about four minutes. Two tests still retry once through Playwright's built-in retry setting, and a nightly GitHub Actions run catches ordering problems. That setup has held for six weeks.

## 6. Caveats And Where It Stands

A browser suite complements unit tests, and it never replaces them. Keep the set under about 30 tests, or your feedback loop turns into a coffee break. Test data also needs obvious synthetic names, because a `test@` account of mine once leaked into demo data after a sloppy seed.

That seed was my mistake, and the rule I took from it: test accounts get a `test-` prefix in every email and name.

The suite has caught nine real bugs since May, and the duplicate-recipe class of bug has stayed dead. It still misses visual problems, because a test can happily click a button that renders half off-screen. I'll write about catching those layout bugs in a future post. If you want to follow along, don't forget to subscribe.
