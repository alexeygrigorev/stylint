# Preparing a Demo Day Where Students Actually Show Work

I wrote this synthetic style exercise as a how-to guide. The course, dates and numbers are fictional. In May 2026 I ran a demo day for a data analysis course where 18 students finished and 7 volunteered to present. The first presenter spent four of the nine minutes on slides about the history of the project.

The demos that worked put the running project on screen in the first minute and let questions drive the rest. I reused the preparation plan from May for the next demo day on 15 August, and I describe its four steps in this post.

In this post, I'll share:

- how to set the timing rules
- how to run one rehearsal
- how to record the backup video
- how to prepare the feedback form
- which caveats matter on the day
- what the second demo day changed

## 1. Set The Timing Rules

We settle the format in writing before anyone prepares slides. Each presenter gets 7 minutes of demo and 3 minutes of questions. The rule that matters most is simple: the running project must appear in the first 60 seconds. Slides are allowed for exactly one intro slide, and the stage timer shows a red line at that mark.

I sent the rules out 14 days before the event, together with the presenter order. Presenters who know they go fifth prepare differently from presenters who expect to hide at the end. I saw the same effect in both editions, where the early slots had the tightest demos. Visitors fade in the middle slots, so we placed the two strongest demos in slots 2 and 5. I keep the format document on one page in the course wiki, right next to the presenter order.

## 2. Run One Rehearsal

We hold one rehearsal a week before the event, in the same room when the room is bookable. We time every demo with a phone timer and give each presenter exactly one note, because a page of notes helps nobody the night before. The August rehearsal ran 95 minutes for 7 presenters and caught two demos that would have run 12 minutes each.

The most common rehearsal note stayed the same across both editions: students explained the dataset for three minutes before showing anything. After the rehearsal we asked every presenter to open on the finished result and explain backwards from there. Presenters who failed the 60-second rule at rehearsal fixed it in the video recording, not on stage. I also send the one note per presenter in writing the same evening, so nobody has to remember it overnight.

## 3. Record The Backup Video

Every presenter records a 5-minute backup video during the rehearsal week. The video is boring on purpose: it shows the project running once, with no audience and no pressure. When the venue projector refuses the laptop adapter, as it did in May for two demos, the backup keeps the slot alive.

Compress the videos before copying them to the venue laptop, because 7 raw recordings at 1.2 GB each don't fit:

```bash
ffmpeg -i demo-raw.mov -vcodec libx264 -acodec aac -b:v 4M demo-backup.mp4
```

Each compressed video came out between 90 and 210 MB, and all 7 fit on one USB stick with room for the slides. We name the files by slot order, from `slot-1-backup.mp4` to `slot-7-backup.mp4`, so a panicked switch takes seconds. The videos also live in a shared drive folder called `demo-day-backups`, and the USB stick is only the second copy. We test the stick on the venue laptop the evening before, and that test has saved every demo day since May.

## 4. Prepare The Feedback Form

The feedback form has three fields, and it goes out as a QR code on the closing slide:

```text
name one thing you saw working
name one thing that was unclear
name one thing you would build next
```

Visitors fill it during the question blocks, which takes under a minute. In May we collected 9 responses from about 34 visitors, all through a link in the chat after the event. In August the QR code and the question blocks produced 26 responses from 41 visitors, and 11 of them contained a suggestion we still use. The form stays open for 48 hours after the event, and the late responses added useful detail on two projects.

## Caveats For The Day

One person owns the timer, because a presenting student can't watch a clock. Keep 5 minutes of buffer between demos, because questions always eat into the next slot.

Treat the backup videos as a last resort. A video answers no questions, and the question block is where visitors actually engage.

Check the adapter bag the night before as well. One HDMI adapter and one USB-C adapter covered every laptop type in our course.

## Results From The Second Demo Day

The August demo day ran 7 demos in 96 minutes with zero timing overruns, against 4 overruns in May. The running-project rule did most of that work, and the backup videos turned two adapter failures into 30-second pauses. Presenters still over-prepare slides, and two of the seven needed a reminder at rehearsal. If I could keep one part of the plan, I would keep the feedback form.

I'll write about how the suggestions feed the next course in a future post. If you want to follow along, don't forget to subscribe.
