# Splitting a Telegram assistant into focused agents

A Telegram writing assistant can begin as a process that receives a message and transcribes it. It can also fetch a link and update an article. That was enough for the first version.

Later the bot also handled external research, resource descriptions, and verification in one context window. Several URLs could fill the context and slow responses. Details could disappear.

I refactored the workflow with Claude Code subagents. The main agent coordinates the work and processes voice messages. Separate agents handle research, resource descriptions, and verification. Each has a defined responsibility, so the main context doesn't need to contain every long document.

`article-summarizer` accepts one external URL and uses Jina Reader to extract its content. It adds organized research to an existing article with an overview and important ideas. It also includes technical details, insights, and practical takeaways.

`resource-describer` handles links for the newsletter's resources section, writes a short description, and adds it to `interesting-resources.md`.

`verify-content` has a different purpose: it checks whether the main agent accidentally summarized a voice note or left out important context. After the main processing step, it compares the generated material with the original voice messages and fills gaps where necessary.

The main agent keeps a narrower role. It processes voice messages, formats material, coordinates the workflow, and delegates external content. It receives structured outputs rather than ingesting every source in full.

Voice notes therefore remain available for checking while research work stays outside the main context.

The assistant also accepts regular audio files such as MP4 and M4A. Telegram's native voice recording stops when the app goes into the background, which makes longer thoughts inconvenient.

The file is detected, transcribed, and sent through the same pipeline as a voice message. YouTube links are handled by retrieving their transcript and treating it as source material.

For workshop materials I use `create-slides` and `slides-to-pdf`. I dictate the idea, start an interactive Claude Code session, and ask for slides. Then I review them and iterate. A correction can become part of the skill after it repeats, while separating research, drafting, and checking keeps concrete problems visible.

The main agent can therefore keep processing the Telegram workflow while another agent handles a long external article. The result comes back in a structured form that can be checked before it enters the draft.

The same separation helps when the input is an audio file. Transcription can happen in one step, research extraction in another, and verification can still compare the final text with the original recording.
