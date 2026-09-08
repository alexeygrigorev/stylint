# What AI Could Automate in a Certificate Workflow

In January, I ran a two-day workshop in Berlin and needed to give certificates to everyone who attended. The work included designing a certificate, converting it to HTML and CSS, generating PDFs, and hosting the files for download. I used the project to see which parts AI tools could automate reliably.

The design work was the difficult part. I first asked ChatGPT to create a certificate image inspired by a reference, then asked it for a background-only version. Claude used HTML and CSS to recreate the layout on top of that background. The result looked promising, but I spent about 40 minutes giving feedback on spacing, alignment, and element placement. Claude generated code, I reviewed the result, and the loop repeated until the layout looked close enough.

Because manual feedback was the bottleneck, I tried a creator-and-judge setup. One model generated or changed the design, while another evaluated its similarity to the reference. Claude’s image understanding was not reliable enough for detailed comparison, so I used Gemini Flash as the judge. Gemini analyzed borders, colors, textures, typography, and layout and produced a to-do list for Claude.

The loop did not converge. Claude discarded an earlier background and generated a simplified version, though I could revert that with Git. Gemini also rated results around 8 out of 10 when they were visibly far from the reference, calling them close enough. Stricter criteria did not solve the problem. When I tried Claude Opus 4.6, its analysis of the reference was detailed and accurate, but it reused elements from earlier experiments despite being asked to start from scratch. A background-only run took 44 iterations and still produced stylistic variations instead of converging.

I eventually used the certificate from the first approach, where Claude iterated on my own feedback. Design automation needed more manual control than I expected. Code generation usually gave me a useful first draft from a plan, but a visual comparison loop could not judge small differences consistently enough.

Hosting the finished certificates was different. DataTalks.Club already had a certificate pipeline for its courses, but it was tied to Zoomcamps. For standalone workshops and external programs, I wanted a separate system. Normally, certificate hosting takes several hours because it involves S3, CloudFront, HTTPS, DNS records, and configuration debugging.

This time, I gave Claude Code access to the S3 bucket and Cloudflare, followed its instructions for GoDaddy DNS changes, and let it configure CloudFront and HTTPS. When an issue appeared, Claude diagnosed and fixed it. The setup took about ten minutes instead of several hours. Storage, HTTPS, and hosting had clearer constraints and documentation than visual design, so automation was much more reliable.

The contrast was the useful result. AI did not automate the entire certificate project equally. It handled infrastructure as a defined engineering workflow, while matching a visual reference still needed a person to judge the output.
