# Turning Support Conversations into a User Guide

I wrote this synthetic style exercise as a build log. BikeLog, its users and all figures are fictional.

BikeLog is a fictional maintenance app for cycling coaches. During May 2026, it received 63 support emails and 41 messages in a private community. We had expanded the product to 19 screens, while the user guide still had 12 pages.

In the guide, I had explained how to create an account and log a repair. It said almost nothing about athlete records, service intervals, CSV imports or shared workshop views. Users asked about those topics every week.

In this post, I'll share:

- how I grouped 104 support conversations
- how I turned repeated questions into guide tasks
- how I edited generated drafts without inventing behavior
- how I linked the guide from the product
- what changed in support volume after five weeks

## The Support Backlog

Support work lived in three places: email, a community spreadsheet and notes from two coaches. Some questions arrived four or five times with different words. Others were one-off bugs that looked like feature requests.

My first attempt was to write documentation whenever I answered a question. That produced six useful paragraphs and 14 unfinished drafts over two months. Each answer solved one person's problem, and none created a guide I could link to next week.

I needed a repeatable path from question to page. I exported the conversations to CSV and gave each one an identifier, date, channel, screen name and short paraphrase. Cleaning took 3 hours and revealed that 17 emails were continuations of 8 older threads.

That reduced the set to 95 distinct conversations, still too many to document one by one.

## Grouping The Questions

I put the paraphrases into a spreadsheet and grouped them in two passes.

The first pass used five broad buckets:

- getting started and accounts
- athlete records and permissions
- service intervals and reminders
- imports, exports and backups
- workshop views and sharing

The second pass split buckets where the user goal changed. "Athlete records" separated into adding an athlete, editing inherited equipment and transferring a bike between athletes. Those tasks have different starting screens and different failure cases.

The second pass gave me 31 question groups. Nine groups contained six or more conversations and accounted for 61% of all support messages. Another eight contained two or three conversations, and fourteen were singletons that I left out of the first release.

I found the grouping more useful than counting keywords because it captured intent. For example, the question about a disappeared bike and the request to change ownership used different words.

Both entries therefore needed the transfer-ownership task.

## Write Tasks, Not Features

For each large group, I wrote the guide around a user task. I named the transfer page "Move a bike to another athlete". It starts from the athlete list, names the required permission and explains what happens to open repair records.

I drafted the first eight pages with Claude Code. I supplied the screen names, exact buttons, permissions and three anonymized questions. I didn't supply screenshots, because the interface had changed twice since March.

The generated drafts had predictable problems:

- one draft invented a "Save and continue" button on a screen with no such control
- another described an import wizard as a five-step process when it has three steps

I rewrote both passages while clicking through the actual app.

Every page follows one structure:

- what the user wants to accomplish
- the starting screen and required permission
- the numbered steps
- what happens afterward
- the most common failure and its next action

I kept the transfer page to 380 words. It includes the fact that service history remains with the bike and reminders stay with the owner. That detail came from a support thread and prevented a follow-up question in testing.

## Link From The Product

This approach failed once because it placed help outside the user's moment of confusion. I had published the pages, but users searched their email first. So I added context-specific links inside BikeLog.

Each relevant empty state now links to its matching task page. The ownership transfer screen has a "How ownership works" link beside the athlete selector. The CSV import screen links to a page that lists the required columns and the six validation messages.

I also changed support replies. Each saved reply includes one guide link and one request for feedback on the linked page. Two coaches helped test the links during a fictional June workshop. Their feedback led to three title changes, and "Manage relationships" became "Share a workshop view".

I expanded the guide index, and every page states the app version it was checked against. The current version is 2.8.1.

I organized these page groups:

- eight task pages
- six reference pages
- four troubleshooting pages
- one import column list

## Results And Limits

I compared the five weeks after the guide update with the five weeks before it. Distinct support conversations fell from 95 to 61. The nine large question groups produced 24 conversations, compared with 58 before. Imports remained noisy, and permissions still generated one-off questions.

Those numbers are directional, because May included a promotion and June didn't. The more reliable evidence is reply time. The eight saved replies reduced median first response from 9 hours to 3 hours during weekdays.

The current process has one review per month. I reread the eight task pages, click every step and check whether a new support thread exposes a missing failure state. If a page needs more than a small correction, I create an issue rather than editing in place.

## Closing Notes

The useful input was the question grouping, and the useful output was a task page linked from the exact screen. I gained time from generated explanations only after supplying real behavior and failure cases.

A user guide is part of support, rather than a separate documentation project. I'll revisit the 14 singleton questions after one more release.

If you want to follow along, don't forget to subscribe.
