# How an Image Becomes a Story, an Illustration, and an Episode

The kids’ horror stories project is a useful example of a small multimodal pipeline. Its input is an everyday photograph. Its outputs are a Russian story, a matching illustration, a web page, and a podcast episode. The site has grown to more than 1,200 stories, but the workflow is still a sequence of understandable stages.

It begins by choosing an image. The project accepts a file dropped into a local folder or an image uploaded to an S3 input bucket. The processing script takes the first available image and converts it to base64 so it can be sent as an image input to GPT-4o. The model receives a constrained prompt: describe the photograph, write an urban-folklore-style scary story, provide a title, and produce a short English slug for the URL.

The constraints shape the output. A story should contain eight to twelve paragraphs, and its title should be in Russian. The prompt also excludes a set of overused title words and asks the model to avoid plots built around whispers, rustling, or objects returning to the characters. These rules do not create the whole style, but they make the generated drafts more consistent.

The first model is not the final editor. The raw Russian story goes through GPT-5, which corrects grammar and replaces awkward expressions with more natural ones. This separates story generation from language cleanup. The editing step keeps the generated idea while dealing with phrasing that would sound strange to a Russian reader.

The illustration stage uses only the first one or two paragraphs of the edited story. GPT-4o-mini turns that text into a description of one close-up scene, then DALL-E 3 generates a 1024-by-1024 image. The illustration prompt asks for bold outlines, simple vibrant colors, and a playful but slightly eerie feeling. It also limits the scene to the essential objects and one or two people, and tells the model not to add text. The result is resized and stored with the other project images.

Next, the pipeline packages the content as a Jekyll post. A sequential story ID is used in the filename and URL. The post keeps frontmatter such as the title, slug, illustration path, original image path, and audio information. The text is converted to speech with OpenAI’s `tts-1` model and the `onyx` voice. The generated MP3 is uploaded to S3, its size and duration are recorded, and a copy is placed in the site’s audio assets.

The last stages make publishing repeatable. A podcast XML file is used as an RSS feed, which is how Spotify and podcast applications receive the episodes. GitHub Actions automatically pulls images from S3, runs the pipeline, and publishes a new story. The input image is moved to `done/` after success or `failed/` after an error, so the same file is not processed repeatedly.

This design works because each stage has one job: vision and writing, editing, illustration, packaging, speech, and publication. It started as a family activity involving photos of trees and parked cars, then became a static website and an automated podcast without losing that simple input-to-story connection.
