# Shipping a feature from a tram stop

Last week I merged a new feature into the DataTalks.Club course platform, where we manage homework and projects. It gives learners a Spotify Wrapped-style account of their year across our Zoomcamps. There are community highlights and popular courses, along with top learners and a personal page each participant can share.

I did most of the work from my phone during trips to pick up my kid. The idea came while I was waiting at a tram stop. I wanted a page where people could see what they had achieved throughout 2025.

I opened GitHub and dictated a rough issue description, then assigned it to Copilot. About 20 to 30 minutes later, it opened a PR with working pages. I could read the code and look at screenshots without opening my laptop.

From there, I went through the changes on my phone and left comments. I tagged Copilot with specific updates and waited for it to push another version. After reading that version, I could leave another comment if something still needed changing.

That worked for adjusting copy and layout, as well as minor changes to the logic. Each update took roughly 10 to 30 minutes, so I could return to the PR during another gap in the day. I went through this cycle several times while doing other things.

My original issue had a mistake from voice recognition. I had said "top 100", but the transcription said "top 1200", and that number appeared in an early version of the PR. Once I saw it during review, I left a comment and assigned Copilot to fix it.

Copilot could also run the project and attach screenshots directly to the PR. Those let me look at how the page rendered, including its buttons and links. Some styles failed to load because Copilot had no internet access, but I could still see whether anything was obviously broken.

For this kind of small or medium-sized change, I can handle much of the work in short sessions from my phone. I spend that time writing instructions and reviewing what Copilot produces, including correcting mistakes like the number I dictated.

I still sit down at my laptop for complex changes and final approval when something could break production. Larger features need deeper testing than I can do through this review loop.

Once I merge the PR, CI/CD deploys it to our development environment. I test the result visually there before using the production deployment button in GitHub.
