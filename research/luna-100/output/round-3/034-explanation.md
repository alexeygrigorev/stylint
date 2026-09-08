# Comparing automated design feedback with hosting work

For workshop certificates, I needed both a design and a way to distribute the finished PDFs. I tried automating the visual work with Claude and Gemini, then used Claude Code for hosting. The design kept needing my feedback, while the hosting setup took ten minutes.

The first design attempt used a certificate image from ChatGPT, followed by a background-only version. Claude recreated the layout with HTML and CSS. I reviewed the output and requested changes to spacing, alignment, and placement for about 40 minutes.

I wanted to automate that feedback, so I tried using one model to create the layout and another to evaluate it. Claude's image understanding wasn't reliable enough for detailed comparison, and I used Gemini Flash to review similarity with the reference.

Gemini analyzed the design and made a to-do list. Claude then replaced earlier background work with a simplified version instead of changing it incrementally. Git let me revert that replacement.

The evaluator also gave high scores to results that looked quite different from the reference. Ratings around 8 out of 10 came with a judgment that the design was close enough, so the loop stopped too early. Stricter criteria still didn't make it converge.

I repeated the experiment with Opus 4.6 analyzing the reference directly. It identified the background and typography accurately, but the generated version reused elements from earlier attempts. I couldn't cleanly evaluate an independent recreation from that result.

A background-only run continued for 44 iterations. It kept changing the style instead of approaching the reference, and I ultimately used the certificate from the manual feedback process.

For hosting, I already knew the required services. The PDFs needed S3 storage and CloudFront, with HTTPS and DNS configuration. DataTalks.Club had a course-specific setup, but I wanted a separate deployment process for workshops and external programs.

I gave Claude Code access to the S3 bucket and Cloudflare. I updated DNS at GoDaddy by following its instructions, then let it configure CloudFront and HTTPS. Claude debugged configuration problems as they appeared.

That took ten minutes instead of the several hours certificate hosting usually took me. The infrastructure tasks had defined constraints and documentation. I could describe the required setup and let Claude work through the configuration.

For the visual task, the model's feedback didn't reliably reflect the differences I could see. More iterations weren't enough when the evaluator kept accepting the wrong result. I needed to keep reviewing the layout and giving the corrections myself.
