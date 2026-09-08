# Making an AI redesign less generic

I can usually recognize a one-shot AI design immediately. The feature grid has cards with an icon, title, description, and colored accent. An admin page puts every action in the top-right corner. Forms, metrics, tables, and metadata become equal columns. These patterns appear across projects made with both Codex and Claude.

I am not a designer, and I used to avoid front-end work. The DataTalks.Club website I built in 2020 used Bootstrap because I knew it. It had a headline, signup form, illustrations, and empty space. The Course Management Platform also started with Bootstrap. It replaced Google Forms and spreadsheets with homework and project submissions, leaderboards, and course pages. Function mattered more than appearance.

In 2024 a participant opened an issue to migrate the platform to Tailwind. I did not have time, and later redesign attempts did not work for me. In 2026 I finally gave the issue to Codex. The first redesign was a one-shot result that looked like many other AI websites, so I needed a different way to set direction.

GPT Image 2 gave me that direction. I supplied screenshots of the existing platform and asked ChatGPT for redesigned desktop and mobile mockups. After a few iterations the visual direction felt right. I handed the mockups to Codex and asked it to implement them. The result was not identical, but it was close enough to refine page by page.

New pages drifted from the mockups. Buttons moved, spacing changed, page widths differed, and the same controls had inconsistent styles. I asked Codex to find a design system that matched the project. It suggested GitHub Primer, and we documented the result in `design-system.md`. A mockup gave the visual direction; the design system gave agents rules to apply when adding pages.

The working loop became simple: describe the page, generate a mockup, iterate on the direction, ask the coding agent to implement it, review the result, and record the design rules. When something looks wrong, the correction belongs in the system instead of only in the current conversation.

I used the same approach for Pocket Shell, an Android app for managing agents. I photographed the rough project tree and conversation screens, asked ChatGPT for redesigns, and used the mockups as a target while polishing the code. The current screens are better than the first version, though the app is still in progress.

This process does not make me a designer. It gives me a way to express a preference before implementation and keep that preference consistent afterward. The important step is the reference that survives the first page.

The mockup is therefore a conversation tool. It lets me react to a concrete screen before spending time implementing every detail, and the written system helps carry those decisions to the next screen.
