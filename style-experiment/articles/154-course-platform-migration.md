# Migrating Course Content Between Platforms

For three years I ran a fictional 6-week course called "Practical Data Cleanup" on a hosted learning platform. It had 1,842 enrolled students, 87 video lessons and 24 assignments. Last spring the platform announced a pricing change that would have raised our cost from $180 to $620 per month.

This synthetic style exercise describes how I moved that course to a simpler stack. The platform names and numbers are fictional, but the migration order matters: export first, map content second, redirect third and communicate with learners throughout.

In this post, I'll share:

- how I exported and audited the content
- how I mapped lessons to a new structure
- how redirects preserved student links
- how I prepared assignments and progress data
- what I told students and what still needs work

## Audit The Export

The first export arrived as a 3.7 GB ZIP archive. It contained 87 MP4 videos, 92 markdown documents, a CSV of enrollment data and a JSON file for lesson order. It also included 4,118 assignment submissions I hadn't expected.

I unpacked the archive into a temporary directory and wrote a 70-line Python script to inventory every file. For each item, the script recorded its source path, media type, title and lesson ID. It also recorded whether the content was marked published.

The inventory found three surprises:

- 5 lessons were unpublished drafts from 2023
- 7 videos had no matching markdown page
- 2 markdown pages referenced images missing from the archive

Before touching the new platform, I resolved those items with a spreadsheet. I archived the old drafts, attached the seven videos to the correct lessons and recreated both missing images from the original course repository.

## Map The New Structure

The old course had six weekly modules. Each module contained lessons, one quiz and three to five assignments. The new stack used a plain database, so I could keep that structure and add a stable `slug` to every lesson.

I defined a mapping table before importing anything:

```text
source_lesson_id -> slug
title -> title
body_markdown -> body_markdown
video_file -> video_key
published -> status
week_number -> module_number
```

The mapping exposed another naming problem. Old lesson titles such as "Lesson 4.2: Cleaning Messy Date Columns" worked well in the hosted platform, but they made URLs dependent on module numbers. I kept visible titles and generated new slugs from the topic, so a lesson became `cleaning-messy-date-columns` instead of `module-4-lesson-2`.

That decision broke internal links in 19 markdown documents. My script found links by their source lesson ID and replaced them with the new slugs. It wrote a report for every replacement, and I reviewed the full diff before importing the course.

## Preserve Redirects

Students had bookmarked old URLs for more than two years. Some lesson links also appeared in community answers and homework feedback. I didn't want anyone to hit a dead link while debugging a pandas error, so redirects became a migration requirement.

The new site serves Nginx.

I generated one Nginx redirect for each old lesson path:

```nginx
location /courses/cleanup/lessons/4_2 {
    return 308 /courses/practical-data-cleanup/cleaning-messy-date-columns;
}
```

The generated file contained 87 location blocks. A 308 redirect preserves the request method, which mattered for a few assignment form submissions still circulating in old emails.

I tested the redirects with 87 curl requests and one Python script. Every old URL returned 308, and every destination returned 200. The script also verified that each destination title matched the source title in the export inventory.

## Move Assignments And Progress

Assignments required more care than lessons. Students had submitted code, notebooks and screenshots, and 214 submissions had late-penalty decisions. The export included submitted files, but it didn't preserve the association between a submission and a specific assignment version.

I used the assignment version ID from the JSON export and added it to the new database. For the 214 flagged submissions, I copied the instructor note into a separate review table. This preserved the reason for each penalty without making the public assignment history confusing.

Progress data was messier because the hosted platform stored completion as events, while the export gave me only each student's latest state. I imported lesson completion, quiz scores and final project status, but I couldn't reconstruct partial video watches or repeated quiz attempts.

I decided to disclose that limitation. Students who had completed the course kept a completion certificate. Students with partial progress kept their completed lessons and quiz scores, but their progress bars show a fresh estimate rather than historical activity.

## Communicate With Learners

I announced the migration twice before the maintenance window and twice afterward. The first message explained the cost change in general terms, the new URL format and the date. The second message, sent 48 hours before the switch, gave exact times and asked students to save drafts.

The course went offline on a Saturday at 06:00 UTC and returned at 11:20 UTC. I expected 30 minutes of DNS propagation, but the actual propagation took about three hours for some mobile networks. Two students emailed because their browser cache still referenced the old host.

After the switch, I sent a short verification checklist:

- open your current lesson from your bookmark
- check that your assignment history appears
- submit a test file for your next assignment
- reply if a certificate is missing

Fifty-three students replied, and forty-one confirmed that everything worked. Twelve had stale bookmarks or missing progress, and I fixed each case within two days.

## Changes For Next Time

The technical migration worked, and monthly infrastructure cost fell to $55. Video serving remained stable during the next cohort, even with 240 concurrent students on a release day.

But I underestimated communication because one email went to the old platform's mailing list, which some students had muted. Next time, I'll duplicate critical messages in the course dashboard and keep a status page live for a week.

I also wrote the redirect tests after the mapping. Next time, I'll generate those tests from the inventory before the new import. That order would have caught two mapping mistakes during development instead of during smoke testing.

Finally, I would freeze content one week earlier. I made two small lesson edits during migration week, and both caused unnecessary merge conflicts with imported markdown.

I'll describe the migration scripts in more detail in a future newsletter. If you want to follow along, don't forget to subscribe.
