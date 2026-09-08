# Designing an image-to-podcast pipeline

An automated media project becomes easier to manage when each transformation has a clear input and output. For the Kids Horror Stories project, the input is an ordinary photograph. The pipeline produces a web page, an illustration, an audio file, and an RSS entry for a podcast. The stages are connected, but each has one job.

Begin with ingestion by accepting an image from a local `images_input/` folder or an S3 input bucket. After processing, move it to `done/`. On failure, move it to `failed/` and log the error. This prevents the same photo from being processed again and leaves a visible place to look at failures.

The story stage sends the image to GPT-4o with a constrained prompt. The model first describes the photo and then writes an eight to twelve paragraph horror story. The prompt asks for a Russian title and a short English slug. It also excludes several tired plot and title choices.

A second stage sends the result to GPT-5 for Russian grammar and phrasing edits. Separating generation from editing keeps the creative prompt different from the language-editing prompt.

The illustration stage uses only the first one or two paragraphs. GPT-4o-mini turns them into a description of a single close-up scene, with neutral references for people and no text in the image. DALL-E 3 uses that description to create a flat illustration with bold outlines, minimal colors, and a playful eerie mood. The source image and resized illustration are then placed in the site's image directory.

The publishing stage writes a Jekyll post. Sequential IDs make filenames and URLs stable for the site. The frontmatter stores the title, slug, and date. It also stores the illustration, original image, and audio metadata.

A TTS script converts the story to speech with OpenAI's `tts-1` model and the `onyx` voice. It uploads the MP3 to S3. The script records its size and duration, then puts a copy in the site's audio assets.

Jekyll generates an RSS XML file for the podcast feed. Podcast applications such as Spotify read the feed and discover each MP3 through its public URL. GitHub Actions can build the site after a new story is committed.

The project also benefits from a simple layout. Keep raw images, generated images, posts, and audio in recognizable locations. Keep the processing code and RSS template there too. File metadata connects them. If a later stage fails, the input can be moved to `failed` rather than silently disappearing.

The sequence has these steps:

1. Accept an image and generate a story.
2. Edit the story and create one illustration.
3. Save the files, synthesize speech, and publish the metadata.

Each stage can be replaced or checked without rewriting the whole pipeline. File metadata connects the image, story, illustration, and audio. It also connects the RSS feed.
