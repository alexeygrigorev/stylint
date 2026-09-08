# From a photo to a published horror story

About a year ago I built Kids Horror Stories, a project that turns a photograph of an everyday object into a short Russian horror story. The system also creates an illustration and narration, publishes the story on a website, and adds an episode to Spotify through an RSS feed. It now contains more than 1,200 stories.

The idea started with my son. During a walk he pointed at a parked car and asked me to make up a scary story. I improvised one, and he wanted more.

When I ran out of ideas about the objects around us, I took a photo of a tree. I asked ChatGPT to write from the image. The result reminded me of the simple urban legends and campfire stories from childhood. We spent the day photographing random things. We read the results together.

I didn't want the stories to disappear in chat history, so I published them on a small Jekyll site hosted by GitHub Pages. The first version contained photos and text.

Later I turned it into a pipeline that could process images and update the podcast feed. It writes and edits stories, creates illustrations, and generates audio.

An image can arrive in a local input folder or in an S3 bucket. GPT-4o receives the image and a constrained prompt. It describes the photograph, writes an eight to twelve paragraph story, supplies a Russian title, and proposes an English slug.

GPT-5 then edits the Russian grammar and phrasing. I kept these as separate steps because the first model creates the story while the second is used for language cleanup.

For an illustration, the pipeline takes the first two paragraphs and asks GPT-4o-mini to describe one close-up scene. DALL-E 3 generates the image in a flat, linear style with bold outlines, minimal colors, and a slightly eerie cartoon feeling. The original photo and resized illustration are stored alongside the Jekyll post.

The post receives frontmatter with its sequential story number, slug, and title. It also stores the date, image paths, and audio metadata. A separate script sends the finished story to OpenAI TTS with the `onyx` voice. It uploads the MP3 to S3, calculates its duration, and updates the post.

The RSS file is generated for Spotify and other podcast applications.

After success, the source image moves to `done`. Failures move to `failed` and leave an error in the log. GitHub Actions builds the site. The system isn't one model call, but a set of ordinary steps connected by files and metadata. A photo can become a story, an illustration, an audio file, and a published episode without my repeating the process manually.

The original photo stays next to the generated illustration, and the page can show where each story began. The website and podcast both use the edited story text.
