# Splitting a Telegram assistant into focused agents

A Telegram writing assistant can start as one simple process: receive a message, transcribe it, fetch a link, and update an article. That worked for my first version, but the workflow grew. The bot began handling voice notes, external links, research topics, and newsletter resources in one context window. When several URLs arrived together, the context filled up and responses became slower. Sometimes details were lost. The problem was the shape of the system, not just the amount of text.

I refactored the workflow with Claude Code subagents. The main agent now coordinates the work and processes voice messages. Separate agents handle research, resource descriptions, and verification. A subagent has a defined responsibility and constraints, so the main context does not need to contain every long article or document.

The research part uses two agents. `article-summarizer` accepts one external URL, uses Jina Reader to extract its content, and adds organized research to an existing article. Its output includes an overview, important ideas, technical details, insights, and practical takeaways. `resource-describer` handles links intended for a newsletter resources section. It produces a short description of two to four sentences and adds it to `interesting-resources.md`.

The third research-related agent is `verify-content`. Its job is different. It checks whether the main agent accidentally summarized a voice note or omitted context. After the main processing step, it compares the generated material with the original voice messages and fills gaps when necessary. This check exists because instructions alone did not always stop the main agent from compressing a voice note too aggressively.

The main agent keeps a narrower role. It processes voice messages, formats the material, coordinates the workflow, and delegates external content to the other agents. It receives structured outputs instead of reading every source in full. That keeps the context more predictable while leaving the original voice notes intact.

The assistant also gained two input paths. Audio files such as MP4 and M4A can now be sent when Telegram’s native voice recording is inconvenient for a long thought. The system detects the file, transcribes it, and sends it through the same pipeline as a voice message. YouTube links are processed by retrieving their transcript and treating it as source material for an article or draft.

Skills handle repeatable workflows. When I correct the same behavior several times, I can ask the agent to turn the process and corrections into a skill. The assistant has `create-slides` and `slides-to-pdf` skills for workshop materials. I dictate ideas, start an interactive Claude Code session, ask for slides, then review and iterate. Earlier examples make later requests easier to specify.

The useful design principle is separation by responsibility. Research, drafting, and checking have different failure modes, so giving them different agents makes each part easier to inspect and adjust.
