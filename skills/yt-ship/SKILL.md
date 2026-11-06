---
name: yt-ship
description: >-
  Prepare an edited video for upload - chapters, description and
  search text, and the Shorts if the channel makes them - in one file in
  the video's folder, for channels whose videos come out of a pipeline.
  Use for "prepare the upload", "the video is edited", "/yt-ship <code>".
  En español: "prepara la publicación", "ya está editado el video",
  "arma el seo del video".
---

# yt-ship

The video is cut. What is left is the text around it - and the text is what search and AI answers
read. This gathers it in one place, from the files the pipeline already made, so nothing is retyped
from memory.

It orchestrates `/yt-chapters`, `/yt-seo` and, when it applies, `/yt-shorts`. It does not repeat
their rules; it follows them. It does not upload anything.

## Before you start

1. Read `.claude/youtube/channel.md`, `voice.md` and `style.md` in the current project; never
   `~/.claude/youtube/`. `language:` goes to every tool as `--lang`.
2. Read `.claude/youtube/pipeline.md` if it exists: the video folder, the subtitles, the audio,
   the sources file, where the output goes, what has to be updated after publishing. No
   `pipeline.md`: ask for the subtitles and the sources.
3. Find the video by its code and check the folder has what this needs - at least the subtitles.
   Say what is missing rather than working around it.
4. Never invent a number, a result or a source. The description says nothing the sources file and
   the video do not.

## The steps

1. **Chapters.** `/yt-chapters` on the subtitles, with `--lang`. If `style.md` has a `## Timeline`
   section and the folder has the audio per scene, run `timeline.py` first and pass its scene
   starts to `chapters.py` as `--scenes`: a scene is a better chapter boundary than a pause.
   If the subtitles already come in the final video's time, use them as they are.
2. **Search.** `/yt-seo`: the description, the query test, the tags worth having, and - for a
   search video - the AI-citation steps, including the corrected captions.
3. **Shorts.** Only if `style.md` says the channel makes them, and only if the user has the time
   now. Otherwise, one line saying they were skipped and why.

## What to write

One file in the video's folder - `seo.md`, or wherever `pipeline.md` says - with, in this order:
the title and thumbnail text as approved, the description with the chapters in it, the tags, the
pinned comment if there is one, the Shorts if any, and the query test. Every block ready to paste
into Studio.

## The last line before the gate

If `pipeline.md` has `## After publishing`, repeat it as a reminder, with the condition: **only once
the video is actually public**. Dates and series files are updated from the real publication, not
the plan. This skill never updates them itself.

## The gate

Nothing here publishes. This skill writes and you upload. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
