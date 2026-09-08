# The Wrapped Feature I Built Between Tram Stops

Last week, I merged a pull request into the DataTalks.Club course management platform, the system we use for homework and projects. The feature was a Spotify Wrapped-style page for 2025. It showed community highlights, popular courses, top learners, and a separate shareable Wrapped page for each participant. Most of the work happened on my smartphone while I was commuting to pick up my kid.

The idea began while I was standing at a tram stop. I wanted one page that summarized what learners had achieved across the Zoomcamps during the year. I opened GitHub on my phone, dictated a rough issue with voice input, and assigned it to Copilot. After roughly 20 to 30 minutes, Copilot opened a pull request containing working pages, code, and screenshots.

From there, I treated the pull request as a conversation. I scrolled through the changes on the phone, left comments, tagged Copilot, and described a specific update. When Copilot pushed another version, I reviewed it again. This loop was practical for copy changes, layout adjustments, and small pieces of logic. I could return to it several times a day in the short gaps between other tasks.

Voice input introduced errors, so review was still necessary. In the original issue, I said “top 100,” and speech recognition turned it into “top 1200.” That number appeared in an early version of the PR. I caught it while reviewing the result, commented on the problem, and asked Copilot to correct it. The phone made it possible to start the change quickly, but it did not remove the need to read what had been produced.

Copilot could also run the project, generate UI screenshots, and attach them to the pull request. That gave me a way to check the rendered page and see whether buttons and links behaved as expected without opening the project locally. The screenshots were imperfect because Copilot had no internet access and some styles did not load. They were still useful for confirming that nothing was obviously broken.

There was a clear boundary to this workflow. Each comment took about 10 to 30 minutes to produce a new version, and the review cycle worked well for small and medium-sized changes. I did not use my phone for final approval of complex work, deeper testing, or changes that could break production. For those decisions, I used a laptop. After merging, CI/CD deployed the change to a development environment, where I could test it visually. If the result looked good, production deployment was a single button in GitHub.

The feature was a useful test of where the work had moved. The implementation happened through instructions, review, and corrections more often than through typing code directly. For routine changes, that was enough to close a pull request from a tram stop. The laptop remained necessary when the cost of being wrong was higher, but it was no longer necessary for every step.
