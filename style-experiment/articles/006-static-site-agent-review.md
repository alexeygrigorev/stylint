# Reviewing an Agent-Edited Static Site

I wrote this synthetic style exercise as a build log. The project, dates and measurements are fictional. On 2 May I asked a coding agent to add a pricing page to a static site. It created the route, wrote the copy, updated the navigation and left one broken link to `#pricing`.

I passed the page because it existed, and I failed it because I hadn't defined the review path. Since then, I use a five-part checklist before publishing any agent-edited site. The latest review took 16 minutes and caught four issues.

I ran this review on a 14-page Astro project with no client-side JavaScript except one search form. That small scope makes review manageable, but it doesn't remove the need for a route-by-route pass.

In this post, I'll share:

- what the agent changed
- how I look at routes
- how I check copy and links
- how I review metadata and mobile layout
- what I now require before merge

## Changes The Agent Made

The task looked narrow: add a pricing page and connect it to the main navigation. The agent changed nine files. It added `src/pages/pricing.astro`, updated two navigation components and edited the sitemap configuration.

It also rewrote four sentences on the home page, and I hadn't asked for that. The rewrite was defensible because the old sentence mentioned pricing, but it was outside the task boundary. This became the first review rule: compare the changed files with the request, then look at the requested feature.

The agent's summary said all tests passed. The project had only two tests, and neither rendered a page. Its statement was technically true and practically insufficient.

## Routes And Redirects

I start with routes because they define the public surface. The site map has 14 stable URLs, so I list the generated routes in the review note and compare them with the previous build. I expect the pricing page to add one URL and change nothing else.

The build command is ordinary:

```bash
npm run build
```

After the build, I open every changed route and one neighboring route. For the pricing change, I checked `/pricing`, `/`, `/services` and `/contact`. In the neighboring pages, I found that the footer now linked to pricing twice.

The first broken route involved an anchor. The navigation linked to `/pricing#faq`, but the pricing page had no `id="faq"`. Clicking the link left the reader on the pricing top. I added the identifier and moved the section heading to match the navigation.

## Copy And Links

Next I read every changed sentence out loud. This is slower than skimming, and it catches vague claims. The generated pricing page promised "enterprise support", but the site had no support tier at any price.

I use three checks for copy:

- every claim has a matching plan or service
- pricing amounts match the data in `src/data/plans.json`
- no page invents a testimonial, customer name or metric

The agent had invented a sentence that said teams "usually deploy in under a day". I replaced it with the actual deployment range from the fictional project notes: 2 to 6 hours, depending on DNS propagation.

Then I run a link checker, and the project uses `lychee`, a local link-checking tool. It found 11 internal links and 3 external links on the changed pages. One internal anchor failed, and one external documentation URL redirected to a new path.

## Metadata And Accessibility

Each page needs a title, description and canonical URL. The agent generated a title, but the description repeated the title. I wrote a 148-character description that named the three plans and the monthly billing option.

I also check the social preview with the local development server. The generated markup referenced an image named `default.png`, which showed a code editor and didn't match the topic. I replaced it with a simple image containing the three plan names.

Accessibility checks are manual at this scale. I tab through the pricing page, confirm that headings form a sensible order and test the monthly-yearly toggle with a keyboard. The first version used a button without an accessible name, so screen readers announced only "toggle".

## Mobile Layout

The desktop preview usually survives agent edits, but mobile is where details break. I test at 360 by 800 pixels and at 768 by 1,024 pixels, because those sizes cover the smallest common phone and a tablet-width breakpoint.

The pricing table had three problems at 360 pixels:

- plan columns were 118 pixels wide
- feature labels wrapped into five lines
- the yearly price overlapped the monthly price

I replaced the table with a stacked layout under 640 pixels. Each plan becomes a card with the same order of fields. That change added 42 lines of CSS, and it preserved the table on larger screens.

I also zoom the browser to 200% and test one complete purchase path. The call-to-action button remained reachable, but the surrounding text became clipped. A container query fixed the spacing without changing the page structure.

## Before Merge

The final review now ends with a checklist in the pull request. It covers changed routes, copy claims, links and metadata, plus keyboard access and the two mobile widths. The reviewer can mark each item as checked or request a change.

I keep the checklist in `REVIEW.md`, next to the deployment instructions. The agent reads it when I ask for a pre-review, and I still run it myself. The tool can prepare the evidence, but the person decides what ships.

On the latest pricing update, the agent prepared screenshots for four widths and a list of changed links. I found one mismatch between the plan JSON and the rendered annual price, and the fix took three minutes.

The process isn't fully automated because publication is a human decision. I want the agent to make the review easy. I don't want it to approve its own work.

I'll write next about the image checklist for generated landing pages. If you want to follow along, don't forget to subscribe.
