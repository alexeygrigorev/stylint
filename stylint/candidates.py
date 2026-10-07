"""Static candidate finder for the "tool as actor" smell.

The LLM prompt `stylint --prompt noun-phrase-smell` decides whether a
sentence describes the role we gave a tool in our project ("Lovable
generates the React frontend") or the tool's runtime behavior ("FastAPI
generates live documentation at /docs"). This module does not judge. It
collects every sentence where a listed tool sits in an actor-like position,
so the prompt gets a deterministic minimum list to classify.

Recall comes first: over-collecting is fine, missing an occurrence is not.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from pathlib import Path
import re

from .patterns import (
    ABBREVIATION_RE,
    BLOCKQUOTE_RE,
    FOOTNOTE_DEF_RE,
    HEADING_RE,
    LIST_ITEM_RE,
    LIST_RE,
    SENTENCE_END_RE,
)
from .text import strip_frontmatter, strip_inline_code, strip_link_urls


@dataclass(frozen=True)
class Candidate:
    file: Path
    line: int
    tools: tuple[str, ...]
    sentence: str

    def render(self) -> str:
        sentence = " ".join(self.sentence.split())
        return f"{self.file}:{self.line}: [{', '.join(self.tools)}] {sentence}"


@lru_cache(maxsize=1)
def tool_names() -> tuple[str, ...]:
    """Curated tool names, longest first so multi-word names win."""
    raw = resources.files("stylint.data").joinpath("tool_names.txt").read_text(encoding="utf-8")
    names = {line.strip() for line in raw.splitlines()}
    names.discard("")
    names = {n for n in names if not n.startswith("#")}
    return tuple(sorted(names, key=lambda n: (-len(n), n)))


# --- Regex building blocks ------------------------------------------------

@lru_cache(maxsize=1)
def _tool_re() -> str:
    names = "|".join(re.escape(n) for n in tool_names())
    # Case-sensitive, whole-name match: not inside a longer word, a path
    # ("pytest.ini") or a hyphenated compound ("Docker-based").
    return rf"(?<![\w/.-])(?:{names})(?![\w]|[.-]\w)"


@lru_cache(maxsize=1)
def _compiled() -> dict[str, re.Pattern[str]]:
    T = _tool_re()
    det = r"(?:(?i:the|our|your|their|a|an)\s+)?"
    # A tool, or a list of tools: "Docker, AWS, and GitHub Actions".
    group = rf"{T}(?:(?:\s*,\s*(?:and\s+|or\s+)?|\s+(?:and|or|plus|&|\+)\s+|\s*/\s*){det}{T})*"
    word = r"[A-Za-z][\w'-]*"
    aux = (
        r"(?:is|are|was|were|will|would|can|could|should|shall|may|might|must|"
        r"does|do|did|has|have|had|gets|got|keeps|needs|\w+n't)"
    )
    adverb = (
        r"(?:also|then|now|just|still|only|already|never|always|simply|even|"
        r"actually|really|usually|typically|mostly|basically|then|instead|"
        r"\w+ly)"
    )
    # A verb-looking word after a single tool: -s/-ed forms, an auxiliary,
    # or a common irregular past.
    verbish = (
        rf"(?:{aux}|(?!(?:as|us|this|its|his|plus|thus|versus|across|unless|"
        r"towards|besides|whereas|yes|is)\b)[a-z][\w-]*(?:s|ed)|"
        r"ran|built|took|made|wrote|gave|kept|set|put|became|brought|sent|"
        r"spun|shipped|took|went|came|found|caught|told|let|fed)\b"
    )
    stop = (
        r"(?:a|an|the|and|or|but|of|in|on|at|to|for|from|with|by|as|via|into|"
        r"over|under|is|it|its|this|that|these|those|so|if|when|vs|than|then)"
    )
    # Plural subject (a list of tools) takes a bare verb: "... handle".
    any_lower = rf"(?!{stop}\b)[a-z][\w'-]*\b"
    single_or_noun = rf"(?:(?!{stop}\b){word}\s+)?"
    layer_verbs = (
        r"(?:comes?|came|coming)\s+from|"
        r"(?:runs?|ran|running|lives?|living|sits?|sitting)\s+(?:on|in|inside)|"
        r"(?:is|are|was|were|gets?|got|be|been)\s+(?:\w+ly\s+)?"
        r"(?:built|made|written|generated|created|implemented|done|powered|"
        r"handled|served|hosted|deployed|managed|provided|driven|backed|"
        r"run|stored|kept|automated|tested|orchestrated|rendered)\s+"
        r"(?:with|by|on|in|using|via|through|from|to)|"
        r"(?:built|made|written|hosted|deployed|powered|backed|driven|served|"
        r"handled|managed|generated)\s+(?:with|on|by|using|via|in|through|to)|"
        r"(?:relies|rely|relying|depends|depend|depending)\s+on|"
        r"(?:is|are|was|were)\s+(?:on|in)"
    )
    jobs = (
        r"(?:job|jobs|role|roles|responsibility|responsibilities|task|tasks|"
        r"work|purpose|part|duty|duties|function|area|domain|half|side|end|"
        r"place|contribution|share)"
    )
    return {
        "tool": re.compile(T),
        # Subject: tool (+ optional modifier noun) then a verb-like word.
        "subject": re.compile(
            rf"(?P<g>{T})\s+{single_or_noun}(?:{adverb}\s+)?{verbish}"
        ),
        # A list of tools as subject takes a bare plural verb.
        "list_subject": re.compile(
            rf"(?P<g>{T}(?:(?:\s*,\s*(?:and\s+|or\s+)?|\s+(?:and|or|plus|&|\+)\s+|\s*/\s*){det}{T})+)"
            rf"\s+(?:{adverb}\s+)?{any_lower}"
        ),
        # Causative: "let Lovable generate", "have Claude Code write".
        "causative": re.compile(
            rf"\b(?i:let|lets|letting|have|has|had|having|make|makes|made|making|get|gets)\s+"
            rf"{det}(?P<g>{group})\s+(?:{adverb}\s+)?{any_lower}"
        ),
        # Passive agent: "is handled by GitHub Actions".
        "passive": re.compile(rf"\b(?i:by)\s+{det}(?P<g>{group})"),
        # Possessive owning a job: "Railway's job is ...".
        "possessive": re.compile(
            rf"(?P<g>{T})['’]s?\s+(?:{word}\s+){{0,2}}{jobs}\b"
        ),
        # Appositive or relative clause: "Supabase, which handles auth".
        "appositive": re.compile(
            rf"(?P<g>{group})\s*(?:,|\(|\s-\s|—|–)\s*"
            rf"(?:which|that|who|whose|where|the|our|your|their|a|an|its|now|then)\b"
        ),
        "relative_bare": re.compile(rf"(?P<g>{group})\s+(?:which|that|who)\s+"),
        # Gerund or "with" absolute: "With Lovable generating the UI".
        "gerund": re.compile(
            rf"(?P<g>{group})\s+(?:{adverb}\s+)?[a-z]\w{{2,}}ing\b"
        ),
        # Layer noun + "comes from / runs on / is built with": the tool is
        # the object, but it is still doing the project's job.
        "layer": re.compile(rf"\b(?i:{layer_verbs})\s+{det}(?P<g>{group})"),
        # Label-colon assignment: "Frontend: Lovable".
        "label": re.compile(rf"^[\w /&+-]{{1,30}}:\s+{det}(?P<g>{group})"),
        # Unit start (bullet item, table cell, sentence start).
        "start": re.compile(rf"^\W*{det}(?P<g>{group})"),
        "pronoun": re.compile(r"^\W*(?:It|They|Both|Each)\b(?:['’]s)?\s"),
    }


# --- Prose extraction -----------------------------------------------------

_HTML_TAG_RE = re.compile(r"<[^>\n]*>")
_URL_RE = re.compile(r"<?\bhttps?://\S+|\bwww\.\S+")
_REF_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s")
_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")


def _plain(line: str) -> str:
    """Prose text of one markdown line with the same exclusions the checker
    uses (inline code, link targets) plus bare URLs and HTML tags."""
    text = _IMAGE_RE.sub(r"\1", line)
    text = strip_inline_code(strip_link_urls(text))
    text = _URL_RE.sub(" ", text)
    text = _HTML_TAG_RE.sub(" ", text)
    return text


@dataclass
class _Unit:
    """A run of prose: a paragraph, a list item, or a table cell."""
    kind: str  # "para", "item", "cell", "heading"
    pieces: list[tuple[int, str]]  # (line_no, plain text)


def iter_units(text: str):
    """Yield prose units, skipping frontmatter, fenced code and blockquotes
    the same way check_page does."""
    body = strip_frontmatter(text)
    offset = text.count("\n") - body.count("\n") if body != text else 0
    in_code = False
    para: list[tuple[int, str]] = []
    item: list[tuple[int, str]] = []

    def flush():
        nonlocal para, item
        if para:
            yield _Unit("para", para)
        if item:
            yield _Unit("item", item)
        para, item = [], []

    for index, line in enumerate(body.splitlines()):
        line_no = index + 1 + offset
        stripped = line.strip()
        if line.lstrip().startswith("```") or line.lstrip().startswith("~~~"):
            yield from flush()
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped:
            yield from flush()
            continue
        if FOOTNOTE_DEF_RE.match(line) or _REF_DEF_RE.match(line):
            yield from flush()
            continue
        if BLOCKQUOTE_RE.match(line):
            # Quoted material is someone else's text; the checker skips it.
            yield from flush()
            continue
        if HEADING_RE.match(line):
            yield from flush()
            yield _Unit("heading", [(line_no, _plain(line.lstrip("#").strip()))])
            continue
        if line.startswith("|"):
            yield from flush()
            cells = line.strip().strip("|").split("|")
            for cell in cells:
                if re.fullmatch(r"\s*:?-{2,}:?\s*", cell):
                    continue
                yield _Unit("cell", [(line_no, _plain(cell).strip())])
            continue
        if LIST_RE.match(line):
            yield from flush()
            item = [(line_no, _plain(LIST_ITEM_RE.sub("", line)).strip())]
            continue
        if line.lstrip().startswith("<!--"):
            continue
        if item and (line[:1].isspace() or not para):
            # Wrapped continuation of the current list item.
            item.append((line_no, _plain(stripped)))
            continue
        para.append((line_no, _plain(stripped)))
    yield from flush()


def _sentences(unit: _Unit) -> list[tuple[int, str, list[tuple[int, int]]]]:
    """Split a unit into sentences, keeping char offsets -> line numbers.

    Returns (start_offset, sentence, line_spans) per sentence, where
    line_spans maps offsets in the joined text to line numbers."""
    joined = ""
    spans: list[tuple[int, int]] = []
    for line_no, piece in unit.pieces:
        if joined:
            joined += " "
        spans.append((len(joined), line_no))
        joined += piece
    # Mask abbreviation dots so they don't end a sentence.
    masked = ABBREVIATION_RE.sub(lambda m: m.group(0).replace(".", "\x00"), joined)
    out = []
    start = 0
    for match in SENTENCE_END_RE.finditer(masked):
        end = match.end()
        out.append((start, joined[start:end]))
        start = end
    out.append((start, joined[start:]))
    result = []
    for begin, sentence in out:
        lead = len(sentence) - len(sentence.lstrip())
        sentence = sentence.strip()
        if sentence:
            result.append((begin + lead, sentence, spans))
    return result


def _line_at(spans: list[tuple[int, int]], offset: int) -> int:
    line = spans[0][1]
    for start, line_no in spans:
        if start <= offset:
            line = line_no
        else:
            break
    return line


def _tools_in(text: str) -> list[str]:
    return [m.group(0) for m in _compiled()["tool"].finditer(text)]


def _dedupe(items):
    seen = []
    for item in items:
        if item not in seen:
            seen.append(item)
    return seen


def sentence_candidates(sentence: str, unit_start: bool) -> tuple[list[str], int | None, bool]:
    """Return (tools, first_match_offset, tool_is_subject) for one sentence.

    unit_start marks a sentence that opens a bullet item or table cell,
    where any leading tool counts."""
    pats = _compiled()
    hits: list[tuple[int, list[str]]] = []
    for name in (
        "subject", "list_subject", "causative", "passive", "possessive",
        "appositive", "relative_bare", "gerund", "layer", "label",
    ):
        for m in pats[name].finditer(sentence):
            hits.append((m.start("g"), _tools_in(m.group("g"))))
    if unit_start:
        m = pats["start"].match(sentence)
        if m:
            hits.append((m.start("g"), _tools_in(m.group("g"))))
    start = pats["start"].match(sentence)
    subject_is_tool = bool(start) and any(
        h[0] == start.start("g") for h in hits
    )
    if not hits:
        return [], None, False
    hits.sort(key=lambda h: h[0])
    tools = _dedupe(t for _, ts in hits for t in ts)
    if subject_is_tool:
        subject_tools = _tools_in(start.group("g"))
    else:
        subject_tools = []
    return tools, hits[0][0], bool(subject_tools)


def find_candidates_in_text(text: str, rel: Path) -> list[Candidate]:
    candidates: list[Candidate] = []
    pats = _compiled()
    for unit in iter_units(text):
        # Tools named in the previous sentence. A pronoun opener ("It",
        # "They") right after one may refer to the tool, so it is collected
        # too; recall wins over precision here.
        prev_tools: list[str] = []
        for index, (begin, sentence, spans) in enumerate(_sentences(unit)):
            unit_start = index == 0 and unit.kind in {"item", "cell", "heading"}
            tools, offset, _ = sentence_candidates(sentence, unit_start)
            if tools:
                line = _line_at(spans, begin + offset)
                candidates.append(Candidate(rel, line, tuple(tools), sentence))
            elif prev_tools and pats["pronoun"].match(sentence):
                line = _line_at(spans, begin)
                label = tuple(f"{t} (via pronoun)" for t in prev_tools)
                candidates.append(Candidate(rel, line, label, sentence))
                continue  # keep the referent for a following "It ..."
            prev_tools = _dedupe(_tools_in(sentence))
    return candidates


def find_candidates(pages: list[tuple[Path, Path]]) -> list[Candidate]:
    """Run the finder over discovered (root, page) pairs."""
    found: list[Candidate] = []
    for root, page in pages:
        try:
            rel = page.relative_to(root)
        except ValueError:
            rel = page
        found.extend(find_candidates_in_text(page.read_text(encoding="utf-8"), rel))
    return found
