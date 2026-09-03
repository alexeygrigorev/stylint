# Running a Question of the Week from Community Threads

This synthetic style exercise describes a fictional community series with invented threads and names. All counts, dates and quoted topics below are fictional, and no real events are reported.

Last February I managed a Python learner forum with about 6,200 members and 300 new threads per month. Good answers kept disappearing into long threads, and the same beginner questions returned every three weeks. I wanted one featured answer per week that the whole forum could reuse.

I first picked questions by gut feel during my Sunday review. That approach favored advanced topics I found interesting, and beginners ignored the picks. After five weeks, featured posts averaged 34 views against 410 views for ordinary popular threads.

I replaced gut feel with a small selection routine that scores threads weekly. Over the next 12 weeks, featured answers averaged 890 views each, and three of them entered the onboarding docs. The routine takes about 90 minutes per week, including the write-up.

In this post, I'll share:

- how I measure thread volume and pick candidates
- why my first gut-feel picks flopped
- how I write the answer and credit the authors
- how I reuse featured answers in docs and onboarding
- what the series costs and where it still falls short

## Thread Volume And Selection Rules

The forum exports threads with reply counts, view counts and reaction totals per week. I pull the export every Sunday evening and keep the top 20 threads by replies. From those 20, I drop announcements, job posts and threads with fewer than five replies.

ThreadPick, a small Python script that scores weekly threads, ranks the survivors by a simple sum. It adds replies, helpful reactions and newcomer authorship into one score per thread. A thread from a first-time poster with eight replies outranks a regular debate with 30 replies.

The shortlist rule keeps the series grounded in learner needs.

I keep three candidate threads each week, and each candidate must meet these conditions:

- at least five replies from at least three people
- one answer marked helpful by the asker or a moderator
- a question that fits one page when rewritten

Twelve weeks produced 36 candidates from roughly 900 threads. About half concerned file handling, virtual environments and dependency errors, which matched the beginner-heavy membership.

## The First Pick That Flopped

My first five picks ignored the shortlist and followed my own taste. I featured an async refactor, a packaging deep dive and a metaclass explainer in consecutive weeks. Each post took over two hours to polish, and each drew fewer than 50 views.

The failure was plain in the numbers. Ordinary threads about installing packages drew 400 to 600 views in the same weeks, while my featured metaclass post drew 28 views. I had written for the ten most advanced members and bored the other 6,190.

The rule I took from those weeks: feature the question beginners actually ask, and leave advanced topics to ordinary threads.

The sixth week tested the rule directly. I featured a path-handling question from a first-time poster with nine replies and two competing answers. That post drew 640 views in seven days, which beat all five earlier picks combined. Selection by evidence replaced selection by taste from that week on.

## Answer Format And Credits

Each featured post follows the same structure so readers know where to look. I open with the original question in two sentences, then give the tested answer with code, then list two common errors. The whole post stays under 500 words and runs in one screen.

I verify the answer before publishing it.

The check uses a fresh virtual environment on Python 3.11 with only the packages the thread mentions:

```bash
uv run python /tmp/verify_answer.py
```

The script runs the answer code and prints output plus the package versions used. I paste that output into the post, so readers see proof rather than claims. Verification takes about 15 minutes per answer, including dependency setup.

Credit goes to both the asker and the best answerer by forum handle. I link the original thread, name the contributors in the second paragraph and add the post to their activity records. Two contributors later became moderators, and both cited the feature as their first recognition.

## Reusing Answers In Docs

A featured post earns its cost only when it gets reused beyond the week. I copy each answer into a docs folder with the same code and a link back to the thread. Three file-handling answers now form the first page of the onboarding guide for new members.

I copy each featured post into the docs folder every Friday.

I export the featured markdown, strip forum formatting and add a header with the original date:

```text
source thread: week 9 path handling
verified on: Python 3.11 with pandas 2.1
status: active, reviewed monthly
```

The header tells future editors when to recheck the code. One answer about virtual environments went stale after four months, and the header made the age obvious during review. I updated that page in 20 minutes with the current commands.

Those answers drew 10,680 views across 12 weeks, while the derived docs pages drew another 4,300 views. I link six featured posts from the onboarding guide, and moderators paste those links into new threads instead of retyping answers.

## Keeping The Working Parts

The series now runs on a fixed 90-minute budget per week. Selection takes 20 minutes on Sunday, verification takes 15 minutes and the write-up takes the rest. Skipping verification once produced a broken snippet, so I no longer publish without the run log.

The project taught me a narrower lesson than "publish more content". One reused answer beats ten featured posts that nobody links again, and credit keeps contributors answering. The routine survives because each week ends with a docs link rather than a standalone post.

Gaps remain around advanced topics and quiet weeks. Holiday weeks produce too few candidates, and advanced questions rarely meet the newcomer rule. My next change is a monthly advanced edition with separate selection rules.

I'll write about that advanced edition in a future post. If you want to follow along, don't forget to subscribe.
