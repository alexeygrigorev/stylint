# Building the community site in stages

When I started DataTalks.Club, the website had an email sign-up form. I wanted to see whether people would join before building more. Valeriia and I followed that approach with AI Shipping Labs, although the first site looked more complete.

It had several pages, but the functionality was limited: visitors could subscribe to updates or buy a subscription. We added analytics to see how people used it. Once we saw interest, we began expanding the platform.

## Start with the content and subscription tiers

Valeriia collected ideas for community activities and used ChatGPT to help organize them. After removing irrelevant suggestions, she described three subscription tiers. We reviewed the activities and tiers together before she built the interface.

She chose v0 because she'd used it before and already knew Next.js. Her initial prompt included the tier descriptions. She then reviewed its suggestions for additional sections and added my bio alongside Buildcamp testimonials. A newsletter sign-up form served as the waitlist.

Valeriia connected the generated project to GitHub and continued editing locally with Cursor. For the blog, she adapted scripts I'd written for DataTalks.Club. She copied newsletters into Google Docs, then used the scripts to create Markdown files with image links. The result still needed manual editing.

I took over the hosting and Stripe integration after that version was ready. Valeriia also used my research on AI engineering jobs to create a learning path and interview-question page.

## Describe the work before giving it to agents

We considered existing platforms before building our own, but none covered the whole workflow. Substack didn't support our tier structure, and Ghost lacked the course and community features we needed. Maven had no API for registering students programmatically.

I chose Django for the next version because I've known it since 2010. I wanted to be able to work on the code myself if something went wrong.

I dictated features into my Telegram bot, and Valeriia could contribute ideas there too. Claude Code converted the list into 15 specification files. After reviewing them, I asked it to create GitHub Issues for implementation.

The first tasks were too granular and lacked acceptance criteria. I revised the format until each issue described a clear scope and included an acceptance checklist. Anything needing manual verification received a `human` tag.

## Check the integrations yourself

An orchestrator coordinated the Product Manager, Software Engineer, Tester and On-Call Engineer agents. Setting up the process took an evening. By the next morning, 41 of 46 tasks were done. After 12 hours, it was 51 of 56 because the backlog had grown.

Those counts didn't mean the platform was finished. I still had to provide API keys and configure the integrations. I checked that Zoom meetings were created, payments went through Stripe, and Slack invitations arrived.

The agents also relied too much on Django admin. Some features had no clear place in the interface, and I had to ask explicitly for a user dashboard. The following weeks went into those usability problems.

At the time of the article, the Next.js site was still the main website. The Django version was running on a separate subdomain while I prepared it for production. Switching the domains was a later step.
