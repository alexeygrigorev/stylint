# Adding a New Rule to My Writing Style Linter

I wrote this synthetic style exercise as a build log, and all project details are fictional. In May 2026 I reread four agent-drafted sections and counted nine sentences that denied one thing and asserted another after a "but". Stylint, the linter I run on every draft, had nothing to say about any of them.

The construction reads as punchy once and mechanical the ninth time. My drafts used it more than I noticed, because the agents imitate my voice notes, and my own examples were full of it. So I spent one evening on a new rule, and this post records how it went.

In this post, I'll share:

- the construction the rule targets
- the regex I started from
- the false positives from the first run
- how the tests guard the rule
- what changed in my drafts one month later

## The Construction

The rule targets sentences that deny one thing and then assert another after a comma and "but".

Three examples from my own drafts, lightly disguised:

```text
The score isn't a benchmark, but a set of habits.
The fix wasn't hard, but tedious.
The tool isn't slow, but careful.
```

The three sentences above promise a contrast with little information in it. The second half usually restates the first with a positive spin, and the pair sounded deeper than it was. My style guide already banned the construction, and the linter just didn't know about it.

A real contrast deserves two sentences, because each half needs its own evidence. "The fix wasn't hard, but tedious" tells me nothing about either half. "The fix took 20 minutes, and most of it was waiting on the test suite" tells me what happened. The word tedious never needed to appear.

## The First Regex

The first version matched any sentence with "not" before a comma and "but" after it:

```python
CONTRAST_BUT_RE = re.compile(
    r"\bnot\s+[^,.!?]{1,40},\s+but\s+\b", re.IGNORECASE
)
```

The expression is easy to read. It wants the word "not", up to 40 characters without punctuation, a comma, and then "but". The 40-character window keeps the match inside one clause, because a longer span is usually two separate thoughts that merely share a sentence.

I ran the check over the 40 drafts in my archive folder, about 6,800 sentences in total, and it reported 11 hits. Nine were offenders I agreed with, and the remaining two were false positives I describe below. Four of the nine offenders sat in the two most recent drafts, which told me the habit was growing.

That ratio was good enough to keep tuning instead of starting over from an empty test set.

## False Positives

The first false positive was the "not only" family. A sentence like "the rule flags not only typos but also tone" has a real second half, and cutting the pair would lose information. The tuned rule skips any sentence containing "not only".

The second false positive sat inside a block quote, where an archived author had used the construction deliberately. The linter already skips code blocks and block quotes, so the fix was to run my check after those filters instead of before. Both fixes took about 20 minutes together, and neither changed the regex.

After the two exceptions, the rule reports 9 sentences across the same 40 drafts, and I agree with all 9. The remaining offenders cluster in conclusions, where the temptation to sound decisive is strongest. That placement matched my style guide's complaint, so the rule and the guide now point at the same habit.

## Tests And Continuous Checks

The rule comes with a test file named `tests/test_contrast_rule.py`, and every case pairs one sentence with an expected verdict. That file has 34 cases. 26 sentences should trip the rule, and 8 should pass through untouched.

The false positives from the first run all became negative cases, which is the part I'm most satisfied with. Two of the negative cases still make me pause: a contrast inside a title, and a contrast where the denied half is a number.

The whole suite runs locally with one command:

```bash
uv run pytest tests/test_contrast_rule.py -q
```

It finishes in about 2 seconds, which makes it easy to rerun after every tweak to the regex. The same suite also runs in GitHub Actions on every push, so a change to any rule can't quietly break another. The workflow takes about 90 seconds, and I read the failures more often than I expected during the tuning week.

## One Month Later

In the month since 12 June 2026, the rule has flagged 4 new sentences in fresh drafts, and I rewrote all 4. My agent drafts use the construction less, because the linter now complains early enough to train the session. Each fix took under a minute, since the denied half either got evidence or got deleted.

What the rule can't see are contrasts split across two sentences, and contrasts built on "rather than", which no regex of mine catches cleanly. Those stay a judgment call for the editing pass, where the style guide still does the work.

The arc is small and repeatable. I read old drafts, counted a habit, wrote a rule, and let tests hold it in place. I'll write about the "rather than" family when I figure out its boundaries. If you want to follow along, don't forget to subscribe.
