"""Human-readable explanations for every rule tag.

The inline messages emitted with each finding are terse and sometimes
puzzling. This module holds a fuller explanation per tag: what the rule
catches, a concrete before/after example, and (for umbrella tags) which
specific patterns feed into it. The CLI surfaces these via
``stylint --explain <tag>``.
"""

from __future__ import annotations

from dataclasses import dataclass

from .patterns import ABSTRACT_SUBJECT_LABELS, BANNED_PHRASE_PATTERNS
from .tags import Tag


def _normalize(name: str) -> str:
    """Lower-case and collapse separators to hyphens so the user does not
    have to guess whether a tag uses hyphens, underscores, or spaces."""
    return name.strip().lower().replace("_", "-").replace(" ", "-")


@dataclass(frozen=True)
class Explanation:
    """One tag explanation."""

    tag: str
    title: str
    what: str
    examples: tuple[tuple[str, str], ...]
    note: str = ""

    def render(self) -> str:
        lines = [f"{self.tag} - {self.title}", "", "What it catches"]
        lines.extend(self.what.split("\n"))
        lines.append("")
        lines.append("Examples")
        for before, after in self.examples:
            lines.append(f"  before: {before}")
            lines.append(f"  after:  {after}")
            lines.append("")
        if self.note:
            lines.append(self.note)
            lines.append("")
        while lines and lines[-1] == "":
            lines.pop()
        return "\n".join(lines)


# Aliases: pattern labels and other names that map to a canonical tag.
# "content as actor" is a pattern label inside BANNED_PHRASE_PATTERNS,
# not a Tag enum value; it fires under the abstract-subject tag. Build
# the map so --explain content-as-actor resolves correctly.
_ALIASES: dict[str, str] = {}
for _label in BANNED_PHRASE_PATTERNS:
    _tag = (
        Tag.ABSTRACT_SUBJECT.value
        if _label in ABSTRACT_SUBJECT_LABELS
        else Tag.BANNED_PHRASE.value
    )
    _ALIASES[_normalize(_label)] = _tag
del _label, _tag


_E = Explanation


_EXPLANATIONS: dict[str, Explanation] = {
    Tag.BOLD.value: _E(
        Tag.BOLD.value, "Bold markdown",
        "Bold markers (** or __) appear in prose. This house style does not "
        "use bold for emphasis; it relies on plain text and structure.",
        (
            ("This is **very important**.", "This is very important."),
            ("Call __set_timeout__ here.", "Call `set_timeout` here."),
        ),
    ),
    Tag.ITALIC.value: _E(
        Tag.ITALIC.value, "Italic markdown",
        "Italic markers (*text* or _text_) appear in prose. This house style "
        "does not use italics.",
        (
            ("a *quick* note", "a quick note"),
            ("the _first_ step", "the first step"),
        ),
    ),
    Tag.TABLES.value: _E(
        Tag.TABLES.value, "Markdown tables",
        "A line starting with | is a markdown table. Tables are not used in "
        "this house style.",
        (
            ("| col | col |", "Use a bullet list or a short prose paragraph."),
        ),
    ),
    Tag.HR.value: _E(
        Tag.HR.value, "Horizontal rule",
        "A line that is just --- is a horizontal rule. Horizontal rules are "
        "not used; use a heading to separate sections.",
        (
            ("---", "## Next section"),
        ),
    ),
    Tag.EM_DASH.value: _E(
        Tag.EM_DASH.value, "Em dash",
        "An em dash character appears in prose. Replace it with a hyphen. "
        "When two dashes bracket a parenthetical aside, split that into two "
        "sentences instead of re-bracketing with commas.",
        (
            ("The model - a 384-dim embedder - runs on CPU.",
             "The model is a 384-dim embedder. It runs on CPU."),
        ),
    ),
    Tag.DOUBLE_HYPHEN.value: _E(
        Tag.DOUBLE_HYPHEN.value, "Double hyphen",
        "A double hyphen (--) appears in prose outside HTML comments or "
        "URLs. Use a single hyphen. When the double dash brackets a "
        "parenthetical aside, split into two sentences.",
        (
            ("git commit --amend", "git commit -amend"),
            ("The file - created last week - is missing.",
             "The file was created last week. It is missing."),
        ),
    ),
    Tag.DASH_PARENTHETICAL.value: _E(
        Tag.DASH_PARENTHETICAL.value, "Dash-enclosed parenthetical",
        "A parenthetical aside is enclosed by single dashes (word - aside - "
        "word). Split it into two sentences or fold the aside into the main "
        "clause.",
        (
            ("We use Redis - it is fast - for caching.",
             "We use Redis for caching because it is fast."),
        ),
    ),
    Tag.SMART_QUOTES.value: _E(
        Tag.SMART_QUOTES.value, "Smart quotes",
        "Curly/smart quote characters appear in the text. Use straight "
        "quotes instead.",
        (
            ("It had a curly apostrophe.", "Use a straight apostrophe."),
            ("She used curly double quotes.", "She used straight quotes."),
        ),
    ),
    Tag.BACKTICKS_IN_LINK.value: _E(
        Tag.BACKTICKS_IN_LINK.value, "Backticks inside link text",
        "Link text contains backticks, e.g. [`module`](url). Remove the "
        "backticks from the link text. This tag is off by default; enable it "
        "with --enable backticks-in-link.",
        (
            ("See [`module`](https://example.com).", "See the module."),
        ),
    ),
    Tag.BARE_URL.value: _E(
        Tag.BARE_URL.value, "Bare URL",
        "A raw http:// or https:// URL appears in prose (not inside HTML or "
        "a table cell). Wrap it in a markdown link.",
        (
            ("See https://example.com for details.",
             "See [the docs](https://example.com) for details."),
        ),
    ),
    Tag.ANGLE_URL.value: _E(
        Tag.ANGLE_URL.value, "Angle-bracket URL",
        "A URL in angle brackets <https://...> appears in prose. This form "
        "is not used; wrap it in a markdown link instead.",
        (
            ("Open <https://example.com>.",
             "Open [example.com](https://example.com)."),
        ),
    ),
    Tag.FRONTMATTER_BLANK.value: _E(
        Tag.FRONTMATTER_BLANK.value, "Missing blank line after frontmatter",
        "The closing --- of the YAML frontmatter is immediately followed by "
        "body text with no blank line between them. Insert a blank line.",
        (
            ("---\\ntitle: X\\n---\\nSome text.",
             "---\\ntitle: X\\n---\\n\\nSome text."),
        ),
    ),
    Tag.BLOCKQUOTE_LONG.value: _E(
        Tag.BLOCKQUOTE_LONG.value, "Blockquote too long",
        "A blockquote spans more than 3 lines. Rework it into prose or a "
        "subsection.",
        (
            ("> A long quote spanning several lines...",
             "Summarise the quote in a sentence or two of your own prose."),
        ),
    ),
    Tag.HEADING_QUESTION_WORD.value: _E(
        Tag.HEADING_QUESTION_WORD.value, "Question-word heading",
        "A heading starts with a question word (Why, How, What, When, "
        "Where, Which, Who). Use a statement heading instead. 'How it "
        "works' is an allowed exception.",
        (
            ("## Why we need search", "## Search requirements"),
            ("## How retrieval works", "## How it works"),
        ),
    ),
    Tag.HEADING_QUESTION_MARK.value: _E(
        Tag.HEADING_QUESTION_MARK.value, "Heading ends with a question mark",
        "A heading ends with '?'. Use a statement instead.",
        (
            ("## What is RAG?", "## What RAG is"),
        ),
    ),
    Tag.HEADING_TOO_DEEP.value: _E(
        Tag.HEADING_TOO_DEEP.value, "Heading too deep",
        "A heading at depth ### or deeper appears. Flatten the structure to "
        "use at most ## headings.",
        (
            ("### Sub-detail", "## Detail"),
        ),
    ),
    Tag.LAZY_HEADING.value: _E(
        Tag.LAZY_HEADING.value, "Lazy 'The <abstract noun>' heading",
        "A heading opens with 'The' and contains a vague abstract noun "
        "(problem, issue, challenge, solution, goal, idea, etc.). Name what "
        "the section is actually about.",
        (
            ("## The problem", "## Why the API times out"),
            ("## The big idea", "## Semantic search with embeddings"),
        ),
    ),
    Tag.CODE_NO_LANG.value: _E(
        Tag.CODE_NO_LANG.value, "Code block missing language tag",
        "A code fence has no language tag after the backticks. Add one so "
        "syntax highlighting works (```python, ```bash, ...).",
        (
            ("```", "```python"),
        ),
    ),
    Tag.CODE_TOO_LONG.value: _E(
        Tag.CODE_TOO_LONG.value, "Code block too long",
        "A code block has more than 40 lines. Split it with prose so the "
        "reader can follow the explanation between chunks.",
        (
            ("# a 50-line block with no breaks",
             "Split into two blocks with a sentence between them."),
        ),
    ),
    Tag.CODE_PROMPT.value: _E(
        Tag.CODE_PROMPT.value, "Shell prompt marker in code",
        "A line in a shell code block starts with '$ ', copying the terminal "
        "prompt. Remove the prompt marker.",
        (
            ("$ pip install stylint", "pip install stylint"),
        ),
    ),
    Tag.CONSECUTIVE_CODE.value: _E(
        Tag.CONSECUTIVE_CODE.value, "Consecutive code blocks",
        "Two code blocks appear with no prose between them. Add an "
        "introducing sentence between them.",
        (
            ("```python\\n...\\n```\\n```bash\\n...\\n```",
             "```python\\n...\\n```\\nRun it with:\\n```bash\\n...\\n```"),
        ),
    ),
    Tag.LEAD_IN.value: _E(
        Tag.LEAD_IN.value, "Code or list missing a lead-in",
        "A code block or list appears right after a heading or another "
        "structural block with no introducing sentence. Add a lead-in "
        "sentence. Also fires when a lead-in starts with 'This is' before a "
        "code block.",
        (
            ("## Setup\\n```", "## Setup\\nInstall the package first:\\n```"),
            ("This is how we do it:\\n```", "Run the command:\\n```"),
        ),
    ),
    Tag.LEAD_IN_MULTI.value: _E(
        Tag.LEAD_IN_MULTI.value, "Multi-sentence lead-in before a block",
        "A paragraph that ends with ':' has multiple sentences and then "
        "introduces a list or code block. Make the lead-in (the sentence "
        "with the colon) its own one-sentence paragraph.",
        (
            ("We need two things. First the data. Then the model:\\n- item",
             "We need two things:\\n- item"),
        ),
    ),
    Tag.CHAINED_GET.value: _E(
        Tag.CHAINED_GET.value, "Chained .get().get() in code",
        "Python example code chains .get(...).get(...). Access known keys "
        "directly so the example is clear.",
        (
            ("cfg.get('a').get('b')", "cfg['a']['b']"),
        ),
    ),
    Tag.DOUBLE_BLANK.value: _E(
        Tag.DOUBLE_BLANK.value, "Double blank line in code",
        "Two consecutive blank lines appear inside a code block. Use one "
        "blank line between definitions.",
        (
            ("def a():\\n\\n\\n    pass", "def a():\\n\\n    pass"),
        ),
    ),
    Tag.BANNED_WORD.value: _E(
        Tag.BANNED_WORD.value, "Banned word",
        "A single banned word appears in prose (delve, crucial, leverage, "
        "showcase, very, really, etc.). The full list is maintained in "
        "patterns.py (BANNED_WORDS); the message names the specific word "
        "and gives a replacement. Some words have technical exceptions "
        "(e.g. 'shape' for NumPy arrays) that suppress the finding.",
        (
            ("We delve into the details.", "We dig into the details."),
            ("This is a very important feature.", "This is an important feature."),
        ),
    ),
    Tag.BANNED_PHRASE.value: _E(
        Tag.BANNED_PHRASE.value, "Banned phrase",
        "A banned multi-word phrase or phrasing family appears in prose (in "
        "order to, at this point, reference implementation, close the loop, "
        "rough edges, etc.). The full list lives in patterns.py "
        "(BANNED_PHRASES and BANNED_PHRASE_PATTERNS); the message names the "
        "specific phrase and gives a fix. Regex-based phrase patterns also "
        "fire here.",
        (
            ("In order to run it, use uv.", "To run it, use uv."),
            ("There are some rough edges.", "There are a few limitations."),
        ),
    ),
    Tag.BANNED_OPENER.value: _E(
        Tag.BANNED_OPENER.value, "Banned sentence opener",
        "A sentence starts with a transition filler word: Additionally, "
        "Moreover, Furthermore, Notably, Importantly, or Consequently. Drop "
        "it or rewrite the transition.",
        (
            ("Additionally, we add a cache.", "We also add a cache."),
            ("Moreover, the API is fast.", "The API is also fast."),
        ),
    ),
    Tag.ABSTRACT_SUBJECT.value: _E(
        Tag.ABSTRACT_SUBJECT.value, "Abstract noun as the subject/actor",
        "An abstract noun or content noun sits as the grammatical subject "
        "of a claim, as if the document or an abstraction could act on its "
        "own. The fix is to recast with a real actor (we/you) or to name the "
        "concrete code/output. This is an umbrella tag: several specific "
        "patterns feed into it, and the message names which one fired.",
        (
            ("This workshop turns theory into practice.",
             "We turn theory into practice in this workshop."),
            ("The result is a JSON file with the embeddings.",
             "The command writes a JSON file with the embeddings."),
            ("The work splits itself into two parts.",
             "We split the work into two parts."),
            ("The growth followed shortly.",
             "Subscribers grew 9% that week because the post went viral."),
        ),
        note="Specific patterns under this tag: "
             + ", ".join(sorted(ABSTRACT_SUBJECT_LABELS)) + ".",
    ),
    Tag.THIRD_PERSON.value: _E(
        Tag.THIRD_PERSON.value, "Third-person self-reference",
        "The author's name (set via --author-name, default 'Alexey') appears "
        "in prose, reading as a third-person reference to oneself. Use first "
        "person. Pass --author-name '' to disable.",
        (
            ("Alexey shows how to build this.", "I show how to build this."),
        ),
    ),
    Tag.ANAPHORIC_NO.value: _E(
        Tag.ANAPHORIC_NO.value, "'No X, no Y' anaphoric fragment",
        "A verbless 'No X, no Y' rhetorical fragment appears (including the "
        "'There's no X, no Y' dodge). Describe what is actually happening "
        "instead. Do not just prepend 'There's' - that satisfies the regex "
        "without adding information.",
        (
            ("No frameworks, no magic - just Python.",
             "We use plain Python with no frameworks."),
            ("There's no server, no cost.",
             "It runs without a server, so there is no cost."),
        ),
    ),
    Tag.SEMICOLON.value: _E(
        Tag.SEMICOLON.value, "Semicolon in prose",
        "A semicolon appears in prose. Use two sentences instead.",
        (
            ("It is fast; it is also cheap.", "It is fast. It is also cheap."),
        ),
    ),
    Tag.CLEFT.value: _E(
        Tag.CLEFT.value, "Cleft construction",
        "A cleft construction appears: 'This is what X is about' or 'X is "
        "what made it Y'. State directly what X does or what the cause is.",
        (
            ("This is what the workshop is about.",
             "The workshop covers semantic search."),
            ("Honesty is what made it work.",
             "The honest tone earned the goodwill."),
        ),
    ),
    Tag.GERUND_OPENER.value: _E(
        Tag.GERUND_OPENER.value, "Gerund / participial opener",
        "A sentence opens with an -ing participial phrase followed by a "
        "comma and a new subject (e.g. 'Reading through it, I "
        "noticed...'). Rewrite so the -ing word is not a dangling "
        "participle.",
        (
            ("Looking at the output, we see an error.",
             "The output shows an error."),
            ("Parsing the data, a bug appeared.",
             "While parsing the data, we found a bug."),
        ),
    ),
    Tag.PAST_TENSE_FRAGMENT.value: _E(
        Tag.PAST_TENSE_FRAGMENT.value, "Subjectless past-tense fragment",
        "A sentence starts with a past-tense action verb or participle with "
        "no subject (like a commit message: 'Ran the workshop.', 'Added "
        "tests.'). Add the actor ('I ran...', 'we add...'), rewrite in "
        "present tense, or restructure the participle clause.",
        (
            ("Ran the workshop last week.", "I ran the workshop last week."),
            ("Added tests for the parser.", "We add tests for the parser."),
        ),
    ),
    Tag.PARAGRAPH_TOO_LONG.value: _E(
        Tag.PARAGRAPH_TOO_LONG.value, "Paragraph too long",
        "A paragraph has more than 5 sentences. Split it into 2-4 sentence "
        "paragraphs.",
        (
            ("A six-sentence paragraph...",
             "Split into two three-sentence paragraphs."),
        ),
    ),
    Tag.LONG_SENTENCE.value: _E(
        Tag.LONG_SENTENCE.value, "Sentence too long",
        "A sentence has more than 25 words and no commas. Fix: (1) split "
        "ONCE at a natural boundary into two sentences, not many short "
        "ones; (2) drop filler words; (3) convert to a list if there is "
        "embedded enumeration.",
        (
            ("A 30-word sentence with no commas that runs on and on...",
             "Split it once into two sentences at a natural boundary."),
        ),
    ),
    Tag.LONG_LIST_LIKELY.value: _E(
        Tag.LONG_LIST_LIKELY.value, "Long sentence that looks like a list",
        "A sentence is over 25 words with multiple commas, and the commas "
        "look like enumeration (a colon or 'and X' closer is present). "
        "Convert the items to a bullet list. Use the parallel-completion "
        "test: if you can write one lead-in that all the commas finish, it "
        "is a bullet list.",
        (
            ("We use numpy, pandas, scikit-learn, and matplotlib for the pipeline.",
             "We use these libraries:\\n- numpy\\n- pandas\\n- scikit-learn\\n- matplotlib"),
        ),
    ),
    Tag.LONG_CLAUSE_LIKELY.value: _E(
        Tag.LONG_CLAUSE_LIKELY.value, "Long sentence with clause-boundary commas",
        "A sentence is over 25 words with multiple commas, but the commas "
        "look like clause boundaries (subordinating conjunction, chain of "
        "actions, or mixed subjects). Fix: make ONE split at a natural "
        "clause boundary into two sentences. Do NOT chop into many short "
        "fragments (that trips choppy-rhythm) and do NOT convert to bullets "
        "(that would break the meaning).",
        (
            ("When the request arrives, the handler reads the body, which "
             "contains the query, and passes it to the retriever, that then "
             "searches.",
             "When the request arrives, the handler reads the body, which "
             "contains the query. It passes the query to the retriever, "
             "which then searches."),
        ),
    ),
    Tag.MANY_COMMAS.value: _E(
        Tag.MANY_COMMAS.value, "Too many commas",
        "A sentence has more than 3 commas (but is not over the word limit). "
        "Fix: convert to a bullet list, or split into shorter sentences.",
        (
            ("We install Python, set up venv, add dependencies, and run the tests.",
             "We do four things:\\n- install Python\\n- set up venv\\n- add "
             "dependencies\\n- run the tests"),
        ),
    ),
    Tag.COLON_INLINE.value: _E(
        Tag.COLON_INLINE.value, "Colon-introduced inline list",
        "A sentence uses a colon to introduce an inline run of 3+ items "
        "closed with and/or (the colon signals enumeration intent, so the "
        "items should be bullets). Fix: convert to bullets, drop the colon, "
        "or split the sentence.",
        (
            ("We use these tools: numpy, pandas, and matplotlib.",
             "We use these tools:\\n- numpy\\n- pandas\\n- matplotlib"),
        ),
    ),
    Tag.PARALLEL_SENTENCES.value: _E(
        Tag.PARALLEL_SENTENCES.value, "Parallel sentence openers",
        "Three or more consecutive sentences start with the same two-word "
        "opener. That reads as a list written in prose. Fix: convert to a "
        "bullet list, or vary the openers if the items are not really "
        "parallel.",
        (
            ("We install Python. We set up venv. We add dependencies.",
             "We do three things:\\n- install Python\\n- set up venv\\n- add "
             "dependencies"),
        ),
    ),
    Tag.CHOPPY_RHYTHM.value: _E(
        Tag.CHOPPY_RHYTHM.value, "Choppy rhythm",
        "Two or more consecutive short sentences (9 words or fewer each) "
        "read as staccato. Also fires when a single very short sentence (4 "
        "words or fewer) sits right before a longer one and is too small to "
        "stand alone. Fix: combine them with a conjunction or restructure "
        "as a single longer sentence.",
        (
            ("Retrieval becomes semantic. The data moves somewhere it "
             "survives restarts.",
             "Retrieval becomes semantic, and the data moves to a store that "
             "survives restarts."),
        ),
    ),
    Tag.LABEL_FRAGMENT.value: _E(
        Tag.LABEL_FRAGMENT.value, "Verbless label fragment",
        "A short verbless noun phrase or wh-fragment is used as a label or "
        "lead-in, terminated by a period ('The goal behind it.', 'Why not "
        "Postgres.'). It carries no subject and verb, so the idea is lost. "
        "Fix: fold it into the next sentence, or drop the label and state "
        "the point directly. Do not just swap the period for a colon (that "
        "is the label-colon pattern). Concrete proper-noun labels "
        "('Railway.') are fine.",
        (
            ("The goal behind it. I did not want to pay for a server.",
             "The goal behind it was to avoid paying for an idle server."),
            ("Why not Postgres. The hosts I looked at...",
             "Why not Postgres: the hosts I looked at were too expensive."),
        ),
    ),
    Tag.CONTRACTION.value: _E(
        Tag.CONTRACTION.value, "Expanded form should be a contraction",
        "An expanded form appears that should be contracted in this voice "
        "(it is becomes it's, do not becomes don't, we will becomes we'll, "
        "etc.). The voice uses contractions. Skip only at the end of a "
        "sentence or for deliberate emphasis.",
        (
            ("It is a feature.", "It's a feature."),
            ("We will add tests.", "We'll add tests."),
            ("Do not use bold.", "Don't use bold."),
        ),
    ),
    Tag.COUNT_LIST.value: _E(
        Tag.COUNT_LIST.value, "Count-announced list in prose",
        "The opening sentence announces a count of items ('two things', "
        "'three reasons') and the paragraph then enumerates them across "
        "following sentences. That is a list. Fix: convert the items to a "
        "bullet list and drop the count.",
        (
            ("There are two things to change. First, we swap the model. "
             "Second, we add a cache.",
             "We change two things:\\n- swap the model\\n- add a cache"),
        ),
    ),
    Tag.FLAT_DEFINITION.value: _E(
        Tag.FLAT_DEFINITION.value, "Flat copular definition",
        "A sentence opens with 'The/Its/Our <noun> is a/an/the ...' or "
        "'This is a ...' that just equates the subject with a category. It "
        "reads as dull and formal. Prefer active voice or lead with the "
        "thing itself: 'We use X', 'X does Y'.",
        (
            ("The model is a 384-dim embedder.",
             "We use a 384-dim embedder."),
            ("This is a check for passive voice.",
             "This checks for passive voice."),
        ),
    ),
    Tag.SHORT_LIST_PERIOD.value: _E(
        Tag.SHORT_LIST_PERIOD.value, "Short list item ends with a period",
        "A list that is mostly one- or two-word items has periods at the end "
        "of the short items. Drop periods from mostly one- or two-word lists.",
        (
            ("- Python.\\n- pip.", "- Python\\n- pip"),
        ),
    ),
    Tag.LABEL_COLON.value: _E(
        Tag.LABEL_COLON.value, "Label-colon pattern",
        "A paragraph or line opens with a label-colon pattern ('The "
        "problem: ...', 'Goal: ...', 'What we want: ...', or a short 2-3 "
        "word label line). Use colons only to introduce lists or code "
        "blocks, not to label a chunk of prose. Fix: drop the label and "
        "state the point directly. 'Note:' and 'Important:' are exempt "
        "callouts.",
        (
            ("The problem: the API times out.", "The API times out."),
            ("Rule of thumb:", "State the rule directly."),
        ),
    ),
    Tag.META_FRAMING.value: _E(
        Tag.META_FRAMING.value, "Meta-framing",
        "A sentence uses the '[The/A/Another] <abstract noun> [of X] is that "
        "<claim>' frame. The writer announces the shape of the claim ('here "
        "comes an advantage / limitation / insight') instead of just stating "
        "it. Fix: drop the framing noun phrase and lead with the actual "
        "claim.",
        (
            ("A big advantage of Recorder is that it keeps recording.",
             "Recorder keeps recording."),
            ("The main limitation is that it needs a GPU.", "It needs a GPU."),
        ),
    ),
    Tag.QUESTION_OPENER.value: _E(
        Tag.QUESTION_OPENER.value, "Paragraph opens with a question",
        "A paragraph opens with a rhetorical question ('Why do we need "
        "search?'). Fix: drop the question and lead with the substantive "
        "claim, or rewrite the answer as the opening sentence.",
        (
            ("Why do we need search? Because users ask in many ways.",
             "We need search because users ask in many ways."),
        ),
    ),
    Tag.PROSE_QUESTION.value: _E(
        Tag.PROSE_QUESTION.value, "Question mark in prose",
        "A question mark appears in prose outside a Q&A section. In "
        "technical docs, use questions only in Q&A sections. Rewrite as a "
        "direct statement, move it under a Q&A heading, or ignore "
        "'prose-question' for a real Q&A file.",
        (
            ("Did the build pass?", "The build passed."),
        ),
    ),
    Tag.REPEATED_AND.value: _E(
        Tag.REPEATED_AND.value, "Polysyndetic 'and' chain",
        "Three or more items are joined by repeated 'and' instead of commas "
        "('Claude Code and Codex and OpenCode'). Use the oxford comma form. "
        "Keep the repeated 'and' only when the rhythm is intentional (rare).",
        (
            ("Claude Code and Codex and OpenCode all work.",
             "Claude Code, Codex, and OpenCode all work."),
        ),
    ),
    Tag.NOW_LETS_OVERUSE.value: _E(
        Tag.NOW_LETS_OVERUSE.value, "Too many 'Now' / 'Let's' openers",
        "The file uses more than 4 sentence-starters that begin with 'Now', "
        "'Let's', or 'Let us'. Overuse signals lazy transitions. Vary "
        "openers: try 'After that', 'Then', 'Next', or drop the softener and "
        "use a bare imperative.",
        (
            ("Now we install it. Let's configure it. Now we run it. Let's "
             "test it. Now we deploy.",
             "Install it, then configure it. Run and test it. Finally, deploy."),
        ),
    ),
    Tag.NOW_LETS_COMBO.value: _E(
        Tag.NOW_LETS_COMBO.value, "Redundant 'Now let's' / 'Let's now' pair",
        "The redundant combo 'Now let's' or 'Let's now' appears. Almost "
        "always rewrite. If the sentence introduces a code block: drop both "
        "softeners and use the bare imperative. If it is explanatory: "
        "rewrite declaratively ('We use X').",
        (
            ("Now let's run the tests.", "Run the tests."),
            ("Let's now use the cache.", "We use the cache."),
        ),
    ),
    Tag.PASSIVE_VOICE.value: _E(
        Tag.PASSIVE_VOICE.value, "Passive voice",
        "A passive-voice construction appears (detected by an NLP tagger). "
        "This check only runs with --nlp enabled, which requires the optional "
        "'nltk' dependency. Rewrite in active voice.",
        (
            ("The file was deleted by the script.",
             "The script deleted the file."),
        ),
    ),
}

del _E


def resolve(name: str) -> str | None:
    """Return the canonical tag value for a user-supplied name, or None.

    Accepts hyphens, underscores, and spaces interchangeably, and also
    resolves pattern-label aliases (e.g. 'content as actor' maps to
    'abstract-subject')."""
    norm = _normalize(name)
    if norm in {t.value for t in Tag}:
        return norm
    return _ALIASES.get(norm)


def explain(name: str) -> Explanation:
    """Return the Explanation for a user-supplied name.

    Raises KeyError if the name does not resolve to a known tag."""
    tag = resolve(name)
    if tag is None:
        raise KeyError(name)
    return _EXPLANATIONS[tag]


def all_tags() -> list[str]:
    """All canonical tag values, in enum order."""
    return [t.value for t in Tag]


def all_explanations() -> dict[str, Explanation]:
    """All explanations keyed by canonical tag value."""
    return dict(_EXPLANATIONS)
