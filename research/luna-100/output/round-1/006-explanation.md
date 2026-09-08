# What Phone-Based Coding Changed in This Feature

The Wrapped page for the DataTalks.Club course platform came from a workflow that put an AI coding agent between an idea and a pull request. The page summarized 2025 community highlights, popular courses, top learners, and individual pages that participants could share. The implementation showed where a phone was enough and where a laptop still mattered.

The first step was describing the feature. While standing at a tram stop, Alexey dictated an issue into GitHub on his phone and assigned it to Copilot. In roughly 20 to 30 minutes, Copilot returned a pull request containing pages, code, and screenshots. The initial issue did not need to be a complete specification. It needed to communicate the page that should exist well enough for the agent to create a first version.

The rest of the work used a review loop. Alexey read the changes on his phone, left a comment, tagged Copilot, and waited for a new version. He repeated the process after reviewing the next set of changes. This worked for copy edits, layout changes, and small logic adjustments because each request could be stated in a narrow, concrete way. The pull request became the place where instructions, implementation, and review met.

The loop also exposed why review could not be skipped. Voice recognition changed “top 100” into “top 1200” in an early version. The error was easy to correct after it appeared in the diff, but the agent had no way to know which number Alexey had intended. Clear instructions helped, while inspection caught mistakes that clear instructions could not prevent.

Visual feedback made phone-based review more useful. Copilot could run the project, create UI screenshots, and attach them to the pull request. Alexey could check the page, buttons, and links without opening the project on a computer. The screenshots were incomplete because Copilot had no internet access and some styles failed to load. They were still enough to reveal obvious rendering problems.

There was a practical division of work. Copilot took about 10 to 30 minutes to produce each revision, and the cycle could run several times a day in small gaps between other tasks. Small and medium changes fit this pace. Complex features, deeper testing, and changes that might damage production still required a laptop and a more deliberate approval step.

CI/CD connected the two parts of the process. After a merge, the platform deployed the change to a development environment, where Alexey could test it visually. Production deployment was then a single GitHub button when the result looked correct. The phone was useful for turning an idea into reviewed changes; the development environment and laptop remained important when confidence had to be higher.

The lesson from this historical example is about task shape. A routine change can be expressed as a sequence of small requests and checked through diffs and screenshots. The more costly the mistake, the less suitable that lightweight loop becomes. The tool did not remove engineering judgment; it moved more of the work toward writing precise instructions, reviewing output, and deciding when another level of testing was needed.
