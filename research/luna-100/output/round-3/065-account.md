# Giving an AI Redesign a Point of View

I can usually recognize a one-shot AI design before I know anything about the project. It often has a feature grid with an icon, a title, a short description, and a colored accent. An admin page pushes every action into the upper right. Forms, metrics, tables, and metadata become neighboring columns. Codex and Claude have produced similar patterns in different projects.

I'm not a designer, and I used to stay away from front-end work. The DataTalks.Club website I built in 2020 used Bootstrap because I already knew it. It had a headline, a signup form, illustrations, and generous empty space.

The Course Management Platform also began with Bootstrap. It handled homework and project submissions, leaderboards, and course pages, so function came first.

In 2024, a participant opened an issue asking for a Tailwind migration. I didn't have time then. Later redesign attempts also failed to give me a direction I liked.

In 2026, I finally gave the issue to Codex, whose first redesign looked like many other AI websites. The implementation needed a reference that expressed what I wanted before the agent filled in the details.

GPT Image 2 supplied that reference. I gave ChatGPT screenshots of the existing platform and requested two mockups: one desktop and one mobile. After several iterations, the visual direction felt right.

I gave the mockups to Codex and asked it to implement them. The result wasn't identical to the images, but it was close enough to refine page by page.

I saw the new pages drift as buttons moved, spacing changed, and widths differed. The controls no longer matched one another. I asked Codex to find a design system that fit the project. It suggested GitHub Primer, and we recorded the choice in `design-system.md`.

The mockup established direction, while the design system gave later sessions rules for applying it.

The working loop became concrete:

- describe a page
- generate a mockup
- revise the visual direction
- ask the coding agent to implement it
- review the result
- record recurring rules

When a page needs correction, the useful part of that correction belongs in the system. A future page can then use the decision without relying on a conversation that has ended.

I used the same method for Pocket Shell, an Android app for managing agents. I photographed its rough project tree and conversation screens. I asked ChatGPT for redesigns and used those images as targets while polishing the code. The current screens are better than the first version, although the application remains in progress.

This process hasn't turned me into a designer. It gives me a concrete way to express a preference before implementation and keep that preference available afterward. A mockup lets me react to a screen before spending time building every detail. A written system keeps the decision from disappearing when the next page begins.
