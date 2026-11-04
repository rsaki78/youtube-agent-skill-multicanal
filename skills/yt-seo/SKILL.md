---
name: yt-seo
description: >-
  Write the description, tags and search-facing text for a YouTube video,
  aimed at the query a real person types. Use for "write my description",
  "tags", "SEO", "help this video get found", "nobody is finding this". En
  español: "escríbeme la descripción", "etiquetas", "que me encuentren",
  "SEO del video".
---

# yt-seo

Search is a smaller lever than packaging and a bigger one than people think for evergreen videos.
For a video aimed at the subscriber feed, say so and spend the effort on `/yt-package` instead.

## Before you write

1. Read `.claude/youtube/voice.md` in the current project if it exists. Each channel lives in its
   own project folder with its own profile, so never read or write `~/.claude/youtube/voice.md`.
   That is the user's voice profile: how they talk on camera, the words they never use, who they
   are talking to, what they will not claim. If it does not exist, or is still the blank
   template, run `/yt-voice`: it builds the file from the user's own videos or, for a channel with
   none yet, from a recorded voice test. Read `.claude/youtube/style.md` too if it exists - the
   format, cadence and packaging rules for this channel. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## The description

- **The first two lines are the only ones anyone reads.** They show above "...more" and they are
  the search snippet. Say what the video gives them, in the words they would have typed.
- Then the link or the resource, if there is one, so it is above the fold.
- Then chapters (`/yt-chapters` writes them).
- Then the long version: what is covered, who it is for, what it assumes.

## Tags, honestly

Tags are a weak signal and YouTube has said so. Use them for disambiguation - spellings, the tool
names, the abbreviations people actually type - and stop. Fifteen is plenty. A wall of tags is not
a strategy and stuffing unrelated ones is against the terms.

## The query test

Before handing anything over, write the three search queries this video should win, and check the
title and first two description lines contain the words in those queries. If they do not, the
problem is the title, not the description.

## When an AI answer cites the video

Only for search videos - the evergreen how-to, the question somebody types. ChatGPT, Gemini and
Google's AI answers do not watch the video; they read the text around it: the captions, the
title, the chapters, the description, the pinned comment. So the work is making that text say the
answer plainly. This is a working rule, not a measured one - nobody, this pack included, can see
why an answer cited one video over another. Never promise the user it will happen.

- **Correct the captions.** Auto-captions misspell names and break sentences, and they are the
  transcript the models read. Get them - Studio's Subtitles page, or
  `yt-dlp --write-auto-subs --skip-download --sub-langs es <url>` - check every name against the
  pronunciation list in `voice.md` and the names in the script, and upload the corrected file.
- **The title states the task or the question**, in the words of the first query from the query
  test. For a feed video, `/yt-package` wins and this line does not apply.
- **The long version of the description** opens with the answer in two sentences, then the topics
  as a short list, then the resources.
- **Chapters named as the sub-questions** they answer - the search variant in `/yt-chapters`.
- **A pinned comment from the channel** with the answer as numbered steps and the links. Draft it
  for the user to post; on a how-to, it is the comment `/yt-comment` should pin.
- **Look, if they want to.** Ask ChatGPT, Gemini and Google the three queries from the query test
  and note who is cited, with the date. Answers change from one day to the next: it is an
  observation, not a metric.

Adapted from `skills/ai-seo/references/youtube-ai-citations.md` in Corey Haines'
[marketingskills](https://github.com/coreyhaines31/marketingskills) (MIT), which credits the pattern
to Ross Simmonds / Foundation Inc., "The Anatomy of a YouTube Video AI Cites" (2026). The ideas,
not the figures: its numbers came without sources and are left out.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
