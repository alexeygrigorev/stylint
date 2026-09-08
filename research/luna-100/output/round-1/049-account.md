# Building AI Shipping Labs in stages

Valeriia and I had announced AI Shipping Labs in the previous newsletter. After the live launch stream, we wanted to explain how the platform came together and why it had two versions. The story begins with a simple Next.js website and continues with a Django platform built through an agent team.

The first decision was to keep the product small. When I launched DataTalks.Club, the website had only an email form. We followed the same idea here. The first AI Shipping Labs site had a polished design and several pages, but its functionality was limited to measuring interest through subscriptions and update sign-ups. Analytics gave us a way to see whether people wanted the community before building every feature.

Valeriia planned the activities and tiers. The entry tier offered written deep dives and tutorials. The next tier added accountability circles, group learning, calls, workshops, and webinars. The most exclusive tier included courses and guaranteed feedback from me. She organized the ideas with ChatGPT, removed irrelevant suggestions, and reviewed the descriptions with me before building the interface.

She used v0 because she knew the tool and had worked with Next.js. A single prompt produced a useful first application. v0 suggested pages such as a biography, testimonials, content previews, and an application flow. We kept the parts that matched the launch and used a newsletter sign-up as a waitlist. The generated code went into GitHub and then into Cursor for further work.

The site reused our existing material. Newsletter editorials became blog posts, event recordings were collected, and project ideas came from course capstones and public project discussions. A set of Python scripts converted Google Docs into Markdown with images, although the output still needed cleanup. We also added a filtered grid of tools, models, courses, and other resources.

I later added Stripe and moved hosting from GitHub Pages to AWS S3. Valeriia built an AI Engineer Learning Path and an interview questions page from research I had collected about job descriptions and requirements. For the larger platform, we evaluated Substack, Ghost, and Maven, but each missed important pieces such as tiered access, community operations, course management, or programmatic registration.

The Django implementation used the agent-team process I had been testing. Telegram notes became specifications, then issues with acceptance criteria. The first decomposition failed because tasks were too small and lacked checks, so I corrected the format. Overnight the agents completed 41 of 46 tasks, and later the expanded backlog reached 51 of 56. OAuth, Zoom, Slack, and Stripe integrations worked, but they still needed keys and manual verification.

That first day produced a working platform and also showed its limits. The agents overused Django admin, left some features without a clear interface, and omitted a dashboard. We spent the following weeks improving the UX. The Next.js site remained public while the Django version continued toward production.
