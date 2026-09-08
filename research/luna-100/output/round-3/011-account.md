# Reviewing 2,500 Scholarship Applications

The second cohort of my AI Bootcamp was about to start when I opened scholarships for students who couldn't afford the paid program. More than 2,500 applications arrived. There were far fewer places than applications. I needed a process that could handle the first pass without pretending that a score could replace judgment.

The scholarship was for people already doing meaningful work who wanted to use the training to scale its impact. It wasn't meant for general career exploration. Previous AI experience wasn't necessary. Each application needed a clear connection between the applicant's current work and the reason this bootcamp mattered at that stage.

## Selection criteria

Motivation came first, so I filtered out empty, one-line and generic responses. I also filtered applications focused only on finding a job, learning tools in isolation or earning money quickly. A strong application described a specific problem, explained who would benefit from solving it and showed why the training was relevant now.

I then looked for depth and alignment. I wanted to see that the applicant understood what the bootcamp taught and could connect it to current work. Plans to scale an existing project, reach a community or multiply an existing impact were more useful than abstract promises to learn.

Completion mattered because the program was demanding. Prior long-term projects, concrete plans and existing accountability structures helped me judge whether someone could commit the time and follow through. Not being selected didn't necessarily mean an application was weak. Sometimes the scholarship's purpose didn't match the applicant's situation. Sometimes there were simply more strong applications than places.

## Using Claude Code for the first pass

Reading every submission manually wasn't feasible at this scale. I defined the evaluation logic in custom Claude Code slash commands and used them for an AI-assisted preliminary review. The commands ranked applications and filtered out submissions that clearly didn't fit the scholarship's intent.

Claude Code could run several commands in parallel through sub-agents, which made large batches manageable while keeping the evaluation logic consistent. I used reusable Markdown workflows instead of writing a custom agent in Python. The instructions, the model and the commands reduced the overhead of processing thousands of applications, but I still validated the output myself.

The first pass left me with the top 50 applications. I shuffled that group to reduce bias. Then I read every selected submission in full.

When applicants supplied linked profiles or projects, I checked them as well. I compared the AI-generated scores with the actual substance of each application. I gave more weight to authenticity, clarity of intent and the likelihood of following through than to any numeric score.

This division of labor gave each part of the process a clear job. Claude Code handled the volume and applied the initial logic consistently. I handled the final decision, where context and qualitative details mattered. The process didn't turn scholarship selection into a number. It reserved careful human attention for the smaller group most likely to deserve it.
