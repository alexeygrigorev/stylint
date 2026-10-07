"""Rules mined from the workshop simplify pass: idioms, clefts, meta
narration, and fixes for the contraction and choppy-rhythm false positives."""

from pathlib import Path

import pytest

from stylint import Tag, check_page
from stylint.autofix import apply_auto_fixes


def findings(tmp_path: Path, text: str, tag: Tag):
    page = tmp_path / 'article.md'
    page.write_text(text)
    return [finding for finding in check_page(tmp_path, page) if finding.tag == tag]


@pytest.mark.parametrize('text, tag', [
    ('We rent a Hetzner box for the agent.', Tag.BANNED_WORD),
    ('The layout mirrors the SDK example.', Tag.BANNED_WORD),
    ('LinkedIn rewards a lighter cadence for new accounts.', Tag.BANNED_WORD),
    ('Then the model synthesizes the answer from the snippets.', Tag.BANNED_WORD),
    ('A database would be overkill for twenty rows.', Tag.BANNED_WORD),
    ('We use a deliberately ordinary stack.', Tag.BANNED_WORD),
    ('Put the house rules in the file.', Tag.BANNED_PHRASE),
    ('Pick a project that speaks to several companies.', Tag.BANNED_PHRASE),
    ('Even this small version earns its keep in the repo.', Tag.BANNED_PHRASE),
    ('Caching kicks in automatically for the shared prefix.', Tag.BANNED_PHRASE),
    ('I learned the teardown step the hard way.', Tag.BANNED_PHRASE),
    ('The SDK sends a POST request under the hood.', Tag.BANNED_PHRASE),
    ('We bake the model weights into the image.', Tag.BANNED_PHRASE),
    ('The model decides which tool to call next.', Tag.BANNED_PHRASE),
    ('The failures teach us the most.', Tag.BANNED_PHRASE),
    ('This course teaches you how to build AI apps.', Tag.BANNED_PHRASE),
    ('The script works. Here, we cover the deployment steps in order.', Tag.BANNED_PHRASE),
    ('We write the spec first. Below, I show what that looks like on a real project.', Tag.BANNED_PHRASE),
    ('Above, we saw how the services layer works.', Tag.BANNED_PHRASE),
    ('The framework has a first-class guardrail API.', Tag.BANNED_PHRASE),
    ('The fixed pipeline cannot retry, and the model is a passenger.', Tag.BANNED_PHRASE),
    ('This is where RAG helps the most for library docs.', Tag.CLEFT),
    ('Keeping them separate is what stops an agent from approving itself.', Tag.CLEFT),
    ('You can pick any topic. What matters is that you narrow the field.', Tag.CLEFT),
])
def test_simplify_rules_fire(tmp_path, text, tag):
    assert findings(tmp_path, text, tag), text


@pytest.mark.parametrize('text, tag', [
    ('Type the question into the search box and press enter.', Tag.BANNED_WORD),
    ('The model returns a bounding box for each face.', Tag.BANNED_WORD),
    ('We point pip at a local PyPI mirror.', Tag.BANNED_WORD),
    ('Chromium can synthesize speech for the voice test.', Tag.BANNED_WORD),
    ('Vite runs in the foreground until you stop it.', Tag.BANNED_WORD),
    ('The client speaks to the server over HTTP.', Tag.BANNED_PHRASE),
    ('The person reviewing the pull request decides whether to merge.', Tag.BANNED_PHRASE),
    ('In this lesson, I teach you how to build an agent.', Tag.BANNED_PHRASE),
    ("In this lesson, I'll teach you how to build an agent.", Tag.BANNED_PHRASE),
    ('We learn the most from failures.', Tag.BANNED_PHRASE),
    ('Below 10 requests per second, one server is enough.', Tag.BANNED_PHRASE),
    ('In this post, I describe how we run the workshop.', Tag.BANNED_PHRASE),
    ('A common question is where to put the logic.', Tag.CLEFT),
    ('The quote said "this is where it breaks" and we moved on.', Tag.CLEFT),
])
def test_simplify_rules_skip_literal_uses(tmp_path, text, tag):
    assert not findings(tmp_path, text, tag), text


@pytest.mark.parametrize('text', [
    'We measure how similar they are.',
    'We compare the vectors to see how close they are to each other in the index.',
    'The docs explain what it is and when to use it.',
    'Keep the files where they are for now.',
])
def test_contraction_skips_stranded_be(tmp_path, text):
    assert not findings(tmp_path, text, Tag.CONTRACTION), text


@pytest.mark.parametrize('text', [
    'It is a small script that we run once.',
    'We see how they are doing after the first week.',
    'Check how it does not change the output.',
])
def test_contraction_still_fires_mid_clause(tmp_path, text):
    assert findings(tmp_path, text, Tag.CONTRACTION), text


def test_autofix_leaves_stranded_be_expanded(tmp_path):
    page = tmp_path / 'article.md'
    page.write_text('We measure how similar they are. It is fast, and they are close to each other.\n')
    results = check_page(tmp_path, page)
    apply_auto_fixes(results, [(tmp_path, page)])
    assert page.read_text() == (
        "We measure how similar they are. It's fast, and they're close to each other.\n"
    )


def test_choppy_rhythm_counts_inline_code_as_words(tmp_path):
    text = 'We use `docs.py` for this job. It downloads the FAQ and saves every entry into a local folder for later.'
    assert not findings(tmp_path, text, Tag.CHOPPY_RHYTHM)


def test_choppy_rhythm_still_fires_on_tiny_sentence(tmp_path):
    text = 'It works. The script downloads the FAQ and saves every entry into a local folder for later.'
    assert findings(tmp_path, text, Tag.CHOPPY_RHYTHM)


def test_choppy_rhythm_ignores_code_only_continuation(tmp_path):
    text = (
        '- Computes the full ECR image URI in the form\n'
        '  `<account>.dkr.ecr.<region>.amazonaws.com/<repo>:<tag>`. This is\n'
        '  the address Lambda will use to pull the image at runtime.\n'
    )
    assert not findings(tmp_path, text, Tag.CHOPPY_RHYTHM)
