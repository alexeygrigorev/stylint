# Shipping a Feature from a Tram Stop



I want to describe what happened, because the sequence of small decisions is more useful than a polished summary. 

Hi everyone, Before going into the main topic of today’s newsletter, I want to wish you a happy holiday

season. Merry Christmas, Hanukkah, Kwanzaa, Yule, and a happy New Year to everyone who celebrates! I

started this newsletter less than a month ago, and we're already almost 1,000 subscribers.

https://alexeyondata.substack.com/p/my-newsletter-now-has-a-referralhttps://alexeyondata.substack.com/lea

derboard. Here are the terms: Refer 3 friends to get access to the Tutorial Library, a curated

collection of study resources focused on learning by doing and solving real engineering problems. Refer

10 friends to get an rarly access to an Exclusive Mini-Course on building an action-oriented AI agent.

Refer 25 friends and join a private 30-minute Zoom conversation with me to discuss career decisions,

learning paths, technical challenges, or project feedback, with no fixed agenda.

https://aishippingblog.com/leaderboard?&utmsource=post Now, to the main topic! One Idea I Want to Share

this Week https://courses.datatalks.club/https://courses.datatalks.club/wrapped/2025/ to the platform:

2025 community highlights, the most popular courses, top learners, and individual, shareable Wrapped

pages for each participant. Most of the work happened on my smartphone while I was commuting to pick up

my kid. A preview of the Wrapped page on the course platform Starting the PR from a Tram Stop The idea

came to me while I was standing at a tram stop: it would be useful to have a single page summarizing

what learners achieved across our Zoomcamps throughout the year.

https://github.com/DataTalksClub/course-management-platform/pull/115. Here’s what it looks like: The

initial PR generated from a spoken issue Iterating Without a Laptop Once the PR is open, I review the

changes, and Copilot updates the code based on my comments. I can handle this entire back-and-forth from

my phone. Here’s how I iterate: I scroll through the code changes on my phone, leave comments, tag

Copilot, and ask it to make specific updates. After Copilot pushes a new version, I review it again and

repeat the process if needed. The result works well for small changes like copy tweaks, layout

adjustments, and minor logic updates. Of course, voice recognition sometimes gets things wrong. In the

original issue, I said “top 100,” which became “top 1200,” and that ended up in an early version of the

PR. But these kinds of mistakes are easy to fix: I spot them during review, leave a comment, and

reassign Copilot. One particularly useful detail is that Copilot can run the project itself, generate UI

screenshots, and attach them directly to the PR. That means I can check that the page renders correctly

and that buttons and links behave as expected. The screenshots aren’t perfect since Copilot has no

internet access, and some styles don’t load. But they’re sufficient to confirm that nothing is obviously

broken. Example screenshots attached to the PR Phone vs. Laptop Work After each new comment, Copilot

takes about 10-30 minutes to update the PR with a new version. I go through this review-and-comment

cycle several times a day right from my smartphone, often in short windows between other tasks. For

small and medium-sized changes, it’s remarkably effective. CI/CD workflows What I don’t do from my phone

is final approval for complex changes. For larger features, deeper testing, or anything that could break

production, I



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
