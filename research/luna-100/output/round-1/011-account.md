# How I Reviewed More Than 2,500 Scholarship Applications

The second cohort of my AI Bootcamp was about to start, and I opened scholarships for motivated students who could not afford a paid program. I expected interest, but I received more than 2,500 applications. That was far more than the number of available places, so reading every submission manually was not realistic.

The scholarship was meant for people already doing meaningful work and wanting to use the training to increase its impact. It was not intended for general career exploration. Applicants did not need previous AI experience, but I needed to see a clear connection between what they were building and why this particular training mattered at that point.

Motivation was the first signal. Empty, one-line, and generic responses were filtered out early. Applications focused only on getting a job, learning tools in isolation, or earning money quickly did not match the purpose of the scholarship. Stronger applications described a specific problem, who would benefit from solving it, and why the training was relevant now.

I also looked for depth and alignment. Did the applicant understand what the Bootcamp taught? Could they explain how it connected to their current work? Did they have a plan to scale a project, reach a community, or multiply an existing impact? Abstract statements about wanting to learn were less useful than a concrete project and a reason to make it better.

Completion mattered as well. The program was demanding, so I looked for evidence that an applicant could commit the time and follow through. Long-term projects, concrete plans, and existing accountability structures were useful signals. Not being selected did not necessarily mean an application was weak. Sometimes the scholarship’s purpose did not match the applicant’s situation, and sometimes there were simply more strong applications than available places.

For the first pass, I used Claude Code. I described the evaluation logic in custom slash commands and had it review all applications. The commands ranked submissions and filtered out applications that clearly did not fit the scholarship’s intent. Claude Code could run several commands in parallel through sub-agents, which made the large batch manageable. I used reusable Markdown workflows instead of writing a custom agent in Python.

That first pass gave me a smaller group of 50 applications. I shuffled them to reduce bias, then read every selected submission myself. I checked linked profiles and projects when applicants provided them, and compared the AI-generated scores with the actual substance of each application. At this stage, authenticity, clarity of intent, and the likelihood of following through mattered more than a numeric score.

The combination gave me a workable division of labor. Claude Code handled the scale and made the initial logic consistent. I handled the final judgment, where context and qualitative details mattered. The process did not turn scholarship selection into a score alone. It let me reserve careful human attention for the applications most likely to deserve it.
