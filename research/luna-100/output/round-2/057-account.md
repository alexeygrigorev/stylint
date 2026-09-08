# Collecting my workshops on AI Shipping Labs

My workshop materials were spread across YouTube and GitHub, with some conference notes left in my archives. Two recent workshops had only been shared with AI Shipping Labs members in Slack. I wanted people to find the material in one place, so I added a Workshops section to the website.

That depended on a larger platform update. Valeriia built the first AI Shipping Labs site with Next.js, using v0 and Cursor. It had a landing page and resources, plus a newsletter form and checkout. We wanted to see whether people would sign up before building a larger platform, and more than 80 did.

The site didn't have member profiles or progress tracking. It also couldn't manage event registration or content access by membership tier. I started moving it to Django piece by piece so we could add those features.

I used the library update to change the format as well. Each workshop used to have a long README containing everything on one page. That can work as a reference, but it's hard to find a stopping point when you're learning a 90-minute workshop over several sessions.

I asked Claude Code to turn each README into a tutorial with logical sections and headings that fit the platform. It added Mermaid diagrams where architecture or data flow was easier to show visually. I reviewed every result and fixed the parts that needed judgment.

One agent was enough for this contained task. For larger features, I use a team in which a PM defines acceptance criteria before implementation. A software engineer builds the feature, a tester checks it, and the PM reviews acceptance before commit.

I track those tasks in GitHub Issues and review the changes myself. Comments and follow-up issues become the next work for the team.

The library has eleven workshops, starting with search and RAG. Others cover building agents and coding tools, including skills and reliable ingestion with Temporal. There's also a guardrails workshop and a comparison of AI coding tools using a React Snake game.

In the deployment workshops, we take a FAQ agent from a notebook to a service on Railway, then adapt it for AWS Lambda. Those are membership content, while most of the library is free after sign-up.

Basic membership includes the written deployment materials. The recordings are in Main and Premium, which also include community access and group coding sessions.

I moved AI Hero onto the site too, keeping it free as a seven-day course on building an agent. Each day's lesson now has a page and comments instead of arriving only by email.

People can track completed lessons from their profiles and return to a particular section without searching their inbox. There's also a certificate at the end, earned through a project submission and peer review.
