# How a community platform grew from an MVP

AI Shipping Labs started with a small question: would people join a community for practitioners who want to learn AI by building? The first answer did not require a complete platform. Valeriia built a Next.js site with v0 and Cursor, and the site offered only the essential paths: sign up for updates or buy a subscription. Analytics showed whether people were interested.

This was the same approach I used with DataTalks.Club. Its first website had only an email form. A minimum viable product can still look polished, especially when AI tools help produce the interface, but the functionality should remain narrow enough to test the idea.

Valeriia began by collecting possible activities and shaping subscription tiers. The tiers moved from written tutorials for self-sufficient learners, to community access and activities, to a more exclusive option with course access and feedback. After reviewing the document together, she used v0 to generate a landing page. Its suggestions included an author section, content previews, testimonials, an explanation of the process, and an application section. The useful suggestions were selected and the rest were omitted.

The site content came from several existing sources. Newsletter material became blog content. Project ideas came from capstones, social posts, and project write-ups. Event recordings and curated links became their own sections. Google Docs were converted into Markdown with Python scripts, although the generated files still needed manual editing. Cursor helped adapt the scripts and build a resource grid with filters.

Once the first site existed, Stripe and hosting were added. The site moved from GitHub Pages to S3, and Valeriia turned research about AI Engineer roles into a learning path and interview questions page. The Django version of the platform was developed later because Substack, Ghost, and Maven each covered only part of the required workflow.

The Django platform used an agent team: Product Manager, Software Engineer, Tester, and On-Call Engineer. I dictated features into Telegram, Claude Code turned them into 15 specification files, and those specifications became GitHub Issues. The first tasks were too granular and lacked acceptance criteria, so I revised the format and added a human tag for manual checks.

The team process was useful because it separated a working implementation from a finished experience. A task could be completed in code while still needing a person to test an external service or decide where a feature belonged in the interface.

After one evening of setup, 41 of 46 tasks were complete the next morning. OAuth for Gmail and GitHub, Zoom, Slack, and Stripe were working, but the platform still required API keys and manual testing. Some interfaces relied too heavily on Django admin, and the user dashboard was missing. The first day produced a working system, not a finished product. The remaining work was polishing the user experience and preparing the Django version to replace the Next.js site.
