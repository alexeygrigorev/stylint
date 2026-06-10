"""Optional NLP-based prose checks (off by default).

These checks are heavier than the regex rules: they POS-tag prose to
spot undesirable constructs. They run only when the user passes
``--nlp`` AND there is text to check.

Design notes:

- nltk and its tagger are imported/loaded *lazily* (see ``_tagger``).
  Importing this module must NOT import nltk, so default runs stay
  fast and the dependency stays optional.
- The engine is nltk's ``averaged_perceptron_tagger`` (perceptron POS
  tagger). It loads in ~0.2-0.3s, far lighter than spaCy's parser,
  and POS tags alone are enough to spot the constructs we care about.
- Each check is a small generator that takes a single line of prose and
  yields ``NlpFinding`` records (tag + message + offending span). New
  NLP checks can be added as sibling ``_check_*`` functions and wired
  into ``CHECKS``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Iterator

from .tags import Tag

# ---------------------------------------------------------------------------
# Lazy engine loading
# ---------------------------------------------------------------------------

# Cached after the first successful load. Holds a callable that maps a
# list of tokens to a list of (token, pos_tag) pairs, plus a tokenizer.
_TAGGER: Callable[[list[str]], list[tuple[str, str]]] | None = None
_TOKENIZE: Callable[[str], list[str]] | None = None


class NlpUnavailableError(RuntimeError):
    """Raised when --nlp is requested but nltk or its tagger data is
    missing. Carries an actionable, install-focused message."""


_INSTALL_HINT = (
    "NLP checks require the optional 'nlp' extra.\n"
    "  Install it with:  pip install \"stylint[nlp]\"\n"
    "Then fetch the tagger data once:\n"
    "  python -m nltk.downloader averaged_perceptron_tagger_eng"
)


def _load_engine() -> tuple[
    Callable[[list[str]], list[tuple[str, str]]],
    Callable[[str], list[str]],
]:
    """Import nltk and load the perceptron tagger. Cached. Raises
    NlpUnavailableError with an actionable message on any failure."""
    global _TAGGER, _TOKENIZE
    if _TAGGER is not None and _TOKENIZE is not None:
        return _TAGGER, _TOKENIZE

    try:
        from nltk.tag import pos_tag
        from nltk.tokenize import TreebankWordTokenizer
    except ImportError as exc:  # nltk not installed
        raise NlpUnavailableError(
            f"Could not import nltk: {exc}.\n{_INSTALL_HINT}"
        ) from exc

    tokenizer = TreebankWordTokenizer()

    def tag(tokens: list[str]) -> list[tuple[str, str]]:
        return pos_tag(tokens)

    # Force the tagger data to load now so a missing-data error surfaces
    # as a clean NlpUnavailableError rather than mid-check.
    try:
        tag(["test", "sentence"])
    except LookupError as exc:  # tagger data not downloaded
        raise NlpUnavailableError(
            "The nltk perceptron tagger data is not installed.\n"
            f"{_INSTALL_HINT}"
        ) from exc

    _TAGGER = tag
    _TOKENIZE = tokenizer.tokenize
    return _TAGGER, _TOKENIZE


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NlpFinding:
    """A single NLP-detected construct on one line of prose."""

    tag: Tag
    message: str
    span: str


# ---------------------------------------------------------------------------
# Passive voice
# ---------------------------------------------------------------------------

# Forms of "to be" that can head a passive construction.
_BE_FORMS = {
    "is", "are", "was", "were", "be", "been", "being", "am",
}

# Contraction tails that stand in for a form of "be" (he's gone,
# they're tracked, I'm blocked). nltk's tokenizer splits "'s"/"'re"/"'m"
# off as their own tokens.
_BE_CONTRACTIONS = {"'s", "'re", "'m"}

# Past participles that are almost always predicate adjectives or fixed
# idioms rather than true passives. Suppressed to cut false positives.
# (e.g. "is based on", "is done", "is gone", "is located", "is tired".)
_PARTICIPLE_ALLOWLIST = {
    "based",       # "is based on" - idiomatic
    "done",        # "is done" - state, not action
    "gone",        # "is gone" - state
    "located",     # "is located" - state
    "tired",       # predicate adjective
    "interested",  # predicate adjective (usually tagged JJ anyway)
    "involved",    # "is involved" - state
    "related",     # "is related to" - state
    "supposed",    # "is supposed to" - modal idiom
    "used",        # "is used to" / modal idiom
    "known",       # "is known as/for" - often stative
}

# How many tokens after the "be" form we still treat a VBN as the
# participle of that "be" (covers "was quietly deleted by", "is now
# being rebuilt"). Small window keeps it tight and cheap.
_PASSIVE_WINDOW = 4


def _check_passive_voice(
    tokens: list[str], tagged: list[tuple[str, str]]
) -> Iterator[NlpFinding]:
    """Yield a passive-voice finding for each be-form + past participle
    (VBN) pair found within a short window, minus allowlisted cases."""
    n = len(tagged)
    i = 0
    seen_at: set[int] = set()
    while i < n:
        word, pos = tagged[i]
        low = word.lower()
        is_be = low in _BE_FORMS
        if not is_be and low in _BE_CONTRACTIONS:
            # "'s" is ambiguous: possessive (tagged POS, e.g. "Cloudflare's
            # managed db") vs a contraction of "is" (tagged VBZ, e.g. "it's
            # deleted"). Only the verb reading heads a passive.
            is_be = pos != "POS"
        if is_be:
            # Scan forward a few tokens for a past participle.
            for j in range(i + 1, min(i + 1 + _PASSIVE_WINDOW, n)):
                w2, pos2 = tagged[j]
                w2_low = w2.lower()
                if pos2 == "VBN" and w2_low not in _PARTICIPLE_ALLOWLIST:
                    if j in seen_at:
                        break
                    seen_at.add(j)
                    span = f"{word} ... {w2}" if j > i + 1 else f"{word} {w2}"
                    yield NlpFinding(
                        tag=Tag.PASSIVE_VOICE,
                        message=(
                            f"passive voice ('{span}'); rewrite in active "
                            "voice: name who does the action"
                        ),
                        span=span,
                    )
                    break
                # Stop scanning past another finite verb or sentence
                # break to avoid leaking across clauses.
                if pos2 in {"VBZ", "VBD", "VBP", "MD"} and w2_low not in _BE_FORMS:
                    break
        i += 1


# ---------------------------------------------------------------------------
# Registry of NLP checks. Add new constructs here.
# ---------------------------------------------------------------------------

# Each check takes (tokens, tagged) and yields NlpFinding.
CHECKS: tuple[
    Callable[[list[str], list[tuple[str, str]]], Iterable[NlpFinding]], ...
] = (
    _check_passive_voice,
)


def check_line(line: str) -> list[NlpFinding]:
    """Run every enabled NLP check over one line of prose.

    Loads the tagger lazily on first use. Returns an empty list for
    blank/whitespace-only input without touching the engine.
    """
    if not line or not line.strip():
        return []
    tag, tokenize = _load_engine()
    tokens = tokenize(line)
    if not tokens:
        return []
    tagged = tag(tokens)
    findings: list[NlpFinding] = []
    for check in CHECKS:
        findings.extend(check(tokens, tagged))
    return findings
