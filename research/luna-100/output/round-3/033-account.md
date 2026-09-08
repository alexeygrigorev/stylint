# Making certificates with Claude and Gemini

After a two-day workshop in Berlin in January, I needed certificates for the participants. I needed a design and an HTML/CSS template to generate PDFs, plus hosting so participants could download them. I wanted to see how much of that process AI could handle.

I first asked ChatGPT to create a certificate image using a reference style. The first result looked good, so I asked for a version with only the background. Claude then rebuilt the layout in HTML and CSS on top of that image.

I spent about 40 minutes reviewing the output and asking for changes to spacing, alignment, and placement. I also wanted to learn how to recreate a visual design in HTML and CSS, since that could be useful for other projects.

The repeated manual feedback made me try a different setup. Claude would generate the design, and another model would compare it with the reference and suggest corrections. I used Gemini Flash as the evaluator because Claude's image understanding wasn't reliable enough for detailed layout comparison.

Gemini produced a to-do list from the reference. When I asked Claude to implement it, Claude discarded the background we'd already made and created a simplified replacement. I could undo that change with Git.

Gemini also kept overestimating similarity. It gave results around 8 out of 10 even when they looked far from the reference, and called them close enough. That stopped the loop before the design matched. Stricter criteria didn't make the iterations converge.

After Opus 4.6 came out, I tried again with it analyzing the reference directly. It spent about three minutes identifying the background and typography details accurately.

The generated result still reused parts of earlier experiments, despite my instruction to start from scratch. That made it difficult to tell whether it could reproduce the design independently. I narrowed the task to the background, but 44 iterations produced stylistic variations instead of getting closer to the reference.

I ended up using the first certificate, made with Claude responding to my own feedback. The automated evaluator hadn't replaced that visual review.

Hosting the PDFs went much faster. DataTalks.Club already had certificate hosting for Zoomcamps, but I wanted a separate process for standalone workshops and external programs.

That normally means setting up S3 and CloudFront, configuring HTTPS, and changing DNS records. Configuration problems can turn it into several hours of work.

I gave Claude access to the S3 bucket and Cloudflare. I followed its instructions to update GoDaddy DNS records while it handled CloudFront and HTTPS, including debugging issues that appeared.

Claude completed the hosting setup in ten minutes, compared with several hours it usually took me. The required tasks were clear, with documentation for the tools involved. I could delegate much more of it than the design comparison, where I still needed to judge the result.
