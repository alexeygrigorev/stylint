# Give the coding agent a visual direction

A coding agent is good at producing a page quickly. That's also why its first design can look familiar. One-shot generation tends to use the same feature grid, the same colored card accents, and the same crowded header. On a complex page, it may put a form beside metadata or place metrics, tables, and settings at the same visual level. The code can work while the page becomes harder to read.

I use a separate visual step to show the intended hierarchy. I describe the page, its contents, and the desired hierarchy to ChatGPT, then ask for an interface mockup. I iterate on that image until the direction feels right. It isn't a pixel-perfect specification. It gives the coding agent a reference for what belongs together, which action should be prominent, and how much space the page needs.

Then I give the mockup to the coding agent and ask it to implement the layout. The result won't match every detail. That's expected, though the structure should stay close to the mockup. I look at the page and point out specific problems. For example, a button may belong under the title, or a form may be split into needless columns.

Widths and gaps can also change between screens. I make those corrections page by page instead of accepting the first plausible arrangement.

## Keep the decisions durable

After the first screens, a picture alone isn't enough because a multi-page project needs a written design system recording colors, typography, and spacing.

The design system records control styles, page widths, and placement of common elements. Codex suggested GitHub Primer for the Course Management Platform. I wrote those decisions into `design-system.md`, giving later agents a source to consult when they add a page or control.

The practical loop is straightforward. Describe the page, generate a mockup, and iterate on its direction before implementing and reviewing the result.

Keep a record of decisions that should recur. When a correction keeps coming back, add it to the design system. New pages then have both a visual example and a written boundary instead of asking the agent to improvise from scratch.

## Apply it to mobile screens

This works for mobile applications too. Pocket Shell, an Android app for managing agents from a phone, started with rough screens. I used screenshots and several ChatGPT iterations to establish a direction, then polished the details in code. The same separation helped there. The image set the direction, while implementation and review handled interactions, then code handled the details.

I still make the design decisions myself. I'm the person deciding whether a screen feels clear and whether an action is in the right place. The mockup makes that judgment visible before implementation, and the design system keeps it from disappearing after the conversation ends. Human review remains necessary because neither artifact can reveal every interaction problem.
