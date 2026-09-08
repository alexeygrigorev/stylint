# Building AI Shipping Labs

Valeriia and I started AI Shipping Labs with a simple product idea. We wanted to test whether people wanted a paid community for practitioners who learn AI by building projects. The first version followed the approach I used with DataTalks.Club. We started with the smallest useful website, measured interest, and expanded only after people showed up.

Valeriia built the first platform version with v0 and Cursor. She began with an idea for a paid, invite-oriented community, researched activities and competitors, and used ChatGPT to organize possible options.

Then she designed three subscription tiers. The first was for self-sufficient learners, while the second added the community and its activities. The third included access to my courses and guaranteed feedback from me on resumes and personal platforms.

For the interface, Valeriia chose v0 because she already knew the tool and had worked with Next.js before. One prompt generated a useful starting point. v0 suggested sections such as an About page, content previews, testimonials, and an application flow. She selected what made sense, added my bio, used testimonials from the AI Engineering Buildcamp, and connected the project to GitHub before continuing in Cursor.

The site then grew through practical content work. Valeriia organized it into Project Ideas, Event Recordings, Curated Links, and Blog. Moving newsletter posts was indirect because Substack didn't provide a convenient import API.

She copied each post into a Google Doc and ran Python scripts from the DataTalks.Club repository. The generated Markdown files still needed manual editing, but the scripts handled most repetitive work. The Curated Links section became a filterable grid, and Project Ideas came from Demo Day projects, social posts, and newsletter editorials.

After that, I added Stripe so people could buy subscriptions and we could receive notifications. Valeriia also turned my research about AI Engineer job descriptions, requirements, and interviews into an AI Engineer Learning Path and an interview-questions page. The original site started on GitHub Pages and later moved to AWS S3. It now has a subdomain for the Django version, which is still a work in progress.

The Django platform came from the limits of existing products. Substack didn't support the tier structure. Ghost didn't cover courses, events, and community features. Maven was strong for courses but lacked programmatic student registration and other workflow pieces.

Since no single platform covered the full system, I used an agent-team process. Its roles were PM, SWE, Tester, and On-Call Engineer.

I dictated features into a Telegram bot. Claude Code turned them into 15 specification files and then into GitHub Issues. The first task breakdown was too granular and lacked acceptance criteria, so I revised the format and added a `human` tag for manual checks.

After one evening of setup, the agents completed 41 of 46 tasks overnight. Twelve hours later, the count was 51 of 56 because the backlog grew as the PM decomposed more work.

The first login showed Gmail and GitHub OAuth were working, along with Zoom, Slack, and Stripe integrations. They still required API keys, configuration, and manual testing. The agents also overused Django admin and left features without clear UI locations.

They missed a user dashboard as well. The platform was working after the first 24 hours, but the following weeks went into UX and production preparation. The Django version is running at `prod.aishippinglabs.com`, while the public site remains Valeriia's Next.js version until the new platform is ready.
