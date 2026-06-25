"""Compiled patterns, thresholds, and rule data."""

import re


LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
QUESTION_HEADING_RE = re.compile(
    r"^#{1,6}\s+(Why|How|What|When|Where|Which|Who)\b"
)
# Allow-list for question-word headings that read as standard section
# names rather than rhetorical questions.
QUESTION_HEADING_ALLOWLIST = frozenset({
    "how it works",
})
QUESTION_MARK_HEADING_RE = re.compile(r"^#{1,6}\s+.*\?\s*$")
DEEP_HEADING_RE = re.compile(r"^#{3,}\s")
ITALIC_RE = re.compile(
    r"(?<![\w*])\*[^*\s][^*]*\*(?![\w*])|(?<![\w_])_[^_\s][^_]*_(?![\w_])",
)
SMART_QUOTES = {
    "‘": "left smart single quote",
    "’": "right smart single quote",
    "“": "left smart double quote",
    "”": "right smart double quote",
}
BARE_URL_RE = re.compile(r"\bhttps?://")
ANGLE_URL_RE = re.compile(r"<https?://")
DOUBLE_HYPHEN_RE = re.compile(r"(?<![<!/])--(?![/>])")
FOOTNOTE_DEF_RE = re.compile(r"^\s*\[\^[^\]]+\]:")
DASH_PARENTHETICAL_RE = re.compile(
    r"[a-zA-Z]\s+-\s+.*?\s+-\s+[a-zA-Z]"
)
LIST_ITEM_RE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
# Sentence-start "No X, no Y..." anaphora — typical verbless rhetorical
# fragment like "No frameworks, no magic - just Python and an LLM."
# Also catches the lazy "There's no X, no Y" / "There is no..." /
# "There are no..." dodge, which keeps the same anaphora behind a thin
# subject+verb scaffold.
ANAPHORIC_NO_RE = re.compile(
    r"(?:^|[.!?]\s+)"
    r"(?:There(?:'s|\s+is|\s+are)\s+no|No)"
    r"\s+\w+(?:\s+\w+){0,2},\s+no\s+\w+"
)
# Label-colon paragraph openers: "The problem: ...", "Goal: ...",
# "Three reasons: ...". Polish.md explains: use colons only to introduce
# lists, not to label a chunk of prose. Requires 2+ words after the
# colon so single-link references like "Code: [notebook.ipynb](url)"
# don't trip the rule.
LABEL_COLON_OPENER_RE = re.compile(
    r"^(?:The\s+)?[A-Z][a-zA-Z]+(?:\s+[A-Za-z]+){0,2}:\s+\w+\s+\w"
)
# Standalone two- or three-word label lines like "Rule of thumb:" or
# "What we cover:". These read as documentation labels rather than
# prose lead-ins. One-word labels are handled by the paragraph opener
# rule above when they introduce prose, with Note:/Important: exempted.
SHORT_LABEL_COLON_RE = re.compile(
    r"^[A-Z][A-Za-z'-]+(?:\s+[A-Za-z][A-Za-z'-]+){1,2}:\s*$"
)
# Single-word labels that work as callout / admonition blocks. `Note:`
# and `Important:` are the classic admonitions; `Video:` and `Code:`
# are common in lesson READMEs ("Video: <link>", "Code: [code/](code/)")
# and read as resource pointers, not prose labels. Other words read as
# ad-hoc labels and the rule still flags them.
CALLOUT_LABELS = frozenset({"note", "important", "video", "code"})
# Filler sentence-openers: "Now", "Let's", "Let us". Fine in moderation;
# overuse signals lazy transitions. Counted at file scope: flagged only
# when there are too many in a single document.
NOW_LETS_OPENER_RE = re.compile(r"(?:^|[.!?]\s+)(Now|Let's|Let us)\b")
NOW_LETS_MAX_PER_FILE = 4
# Redundant combos: "Now let's X" / "Let's now X". Almost always
# rewrite, regardless of count. The right rewrite depends on what
# follows:
#   - immediately before a code block: drop both softeners, use
#     the bare imperative ("Now let's run X." -> "Run X.").
#   - in a paragraph that explains rather than instructs: rewrite
#     declaratively ("Now let's use X." -> "We use X." or
#     "This lesson uses X.").
# Keeping just "Let's" is acceptable but not the preferred fix.
NOW_LETS_COMBO_RE = re.compile(
    r"(?:^|[.!?]\s+)(Now\s+let's|Let's\s+now)\b",
    re.IGNORECASE,
)

# Paragraph opening with a rhetorical question, like "Why do we need
# search?" or "What does this mean?". Polish.md says: state the point
# directly instead.
PARAGRAPH_QUESTION_OPENER_RE = re.compile(
    r"^(?:Why|How|What|When|Where|Which|Who|Is|Are|Can|Could|Should|Will|Would|Do|Does|Did)\b[^.!?\n]*\?"
)
# Cleft "[This/That/It] is what X is/are about" - pointless abstract
# framing. Polish.md flags clefts as judgment; this specific variant is
# distinctive enough to script.
THIS_IS_WHAT_ABOUT_RE = re.compile(
    r"\b(?:This|That|It)\s+is\s+what\s+\w+(?:\s+\w+){0,3}\s+(?:is|are|was|were)\s+about\b"
)
# Pseudo-cleft "X is [exactly] what made it Y" - inflates a plain causal
# claim into a cleft. Prefer "people found it useful because ...".
PSEUDO_CLEFT_MADE_RE = re.compile(
    r"\b(?:is|are|was|were)\s+(?:\w+\s+)?what\s+(?:made|makes|make)\s+"
    r"(?:it|them|this|that|him|her|us)\b",
    re.IGNORECASE,
)
THIS_IS_CODE_LEAD_IN_RE = re.compile(r"^This is\b.*:\s*$")

# Lazy headings starting with "The X". Catches both the bare "## The
# problem" and the suffix form "## The RAG idea" / "## The chunking
# problem" - any heading that opens with "The" and contains one of these
# vague abstract nouns. Specific nouns are fine ("## The Function URL").
LAZY_HEADING_LABELS = (
    "problem", "issue", "challenge", "solution", "goal", "idea",
    "reason", "answer", "catch", "fix", "approach", "trick",
    "concept", "point", "result", "way", "story", "principle",
    "takeaway", "insight", "lesson",
)
LAZY_HEADING_RE = re.compile(
    r"^#{1,6}\s+The\s+.*?\b(?:"
    + "|".join(LAZY_HEADING_LABELS)
    + r")\b",
    re.IGNORECASE,
)

# Single banned tokens. Whole-word, case-insensitive in prose.
BANNED_WORDS: dict[str, str] = {
    "twist": "drop the narrative cliche; state what actually changed",
    "angle": "drop the vague writing-jargon; name the focus ('what the post is about', 'the decision you made')",
    "delve": "use 'look at' / 'dig into' / 'explore'",
    "crucial": "drop or use 'important' / 'essential'",
    "pivotal": "drop the puffery",
    "vibrant": "drop the puffery",
    "intricate": "use 'detailed' or rewrite",
    "garner": "use 'gather' / 'get'",
    "bolster": "use 'strengthen' / 'add'",
    "foster": "use 'build' / 'help'",
    "showcase": "use 'show'",
    "enhance": "use a specific verb (improve / add / extend)",
    "emphasize": "name the concrete thing",
    "leverage": "use 'use'",
    "multifaceted": "drop or use the concrete description",
    "realm": "drop the metaphor",
    "captivating": "drop the puffery",
    "elevate": "use 'raise' / 'improve'",
    "suddenly": "drop",
    "basically": "drop",
    "very": "drop",
    "really": "drop",
    "underneath": "use 'under the hood' / 'inside' / 'behind'",
    "surprisingly": "drop the editorializing",
    "remarkably": "drop the editorializing",
    "faithful": "drop the metaphor; describe the concrete match",
    "prose": "use 'text', 'explanation', 'paragraph', or a concrete noun",
    "itself": "use sparingly; if it does not change the meaning, drop it",
    "non-negotiable": "drop the corporate-speak; name what is actually required",
    "inspect": "use 'look at' unless this is an exact API/tool word",
    "love": "use 'like' or name the concrete reason",
    "shape": "use a concrete word like 'structure', 'version', or name the code directly; keep only for NumPy array shapes",
    "contract": "drop the metaphor; name the concrete thing ('the schema', 'the API', 'the settings'). Keep only for a legal or smart contract",
    "rhythm": "use 'schedule', 'cadence', 'flow', or the concrete timing",
    "latched": "drop the metaphor; use 'picked it up', 'took it on', or name the action",
    "halves": "drop 'halves'; name the parts directly (the two processes, 'ingest and serve')",
    "trick": "drop the framing; there is no trick, just state the action directly ('ask the agent to...', 'we do X')",
    "wire": "use a concrete verb: connect, pass, add, configure, call, or name the exact change",
    "wired": "use a concrete verb: connected, passed, added, configured, called, or name the exact change",
    "wiring": "use a concrete verb: connecting, passing, adding, configuring, calling, or name the exact change",
}

# Multi-word banned phrases. Substring match, case-insensitive.
BANNED_PHRASES: dict[str, str] = {
    "in order to": "use 'to'",
    "this matters because": "give the concrete reason directly",
    "at this point": "use 'now' or cut",
    "this gives us": "use 'now we have' / 'we'll use'",
    "this is useful because": "name the use directly",
    "is what makes this": "rewrite with a direct verb and concrete subject",
    "the point is": "rewrite around what the reader should learn",
    "the point of": "rewrite around what the reader should learn",
    "the intent is": "name the action directly; abstract opener",
    "the goal is": "state what we are doing, not the goal",
    "the idea is": "state the idea directly",
    "the short rule": "drop the preamble; state the rule",
    "the short answer": "drop the preamble; give the answer",
    "the longer answer": "drop the preamble; give the answer",
    "the long answer": "drop the preamble; give the answer",
    "the important difference": "rewrite as a direct contrast",
    "the live build": "the workshop session is not a 'build'; use 'the live session' / 'the session'",
    "for the live build": "the workshop session is not a 'build'; use 'in the live session'",
    "reference implementation": "use 'finished app' / 'example app' / 'working version'",
    "demo artifact": "name the file/app/output",
    "framework-agnostic": "use 'works across frameworks'",
    "direct command interception": "use 'run slash commands before the model sees them'",
    "further reading": "use 'to learn more'",
    "for follow-up reading": "use 'to learn more'",
    "known-good version": "use 'working version'",
    "a clear pattern emerged": "drop the cliche",
    "here's the catch": "drop the cliche",
    "now for the fun part": "drop the cliche",
    "fresh struggle": "drop the cliche. Name the concrete feeling or situation ('you don't feel stuck when posting', 'you're not starting from scratch each week')",
    "hard to sit with": "drop the cliche; say plainly what was difficult ('it was not easy to deal with all the hate')",
    "nothing fancy": "drop the filler; state the concrete benefit",
    "nails it": "use 'works' or name the concrete behavior",
    "marks a pivotal moment": "drop the puffery",
    "turning point": "drop the puffery; name what actually changed",
    "a testament to": "drop the puffery",
    "reflects broader trends": "drop the puffery",
    "experts argue": "drop the vague attribution",
    "industry reports suggest": "drop the vague attribution",
    "the wider picture": "use a concrete pivot",
    "the bigger picture": "use a concrete pivot",
    "zooming out": "use a concrete pivot",
    "stepping back": "use a concrete pivot",
    "if you squint": "use a concrete pivot",
    "the bird's-eye view": "use a concrete pivot",
    "low-hanging fruit": "drop the idiom",
    "off the table": "say it directly",
    "at the end of the day": "drop the idiom",
    "in the first place": "drop the filler idiom",
    "cut to the chase": "drop the idiom",
    "the elephant in the room": "drop the idiom",
    "that bites us": "describe the event neutrally",
    "that bit me": "describe the event neutrally",
    "we got burned": "describe the event neutrally",
    "what follows is": "drop; let the headings show what is next",
    "in this section we will": "drop the meta-narration",
    "below you will find": "drop the meta-narration",
    "the next few paragraphs": "drop the meta-narration",
    "this section is short": "drop the meta-comment about length; go straight to the change",
    "this part is short": "drop the meta-comment about length; go straight to the change",
    "this write-up is based on": "open with what the reader will build, compare, or do",
    "as we shall see": "drop the meta-narration",
    "for reasons that will become clear": "give the reason on the same line",
    "the single most": "drop the superlative",
    "the hardest part": "drop the superlative",
    "the trickiest step": "drop the superlative",
    "the key insight": "drop the editorializing",
    "the big idea is": "state the idea directly",
    "this is where it gets interesting": "drop the editorializing",
    "the shape of": "show the shape, do not announce it",
    "on the wire": "name the bytes/payload directly; 'on the wire' is network jargon",
    "out of the box": "describe the default behavior in plain words",
    "tight inner loop": "describe the actual workflow (rebuild time, edit-test cycle)",
    "tight loop": "describe the actual workflow (rebuild time, edit-test cycle)",
    "lean on": "use a direct verb: use / depend on / rely on / ask",
    "leaned on": "use a direct verb: used / depended on / relied on / asked",
    "reusable principle": "name the workflow or habit directly",
    "serves as": "use 'is'",
    "stands as": "use 'is'",
    "stands in for": "use 'replaces', 'simulates', or 'we use X to fake Y'",
    "packaged up": "use 'created', 'stored', or name the object directly",
    "apply the same pattern": "name the concrete change instead",
    "is a good example": "start with 'For example,' and the concrete case",
    "diverse array": "drop the puffery",
    "commitment to excellence": "drop the puffery",
    "boasts a": "use 'has'",
    "let me tell you": "drop the filler",
    "let me explain": "drop the filler",
    "let me expand on": "drop the filler",
    "i want to be clear": "state the thing directly",
    "you could also": "avoid alternate-tactic padding; keep one clear path or example",
    "as mentioned above": "drop the backward reference; trust the reader or move the content",
    "as i mentioned above": "drop the backward reference; trust the reader or move the content",
    "as described earlier": "drop the backward reference; trust the reader or move the content",
    "is a reminder that": "drop the abstract framing; state the point directly",
    "pull request ceremony": "drop the jargon noun",
    "one benefit of": "state the benefit directly",
    "one clear": "name the exact value or property instead of using this filler",
    "on the table": "say it directly",
    "in action": "drop the cliche; describe what is actually happening",
    "rule of thumb": "state the rule directly",
    "the power of": "drop the abstract framing; describe what the design does",
    "the advantage of": "drop the abstract framing; name the concrete benefit",
    "the beauty of": "drop the puffery; describe the concrete property",
    "the magic of": "drop the puffery; describe the concrete mechanism",
    "the strength of": "drop the abstract framing; name the concrete property",
    "the elegance of": "drop the puffery; describe the concrete property",
    "the simplicity of": "drop the abstract framing; describe the concrete property",
    "the backbone of": "drop the metaphor; describe what the component actually does",
    "the heart of": "drop the metaphor; describe what the component actually does",
    "the core of": "drop the metaphor; describe what the component actually does",
    "the cornerstone of": "drop the metaphor; describe what the component actually does",
    "the foundation of": "drop the metaphor; describe what the component actually does",
    "works well": "drop the filler; name the concrete property that fits",
    "works great": "drop the filler; name the concrete property that fits",
    "fits well": "drop the filler; name the concrete property that fits",
    "all of this": "name the concrete actions, files, screens, or behavior",
    "suffer": "do not anthropomorphize - inanimate things don't suffer; "
               "describe what actually goes wrong "
               "('the answer is wrong', 'the latency doubles')",
}

# Regex banned phrases. Use these for phrasing families where exact
# substring matching would miss the pattern.
BANNED_PHRASE_PATTERNS: dict[str, tuple[re.Pattern[str], str]] = {
    "close the loop": (
        re.compile(r"\bclos(?:e|es|ed|ing)\s+the\s+loop\b", re.IGNORECASE),
        "drop the cliche; state plainly what now works or what connects to what",
    ),
    "rough edges": (
        re.compile(r"\b(?:rough|sharp)\s+edges?\b", re.IGNORECASE),
        "drop the cliche; name the concrete problems or limitations",
    ),
    "pin (verb)": (
        re.compile(r"\bpin(?:s|ned|ning)?\b", re.IGNORECASE),
        "drop the verb metaphor; use 'set', 'fix', 'force', or name the "
        "action. Keep only for the literal git/pip 'pin a version' sense",
    ),
    "lock in": (
        re.compile(r"\block(?:s|ed|ing)?\s+in\b", re.IGNORECASE),
        "drop the metaphor; use 'set', 'fix', 'force', or name the action",
    ),
    "fuel (verb)": (
        re.compile(r"\bfuel(?:s|ed|ing|led|ling)?\b", re.IGNORECASE),
        "drop the 'fuel' metaphor; name what it provides ('that backlog "
        "gives you topics', 'feeds', 'supplies'). Keep only the literal "
        "noun sense (diesel fuel)",
    ),
    "carry (metaphor)": (
        re.compile(r"\bcarr(?:y|ies|ied|ying)\b", re.IGNORECASE),
        "drop the 'carry' metaphor; say what it does plainly ('includes', "
        "'sends', 'holds', 'has', 'persists', 'transfers')",
    ),
    "break down (explain)": (
        re.compile(
            r"\bbreak(?:s|ing)?\s+down\s+"
            r"(?:the|a|an|this|that|these|those|how|what|why|your|our|"
            r"each|every|its)\b",
            re.IGNORECASE,
        ),
        "drop the 'break down' cliche; use 'describe', 'outline', or "
        "'discuss'. Keep the literal 'fails' sense ('where it breaks down')",
    ),
    "makes ... concrete": (
        re.compile(
            r"\bma(?:ke|kes|de)\s+(?:[\w'-]+\s+){1,4}concrete\b(?!\s+[a-z])",
            re.IGNORECASE,
        ),
        "drop the 'makes X concrete' cliche; show the concrete thing "
        "directly (state the points, give the example)",
    ),
    "drive home (cliche)": (
        re.compile(
            r"\bdr(?:ive|ives|ove|iving|iven)\s+(?:[\w'-]+\s+){0,3}home\b",
            re.IGNORECASE,
        ),
        "drop the 'drive home' cliche; state the point directly",
    ),
    "one of these (vague list lead-in)": (
        re.compile(r"\bone of (?:these|the following)\b", re.IGNORECASE),
        "name what the list contains instead of 'one of these'; the "
        "lead-in should describe the items",
    ),
    "walk the text": (
        re.compile(
            r"\bwalk(?:s|ed|ing)?\s+(?:through\s+|across\s+|over\s+|down\s+)?"
            r"the\s+(?:text|string|data|array|list|sequence|file|input|"
            r"document|characters|chars|tokens|rows|bytes)\b",
            re.IGNORECASE,
        ),
        "don't anthropomorphize iteration - code doesn't 'walk' the text; "
        "say what it does ('takes a window of N characters', 'iterates over "
        "the rows', 'slides across the text')",
    ),
    "the/a ... below": (
        re.compile(
            r"\b(?:the|a|an)\s+[\w`-]+(?:\s+[\w`-]+){0,3}\s+below\b",
            re.IGNORECASE,
        ),
        "drop the forward reference; name the thing directly",
    ),
    "the/a ... result is": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:the|a|an)\s+(?:[A-Za-z][\w-]*\s+){0,2}"
            r"result\s+(?:is|was)\b",
            re.IGNORECASE,
        ),
        "name the actor or concrete output directly: 'we now have', "
        "'this creates', 'the command prints', 'the script returns'",
    ),
    "the/a ... fix is": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:the|a|an)\s+(?:[A-Za-z][\w-]*\s+){0,2}"
            r"fix\s+(?:is|was)\b",
            re.IGNORECASE,
        ),
        "name the concrete change instead: 'we raise max_tokens', "
        "'set X', 'add the flag'",
    ),
    "the/a ... flow is": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:the|a|an)\s+(?:[A-Za-z][\w-]*\s+){0,2}"
            r"flow\s+(?:is|was)\b",
            re.IGNORECASE,
        ),
        "drop the topic-introducer and start with the actions in the flow",
    ),
    "the/a ... setup is": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:the|a|an)\s+(?:[A-Za-z][\w-]*\s+){0,2}"
            r"setup\s+(?:is|was)\b",
            re.IGNORECASE,
        ),
        "drop the recap sentence and move to the next concrete point",
    ),
    "the/a ... hurdle is": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:the|a|an|another|final)\s+"
            r"(?:[A-Za-z][\w-]*\s+){0,2}hurdle\s+(?:is|was)\b",
            re.IGNORECASE,
        ),
        "drop the abstract hurdle label and name the concrete problem",
    ),
    "the/a ... aim is": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:the|a|an|our|my)\s+"
            r"(?:[A-Za-z][\w-]*\s+){0,2}aims?\s+"
            r"(?:is|isn't|are|was|wasn't|is\s+not|was\s+not)\b",
            re.IGNORECASE,
        ),
        "drop the 'the aim is' framing; state it directly ('you don't need "
        "a perfect post, just three clear drafts')",
    ),
    "the/a ... example:": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:the|a|an|another|recent)\s+"
            r"(?:[A-Za-z][\w-]*\s+){0,2}example:\s+",
            re.IGNORECASE,
        ),
        "drop the example label and start with the example itself",
    ),
    "the/a ... option is": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:the|a|an|another)\s+"
            r"(?:[A-Za-z][\w-]*\s+){0,2}option\s+(?:is|was)\b",
            re.IGNORECASE,
        ),
        "avoid alternate-tactic padding; keep one clear path or example",
    ),
    "here is a ...": (
        re.compile(
            r"(?:^|[.!?]\s+)here(?:'s|\s+is)\s+"
            r"(?:a|an|the)\s+[A-Za-z][\w-]*\b",
            re.IGNORECASE,
        ),
        "drop the label and state the concrete point directly",
    ),
    "buy (transactional metaphor)": (
        re.compile(
            r"\b(?:buy|buys|bought|buying)\s+"
            r"(?:us|you|me|them|nothing|little|much|anything|everything)\b",
            re.IGNORECASE,
        ),
        "drop the transactional metaphor; name the concrete result. "
        "'buys us X' -> 'gives us X'; 'buys nothing' -> 'is wasted', "
        "'goes unused', 'does nothing for us'",
    ),
    "the only question ... is": (
        re.compile(
            r"(?:^|[.!?]\s+)the\s+only\s+question\b"
            r"(?:\s*:|(?:\s+[A-Za-z][\w-]*){0,8}\s+is\s*:)",
            re.IGNORECASE,
        ),
        "drop the scaffolding; ask or state the question directly",
    ),
    "pattern behind ... is": (
        re.compile(
            r"\b(?:the|a|an|this|that)?\s*pattern\s+behind\b"
            r"[^.!?]*?\b(?:is|are|was|were|be|been|being)\b",
            re.IGNORECASE,
        ),
        "abstract summary subject pointing back at the previous sentences; "
        "write a direct statement with a concrete subject and verb "
        "(e.g. 'you get exposure')",
    ),
    "the/a ... pattern is": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:a|an|one|another|the)\s+(?:[A-Za-z][\w-]*\s+){0,2}"
            r"pattern\s+(?:is|was|here\s+is)\b",
            re.IGNORECASE,
        ),
        "drop the 'pattern' framing; state the approach directly ('publish "
        "on a blog and republish to Substack')",
    ),
    "content as actor": (
        # A content noun (the workshop/section/part/lesson/page/notebook/...)
        # as the grammatical subject at the start of a sentence. Intentionally
        # broad: any word may follow, so copulas and compounds flag too ("the
        # workshop is one repo", "the workshop code puts...", "the notebooks
        # have..."). Rewrite with a real actor (we/you) or recast.
        re.compile(
            r"(?:^|[.!?]\s+)"
            r"(?:The|This|That|Next|Last|Previous|Final|Current)\s+"
            r"(?:[a-z]+\s+)?"
            r"(?:lessons?|sections?|chapters?|parts?|modules?|units?|"
            r"tutorials?|workshops?|guides?|pages?|articles?|write-ups?|"
            r"readmes?|documents?|docs?|notebooks?)\s+"
            r"[a-z]",
            re.IGNORECASE,
        ),
        "content does not act; write 'in the previous lesson, we added' "
        "or name the concrete code/output",
    ),
    "need ... ideas": (
        re.compile(
            r"\b(?:we|you|i|they)\s+need(?:\s+\w+){0,3}\s+ideas?\b",
            re.IGNORECASE,
        ),
        "name the concrete concepts, steps, or tasks instead of saying "
        "the reader needs ideas",
    ),
    "first, how do we": (
        re.compile(
            r"(?:^|[.!?]\s+)first,\s+how\s+do\s+we\b",
            re.IGNORECASE,
        ),
        "avoid rhetorical question scaffolding; state the first action directly",
    ),
    "scope/source material opener": (
        re.compile(
            r"^(?:#{1,6}\s+)?(?:scope|source material)\b",
            re.IGNORECASE,
        ),
        "open with what the reader will build, compare, or do",
    ),
    "face the call": (
        re.compile(
            r"\bfac(?:e|es|ed|ing)\s+(?:the\s+)?(?:same\s+)?call\b",
            re.IGNORECASE,
        ),
        "drop the cliche; name the decision directly "
        "('you may have to make the same choice')",
    ),
    "neither ... nor": (
        re.compile(
            r"\bneither\b[^.!?]{0,80}\bnor\b",
            re.IGNORECASE,
        ),
        "drop the 'neither ... nor' construction; it is hard to parse. "
        "Rewrite positively ('both X and Y read from disk') or with a "
        "plain negative ('X never hits the network')",
    ),
    "runs on a laptop (filler)": (
        re.compile(
            r"\b(?:everything runs|it all runs|you can run "
            r"(?:everything|the workshop|it all|this(?:\s+workshop)?))\b"
            r"[^.!?]{0,25}\bon (?:a|your) laptop\b",
            re.IGNORECASE,
        ),
        "drop the filler scene-setting ('runs on a laptop'); list the actual "
        "prerequisites instead, or cut it",
    ),
    "has none": (
        re.compile(
            r"\b(?:has|have|had|gets?|got)\s+none\b",
            re.IGNORECASE,
        ),
        "vague; name what is actually missing instead of 'none' "
        "('has no embedder', 'ships without one', 'does not include one')",
    ),
    "land (verb)": (
        re.compile(
            r"\b(?:to\s+land|land(?:s|ed|ing))\b",
            re.IGNORECASE,
        ),
        "drop the 'land' metaphor; data, files, and walkthroughs do not "
        "'land'. Say it plainly: 'is committed to git', 'is written to', "
        "'ends up in', 'goes on Turso', 'arrives'. (The noun 'land' and "
        "'landing page' are fine.)",
    ),
    "hand (verb)": (
        re.compile(
            r"\b(?:to\s+hand|hand(?:s|ed|ing))\b",
            re.IGNORECASE,
        ),
        "drop the 'hand' metaphor. A tool, system, or workshop does not "
        "'hand' the reader anything. Use 'give', or say it plainly: 'gives "
        "you a system', 'you get a repeatable process', 'it sets up'. (The "
        "noun 'hand', 'hands-on', and 'hand off' are fine.)",
    ),
    "built around (framing)": (
        re.compile(
            r"\b(?:whole\s+|entire\s+)?(?:workshop|session|course|class|"
            r"tutorial|lesson|chapter|article|post|talk|guide)\s+is\s+"
            r"built\s+around\b",
            re.IGNORECASE,
        ),
        "drop the 'built around X' framing. It narrates the document instead "
        "of delivering it. State the thing directly: 'You run one challenge "
        "after the session', 'We cover X, then Y'.",
    ),
    "structure signposting": (
        re.compile(
            r"\bthe\s+(?:first|second|latter|former)\s+half\s+"
            r"(?:is|covers?|focuses?|deals?|introduces?|explains?|walks?|"
            r"goes?|gets?|starts?)\b",
            re.IGNORECASE,
        ),
        "drop the 'first half ... second half' signposting. Use 'in the "
        "first ..., in the second ...' ('in the first part we work on "
        "mindset, in the second we get practical'), or just write the "
        "content of each part directly.",
    ),
    "section self-narration": (
        re.compile(
            r"\b(?:this|the)\s+(?:section|part|chapter|page|post)\s+"
            r"(?:ends?|opens?|closes?|starts?|begins?|finishes?|wraps?)\s+"
            r"(?:up\s+)?(?:with|by)\b",
            re.IGNORECASE,
        ),
        "don't narrate where content sits in the document ('this section "
        "ends with why', 'this part opens with setup'). Say what you do "
        "('we explain why') or just deliver the content.",
    ),
    "abstract subject splits itself": (
        re.compile(
            r"\b(?:the\s+)?(?:work|task|job|project|process|pipeline|flow|"
            r"workflow|build|setup|code|logic)\s+"
            r"(?:splits?|divides?|breaks?|separates?|falls?)\s+"
            r"(?:up\s+|down\s+|apart\s+)?into\b",
            re.IGNORECASE,
        ),
        "abstract subject acting on its own - 'the work' does not split "
        "itself. Prefer active voice with a real actor: 'we split the work "
        "into ...', 'we run two processes'",
    ),
    "worth <gerund>": (
        re.compile(
            r"\bworth\s+(?:[a-z]+ing|a\s+(?:look|read|mention|try|shot))\b",
            re.IGNORECASE,
        ),
        "drop the 'worth X' framing; it is passive-sounding filler. State "
        "the point or the action directly ('we change two things here', "
        "'these reasons matter because...')",
    ),
    "menu (metaphor)": (
        re.compile(
            r"\b(?:wider|broader|bigger|fuller|full|whole)\s+menu\b"
            r"|\bmenu\s+of\s+(?:options|ideas|choices|topics)\b",
            re.IGNORECASE,
        ),
        "drop the 'menu' metaphor; name the options directly ('post ideas "
        "fall into three groups')",
    ),
    "for good (permanently)": (
        re.compile(
            r"\bfor good\b(?!\s+(?:results?|reasons?|measure|practices?|examples?|luck))",
            re.IGNORECASE,
        ),
        "drop 'for good'; it just solves the problem",
    ),
    "at once": (
        re.compile(r"\bat once\b", re.IGNORECASE),
        "drop 'at once' and let the editor pick the contextual replacement: "
        "'in one go' / 'in a single call' / 'in one batch' for the "
        "single-operation sense, or 'at the same time' for the simultaneous "
        "sense",
    ),
    "the/a ... followed": (
        re.compile(
            r"(?:^|[.!?]\s+)(?:the|a|an|our)\s+(?:[A-Za-z][\w-]*\s+){0,2}"
            r"followed(?=[.,;:]|\s+(?:soon|quickly|shortly|naturally|then|next)\b)",
            re.IGNORECASE,
        ),
        "abstract noun as the actor of a vague consequence ('the growth "
        "followed'). Name what happened and why: 'subscribers grew 9% that "
        "week because ...'",
    ),
}

# Labels in BANNED_PHRASE_PATTERNS that belong to the "abstract noun as the
# subject/actor of a claim" family. These emit the `abstract-subject` tag
# instead of the generic `banned-phrase` so the family is filterable and has
# one home. The smell is broader than any regex can catch deterministically
# (see polish.md "Don't make an abstract noun the subject"); these patterns
# only catch the narrow, unambiguous offenders.
ABSTRACT_SUBJECT_LABELS: frozenset[str] = frozenset({
    "the/a ... result is",
    "the/a ... fix is",
    "the/a ... flow is",
    "the/a ... setup is",
    "the/a ... hurdle is",
    "the/a ... option is",
    "the/a ... aim is",
    "the/a ... pattern is",
    "content as actor",
    "abstract subject splits itself",
    "the/a ... followed",
})

# Sentence openers. Capitalized, must start the line (allowing optional list
# marker). Match is case-sensitive on the opener token itself.
BANNED_OPENERS: dict[str, str] = {
    "Additionally": "drop or rewrite",
    "Moreover": "drop or rewrite",
    "Furthermore": "drop or rewrite",
    "Notably": "drop or rewrite",
    "Importantly": "drop or rewrite",
    "Consequently": "drop or rewrite",
}
OPENER_RE = re.compile(
    r"^(?:[-*]\s+|\d+\.\s+)?(" + "|".join(re.escape(w) for w in BANNED_OPENERS) + r")\b"
)
WORD_RES: dict[str, re.Pattern[str]] = {
    word: re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)
    for word in BANNED_WORDS
}

# Per-word exception contexts. When a banned word appears ONLY inside one of
# these patterns on a line, it is a valid technical use rather than the banned
# sense, so it is not flagged. (Code spans and fenced blocks are already
# stripped before the check, so these only handle valid uses in prose.)
WORD_EXCEPTION_RES: dict[str, re.Pattern[str]] = {
    # "shape" is fine for NumPy/tensor array shapes and attribute access:
    # "X.shape", "a tensor with shape (2, 768)", "the output shape".
    "shape": re.compile(
        r"\.shape\b"
        r"|\b(?:numpy|np|tensor|tensors|array|arrays|ndarray|matrix|matrices|"
        r"vector|vectors|output|input|embedding|embeddings|batch|hidden|"
        r"logits|dimension|dimensions)\b[^.!?`]{0,25}\bshapes?\b",
        re.IGNORECASE,
    ),
    # "contract" is fine as the technical term "API contract".
    "contract": re.compile(r"\bAPIs?\s+contract\b", re.IGNORECASE),
}

# Per-phrase exception contexts for BANNED_PHRASE_PATTERNS (same idea as
# WORD_EXCEPTION_RES).
PHRASE_EXCEPTION_RES: dict[str, re.Pattern[str]] = {
    # "landing page" / "landing pad" / "landing zone" are fixed nouns, not
    # the banned "land" verb metaphor.
    "land (verb)": re.compile(
        r"\blanding\s+(?:page|pad|zone)s?\b",
        re.IGNORECASE,
    ),
    # "pin" is fine in the literal git/pip sense: pinning a version, a
    # dependency, or a commit (the rule only bans the "hold/fix" metaphor).
    "pin (verb)": re.compile(
        r"\bpinned\s+(?:commit|version|dependency|dependencies|sha|tag|release)\b"
        r"|\bpin(?:s|ned|ning)?\b[^.!?`]{0,25}\b(?:version|versions|dependency|"
        r"dependencies|commit|commits|python|requires-python|sha|hash|tag|"
        r"release|uv\.lock|pyproject)\b"
        r"|\b(?:version|dependency|dependencies|commit|python|requires-python|"
        r"repo|template|pyproject|toml|uv|prototype)\b[^.!?`]{0,25}"
        r"\bpin(?:s|ned|ning)?\b"
        r"|\b(?:the|a|this)\s+(?:\w+\s+)?pin\b"
        r"|\brelax(?:es|ed|ing)?\s+the\s+pin\b",
        re.IGNORECASE,
    ),
    # "hands-on", the phrasal "hand off / over / back / out / in", and
    # "-handed" compounds are noun/idiom uses, not the banned "hand (someone
    # something)" giving metaphor.
    "hand (verb)": re.compile(
        r"\bhands?-on\b"
        r"|\b(?:to\s+)?hand(?:s|ed|ing)?\s+(?:off|over|back|out|in)\b"
        r"|\b[a-z]+-handed\b",
        re.IGNORECASE,
    ),
}
CODE_BLOCK_MAX_LINES = 40
BLOCKQUOTE_MAX_LINES = 3
HEADING_RE = re.compile(r"^#{1,6}\s")
LIST_RE = re.compile(r"^\s*[-*]\s|^\s*\d+\.\s")
BLOCKQUOTE_RE = re.compile(r"^\s*>")
PYTHON_CHAINED_GET_RE = re.compile(r"\.get\([^)]*\)\.get\(")
PARAGRAPH_MAX_SENTENCES = 5
# Upper bound on sentence length. Set at 25, not lower: a tighter cap
# (we ran 20 for a while) pushes authors to chop flowing sentences into
# staccato fragments, which reads worse than one slightly-long sentence
# and trips choppy-rhythm / label-fragment instead. The fix for a real
# over-length sentence is ONE natural split into two sentences, not many
# short ones - the rule messages say so.
SENTENCE_MAX_WORDS = 25
SENTENCE_MAX_COMMAS = 3
# Choppy-rhythm threshold: a sentence with at most this many words
# counts as "short". TWO short sentences in a row already read as
# staccato - especially with a longer sentence right after - so the run
# bar is 2, not 3 ("So we make two changes. Retrieval becomes semantic.
# The data moves somewhere it survives restarts without paying for a
# server." -> "We make two changes: retrieval becomes semantic, and the
# data moves to a store that survives restarts without a paid server.").
CHOPPY_SENTENCE_MAX_WORDS = 9
CHOPPY_SENTENCE_MIN_RUN = 2
# A single very short sentence (this many words or fewer) sitting right
# before a longer one is a merge candidate on its own, even when it is
# not part of a run of short sentences: "Retrieval becomes semantic. The
# data moves somewhere it survives restarts..." -> join the small clause
# onto the longer sentence.
MERGE_SHORT_MAX_WORDS = 4
SENTENCE_END_RE = re.compile(r"[.!?](?=[\s\"')\]]|$)")
# Colon-introduced inline list with 3+ items and a terminal and/or.
# "We use these tools: numpy, pandas, scikit-learn, and matplotlib" -
# the colon signals enumeration intent, so the items should be bullets.
COLON_INLINE_LIST_RE = re.compile(
    r":\s+(?:[^,.;:!?\n]+,\s+){2,}(?:and|or)\s+[^.!?\n]+[.!?]?\s*$"
)
# Minimum consecutive sentences sharing a 2-word opener that triggers
# a "consider a bullet list" flag. Three is the smallest run that reads
# as repeated parallel structure rather than coincidence.
PARALLEL_SENTENCE_MIN_RUN = 3

# Shared decision hint embedded in error messages that suggest list
# conversion. The heuristic lives here (and not only in stylint/style_guide/polish.md)
# because agents reading the lint output often skip reference docs.
LIST_HEURISTIC_HINT = (
    "Convert to a bullet list only when BOTH (a) each item is 3+ words "
    "and items are parallel in structure, AND (b) the author already "
    "signalled enumeration (colon + items, or 3+ adjacent sentences "
    "with the same opener). Skip conversion when items end in "
    "'and others'/'and more'/'and so on', when commas are clausal "
    "(joining clauses, not items), or when inline reads fine."
)
# The parallel-completion test - the human-facing rule for deciding
# between bullet list and sentence split. The classifier
# (classify_long_with_commas in text.py) is just a hint; the rule below
# is what an editor actually applies.
PARALLEL_COMPLETION_TEST = (
    "Test: can you write a single lead-in line that all the commas "
    "finish without re-introducing the subject or verb? "
    "Yes -> bullet list. "
    "No -> split into 2-3 sentences."
)
# Open enumerations - "..., and others", "..., and so on", "etc.".
# These signal the writer intentionally left the list open, so the
# inline form is the right choice. Skip the long-and-commas fire here.
# Allow trailing footnote refs like [^12][^7] after the closer so the
# rule still fires on cited prose.
OPEN_ENUM_TAIL_RE = re.compile(
    r"(?:,\s+(?:and\s+)?(?:others|more|so\s+on)|\betc\.?)"
    r"(?:\s*\[\^[^\]]+\])*\s*[.!?]?\s*$",
    re.IGNORECASE,
)
# Footnote reference (Pandoc-style): [^1], [^abc]. Strip these before
# classifying long-and-commas so they don't break end-of-sentence anchors.
FOOTNOTE_REF_RE = re.compile(r"\[\^[^\]]+\]")
# Action-chain detection: 2+ comma chunks that start with a transitive
# verb sharing an elided subject ("you open X, pick Y, choose Z").
# These look list-shaped but are sequential actions; bulleting them
# reads as robotic. Classify as clause-likely so the fix is a split.
ACTION_CHAIN_VERBS = (
    r"pick|choose|select|find|get|take|give|send|receive|make|build|do|"
    r"create|delete|remove|add|edit|modify|change|replace|update|"
    r"click|press|type|drag|drop|copy|paste|save|load|"
    r"run|execute|install|uninstall|configure|set|test|debug|fix|"
    r"open|close|start|stop|end|finish|begin|continue|"
    r"write|read|parse|format|convert|transform|fetch|store|"
    r"ask|tell|say|show|hide|display|present|describe|explain|define|"
    r"think|consider|decide|plan|design|"
    r"deploy|ship|release|publish|"
    r"use|try|keep|wait|move|"
    r"correct|verify|validate|review|check"
)
ACTION_CHAIN_RE = re.compile(
    # Match the verb stem optionally followed by -s (3rd person), -ed
    # (past), or -ing (continuous), optionally preceded by a chunk
    # connector like "and"/"or"/"then". Catches "..., and checks X",
    # "..., extracts Y", "..., running Z".
    rf",\s+(?:and\s+|or\s+|then\s+|also\s+)?"
    rf"(?:{ACTION_CHAIN_VERBS})(?:s|es|ed|d|ing)?\s+",
    re.IGNORECASE,
)
# Irregular past-tense action verbs at chunk start. These don't fit
# the stem+suffix pattern above.
IRREGULAR_PAST_RE = re.compile(
    r",\s+(?:and\s+|or\s+|then\s+|also\s+)?"
    r"(?:ran|went|came|took|made|gave|sent|got|saw|said|"
    r"wrote|bought|sold|thought|brought|caught|taught|fought|sought|"
    r"found|kept|left|met|paid|built|spent|held|told|drew|grew|"
    r"knew|threw|flew|drove|broke|spoke|woke|chose|ate|drank|stole)\s+",
    re.IGNORECASE,
)
# Meta-framing: '[The/A/Another] <abstract noun> [of X] is that <claim>'.
# The writer announces the shape of the claim ('here comes an
# advantage / limitation / insight / trick') instead of just stating
# the claim. Same family as label-colon ('The problem: ...') but in
# sentence form with 'is that' as the marker. Fix: drop the framing
# noun phrase and lead with the actual claim.
META_FRAMING_NOUNS = (
    r"advantage|disadvantage|benefit|drawback|downside|upside|"
    r"limitation|restriction|constraint|"
    r"problem|issue|challenge|catch|gotcha|"
    r"point|idea|insight|takeaway|lesson|"
    r"trick|secret|magic|beauty|strength|elegance|simplicity|"
    r"power|value|virtue|"
    r"principle|intent|goal|reason|motivation|rationale|"
    r"difference|distinction|"
    r"hope|fear|"
    r"fact|truth|reality|thing|"
    r"key|core|gist|crux|essence"
)
REPEATED_AND_RE = re.compile(
    # Three or more items joined by 'and' instead of the usual oxford
    # comma: 'Claude Code and Codex and OpenCode' rather than
    # 'Claude Code, Codex and OpenCode'. Each item is a 1-4 word token
    # group (lowercased or proper noun). Catches polysyndetic chains
    # users sometimes write to dodge the 'and X' list-classifier
    # heuristic. Idioms ('more and more', 'date and time') still fire
    # when they appear inside a longer chain - 'X and more and more Y'
    # reads as bad as any other polysyndetic chain.
    r"(?:\b[A-Za-z][\w.]*(?:\s+[A-Za-z][\w.]*){0,3}\s+and\s+){2,}"
    r"[A-Za-z][\w.]*(?:\s+[A-Za-z][\w.]*){0,3}\b",
)
META_FRAMING_RE = re.compile(
    r"(?i)\b(?:the|a|an|another|one)\s+"
    # 0-2 modifier tokens between the determiner and the framing noun
    # (e.g. 'a big advantage', 'another phone limitation', 'the key insight')
    r"(?:[A-Za-z][\w-]*\s+){0,2}"
    rf"(?:{META_FRAMING_NOUNS})"
    # optional qualifier: "of/about/with/between X (...)"
    r"(?:\s+(?:of|about|with|between|to|for|behind)\s+\S+(?:\s+\S+){0,4})?"
    r"\s+is\s+that\b"
)
# Generic verb-led chunk detector: a comma chunk that does NOT start
# with a determiner/pronoun/preposition is likely verb-led. This
# catches action chains the curated verb list misses (detects,
# extracts, calculates, summarises, ...). Used as a fallback signal.
NON_VERB_STARTERS = frozenset({
    "a", "an", "the", "this", "that", "these", "those",
    "my", "your", "his", "her", "its", "our", "their",
    "some", "any", "no", "every", "each", "all", "both",
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "another", "such", "many", "few", "much", "little", "most",
    "of", "in", "on", "at", "to", "for", "by", "with", "from",
    "into", "onto", "through", "around", "over", "under", "above",
    "below", "between", "among", "during", "after", "before", "since",
    "though", "although", "while", "because", "if", "when", "where",
    "as", "than", "but", "or", "and", "so", "yet",
    "which", "that", "who", "whom", "whose", "what", "whatever",
    "however", "moreover", "additionally", "instead",
})
# Subordinating / coordinating conjunctions that appear AFTER a comma
# and signal a clause boundary (not a list item). When any of these
# follow a comma in a long-and-commas sentence, the right fix is a
# sentence split - bullets would butcher the meaning.
CLAUSE_MARKER_RE = re.compile(
    r",\s+(?:which|that|who|whom|whose|while|though|although|because|"
    r"since|but|however|so|when|if|then|after|before|where|whereas)\b",
    re.IGNORECASE,
)
# Colon precedes the comma run: "X includes A, B, and C". Strong
# signal the writer already framed the commas as enumeration.
COLON_BEFORE_COMMAS_RE = re.compile(r":\s+[^,.;:!?\n]+,")
# Terminal "and X" / "or X" closing an enumeration. Combined with 3+
# comma chunks, this is a list-shape closer.
TERMINAL_AND_OR_RE = re.compile(
    r",\s+(?:and|or)\s+[A-Za-z][^.!?\n]*[.!?]?\s*$",
    re.IGNORECASE,
)
ABBREVIATION_RE = re.compile(
    r"\b(?:e\.g|i\.e|etc|vs|cf|Mr|Mrs|Ms|Dr|St|Jr|Sr|U\.S|U\.K|a\.m|p\.m|Inc|Ltd|Co)\.",
    re.IGNORECASE,
)
GERUND_NOUN_EXCEPTIONS = {
    "spring", "string", "building", "setting", "meeting",
    "heading", "wedding", "beginning", "ending", "standing",
    "wing", "sing", "ring", "king", "thing", "bring",
    "everything", "nothing", "something", "anything",
    "morning", "evening", "saying", "streaming",
}
# Participial phrases: -ing phrase, then COMMA, then a likely new subject.
# Matches "Reading through it, I noticed..." but not "Calling them works, but..."
# (the gerund-as-subject form, where the verb sits before the comma).
_PARTICIPIAL_TAIL = r"\b[^.!?]{0,150},\s+(?:I|we|you|they|he|she|it|the|a|an|this|that|these|those)\b"
GERUND_LINE_START_RE = re.compile(r"^([A-Z][a-z]{3,}ing)" + _PARTICIPIAL_TAIL)
GERUND_MIDLINE_RE = re.compile(r"[.!?]\s+([A-Z][a-z]{3,}ing)" + _PARTICIPIAL_TAIL)

# Subjectless past-action fragments like "Ran the workshop." or
# "Added tests." These usually come from notes or commit messages and
# need an explicit actor in article/tutorial prose: "I ran..." or
# "We add...". Keep the list conservative; many -ed words are valid
# adjectives ("finished app", "managed runtime").
PAST_TENSE_FRAGMENT_IRREGULARS = (
    r"ran|built|wrote|made|got|took|sent|found|kept|left|met|paid|held|"
    r"told|drew|grew|knew|threw|flew|drove|broke|spoke|chose"
)
PAST_TENSE_FRAGMENT_RE = re.compile(
    r"(?:^|[.!?]\s+)"
    r"([A-Za-z][A-Za-z-]{2,}ed|" + PAST_TENSE_FRAGMENT_IRREGULARS + r")\s+"
    r"(?!when\b|while\b|because\b|if\b|that\b|which\b)"
    r"[a-zA-Z0-9`][^.!?\n]{0,120}[.!?]?",
    re.IGNORECASE,
)

# Chopped label fragments: a short verbless noun phrase used as a
# pseudo-label or lead-in, terminated by a period instead of being
# folded into the sentence it introduces. "The goal behind it. I did
# not want to pay for a server." / "Why not Postgres. The hosts I
# looked at..." The reader loses the idea because the fragment carries
# no subject+verb. Same family as label-colon ("The problem: ...") but
# with a period. Concrete proper-noun labels ("Railway.", "Render.")
# are NOT flagged - only abstract determiner+noun fragments and
# verbless wh-fragments, where meaning actually drops out.
FRAGMENT_MAX_WORDS = 6
FRAGMENT_DETERMINERS = frozenset({
    "the", "a", "an", "this", "that", "our", "its", "my", "their",
    "these", "those",
})
FRAGMENT_WH = frozenset({
    "why", "what", "how", "when", "where", "which", "who",
})
# Abstract head nouns that read as labels rather than concrete subjects.
# Reuses the lazy-heading label set plus a few more.
FRAGMENT_ABSTRACT_NOUNS = frozenset(LAZY_HEADING_LABELS) | frozenset({
    "motivation", "rationale", "intent", "plan", "setup", "target",
    "thinking", "logic", "tradeoff", "tension", "gist", "crux",
    "upshot", "aim", "purpose", "difference", "distinction", "rule",
    "thing", "deal", "case", "situation",
})
# Tokens that signal a finite verb / predicate is present, so a short
# sentence is a real sentence rather than a label fragment. The -ed/-ing
# inflections are caught separately; bare -s is NOT treated as a verb
# signal (too many plural nouns end in -s), so the common -s verb forms
# that show up in tiny sentences are listed explicitly.
FRAGMENT_VERB_TOKENS = frozenset({
    "is", "are", "was", "were", "be", "been", "being", "am",
    "'s", "'re", "'m",
    "do", "does", "did", "doing", "done",
    "have", "has", "had", "having",
    "can", "could", "will", "would", "shall", "should", "may", "might",
    "must", "ought",
    "get", "gets", "go", "goes", "let", "lets", "see", "sees",
    "know", "knows", "want", "wants", "need", "needs", "use", "uses",
    "make", "makes", "run", "runs", "add", "adds", "set", "sets",
    "work", "works", "stay", "stays", "keep", "keeps", "help", "helps",
    "give", "gives", "take", "takes", "put", "puts", "find", "finds",
    "say", "says", "show", "shows", "mean", "means", "come", "comes",
    "become", "becomes", "live", "lives", "cost", "costs", "sit", "sits",
    "pay", "pays", "rent", "rents", "win", "wins", "fit", "fits",
    "drop", "drops", "end", "ends", "remain", "remains", "exist",
    "exists", "matter", "matters", "count", "counts", "look", "looks",
    "feel", "feels", "seem", "seems", "turn", "turns", "start", "starts",
    "wipe", "wipes", "hold", "holds", "lives", "rebuild", "rebuilds",
})

# Count-as-list lead-in: a sentence that announces a number of items
# ("two things", "three reasons", "a few changes") and then enumerates
# them across following sentences. The count is the author's own signal
# that the content is a list. Fix: convert to a bullet list and drop the
# count - the bullets show it.
COUNT_LIST_LEAD_RE = re.compile(
    r"\b(?:one|two|three|four|five|six|seven|eight|nine|ten|"
    r"a\s+few|a\s+couple\s+of|a\s+number\s+of|several|\d+)\s+"
    r"(?:[a-z]+\s+){0,2}"
    r"(?:things?|reasons?|points?|changes?|steps?|options?|ways?|"
    r"problems?|issues?|parts?|items?|factors?|differences?|benefits?|"
    r"advantages?|approaches?|choices?|properties?|aspects?|areas?|"
    r"categories?|kinds?|types?|examples?|tasks?|goals?|rules?|"
    r"process(?:es)?|stages?|phases?|components?|pieces?)\b",
    re.IGNORECASE,
)

# Contractions. The voice guide mandates contractions ("it's", "don't",
# "we'll"). Flag the most common expanded forms and suggest the
# contraction. Each entry is (compiled pattern, replacement) where the
# pattern captures the exact span so the message can quote it. The forms
# here are safe to contract in almost every context; the message still
# tells the author to skip sentence-final or emphatic cases.
_CONTRACTION_SPECS: list[tuple[str, str]] = [
    (r"\bit is\b", "it's"),
    (r"\bthat is\b", "that's"),
    (r"\bthere is\b", "there's"),
    (r"\bhere is\b", "here's"),
    (r"\bwhat is\b", "what's"),
    (r"\bwho is\b", "who's"),
    (r"\bhe is\b", "he's"),
    (r"\bshe is\b", "she's"),
    (r"\bI am\b", "I'm"),
    (r"\bwe are\b", "we're"),
    (r"\byou are\b", "you're"),
    (r"\bthey are\b", "they're"),
    (r"\bwe will\b", "we'll"),
    (r"\byou will\b", "you'll"),
    (r"\bI will\b", "I'll"),
    (r"\bthey will\b", "they'll"),
    (r"\blet us\b", "let's"),
    (r"\bdo not\b", "don't"),
    (r"\bdoes not\b", "doesn't"),
    (r"\bdid not\b", "didn't"),
    (r"\bis not\b", "isn't"),
    (r"\bare not\b", "aren't"),
    (r"\bwas not\b", "wasn't"),
    (r"\bwere not\b", "weren't"),
    (r"\bcannot\b", "can't"),
    (r"\bcan not\b", "can't"),
    (r"\bwill not\b", "won't"),
    (r"\bwould not\b", "wouldn't"),
    (r"\bshould not\b", "shouldn't"),
    (r"\bcould not\b", "couldn't"),
    (r"\bhas not\b", "hasn't"),
    (r"\bhave not\b", "haven't"),
    (r"\bhad not\b", "hadn't"),
]
CONTRACTION_RES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(pattern, re.IGNORECASE), replacement)
    for pattern, replacement in _CONTRACTION_SPECS
]

# Flat copular definition: a sentence opening with "The/Its/Our <noun>
# is/are a/an/the ..." that just equates the subject with a category.
# Reads as dull and formal: "The model is `Xenova/...`, a 384-dim
# embedder." (code spans are stripped before the check, so the appositive
# shows up as "is , a"). Prefer active voice or lead with the thing
# itself: "We use X", "X does Y". The article (a/an/the) after the copula
# is what marks it as a definition, so "The result is wrong" (predicate
# adjective) and "The point is clear" do not fire.
FLAT_DEFINITION_RE = re.compile(
    r"(?:^|[.!?]\s+)"
    r"(?:The|Its|Our|Their|This|That|These|Those)\s+"
    r"(?:[A-Za-z][\w-]*\s+){1,4}"
    r"(?:is|are)\s*(?:,\s*)?(?:an?|the)\b"
    # but not "is the same / best / only / first / last / right ...": a
    # predicate adjective with an article is not a definition.
    r"(?!\s+(?:same|best|only|first|second|third|last|latest|next|right|"
    r"wrong|opposite|case|point|default|norm)\b)",
    re.IGNORECASE,
)
# Bare demonstrative definitions: "This is a check.", "These are the steps.",
# "That is not a real fix." The indefinite article (a/an) marks it as a flat
# categorization; "the" is left out because "This is the file we edit" usually
# points at something rather than defining it.
FLAT_DEFINITION_DEMO_RE = re.compile(
    r"(?:^|[.!?]\s+)"
    r"(?:This|That|These|Those)\s+"
    r"(?:is|are)\s+(?:not\s+)?an?\b",
    re.IGNORECASE,
)
