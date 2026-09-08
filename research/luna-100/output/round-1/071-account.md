# How I Choose a Portfolio Project

When I prepare plans for AI Shipping Labs members, one question comes up often: what should I build for my portfolio? There are many possible answers, which makes choosing one harder. I use a domain first, then work backwards from the problems companies in that domain are trying to solve.

A portfolio is useful because hiring managers often inspect GitHub, but that is only one reason to build one. Public work can lead to collaborations, freelance conversations, and other opportunities. Personal utilities are valuable evidence that you notice problems, although one private tool may not say much about the role you want. A take-home assignment, a hackathon contribution, community project, or open-source change can also become portfolio material when its origin is explained.

For a role-targeted project, I would not begin by choosing a fashionable framework. I would choose a domain and list five to ten companies that hire for the role. Current job openings help, but engineering blogs, case studies, and product pages are useful too. The goal is to understand what teams build and what problems recur across several companies.

Job descriptions reveal responsibilities and team context. Engineering posts show the problems teams met in practice. I collect these materials separately, then extract problems rather than copying technology lists. For example, a post about an AI conversation partner may point to dialogue quality, feedback, grounding, evaluation, or latency. Those are project directions. A stack mentioned in the post is evidence for a later technology choice.

The next step is to group problems that appear across companies. A problem found in one job description may be too narrow, or it may be tied to one team’s temporary situation. A shared theme is more likely to produce a project that makes sense in several interviews. Once I have that list, I create several candidates. Each candidate should name the user, the input, the output, and why it fits the domain.

Only then do I choose technologies. I ask which tools the target companies actually use and map each proposed technology back to a source. The final stack is still my decision. I do not try to learn every tool mentioned in the research, because one project becomes hard to finish when it contains too many new things.

I also plan evaluation and monitoring from the beginning. A system that generates an answer without checking whether it is correct is incomplete. The project should have an evaluation harness, logs or monitoring, tests for important behavior, and a README that explains the result quickly. A hiring manager should be able to see what the project does, who uses it, what goes in, what comes out, how it is evaluated, and why the stack fits.

This process is slower than applying everywhere and attaching a random project to each application, but it gives the work a direction. A second project can vary the model provider or technical approach while staying in the same domain. Over time, the portfolio shows both range and a reason for the choices. That is much easier to discuss than a collection of unrelated demos.
