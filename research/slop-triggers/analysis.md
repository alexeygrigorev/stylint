# What triggers voi-slop-detect-380M — ablation analysis vs stylint

Date: 2026-11-18. Corpus: the 57 scheduled Typefully posts in `/tmp/unique_scheduled_posts.json` (DTC + Alexey Grigorev sets, scores 0.32–0.999). Model: `voi-slop-detect-380M` ONNX q8 via `~/.local/bin/slop-detect`, scored directly with `~/.local/share/slop-detect/venv/bin/python` + `slop_detect.score_text` (one model load, ~120 scored variants). Stylint: `/home/alexey/git/stylint` at HEAD. Experiment scripts: `/tmp/slop_ablation/*.py`.

## TL;DR

1. **The trigger is register, not vocabulary.** No phrase, transition, bullet format, punctuation choice, or opening/closing formula moves these posts off their score. Leave-one-out sentence deletion on the top posts changes the score by at most −0.01 to −0.39 (the −0.39 case is removing 40% of the text). The score is a property of the whole smooth, declarative, well-formed announcement prose.
2. **The podcast-announcement template is the single biggest lever measured: +0.68.** Post 55 (score 0.316) re-flowed — same facts, same CTA — into the template "hook sentence → *X, Title at Company, joins the DataTalks.Club podcast to talk about …* → *We will cover …, …, and …* → *Join us live on DATE at TIME CET.*" jumps to **0.997**.
3. **Sentence shape beats topic.** The hook *"AI agents that query live data can look impressive in a demo and still be hard to trust in production"* scores **0.997** inside neutral filler text; swapping the topic words keeps it there: *"Dashboards that query live data can look impressive in a demo and still be hard to trust in production"* = **0.997**, *"Scripts that query live data…"* = **0.998**. A balanced concessive sentence (modal `can` + `and still` + parallel in X / in Y phrases) is the pattern.
4. **The 0.10 gate is unreachable for coherent announcements on this corpus.** Fresh scores: min 0.284, median 0.582, none < 0.10. Even a bare URL line scores 0.62 and `"I like cheese." ×15` scores 0.22. Alexey's own hand-written reference prose scores up to **0.99** (`stylint/style_guide/voice.md` = 0.989; his published good posts span 0.12–0.99). The gate at 0.10 therefore classifies tidy human English as AI, and no amount of phrase editing fixes it.
5. **Stylint compliance does not reduce the slop score.** Fixing every stylint finding in post 0 (contractions, `really`, `lean on`, bare URL) leaves it at **0.998** (base 0.999). Correlation between stylint finding count and slop score across the 57 posts: **r = −0.29** (weakly negative — bullet-heavy posts trip stylint's list rules but score lower on slop). The two tools measure different things.
6. **Data correction:** the `score` field in the JSON is the **max of each A/B pair**, not per-post (verified: idx 55 and 56 share one stored score to full precision; fresh scoring of idx 55 gives 0.316 vs stored 0.349). Fresh per-post scores are the ground truth below.

## Data: fresh per-post scores

Stored pair-max vs fresh (both members re-scored):

| idx | stored | fresh | note |
|---|---|---|---|
| 0, 1 | 0.999 | 0.999 | podcast announcement, full template |
| 2, 3 | 0.998 | 0.997/0.998 | podcast announcement |
| 4, 5 | 0.996 | 0.995/0.996 | podcast announcement |
| 6, 7 | 0.913 | 0.913/0.582 | course outline (numbered modules) |
| 9 | 0.909 | 0.909 | decision record, list flattened to prose |
| 8 | 0.909 | **0.608** | same content with bullets |
| 12, 13 | 0.836 | 0.836/0.678 | clip post |
| 16 | 0.773 | 0.773 | clip post with bullets |
| 17 | 0.773 | **0.421** | flattened variant, no contractions |
| 30 | 0.607 | 0.607 | question hook + "Don't send" imperative |
| 29 | 0.607 | **0.284** | statement + question hook variant |
| 55, 56 | 0.349 | 0.316/0.349 | clip post, quoted prompt block |

Summary (fresh): min 0.284, p25 0.452, median 0.582, p75 0.739, max 0.999. **n below the 0.10 gate: 0 of 57.**

## Measured deltas

### A. Leave-one-out (delete one sentence, keep everything else)

- Post 0 (0.9993): dropping any single sentence → 0.991–0.999 (deltas −0.0008 to −0.0081). The title+Luma-link block *raises* the score slightly if removed (+0.0005).
- Post 2 (0.9971): dropping *"We will cover the product and engineering work…"* −0.227 (→0.770); dropping *"Shipping an AI demo is one thing."* −0.082; everything else ≤ −0.03.
- Post 4 (0.9945): dropping the guest sentence −0.393 (→0.601; it is 40% of the words); dropping the CTA −0.041.

Interpretation: where big deltas exist they are proportional to text removed, not to special phrases.

### B. The announcement template (the big lever)

Incremental build on a **gardening** topic (same template, non-AI content), scoring the accumulating text:

| Add | Score |
|---|---|
| hook: "Compost bins that never smell can look great in a garden center and still be hard to trust in your backyard." | 0.735 |
| + guest: "Jane Smith, Master Gardener, joins the … podcast to talk about how reliable those bins really are." | 0.959 |
| + "We will cover where they break down, how to check their results, and what needs to be in place…" | 0.999 |
| + "Join us live on Wednesday, 2 December 2026 at 12:30 CET." | 0.9995 |
| + title + link | 0.999 |

Components in isolation, sandwiched in neutral filler sentences:

| Component | Score in sandwich |
|---|---|
| AI-agents hook (real post 0 sentence) | **0.997** |
| "We will cover where they break down, how to check their answers, and what needs to be in place…" | 0.798 |
| Guest sentence ("…joins the DataTalks.Club podcast to talk about…") | 0.688 |
| CTA ("Join us live on …") | 0.616 |
| CTA alone (no sandwich) | 0.318 |

Same-content reformat of post 55 (0.316) into the full template: **0.997 (+0.681)**.

### C. Hook-pattern variants (same content, neutral sandwich)

| Hook | Score |
|---|---|
| "AI agents that query live data can look impressive in a demo and still be hard to trust in production." | 0.997 |
| "Dashboards that query live data can look impressive in a demo and still be hard to trust in production." | 0.997 |
| "Scripts that query live data can look impressive in a demo and still be hard to trust in production." | 0.998 |
| "…can look good in a demo and still be unreliable in production." | 0.975 |
| "…can look impressive in a demo and still fail in production." | 0.977 |
| "AI agents that query live data look impressive in demos and fail in production." | 0.966 |
| "Shipping an AI demo is one thing. Making a feature that people actually use is another." | 0.996 |
| "An AI demo ships in a day. A feature people use takes months." | 0.927 |
| "Your agent can generate 1,000+ images. The question is what it costs." | 0.616 |
| "Can your agent generate 1,000+ images without running out of memory?" | 0.540 |
| "Before you pick a model, write the decision down." | 0.789 |

Pattern extracted: **declarative subject + relative clause + modal + balanced concessive/contrastive parallel ("X in A and still Y in B", or the mirrored "is one thing / is another" pair)** → 0.93–1.00 regardless of topic words. Question hooks and imperative hooks score 0.54–0.79.

### D. Phrase-level edits (all noise: |Δ| ≤ 0.01)

On post 0: "We will"→"We'll" (+0.000); "lean on"→"rely on" (+0.000); "break down"→"fail", "check"→"verify" (−0.000); Title Case title → sentence case (−0.000); insert em dash (−0.003; the em dash is a *regex* hard tell, the model doesn't care); drop CTA (−0.001); drop title+link (+0.001); reorder CTA first (−0.010); one-paragraph blob (+0.000).

On post 2: mirror pair → semicolon version (+0.001); mirror pair → plain contrast ("easy…harder") (+0.000); "the real cost of…"→"what a useful AI feature costs" (+0.001); "tend to underestimate"→"underestimate" (+0.001).

On post 4: drop "actually" (−0.004); "useful insights"→"insights" (−0.000).

Hand-written rough rewrite of post 0 (contractions, fragments, questions, no template): still **0.996** — a human-sounding rewrite of *this content in declarative paragraphs* does not drop either.

### E. Formatting / structure (mostly noise)

| Edit | Post | Δ |
|---|---|---|
| bullets → comma-enumeration sentence | 22 (0.452) | −0.005 |
| slide markers "1/4…4/4" stripped | 23 (0.676) | −0.015 |
| one "1/4" marker inserted | 22 | −0.003 |
| module headers merged into prose | 6 (0.913) | +0.029 |
| module paragraphs → bullets | 6 | +0.025 |
| drop "What you have at the end:" label | 6 | **−0.061** |
| drop final Apply CTA | 6 | −0.027 |
| drop "What each module covers:" lead-in | 6 | −0.002 |
| question opener → statement | 6 | −0.000 |
| drop "The last line answers the main question." | 8 (0.608) | **−0.162** |
| bullets → prose sentences | 8 | −0.003 |
| self-host contrast: 2 sentences → 1 semicolon sentence | 8 | **+0.142** |
| opener imperative → third-person statement | 8 | **−0.065** |
| cover sentence → two sentences | 4 | −0.047 |
| "moving from that reporting cycle to people analytics that actually helps leaders decide" → "moving from routine reports to people analytics" | 4 | −0.054 |

The only sizeable structural wins: delete meta-sentences that *comment on the text itself* ("The last line answers the main question.", "What you have at the end:"), and break the balanced two-sentence contrasts (note the +0.142: *merging* the contrast into one sentence raised it — balanced parallel pairs are a positive trigger).

### F. Contractions (controlled expansion sweep)

Expanding don't/doesn't/can't/it's/that's/you're/There's across 11 posts: deltas +0.000 to +0.081 and −0.013 to −0.128, median +0.02. **Noise.** The large A/B pair gaps (8→9: 0.608→0.909; 22→23: 0.452→0.676; 16→17: 0.773→0.421) are caused by the other bundled changes (bullet flattening, balanced enumerations, meta-sentences), not contractions — e.g. idx 17 (formal "cannot/do not", flattened) scores *lower* than idx 16.

### G. What scores below ~0.3 (the only reliable drops)

- Bullet list only: 0.283. CTA alone: 0.318. Question + short answer pairs: 0.40–0.53.
- Post-0 rewritten as chat style — guest name line, `Topic:` line, three questions, fragment CTA ("Wednesday, 2 December 2026, 12:30 CET. See you there."), title+link kept: **0.456** (from 0.999).
- Casual filler ("ok so basically … idk thats it lol") around a clean sentence: 0.42. Punctuation stripped: 0.24. Repeated trivial sentences: 0.20–0.22.
- **Nothing coherent ever approached 0.10.**

## slop-detect vs stylint coverage

stylint run on all 57 posts: 272 findings, mean 4.8/post. Top tags: bare-url 57, contraction 38, prose-question 32, third-person 25, label-colon 16, banned-word 13, colon-inline 12, choppy-rhythm 11, many-commas 10, long-clause-likely 10.

**What slop-detect catches that stylint does not:**

1. The model score itself — smooth declarative register. Stylint has no rule class for it (its list heuristics actively push *toward* more bullets, which is score-neutral here).
2. En dash `–` as a hard tell: stylint has `em-dash` and `double-hyphen` tags but **no en-dash rule** (verified live: an en dash passes stylint clean).
3. Negative parallelism "It's not X. It's Y." as a mechanical rule: stylint covers mirrored pairs only in the `empty-rhetoric` *LLM prompt*, not mechanically (`parallel-sentences` only catches identical two-word openers).
4. Emoji bullets (stylint has no emoji rule).
5. Vocab soft-tell list vs stylint `BANNED_WORDS` — **stylint is missing 17 of slop-detect's 27 terms**: tapestry, landscape, robust, seamless, unlock, empower, navigate, game-changer, deep dive, double-edged sword, treasure trove, testament to, bustling, "in today's", paradigm, unleash, supercharge. (Stylint has: delve, leverage, elevate, foster, crucial, pivotal, vibrant, moreover, furthermore, at-the-end-of-the-day, plus ~80 more of its own.)

**What stylint catches that slop-detect ignores:** all markdown mechanics (headings, code blocks, tables, smart quotes, bare URLs), the list-shape heuristics, voice rules (contractions, third-person, label-colon, questions in prose), and ~80 banned words/phrases beyond slop's vocab list.

**Conflict to know about:** stylint's `bold` rule ("bold markdown is not used") vs slop-detect's `bold-bullet` soft tell — both discourage bold-label bullets, consistent. But stylint *requires* contractions ("It is → it's") while slop's model slightly prefers contractions too — consistent as well; the real conflict is that fixing stylint's findings leaves the slop score untouched (measured above).

## Trigger patterns, with measured separators (candidate stylint rules)

Regexes tested against all 57 fresh scores (precision-style evaluation: hit scores vs non-hit scores):

| Candidate rule | Regex (case-insensitive unless noted) | Hits | Hit scores | Min non-hit |
|---|---|---|---|---|
| guest-announcement | `\bjoins?\s+the\s+[^!?\n]{3,60}?\b(podcast\|course\|workshop\|webinar\|session\|stream)\b` | 6 | **all ≥ 0.995** | 0.913 elsewhere |
| we-will-cover opener | `(?m)^We (will\|'ll\|’ll) cover\b` | 3 | all ≥ 0.994 | — |
| join-us-live CTA | `\bJoin us live on\b` | 3 | all ≥ 0.994 | — |
| mirror pair | `\bis one thing\b[.!?\n]+\s*[^!?\n]{3,80}\bis another\b` | 2 | 0.997/0.998 | — |
| concessive-still | `\b(can\|will\|may\|might)\b[^!?\n]{5,70}?\band still\b[^!?\n]{3,70}[.!?]` | 4 | 0.57–0.999 | no false positives < 0.5 |
| tri-list-cover | `\bcover (where\|how\|what\|why)[^!?\n]{10,80},\s*(how\|what\|where\|why)[^!?\n]{3,80},\s*and\s` | 1 | 0.999 | — |
| when-you balanced pair | `When you [^!?\n]{5,80}\.\s+When you ` | 2 | 0.608/0.909 | — |
| declarative you-can opener | `\bYou can\b[^!?\n]{10,90}\.` | 2 | 0.624/0.729 | — |

Note the corpus caveat: the first four rules fire exactly on Alexey's *legitimate, hand-approved announcement format* — that format is precisely what the model scores ~1.0. These rules are therefore "known-high-score class" flags for routing (announce-and-exempt, or score against a class-specific threshold), not bans.

**Hard/soft tells in this corpus:** 0 hard-tell hits (no em/en dashes, no negative parallelism), 1 vocab soft tell across all 57 posts ("landscape" in post 6). Every gate failure here is 100% model-score-driven.

## Recommendations

1. **Re-calibrate the gate per format; 0.10 is not achievable for announcements.** Evidence: 0/57 posts below 0.28; Alexey's own hand-written voice guide scores 0.99; a bare URL scores 0.62. Suggested actions: (a) treat "joins the … podcast/course" guest announcements as a recognized class with its own expected range (~0.99) and gate them on the regex tells + human review instead of the model score; (b) or move the general gate to the model's own "human" band edge (~0.15–0.2) for social formats and keep 0.10 only for long-form prose; (c) record that a *pass* on short social posts is currently impossible, so the standing rule as written blocks all scheduled content.
2. **Stop editing phrases to chase the score — it does not work.** Measured: every phrase-level edit ≤ 0.01; contractions noise; formatting noise. The only effective levers are structural register changes (fragments, questions, `Topic:` lines → 0.456), which change the post's voice. Rewrite decisions should be editorial, not numeric.
3. **Port the missing mechanical catches into stylint** (slop-detect catches, stylint misses):
   - `en-dash`: flag `–` like the existing `em-dash` tag.
   - `negative-parallelism`: mechanical rule for `(?i)\b(it'?s|this is|that'?s|they'?re)\s+not\s+…[.;,]\s*(it'?s|this is|that'?s|but)\b` — currently only an empty-rhetoric prompt; promoting it makes the check enforceable in `stylint --workflow final`.
   - Extend `BANNED_WORDS` with the 17 vocab terms stylint lacks (robust, seamless, unlock, empower, navigate, game-changer, deep dive, double-edged sword, treasure trove, testament to, bustling, paradigm, unleash, supercharge, tapestry, landscape, "in today's") — cheap, zero-risk additions consistent with existing entries.
   - Optional `emoji-bullet` tag (slop soft tell, stylint blind).
4. **Add the announcement-pattern rules as a "register-class" checker in stylint** (flag-for-review, not banned): guest-announcement, we-will-cover opener, join-us-live CTA, mirror pair, concessive-still, tri-list-cover, when-you pair. These fire with 0 false positives below 0.5 on this corpus and identify exactly the text the model will score ≥ 0.99. Wire the flag to guidance: "this is the announcement register; expect a slop score near 1.0; route for human approval rather than rewriting."
5. **Promote the mirrored-pair and self-comment rules** already implied by stylint's prompts into mechanics: mirror pair (measured 0.997/0.998) and `label-colon`-style meta-sentences ("The last line answers the main question.", "What you have at the end:") — deleting these gave −0.16 and −0.06, the largest legitimate single-edit drops found.
6. **Keep the two tools in their lanes.** Stylint = mechanical style/voice; slop-detect = register score + tells. Do not use stylint passes as slop evidence (r = −0.29) and do not let the deslop workflow degenerate into threshold-chasing (see recommendation 2). If the gate stays as is, pair every failure with the regex class identified above so rewrites target the register, not the vocabulary.

## Reproduction

- `/tmp/slop_ablation/ablate1.py` — leave-one-out (posts 0, 2, 4)
- `/tmp/slop_ablation/ablate2.py` — phrase/structure edits (posts 0, 2, 4)
- `/tmp/slop_ablation/calibrate.py` — human-text calibration + mangling probes
- `/tmp/slop_ablation/calibrate2.py`, `reverse55.py` — Alexey good-posts scoring; post 55 reverse probes
- `/tmp/slop_ablation/template.py` — template incremental build, component isolation, hook variants
- `/tmp/slop_ablation/topic_struct.py` — topic swap, stylint-fixed post 0, posts 6/8
- `/tmp/slop_ablation/rescore.py` — fresh scores for all 57 posts (pair-max discovery)
- `/tmp/slop_ablation/factors.py` — contraction sweep, markers, bullets, hook internals, rewrites
- `/tmp/slop_ablation/threshold.py` — sub-0.10 probes
- `/tmp/slop_ablation/rules.py`, `final.py` — vocab overlap, candidate-rule precision, correlation
- `/tmp/slop_ablation/stylint_all.txt` — full stylint output on the corpus
