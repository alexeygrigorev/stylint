# Slop-trigger analysis (voi-slop-detect-380M)

What makes voi-slop-detect-380M score text >= 0.99, measured by ablation
against the 57-post Typefully corpus (2026-11-18, by Orin). The headline
finding: the trigger is the smooth, declarative announcement register, not
vocabulary - phrase edits move the score by at most 0.01.

This analysis drove the stylint changes that port the mechanical tells
(en-dash, negative-parallelism, emoji bullets, 17 banned vocab terms) and
add the flag-for-review `announcement-register` tag
(`stylint --explain announcement-register`).

Full report: [analysis.md](analysis.md).
