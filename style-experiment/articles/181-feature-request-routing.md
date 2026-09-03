# Routing Feature Requests from Conversations to Issues

I wrote this synthetic style exercise as a build log, and all project details are fictional. In April 2026 I sat down to plan the next release of `replan`, a shift-scheduling tool I maintain for two clinics. I found 46 feature requests spread across three Telegram chats and one email thread.

Four of those requests appeared twice with different wording, and one appeared four times. I answered two copies of the same idea in one week and promised it to two people. The requests lived where the conversations happened, and nothing in my setup collected them.

In this post, I'll share:

- why my shared doc stopped working
- how I export conversations into plain files
- how the pipeline deduplicates and groups requests
- how evidence gets attached before an issue opens
- how the weekly roadmap stays current
- what changed after six weeks of runs

## A Shared Doc That Rotted

My first attempt was a doc called `ideas.md` in the repo. After every call I pasted the request, the date and the role of the person who made it. By February the doc held 38 entries, and during busy weeks I stopped updating it.

I also couldn't trace the evidence behind any entry, either. One entry said "wants shift swap on mobile" with no link to any conversation. I had no way to tell whether three people wanted the feature or one person mentioned it twice. My mistake was keeping a second place to copy requests into. The rule I took from it: the pipeline has to read the conversations directly.

## Exporting The Conversations

In late April I wrote `pull_chats.py`, a small script that calls the Telegram export API and writes one markdown file per chat. Each file keeps the date, the sender's first name and the message text. The export for the larger clinic covers 1,900 messages since January. The API needs a session token per chat, so the first setup took about 20 minutes per chat.

The script takes a cutoff date and an output folder:

```bash
uv run python pull_chats.py --since 2026-01-01 --out chats/
```

The folder held nine markdown files after the first run, and the full export took about 12 seconds. I committed the folder to a private repo, so the coding agent could read it without touching any chat client.

## Deduplicating And Grouping

Next came `route_requests.py`, a script that sends the chat files to Claude Code with a strict prompt. The agent may mark a message as a request only if it asks for a change to the product. Greetings, bug reports and scheduling questions get dropped at this stage.

The prompt asks for three fields per request:

- the exact quote, with the file name and line number
- a one-sentence summary in fixed wording
- a group name from a list of six known areas

The first run on the April export returned 52 raw requests and merged them into 41 groups. All four copies of the shift-swap request collapsed into one group, which the February doc had never managed.

## Evidence Before Issues

A group was still just a claim, so I added an evidence gate before any issue opens. The gate accepts two kinds of proof. A group passes with two quotes from two different people. One quote also works with a measured cost attached, such as "manual swaps take about 25 minutes per week". Groups with weak evidence go to a file called `maybe.md` instead of the tracker.

The same script drafts an issue body for every group that passes.

The May log kept one drafted command:

```bash
gh issue create -R clinic/replans --title "Shift swap on mobile" --body-file groups/shift-swap.md
```

Each issue body starts with the quotes, so a reader can check the claim before reading my summary. In May I reviewed all 41 groups and opened 17 issues. Nine groups had a single quote each, and they went to `maybe.md` rather than into the tracker on a guess.

## Keeping The Roadmap Current

The pipeline reruns every Monday at 07:00 through cron on a small server at home. Each run rewrites `roadmap.md` next to the issues, with one line per open group and the date of the newest quote. When a group gets no new quote for 60 days, its line moves to a cold list at the bottom of the file.

That cold list caught my favorite failure. A dark-mode request from January got no new quotes after 12 February. It stayed on the roadmap for nine weeks because I liked the idea. The rule I took from it: I keep a request on the roadmap only while fresh quotes keep arriving.

## Results After Six Weeks

The pipeline moved my work from remembering to reviewing. I spend about 20 minutes each Monday on the grouped output, down from an hour of scrolling chats at the end of every month. Both clinics now see their own quotes inside the issues, and the "did you forget my request" emails stopped after mid-May.

The pipeline still fails on mixed languages. One chat switches between Ukrainian and English, and in May the agent merged two requests that described the same feature in different languages. I now spot-check every merged group with both quotes side by side, which adds about five minutes to the Monday review.

I'll write about the evidence file format in a future post. If you want to follow along, don't forget to subscribe.
