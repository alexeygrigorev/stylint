# The Checklist I Run Before Pressing Publish

This synthetic style exercise follows a fictional publishing routine I tried in March. I publish about two posts per month and I missed three deadlines in a row. The missed dates forced me to write down every check I run before publishing.

I work in VS Code and I deploy with GitHub Pages. I've lost readers twice because of broken links and I don't want a third miss. My drafts live in a folder with 48 markdown files and 112 images.

I built PublishCheck, a small Python script that validates links and images before I publish. It runs in about 20 seconds and it catches most mechanical errors. The script grew from a five-line checker I wrote in January.

In this post, I'll share:

- why late publishing hurts small newsletters
- how the pre-publish checklist runs in order
- what link and image checks catch early
- how I review claims and code samples
- where the checklist still misses errors

## Publishing Misses That Forced A List

My worst miss happened in February. I published a post about Postgres indexes at 9 p.m. and I linked to a migration guide that had moved. Twelve readers clicked the dead link in the first hour and two of them emailed me about it.

I fixed the URL the same evening and I added a redirect note at the top. The fix took 11 minutes, but the embarrassment lasted longer. I had reviewed the text twice and I had skipped the links entirely.

A second miss came two weeks later. I renamed an image folder from `assets` to `images` and I forgot to update three references. The post showed two broken icons on mobile and one missing diagram on desktop. A friend sent me a screenshot the next morning.

The rule I took from those misses: mechanical checks come before style review, and they run the same way every time.

I chose a checklist file because I know I'll skip steps from memory. The file lives at `checklist.md` and it holds 18 items grouped by stage. That explicit order removes one decision - whether the draft feels ready.

## Checklist Walkthrough From Draft To Ready

The checklist starts with front matter and file hygiene. I confirm the title, date, slug, and draft flag before I read a single paragraph. That early pass takes about three minutes and it prevents publishing with a wrong date.

I run the mechanical script next because manual review misses repeatable errors.

The command reads the draft and it prints missing files, duplicate slugs, and absent alt text:

```bash
uv run python scripts/publish_check.py drafts/publish-checklist.md
```

The output lists each failure with a file path and a line number. I fix the listed items and I rerun the script until the output shows zero failures. That loop usually takes two passes and about six minutes.

The third stage covers readability on small screens. I open the preview on my phone and I scroll through every section without zooming.

The checklist file shows the full order:

```text
front-matter
links
images
claims
code
mobile
final-read
```

## Link And Image Verification

Links break more often than I expected. My archive holds 61 posts and a link audit in March found 14 dead outbound links.

PublishCheck reads every markdown link and it records the target, line number, and link text. It skips `localhost` addresses and it marks external links for a HEAD request. The script checks 40 to 60 links per post in under 15 seconds.

I review redirects by hand because automatic checks miss context changes. A docs page can return 200 while the content now describes a different feature. I open each redirect and I confirm the section still supports my sentence.

Images get a separate pass with three checks. I confirm the file exists, the width stays under 1600 pixels, and the alt text describes the content in under 140 characters.

One mistake taught me to check image licenses at this stage. I used a diagram from a conference slide deck in February without recording the source. I replaced the image the next day and I added a source field to the checklist.

## Claims Evidence And Code Samples

Every claim in a short post still needs concrete evidence from a run, a doc, or a sample.

My review accepts three kinds of support:

- a measured number from my own run
- a linked doc that states the fact
- a code sample the reader can run

Anything without one of those gets cut or rewritten.

I keep a claims table at the bottom of each draft during review. Each row holds the claim, the evidence type, and the link or command that backs it.

Code samples get executed from the draft, not from memory. I copy each block into a fresh virtual environment and I run the commands in order.

I test one install step more than others:

```bash
uv add fastapi uvicorn
```

I run the server after install and I request the health endpoint with `curl`. If the response returns 200 within two seconds, I mark the sample as verified.

## Reflection And Next Steps

The checklist cut my post-publish fixes from nine in January to two in May. Both May fixes were wording tweaks, not broken links or missing images. The average review time rose from 32 minutes to 51 minutes, and that trade feels right for my audience.

I still miss subtle errors when I'm tired. The checklist doesn't catch a dull opening or a repeated argument across sections. I leave those judgments for a morning read with coffee, away from the screen for at least an hour first.

I plan a small freshness check for outbound links older than six months. I'll store last-checked dates in a JSON file and surface links that need another look. That addition should take an afternoon and it should prevent another February-style dead link.

I'll write about that link freshness check in a future post. If you want to follow along, don't forget to subscribe.
