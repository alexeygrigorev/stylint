# Using Static Analysis to Enforce a Writing Style

I wrote this analysis as a synthetic style exercise, and the rule names, test cases, and precision measurements are fictional. In the invented project, I added static checks to a writing workflow that produced 84 technical articles over 18 months.

My goal was narrow, so I targeted habits that a human editor should never have to mark again.

In this post, I'll share:

- the first rule set and its false positives
- how I represented sentences and paragraphs
- the check for overly long clauses
- how editors used the machine findings
- what the measurements changed

## First Rules

I started with a 90-line Python script and regular expressions. It read Markdown and skipped code fences.

The four checks covered bold text, em dashes, marketing verbs, and untagged code blocks. On the first corpus of 84 articles, they found 617 em dashes and 51 untagged code blocks.

They also found 83 uses of a verb my banned-word list rejected outright.

Those findings were easy to verify. They also showed why the work belonged in a script: no editor wanted to scan for punctuation manually.

The first broad check looked for adverbs ending in `ly`. It reported 1,204 hits, and 741 were legitimate words such as "only" or "family".

That result was my first lesson. A rule needs a concrete definition of the thing it detects, and a low false-positive rate matters more than coverage.

## Sentences and Paragraphs

To check sentence length, the tool had to distinguish ordinary text from Markdown structure. I wrote a parser that treated blank lines as paragraph boundaries.

The sentence splitter handled abbreviations poorly. It split the name Doctor Marta Ruiz into two sentences, and it counted the abbreviation e.g. as a boundary.

I replaced the naive split with a small list of exceptions and added 22 unit tests from actual article sentences.

```python
def paragraph_texts(markdown: str) -> list[str]:
    outside_fence = strip_code_blocks(markdown)
    blocks = outside_fence.split("\n\n")
    return [join_wrapped_lines(block) for block in blocks if block.strip()]
```

With the parser stable, each paragraph became an object with its starting line, plain text, and sentence list. That choice made errors actionable. The command could report line 214 rather than asking a writer to search for a vague rule name.

## Long Clauses

Length alone was too blunt. A 29-word sentence with a list read fine, while a 21-word sentence with three dependent clauses often felt exhausting. I added a second condition that counted commas and conjunction boundaries.

The first version flagged a sentence when it exceeded 25 words and contained at least two clause boundaries. Later corpus tests showed that the comma count was more reliable. The final check required more than three commas, or more than 25 words plus a coordinating conjunction after the fifteenth word.

This found 329 sentences in the corpus. I sampled 80 findings and agreed with 69, for a measured precision of 86%. Most true findings buried a second subject after a comma. Most false findings were legitimate lists such as "Python, PostgreSQL, Docker, and GitHub Actions".

```text
line 118: sentence has 31 words and 4 commas
fix: split at the clause boundary after "payment webhook"
```

The suggested location helped, but the tool never rewrote the sentence automatically. Splitting at the wrong boundary could change emphasis or invent a causality the writer didn't intend.

## Editors and Findings

I ran the checker locally, in continuous integration, and as a pre-commit hook. Local output showed every finding. Continuous integration failed only on new findings, so old articles could remain untouched while writers improved new drafts.

The editor workflow had two passes. First, the writer accepted mechanical fixes and pushed the revision. Second, a human editor reviewed structure, evidence, and claims with the machine output hidden. We deliberately kept those concerns separate.

Editors logged disagreements in a shared file, and they rejected 116 findings over three months. The largest group was 44 technical terms that matched banned words.

The term "signal processing" was the largest subgroup. Another 31 rejected findings were intentional sentence fragments used in captions.

Those disagreements drove the allowlist design. I stored each exception beside the rule, and an editor could see exactly which phrase it allowed.

## Measured Effect

After six weeks, the median time from submitted draft to publication fell from 4.1 days to 2.6 days. I can't attribute all of that to static analysis. Three new editors joined, and the team also shortened its review checklist.

The clearer change was in first-pass comments. Before the checks, 42% of editor comments were mechanical, and that fell to 13% in the following month.

Writers changed behavior fastest when findings appeared locally before a pull request. The CI check caught only 17% of violations after they had already been pushed.

## Rules That Held Up

Static analysis worked because the scope was small. The rules handled punctuation, formatting, repetition, and measurable sentence structure. They never judged whether an article had an argument, a fair claim, or a useful example.

I would still collect disagreement samples from day one. The 80-finding review took only 70 minutes and prevented two bad rules from shipping.

One rejected rule illustrates the point. It flagged every sentence ending in "ing", but it missed the difference between trailing filler and a legitimate present-participle clause.

I plan to publish the rule-design checklist in a future article. Subscribe if you want to read how it evolves as the corpus grows.
