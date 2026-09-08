# A Practical Image-to-Podcast Pipeline



The useful part of this example is the workflow. I will walk through the problem, the decisions, and the limits so the idea stays connected to what actually happened. 

One Idea I Want to Share this Week https://github.com/alexeygrigorev/kids-horror-stories-ruhttps://github

.com/alexeygrigorev/kids-horror-stories-ruhttps://alexeygrigorev.com/kids-horror-stories-ru/https://open.

spotify.com/show/3vo7Q3MiEgw9ZeZBU2iDGr via an RSS feed. Podcast on Spotify

https://alexeygrigorev.com/kids-horror-stories-ru/stories/1255-the-green-wall/ so you can get a sense of

the format and tone: 0:00 -2:25 Audio playback is not supported on your browser. Please upgrade. In this

post, I want to walk through how the project is built: its architecture, scripts, prompts, and

automation. Inspiration: Storytelling With My Son The result project started with my son asking for

scary stories. During a walk, he pointed at a parked car and asked if I could make up a horror story

about it. I improvised something, and he liked it. I asked Gemini to make a comic about the story with

my son After that, he started pointing at more and more objects. At some point, I ran out of ideas. When

he asked for a story about a tree we passed, I did what felt natural to me: I took a photo of the tree

and asked ChatGPT to write a scary story based on the image. The result was better than I expected. The

tone reminded me of the short urban legends and campfire horror stories I grew up with: simple,

sometimes a bit silly, but kids loved them. We ended up spending the rest of the day taking photos of

random objects and reading the generated stories together. After a while, we had accumulated quite a few

stories, and it felt wrong to leave them buried in chat history. So I decided to publish them somewhere.

Project Website The fastest option was a static site, a small Jekyll project hosted on GitHub Pages. I

already had experience with that setup, so it came together quickly. The first version was minimal: just

photos and text stories rendered as static pages. Over time, this evolved into a fully automated

pipeline that now generates stories, illustrations, audio, and podcast episodes on its own. Below, I’ll

show you how I put together it. Architecture Overview At a high level, the system does this: 1. Input

image: Either dropped into a local folder or uploaded to an S3 bucket. GPT-4owith title + slug using a

constrained prompt. GPT-5: Clean up grammar and phrasing in Russian. DALL-E 3: Use the first 1-2

paragraphs to create a prompt and generate an illustration in a consistent style. Jekyll: Save markdown

post with frontmatter, original image, illustration, and audio metadata. TTStts-1, voice onyx, store

audio and record metadata. locally or on S3. XML is updated and used by Spotify / podcast apps. Project

Layout A minimal layout looks like this: . local option ├── images/ Resized images and illustrations │

├── XXX-slug.jpg AI illustration resized .md with frontmatter ├── assets/ │ └── audio/ MP3 files ├──

processstories.py Main pipeline: image → story → illustration → files ├── generateaudio.py Story → TTS →

MP3 + metadata ├── podcast.xml RSS feed for Spotify / podcast apps └── .github/ └── workflows/ └──

main.yml GitHub Actions workflow Story Creation Pipeline https://alexeygrigorev.com/kids-horror-stories-r

u/stories/999-silence/https://github.com/alexeygrigorev/kids-horror-stories-ru/blob/main/processstories.p

y, with the main pipeline. The prompts I use are in Russian, but I have translated them into English for

you. Step 1: Input Image Example photo The script picks the first available image



That is the part I would keep from this example: connect each tool to the problem that made it necessary, and keep the limitation next to the claim. The details matter because they explain what can be reused and what was specific to this project.
