# Building a Content Calendar from Six Months of Raw Notes

I wrote this synthetic style exercise as a build log with fictional details, not real events. In February I faced 212 scattered notes and no clear plan for spring content. The notes held interviews, terminal snippets and half-formed outlines from six months.

The mess had grown slowly across two projects and one workshop series. I saved every idea in `~/notes` with a date prefix and no tags. Finding a strong topic meant opening dozens of files and trusting memory.

That approach stopped working when I needed twelve solid topics for April. I spent three evenings scrolling filenames and still missed two strong ideas. I decided to build a small calendar from the notes themselves.

In this post, I'll share:

- how I collected six months of raw notes
- how I grouped ideas by problem and proof
- how I scored topics for audience fit
- how I placed twelve topics on a calendar
- what broke in the first month of use

## Six Months of Scattered Notes

My notes lived in three folders with 212 markdown files from August to January. Each file had a date, a rough title and a few lines of text. Some files held full transcripts, while others held two sentences written on trains.

I collected everything into one folder in early February with a short script. The script copied files, normalized filenames and wrote a CSV index with dates and word counts. The full copy took 14 seconds on my ThinkPad.

The index showed 212 files with 48,300 words in total. The median file had 140 words, while the longest had 1,900 words from a workshop transcript. Forty files had fewer than 50 words and looked more like reminders than notes.

Reading all of them took four evenings at about 45 minutes per evening. I marked each file with one line in the index about the core problem it described. That line became the basis for grouping in the next step.

The rule I took from that review: a calendar needs a complete inventory first, and memory alone doesn't provide that inventory.

## Grouping by Problem and Proof

Grouping meant turning 212 one-line summaries into clusters I could count. I first tried automatic clustering with embeddings and Chroma on my laptop. The clusters looked tidy and mixed unrelated problems that shared vocabulary.

I switched to manual grouping across two afternoons with printed summaries. I sorted ideas by the reader problem they addressed, then checked whether I had proof from my own work. Proof meant logs, measurements or code I had run.

Three large groups emerged from that pass with enough material for multiple posts:

- pipeline failures I had debugged with timelines and fixes
- agent setups I had tested across three projects with costs
- workshop lessons I had repeated with attendance numbers

Two smaller groups held single ideas with strong proof but narrow appeal. I kept those aside for later months instead of forcing them into April.

The grouping took about five hours in total with coffee breaks included. I stored the result in `groups.md` with 34 grouped ideas under seven headings. Each idea kept its source filename, date and one-line problem statement for traceability.

## Calendar Structure in Markdown

The calendar lives in one markdown file called `calendar.md` with twelve rows for April. Each row holds a date, a working title, the source note and the proof I plan to show. I edit the file directly and review it every Sunday.

I scored each grouped idea on three practical questions before placing it. I asked whether readers had requested the topic, whether I had measurements to share and whether the draft could be ready in one week. Each answer used a simple yes or no.

Twelve ideas scored yes on all three questions and became the April slate. I placed the strongest proof first to build trust early. I spaced workshop lessons between technical posts to vary the pace across weeks.

The file uses a simple layout I can scan in under a minute:

```text
2026-04-03 | queue delays | 43 delayed tasks, Grafana gap
2026-04-10 | agent review gates | 13 tasks, four rejections
2026-04-17 | transcript cleanup | 611 words, 27 fragments
```

That layout shows the date, the topic and the concrete evidence at a glance. When proof looks thin on one row, I swap in a backup idea from the smaller groups.

## First Month Using the Calendar

April started well with the first three posts drafted on schedule. Each draft took about 90 minutes because the source notes and proof were already linked in the calendar. I didn't search folders during drafting.

The fourth week exposed a gap I hadn't planned for. A production incident gave me fresher material on Postgres locks with a 28-minute timeline. The scheduled topic felt stale beside real events from that same week.

I swapped the fourth post with the incident story and moved the original topic to May. The swap took 20 minutes of editing in `calendar.md` plus a note about why I changed the order.

Results after April looked solid on the measures I track:

- twelve posts planned and twelve posts published on time
- median drafting time fell from 150 minutes to 92 minutes
- three posts drew replies that cited specific numbers from the text
- one scheduled topic moved to May without disrupting the sequence

The calendar didn't write anything for me. It removed the Sunday panic about what to cover next, and it kept proof attached to every planned topic.

## Limits of the Current Calendar

The calendar still has gaps because it reflects only what I already recorded. It doesn't surface missing topics or questions I never wrote down. Two reader requests in April named subjects with no source notes at all.

Freshness is another limit I watch closely now. A topic that looked strong in February can feel dated by April when tools change. I now recheck numbers the week before drafting instead of trusting the February snapshot.

Maintenance takes about 30 minutes each Sunday across reviewing new notes and updating rows. I add five to eight new fragments per week and retire ideas that lost relevance.

This project taught me a practical lesson about planning from notes. A complete inventory beats clever scoring, and dated proof beats vague enthusiasm every time.

I'll extend the calendar through summer with the same grouping method. If you want to follow along, don't forget to subscribe.
