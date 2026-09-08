# From a Walk with My Son to a Kids’ Horror Podcast

This project started with my son asking for scary stories. During a walk, he pointed at a parked car and asked whether I could invent a horror story about it. I improvised one, and he liked it. Then he began pointing at more objects. I asked Gemini to make a comic about the first story, but the harder problem was that I eventually ran out of stories to tell.

When he asked about a tree we passed, I took a photo and asked ChatGPT to write a scary story from the image. The result was better than I expected. It reminded me of the short urban legends and campfire stories I grew up with. They were simple and sometimes a little silly, but children enjoyed them. We spent the rest of that day photographing random objects and reading the generated stories together.

After we had accumulated quite a few stories, leaving them in chat history felt wrong. I decided to publish them. The quickest option was a small static Jekyll site hosted on GitHub Pages because I already knew that setup. The first version contained only photos and text rendered as static pages. That was enough to make the stories available outside the conversation.

The project grew from there. A photo can arrive in a local input folder or in an S3 bucket. GPT-4o looks at it and writes a Russian story with a title and a short URL slug. GPT-5 then cleans up the grammar and phrasing. I use the opening one or two paragraphs to create a prompt for an illustration, and DALL-E 3 generates an image in a consistent, playful style.

The rest of the work is about turning that text into something people can find and listen to. Jekyll saves a post with frontmatter, the original photo, the illustration, and audio metadata. OpenAI’s `tts-1` model, using the `onyx` voice, converts the story into speech. The MP3 is uploaded to S3 and also placed in the project’s audio assets. An RSS XML feed lets Spotify and other podcast applications discover the episodes.

There are small operational details that make the pipeline usable. Each story receives a sequential ID for its filenames and URLs. Successfully processed input images move to `done/`; failed ones go to `failed/` and the error is logged. GitHub Actions pulls new images from S3, selects the first available one, runs the processing steps, and publishes the result.

The system now contains more than 1,200 stories, all in Russian. I translated one story, “The Green Wall,” so readers could see the format and tone, but the published collection remains Russian. The important part for me is still the original loop: an ordinary object, a photo, a story to read with my son, and eventually a place where that story can live.
