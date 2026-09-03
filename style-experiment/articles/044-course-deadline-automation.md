# Automating Course Deadline Reminders Without Becoming Noisy

In February 2026 I ran a six-week course for 214 students and sent deadline reminders to everyone. Four people thanked me, while eleven asked me to stop. That imbalance told me I had to redesign the reminder system.

I wrote this as a synthetic style exercise with invented students, dates, and response rates. I would still reuse the segmentation workflow with a real course.

In this post, I'll share:

- what made the first reminder campaign noisy
- how I segmented students by submission state
- which escalation rules I added
- how quiet hours changed delivery
- what the six-week results showed

## The First Campaign

The obvious solution was one announcement before each deadline. I scheduled messages at 09:00, two days before every assignment closed. Each message contained the assignment name, deadline, submission link, and office-hours time.

The campaign reached 214 students six times. Open rates ranged from 38% to 61%, and submissions rose in the final 24 hours. Those numbers looked healthy until I counted complaints.

Eleven students replied with some version of "I already submitted". Three had submitted during the first week. The remaining eight had submitted before the reminder arrived, and the announcement still told them to hurry.

I had optimized for reach and ignored state. The announcement treated a completed student and a missing student identically.

## Segment by Submission State

For the next cohort, I exported enrollment data into a local SQLite database.

Each row had these fields:

- student ID
- cohort
- assignment
- submission timestamp
- extension status
- preferred channel

The export contained no grades.

A short Python script classified every student into four groups:

- submitted
- extension approved
- missing with recent activity
- missing with no recent activity

Students in the submitted group received no further reminders for that assignment. Students with approved extensions received a reminder tied to their extended date. The other two groups received the standard deadline message.

The classifier ran every hour and wrote its decisions to `reminder_state.jsonl`. Each line included the student segment, assignment, decision, and reason. I reviewed a random sample of 40 decisions before enabling delivery.

## Escalation Rules

The first version used one message per assignment. The new system separates an informational reminder from an escalation, and each level has a different purpose.

I settled on four levels:

- seven days before deadline: one informational message
- 48 hours before deadline: message only for missing students
- 12 hours before deadline: message plus direct submission link
- after deadline: submission status and extension options

No student receives more than two messages per assignment unless they request an extension. That ceiling forced me to choose timing instead of sending another nudge every few hours.

The after-deadline message is deliberately calm. It states whether we recorded a submission, lists the late-submission rule, and gives one link to the extension form. It doesn't scold anyone.

## Quiet Hours and Delivery

The old scheduler delivered at 09:00 because that time was easy. The new scheduler checks each student's course time zone and holds messages outside a delivery window.

I chose these defaults after looking at prior activity:

- weekdays from 09:00 to 19:00
- Saturday from 10:00 to 14:00
- no delivery on Sunday

If a message misses its window, delivery moves to the next allowed slot. The delay is visible in the log, so I can tell whether a student received the 12-hour warning or a post-deadline version.

I also separated channels, so operational deadlines go by email while general cohort announcements go to the course forum. I removed automated direct messages because they felt more intrusive than email.

## Results After Six Weeks

The next cohort had 239 students and the same six assignments. The scheduler prepared 1,014 candidate reminders and delivered 486. The other 528 were suppressed because the student had already submitted or belonged to a quiet channel.

Submission timing shifted a little. Final-24-hour submissions fell from 61% of all work to 54%, while submissions four to seven days early rose from 17% to 26%. I can't prove the reminders caused the shift, but the direction was useful.

Complaints fell from 11 in the old cohort to 1. That student had an approved extension and still received the public deadline message because my extension sync job failed for 40 minutes.

The failure log exposed the bug immediately. I added a retry with exponential backoff and a daily reconciliation report. I also stopped the scheduler if extension updates fall more than one hour behind.

I kept the database and scheduler small. SQLite handles the cohort, and a single Python process runs the classifier. That choice limits concurrency, but a distributed setup would add operational risk without solving a current problem.

The bigger risk is privacy. The scheduler knows who submitted, but it doesn't need grades or message content. I kept the state export to timestamps and segment labels, and the delivery log stores a student ID rather than the email body.

## Permanent Changes

The reminder system is now a state machine, not a calendar blaster. Submission state decides whether delivery happens. Deadline distance decides which message the student receives.

The most useful number isn't the open rate. We now deliver 2.1 messages per completed assignment, and the complaint rate gives me a rough upper boundary for acceptable volume.

I still review the suppression sample weekly. Automation can remove obvious noise, but a person should decide when the rules have become annoying.

I plan to write about the reconciliation report in a future article. Subscribe if you want the follow-up.
