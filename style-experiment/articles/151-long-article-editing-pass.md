# Editing a Long Article in Four Passes

Last winter I wrote a 6,400-word guide to deployment checks and couldn't get it published. The argument was complete, but every reading session found another problem. I fixed a paragraph about health probes, noticed a missing cost number, then rewrote two sentences and lost the thread. This went on for three evenings.

I used that frustrating project to develop a stricter editing method. This synthetic style exercise uses its structure, but the project, dates and measurements are fictional. I now edit long drafts in four passes, and I keep each pass focused on one layer of the piece.

In this post, I'll share:

- why editing while writing failed
- how I separate structure from evidence
- what the sentence pass looks for
- how I handle publication details last
- what I learned from a 6,400-word draft

## The First Editing Workflow

I compared three deployment workflows for small machine learning services in the guide. It had a running example, eleven command blocks and 42 links. The first version also had a conclusion that promised more than the body delivered.

I edited it the way I used to edit emails: read from the top, change whatever looked wrong, continue. That works for 800 words, but my attention ran out on the longer draft. I never knew whether a change in section 7 had broken a claim made in section 2.

The obvious solution was to give the draft to Claude and ask it to improve the article. It returned a fluent version with a smoother introduction. It also removed an important caveat about DNS propagation and introduced a pricing number it couldn't know. The draft sounded better and knew less.

The rule I took from that attempt: editing is a review job, and a reviewer needs a limited question for each pass.

## Pass 1: Structure

The first pass ignores sentences. I export the title, every heading and the first sentence of each section into a text file. For that article, the outline filled one screen and exposed the problem in minutes.

The outline exposed the mismatch immediately: I had promised more stages than the body contained. Rollback appeared twice, and evidence sat before the system description. I moved evidence after the component overview, moved rollback after failure handling and merged the duplicate sections.

I now use this checklist for the structure pass:

- every roadmap item has a matching section
- sections appear in the order the reader needs them
- no two sections answer the same question
- the closing claim follows from the evidence

I make these changes directly in the article and don't rewrite paragraphs yet. If a section has no clear first sentence, I mark it for restructuring and move on.

## Pass 2: Evidence

In the second pass, I walk through claims and list every number, version, command and factual assertion in a spreadsheet. That draft produced 63 rows. Each row had the claim, the supporting source and a status.

The process sounds bureaucratic until the errors appear. I had written "about $20 per month" for a small server, based on a 2024 price. The fictional exercise version uses $27, but I had still stored the old number in the draft from memory. Two commands had flags from an older CLI, and one benchmark used a warm cache while the text implied a cold start.

For a technical claim, I run the command or open the documentation. For an experience claim, I check whether the draft says what actually happened. I replace "typically takes five minutes" with either a measured range or a plain statement that I haven't measured it.

At the end of this pass, I mark unsupported claims for deletion. On the long guide, 11 of the 63 claims failed. Six had sources I could check, three needed new tests and two turned out to be repetition.

## Pass 3: Sentences

Only now do I edit language. The structure holds, I've attached the evidence to spreadsheet rows, and I read the draft aloud one section at a time.

The sentence pass has three jobs:

- keep one term for each thing
- reduce paragraphs to one to three sentences
- remove sentences that announce an idea without adding information

In the draft, "service", "app" and "application" described the same program. I settled on "service" and used it for every reference to the deployed program.

I don't aim for polished writing because I want a direct practitioner report. "The cache made deployment feel faster" becomes "The cache reduced deployment time from 96 seconds to 38 seconds".

Long articles also hide repeated explanations. I had added the cold-start explanation in three separate writing sessions, so I kept the fullest version and linked the later mentions back to it.

## Pass 4: Publication Details

The final pass handles details at the article's boundary. I start with titles: I write five candidates and check whether each one describes the actual promise. For that guide, "Three Ways to Deploy Small Models" beat a cleverer title because it named the comparison.

Then I check the opening, the roadmap and the close. In the opening, I say what problem I hit, and the roadmap has to match the final headings. In the close, I state what still doesn't work and what I'd try next. Finally, I check links, image captions, code language tags and alt text.

The checklist is short:

- the title makes a promise the body keeps
- the first paragraph puts the reader in the concrete situation
- every roadmap bullet maps to a heading
- every code block runs or explains why it doesn't
- the final section names a limitation

Publication details take one to two hours on a long draft. Doing them earlier wastes time, because a structural change can make the title or introduction obsolete.

## Lessons From The Draft

The four-pass method doesn't make writing fast. I still needed four working sessions after I changed the method. But the sessions became predictable, and I could stop without holding the whole article in my head.

The evidence pass surprised me most. It caught errors that fluent wording had hidden, especially in sections I had revised often. A sentence can sound settled long after its claim has gone stale.

I now use the same method for anything above 2,500 words. For shorter posts, I usually combine structure and evidence, then keep sentences and publication details separate. The rule matters more than the exact split: I don't ask one pass to fix the argument, the facts and the wording.

I'll describe the evidence spreadsheet in more detail in a future newsletter. If you want to follow along, don't forget to subscribe.
