# Reviewing Copilot changes from my phone

I use the DataTalks.Club course platform to manage homework and projects. For the end of 2025, I wanted a page showing what people had achieved across our Zoomcamps. We added a Spotify Wrapped-style page with community highlights and popular courses. It also showed top learners and gave each participant a page they could share.

Most of the work on this feature happened while I was travelling to pick up my kid. I could describe a change on my phone, let Copilot work on it, and review the result when I had another few minutes.

I started at a tram stop by dictating a rough GitHub issue. I assigned it to Copilot, which opened a pull request about 20 to 30 minutes later. The PR included working pages and screenshots alongside the code.

Once there's a PR, I can scroll through the changes in GitHub and leave a comment about what needs fixing. I tag Copilot and ask for the update, then review the next version when it's ready. I repeat this if something still needs work.

For this feature, I used that process for copy changes and layout adjustments, as well as small changes to the logic. Each update took about 10 to 30 minutes. I could come back to the PR several times during the day without staying at my computer while Copilot worked.

I still need to read what it produces. In the original issue I said "top 100", but voice recognition transcribed it as "top 1200". Copilot used that number in an early version, so I left a correction and assigned the work again.

Screenshots help with the visual review because reading a diff on a phone doesn't show me how the page looks. Copilot can run the project and attach screenshots to the PR. I use them to check the rendering, including the buttons and links.

Some styles don't load because Copilot has no internet access. The screenshots are incomplete, but I can still spot obvious problems before opening the project on my laptop.

For small and medium-sized changes, this lets me get work done in gaps between other tasks. I spend those gaps describing what I want and reviewing the changes, including mistakes in my own dictated instructions.

I still use my laptop for larger features and deeper testing. That includes final approval of complex changes or anything that could break production.

After I merge a PR, CI/CD deploys it to our development environment. I can then test the pages visually, and if everything looks right, deploy to production with a button in GitHub.
