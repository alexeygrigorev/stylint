# Understanding a Free Course Enrollment Funnel

I wrote this synthetic style exercise as a build log, and all numbers and names in it are fictional. In January 2026 I started measuring a free course funnel. It drew 12,400 site visits in the month and converted 310 of them into registrations.

Students who finished the course rated it 4.7 out of 5 in an internal survey, so the content was fine. The leak sat somewhere between the visit and the certificate, and I had no instrument for finding it.

I had run three cohorts of this course while watching only the totals. I knew signups and graduations, and nothing in between.

In this post, I'll share:

- what the January logs showed between visits and registrations
- why my first fix left the numbers flat
- how I added activation tracking with a Postgres table
- what two reminder emails changed in March
- what the funnel looks like as of July 2026

## January Numbers From the Raw Logs

I pulled three numbers for January from the raw nginx logs and the `signups` table in Postgres.

The gaps between stages were bigger than either end:

- 12,400 visits reached the course landing page
- 2,900 of them opened the enroll page
- 310 visitors finished the registration form

The registration rate was 2.5 percent of visits and 11 percent of enroll page views. I read both numbers as healthy and assumed the course grew by reputation. That reading was comfortable and wrong.

## My First Fix and Why It Failed

My first move was the cosmetic one. In early February I rewrote the landing page copy, added two testimonials, and cut the registration form from six fields to four. The work took one evening, and I expected the rate to climb within days.

February ended at 11,800 visits and 302 registrations, which rounds to the same 2.6 percent as January. I had redecorated the top of the funnel without touching the place where people quit.

My mistake was fixing the stage I could already see. The rule I took from it: measure every stage before changing any page.

## Adding Activation Tracking

At that point I stopped editing pages and started counting. I defined activation as opening lesson one within seven days of registering, and I built the tracking around a single Postgres table.

The table keeps one row per student and stage:

```text
create table funnel_events (
    email       text,
    stage       text,      -- signup, activated, completed
    happened_at timestamptz
);
```

The signup row appears when the form succeeds, and the activated row appears when a student opens lesson one through the welcome email. A completion row appears when the grading script accepts the final project.

A script called `count_funnel`, a thirty-line Python file that queries Postgres, prints the funnel for any month:

```bash
python scripts/count_funnel.py --month 2026-02
```

The February output showed 124 activated students out of 302 registrations, about 41 percent. Completion split the cohorts apart: students who activated finished at 71 percent, and the rest finished at 6 percent.

The 6 percent tail explained the completion problem better than any survey had, because most registered students never opened lesson one.

## Two Reminder Emails in March

The 41 percent activation rate made the welcome email the main suspect. It went out once, 20 minutes after signup, and many students never opened it. In March I added two plain-text reminders sent by a cron job through the mailing provider's API.

The day-3 reminder is four sentences long:

```text
Subject: Your spot in the course is saved

You registered on Tuesday but haven't opened lesson one yet.
The first lesson takes about 25 minutes.
Reply to this email if anything blocks you.
```

The reminders reuse the welcome email's link, so the activated row fires no matter which message the student clicks. Everything else in the funnel stayed frozen during March, which keeps the comparison honest.

The March cohort reached 57 percent activation, up from 41 percent in February. Completion moved from 19 percent to 27 percent for a cohort of almost the same size. Registrations barely moved, which fits the data, because the leak sat downstream of the form.

## The Funnel in July 2026

Three pieces run the whole funnel now:

- one Postgres table with three stage rows
- a nightly cron job that refreshes the monthly counts
- two reminder emails on day 3 and day 7

In June the course drew about 11,000 visits, and 3.1 percent of them registered. Activation held at 57 percent, and completion held at 27 percent. The monthly report takes about ten minutes to refresh by hand.

The tracking still has blind spots. Activation still means a click on the emailed link, so a student who finds lesson one by searching the site never appears in that stage. A manual check in May put that group at roughly one registration in ten.

Completion is the other open problem. It has sat at 27 percent since March, and I don't yet know which stage feeds the ceiling.

## Lessons From One Funnel

The arc took six months, and the useful move cost one evening. I redecorated a page for nothing in February, measured four stages in the same month, and fixed the stage that fed completion in March.

The flat February taught me more than the successful March, because it showed that measurement mattered more than copy. A funnel stage without a number stays invisible, and I had run three cohorts on two numbers.

I still don't know how to push completion past 27 percent, and that's the next thing I want to change. I'll write about the completion ceiling in a future post, hopefully with a fix that works. If you want to follow along, don't forget to subscribe.
