# Preparing a Live Session for Two Time Zones

I wrote this synthetic style exercise as a how-to guide. The course, dates and numbers are fictional. In May 2026 I ran a session for a course cohort split across two time zones. The group had 23 people in Central Europe and 11 in Singapore.

My first attempt back in February was rough. I scheduled the call at 18:00 Berlin time, which is 01:00 in Singapore. Nine of the Singapore group joined anyway, most of them from phones.

Since March 2026 I prepare every session for both zones with a checklist. Preparation takes about 60 minutes per session, and the May session ended with questions answered in both zones.

In this post, I'll share:

- how I pick a time that works in both zones
- how I prepare the recording and the chat
- how I adapt the examples for each zone
- how I set up the homework handoff
- where the setup still falls short
- what I plan for the next cohort

## 1. Pick The Time And Publish It Early

I keep one fixed slot for the whole cohort, 16:00 to 17:30 Berlin time. That slot is 22:00 in Singapore, which is late but workable. An 18:00 slot is 01:00 in Singapore, and no amount of enthusiasm fixes 01:00.

I publish the date 3 weeks ahead, and every announcement shows both local times in the title. Ambiguity about time zones cost me one missed session in February, so the title now reads "Session 4, 16:00 Berlin, 22:00 Singapore".

Before I fix a slot, I check the conversion with GNU date instead of doing the math in my head:

```bash
TZ=Asia/Singapore date -d "2026-10-08 16:00 CEST"
```

That prints 22:00 for the October dates, and daylight saving shifts have surprised me twice. The check takes 5 seconds and has saved at least one wrong announcement.

## 2. Prepare Recording And Chat

I record the screen and audio locally with OBS, an open-source recording tool, and I post the recording within 2 hours. The local file gets a dated name such as `2026-05-14-session-4.mp4`, and the upload uses the same title as the thread post. The Singapore group watches at 22:00 or the next morning, so the recording is their primary session. Platform recordings failed me once before, so now I keep a local copy and upload it myself.

Chat needs two homes, because the live chat during the call moves fast and disappears. Important links also go into a forum thread I open before we start. After the May call I answered 14 forum questions before breakfast the next day, most from the Singapore group.

## 3. Adapt The Examples For Each Zone

Most demos don't depend on the clock. The ones that do get pre-recorded, and I narrate the clip as if it were live. In the May session the cron demo showed a nightly job. I recorded the 03:00 run in advance and played the clip during the call.

The example datasets get the same treatment. Timestamps render in UTC with both local times beside them, because a chart that says 03:00 confuses one zone or the other. That change took one template edit in the course repo and now happens automatically.

## 4. Set Up The Homework Handoff

The homework goes out in the same forum thread as the recording, within the same 2 hours. The deadline has no fixed time zone, and that's deliberate. I write "end of day, 12 October, your local time" instead of a fixed hour. It reads informal, and it removed every deadline argument I used to have.

The thread post follows one template:

```text
session 4 - queue monitoring
recording: 62 minutes, posted 20:40 Berlin time
homework: add a dead-letter queue to task-worker
deadline: end of day, 12 October, your local time
questions: reply in this thread, answers within 24 hours
```

Submissions arrive as pull requests against `course-homework`, a small practice repo, and I review them in the order they arrive. The thread keeps everything in one place, so nobody needs a second link.

## Caveats And Costs

A 22:00 finish is still late, and I now say so in week 1. Nobody should feel obliged to attend every session live, and attendance in the Singapore zone sits around 40%.

Chat during the call splits my attention, so a teaching assistant watches it and holds 2 or 3 questions for the break. That arrangement started in April and stuck. Recordings also age badly. One storage move broke 6 links from the February cohort, and I fixed them in an evening.

Preparation costs real evenings too. The checklist work happens after my day job, and 60 minutes on a Wednesday is 60 minutes I don't spend drafting.

## My Plan For The Next Cohort

The October cohort starts on 8 October with 34 people enrolled, and the same checklist applies. The fixed slot stays, along with the thread template and the two-home chat.

What still doesn't work is live attendance in the Singapore zone. The recording and the forum cover those 11 people, yet I haven't found a format that makes 22:00 feel optional. A second shorter run of the same session at Singapore morning hours is the next experiment, and I want to test it in November.

I'll write about the homework review workflow in a future post. If you want to follow along, don't forget to subscribe.
