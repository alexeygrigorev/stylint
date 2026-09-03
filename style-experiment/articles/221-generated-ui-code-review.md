# Reviewing Generated UI Code Against a Mockup

This synthetic style exercise follows a fictional dashboard project with invented details. Every name, count, and timeline below is fictional, and none of it describes real events. In April a coding agent built a dashboard page from a mockup with nine screens.

The mockup lived in Figma and covered a course admin dashboard with charts, tables, and filters. I asked Claude Code to generate the page in React with TypeScript. It returned 11 files and 1,400 lines in about six minutes.

I spent three evenings reviewing those 11 files against the nine screens. The review found 34 issues, and only six of them were visible at first glance.

In this post, I'll share:

- what the first generated pass got right
- where the layout drifted from the mockup
- which states and accessibility gaps I fixed
- how design tokens cleaned up the styles
- what the review pass taught me

## First Pass From the Coding Agent

The agent did the boring parts well. It set up routing, typed the API responses, and built the table with sorting and pagination. All 11 files compiled on the first try, and the dev server rendered a recognizable dashboard.

I compared each screen side by side with the mockup at 1440 pixels wide. Six of nine screens matched closely enough that I moved on within minutes. The remaining three screens held most of the 34 issues.

The review habit that paid off was screenshotting every screen before reading code. I saved nine PNG files in `reviews/dashboard-v1/` and marked each gap with a red box. It's simple admin, and it kept the review honest when the code looked convincing.

## Layout Gaps and Missing States

Layout drift clustered in spacing and alignment rather than in big structural mistakes. The sidebar was 16 pixels too narrow, card padding used three different values, and the filter row wrapped at widths where the mockup stays flat. Twelve of the 34 issues were spacing alone.

Missing states were the bigger gap. The generated page handled the happy path with data, and it ignored everything else.

I collected the five absent states in a list for the agent:

- empty table when a new course has no students
- loading skeleton for the charts row
- error banner when the API times out
- filter combination that returns zero rows
- mobile layout under 768 pixels wide

I sent the list back to the agent with one screen per message. It generated all five states in a second pass of 300 lines. I didn't accept that pass blindly, since four of the five states reused padding values from the wrong card.

The rule I took from that evening: generated code covers the path in the prompt, and every other path needs an explicit request.

## Accessibility Fixes Before Merging

The mockup specified most of the accessibility gaps, and I found eight of them.

The eight gaps grouped into three areas for the fix pass:

- missing focus rings on filter buttons
- chart legends with no text alternative
- two color pairs failing contrast at small sizes

I measured contrast with the browser dev tools, and the worst pair scored 2.8 to 1.

One fix deserves a longer note. The agent had built the date filter as a `div` with a click handler, so keyboard users couldn't reach it. I replaced it with a native `select` element, which brought keyboard support and mobile pickers for free. There's a habit here - the habit of building clickable divs, and native elements avoid it.

I reran the checks after the fixes with axe DevTools. The page went from 14 flagged items to zero, and the second run took eleven minutes.

## Design Tokens and Cleanup

Values hardcoded across the 11 files made every tweak painful. I counted 23 distinct hex colors and nine different spacing values. The mockup used eight colors and a four-point spacing scale.

I introduced a token file and connected every component to it:

```tsx
export const tokens = {
  colorText: "#1a1d21",
  colorMuted: "#5b6470",
  spaceCard: 16,
  radiusCard: 8,
};
```

I placed the file at `src/styles/tokens.ts` with colors, spacing, and radii inside. I replaced all 23 hex values with eight token references across two evenings. I don't merge generated styles without this step now, since hardcoded values multiply with every later prompt.

The cleanup removed 180 lines of duplicated CSS in the process. Total line count dropped from 1,700 after the second pass to 1,520. I kept the diff in the pull request under 400 lines per commit so reviewers could follow it.

## Lessons From the Review Pass

The review took nine hours against six minutes of generation, and I consider that ratio healthy. Generation drafts the page, and review makes it shippable for real students. None of the 34 issues would have blocked a demo, and most would have annoyed users within a week.

The work taught me a narrower lesson than never trust generated code. Trust it for scaffolding, and verify it against the mockup screen by screen. My next dashboard starts with tokens and states in the prompt.

I'll write about the prompt template I now reuse in a future post with real numbers. If you want to follow along, don't forget to subscribe.
