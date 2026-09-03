# Launching a Small Course Cohort with Mostly Existing Tools

I wrote this launch log as a synthetic style exercise, and every cohort detail is fictional. In the invented project, I launched a three-week course called Shipping Small Automations for 42 paying students in September 2026.

I had already taught the material in free workshops, but course logistics remained unsolved.

I needed a way to handle registration, reminders, recordings, and homework feedback.

In this post, I'll share:

- how registration worked with forms and payments
- the reminder setup and its message schedule
- how I ran live sessions and collected homework
- what the feedback form showed
- what I would keep and change next time

## Registration

The registration path used Google Forms, Stripe payment links, and a private Notion database. A student filled in the form, paid through Stripe, and forwarded the receipt to a course address. I checked the receipt and manually added their email to the cohort sheet.

That manual step sounds bad. It took about two minutes per student and gave me a natural review gate for discount requests and team registrations. The bigger problem was the delay between payment and access: four students wrote within an hour because they wanted to start the pre-course checklist immediately.

I eventually added an automated confirmation. Zapier watched the form responses and sent a welcome email with the session calendar, required tools, and a link to the private repository. Stripe still handled payment, so the two systems remained separate.

Of 61 applications, 42 completed payment by the September 4 deadline. Seven asked for a deferred decision, and I offered them places in the November cohort. Twelve applications came from one company, so I treated them as a team enrollment and invoiced them directly.

## Reminders

I kept the reminder stack dull. A spreadsheet held the student email, time zone, session registration, and homework status. Google Calendar sent session reminders, while a Python script sent the preparation and follow-up notes through Resend, an email delivery service.

```bash
python scripts/send_cohort_email.py \
  --template emails/session-02-preparation.md \
  --cohort 2026-09 \
  --dry-run
```

The dry run printed the recipient count and previewed the first three email addresses. Once I checked those lines, I reran the command without `--dry-run`. That small pause prevented an embarrassing email to my personal address, which the script had included during an early test.

Students received four messages before the first session. The sequence was a welcome note, a preparation checklist, a calendar reminder, and a one-hour alert.

After that, each week got one preparation email and one follow-up. The follow-up included the recording, slides, homework, and office-hours link.

Unsubscribe data justified the restraint. Across 503 emails, 11 students opened fewer than half, and only two unsubscribed from operational messages. Five students replied to ask for calendar changes, so I added those requests to a shared support note.

## Live Sessions

I ran the sessions on Zoom and streamed the recording to Vimeo. Each session lasted 90 minutes. I used the first 25 minutes for a demonstration, 45 minutes for guided implementation, and 20 minutes for questions.

Attendance started strong and then settled. The first session had 38 live students, the second 31, and the third 29. Recordings reached another eight to eleven students each week, so total weekly participation ranged from 39 to 42.

Homework went into GitHub Classroom. I accepted a link, a screenshot, or a short note explaining why the student couldn't finish.

The important requirement was evidence of the automation run, its input, and one real output file.

I reviewed homework every Wednesday and Sunday. Each submission got a three-line response with one observation, one next step, and one risk to check.

Thirty-five students submitted week one, 29 submitted week two, and 26 submitted the final project.

## Feedback Results

I sent the main feedback form after week two and a shorter form after graduation. Thirty-two students answered the main form. The median confidence score for building an automation alone was 4 of 5, up from a self-reported median of 2 before the course.

The free-text answers gave me the useful detail:

- 19 students wanted more time to debug their own projects
- 11 asked for reusable starter repositories
- 9 wanted clearer guidance on error handling
- 7 asked for a second live session in another time zone
- 5 said the final project scope was too large

I grouped the comments by course module rather than by sentiment. The first week's comments were mostly positive and focused on setup. Week two produced the largest number of questions, so I added a 35-minute debugging recording before week three.

The final form had 28 responses. Twenty-six said they would recommend the course to a colleague, one said maybe, and one skipped that question. Four students had already shipped an automation for their own work.

## Next Cohort

I would keep the payment form, spreadsheet, GitHub Classroom, and four-message preparation sequence. They were boring, observable, and cheap. The whole tooling cost was $31.44 for email delivery, video hosting, and form upgrades during the month.

For the next cohort, I'll reduce the final project to one automation with a documented input and output.

I'll also publish starter repositories before day one and schedule a second optional question session for students outside Central European Time.

The registration delay still bothers me. Before the November cohort, I plan to connect the payment webhook to the welcome email and retain a manual review step for team enrollments.

## Lessons From the Launch

Existing tools handled the course operations, so I had to decide which steps should stay manual.

I then wrote down each message, deadline, and acceptance rule so the next run could repeat them.

Small cohorts made personal feedback possible. They also exposed operations to me, and every late payment, calendar conflict, and homework question arrived in my inbox.

I'll write about the revised project brief in a future article. Subscribe if you want to follow the next cohort.
