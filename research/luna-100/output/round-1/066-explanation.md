# A practical design loop for coding agents

One-shot interface generation is useful for a simple website, but it often produces familiar patterns: icon cards with colored borders, crowded headers, and unrelated columns for forms and metadata. A coding agent can implement those patterns consistently while still making the overall product difficult to use. A better workflow separates visual direction from implementation.

Start with the existing interface. Describe the page and what it needs to contain, then ask an image model to propose a mockup. Iterate on the mockup until the direction is acceptable. The mockup does not need to be a pixel-perfect specification. It gives the coding agent a concrete reference for hierarchy, spacing, and placement.

Next ask the coding agent to build the page from that reference. Review the result on its own. Things will move: a button may appear in the header instead of under the title, a form may split into unnecessary columns, or widths and gaps may differ between screens. Give specific corrections and repeat for the pages that need it.

As the project grows, write a design system. It should record the reference for colors, typography, spacing, control styles, page widths, and expected placement. In the Course Management Platform, GitHub Primer became the reference after Codex suggested it. The resulting `design-system.md` gave later agents a shared source instead of relying on the initial mockup or a conversation that had already ended.

The full loop looks like this:

1. Explain the page and its content.
2. Generate a visual mockup.
3. Iterate until the direction feels right.
4. Give the mockup to the coding agent.
5. Review the implementation and list concrete problems.
6. Choose or document a design system.
7. Require new pages to follow the system.
8. Add recurring corrections back into the system.

The same method works for mobile interfaces. Pocket Shell began with rough Android screens. Screenshots were redesigned through ChatGPT, then used as a direction for implementation. Details were polished in code afterward. The goal is not to outsource design judgment to the image model. It is to make that judgment visible before the coding agent fills in a page with its defaults.

This approach is especially useful for people who are not designers. A reference image helps communicate what a clean layout should feel like, while a written system keeps the decisions consistent. The agent remains responsible for the implementation, but it has fewer opportunities to invent a new layout for every page.

The result still requires review. A design system cannot decide whether a specific action belongs above or below a form, and a mockup cannot reveal every interaction problem. But the combination reduces generic output and gives corrections somewhere durable to live.
