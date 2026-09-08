# Why Infrastructure Automation Worked Better Than Design Automation

The certificate project separated two kinds of work. Recreating a visual reference required subjective comparison, while hosting finished files required a sequence of well-defined infrastructure tasks. AI tools struggled with the first and handled the second much more reliably.

For the design, a creator model generated or modified an HTML and CSS layout, and a judge model evaluated its similarity to a reference image. Claude’s built-in image understanding was not reliable enough for detailed layout comparison, so Gemini Flash was used to analyze borders, colors, textures, typography, and placement. In theory, the judge’s feedback could guide the next iteration.

In practice, the feedback was not a dependable measurement. Gemini often rated visibly different results around 8 out of 10 and marked them close enough. Stricter criteria did not make the loop converge. Claude also sometimes discarded existing work and recreated a simplified design from scratch, although Git made it possible to revert that change.

A second experiment used Claude Opus 4.6 to inspect the reference directly. Its analysis was detailed and correctly identified many visual elements, but the generated result reused parts of earlier experiments even though the instruction was to start over. A background-only attempt ran for 44 iterations and kept producing different stylistic variations. The similarity score and the actual visual difference remained disconnected.

The successful design workflow was therefore the simplest one. Claude generated the HTML and CSS, while a person reviewed the output and described changes to spacing, alignment, and element placement. That loop took about 40 minutes, but it produced the certificate that was ultimately used. Design quality depended on human comparison because the evaluator could not reliably tell whether the result matched the reference.

Infrastructure had clearer boundaries. The finished certificates had to be stored in S3, served through CloudFront, available over HTTPS, and connected to the right domain through DNS. The author gave Claude Code access to the S3 bucket and Cloudflare, followed its instructions for GoDaddy records, and let it configure the services. Claude handled issues as they arose and completed the setup in about ten minutes, compared with the several hours it usually required manually.

The difference was not simply that one model was better. Infrastructure tasks had explicit resources, configuration fields, and documentation. A deployment either exposed the files over the expected domain or it did not. Visual similarity depended on many small judgments that were difficult to express as a score, and an inaccurate score caused the automated loop to stop too early.

This example places a useful boundary around AI automation. When constraints and success conditions are concrete, an agent can execute a documented sequence and debug configuration problems. When success depends on subtle comparison with a visual reference, the person judging the result remains part of the system. The certificate experiment worked after accepting that difference rather than forcing both tasks into the same loop.
