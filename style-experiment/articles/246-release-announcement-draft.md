# Drafting a Release Announcement from Actual Changes

I wrote this piece as a synthetic style exercise, so I invented every version number and download count in it. Last June I shipped version 0.8.0 of dirwatch, a small fictional folder-sync tool with about 400 users. The release held 27 commits across five weeks, and my announcement draft read like a commit log with punctuation.

Nobody commented, nobody shared it, and downloads stayed flat for ten days. The previous release had moved the download count by 30 percent in a week, so the flat line stung. I reread both announcements side by side and saw the difference within minutes.

The old announcement spoke to users about their files and their time. The new one spoke to me about my commits and my refactors. That gap became the project for release 0.9.0, and the new process starts from the changelog instead of my memory.

In this post, I'll share:

- why my commit-based draft bored even me
- how I sort commits by value to readers
- how I state benefits before mechanics
- how copy-ready examples fill the middle
- how upgrade notes remove fear instead of adding it

## A Changelog Nobody Reads

The 0.8.0 draft listed all 27 commits grouped by week. Each entry named the files I touched and the functions I renamed, and none of them said what changed for the user. I published it on a Friday afternoon and watched the download graph stay horizontal.

A user named Tomas emailed me on Monday. He had updated without reading the post, and he asked whether anything mattered for his nightly backups.

The numbers confirmed the feeling. The 0.7.0 post had drawn 310 views and 122 downloads in its first week. The 0.8.0 draft drew 140 views and 41 downloads.

The rule from that week: announcements serve readers deciding whether to care, and commits record work awaiting translation into outcomes.

## Sorting Commits by Reader Value

For 0.9.0 I sorted all 31 commits into three piles. The first pile held 6 changes a user would notice within a day. The second pile held 9 fixes for known annoyances. The third pile held refactors and stayed out of the announcement.

The sort took 40 minutes with one strict question per commit. I asked what a user does differently because of this change, and silence meant the third pile. Eleven commits died on that question, including a threading refactor I had loved writing.

Each survivor got one line in plain user language. The scheduler rename became faster first scans after idle nights. The retry fix became fewer duplicate uploads on flaky hotel wifi. Those 15 lines took about 90 minutes.

I keep the sorted list in the release folder as the announcement source. It names the pile, the visible change, and the commit hash for reference. No claim enters the post without a hash beside it.

## Benefits Before Mechanics

The announcement opens with the changes that matter most, stated as outcomes:

- Version 0.9.0 scans idle folders 4 times faster.
- It retries failed uploads without duplicates.
- It warns before deleting unseen files.

Those lines sit above everything else on the page.

Mechanics follow only after the reader knows the payoff. I give the scan section one paragraph on scheduling, and the retry section gets one on queue ordering. Each paragraph names the behavior change first and the implementation second.

I cut every sentence that described code without a visible effect. The threading refactor lost its paragraph, and nobody asked where it went.

The middle of the announcement follows a fixed skeleton:

```text
Headline with the version number and the top benefit
Three outcome lines, each under 15 words
One example per major change with commands
Upgrade notes with breaking changes first
Thanks to contributors by name
```

That skeleton fits on an index card, and I check each release against it. Twice a thin section delayed an announcement until I finished one more feature.

## Examples Readers Can Copy

I ship every major change with commands a reader can paste into a terminal. In the scan section, I show before-and-after timing on a 12 GB photo folder. In the retry section, I show the log lines that prove duplicates are gone.

I generate each example by running the commands myself:

```bash
dirwatch scan ~/photos --timing
dirwatch retry --dry-run ~/photos
```

Those runs produced the numbers quoted in the post, and I rerun them on release day. Twice a last-minute commit changed the output, and both times the rerun caught the drift before publishing. Examples rot faster than descriptions, so they get tested like code.

The 0.9.0 post drew 9 replies, and 6 of them quoted a command back with a question. Tomas ran the dry-run flag on his backup folder and confirmed zero duplicates across 2,300 files.

When I can't construct a short demo for a feature, the feature is either unfinished or too obscure for the headline. That test demoted two features to the minor list.

## Upgrade Notes Without Fear

Upgrade notes sit near the end with breaking changes first. Version 0.9.0 renamed one config key and dropped Python 3.9, and both facts appear in the first two lines.

I record each breaking change in short lines:

- what I renamed or removed, with old and new names
- the exact edit that restores working behavior
- the version where the old form stops working

The Python 3.9 note took two lines and saved real support time. Three users thanked me for the early warning, and zero filed confused issues. Previous releases averaged 4 such issues each.

Minor notes stay to one line each. The default retry count moved from 3 to 5, and most users will never notice.

## Announcements I Now Enjoy Writing

The 0.9.0 post drew 420 views and 168 downloads in its first week. Those numbers beat the 0.7.0 baseline, and Tomas shared the post with his backup-admin channel. The process took 5 hours against 2 for the failed draft.

Announcements work when every line answers what the reader does differently, and commit hashes stay in the source file as receipts. Readers reward translation over transcription.

I still write slowly, the skeleton fits tools better than libraries, and non-English users get no translated version. If the user base doubles, I'll ask for translation help first.

I'll describe the release-day checklist in a future post on this blog. If you want to follow along, don't forget to subscribe.
