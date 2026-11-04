---
name: yt-chapters
description: >-
  Write YouTube chapters from a transcript, validated against YouTube's
  own rules so they actually render. Use for "add chapters", "timestamps",
  "break this video into sections". En español: "capítulos", "marcas de
  tiempo", "timestamps del video".
---

# yt-chapters

```bash
python3 chapters.py transcript.srt --target 8
```

## Before you write

Read `.claude/youtube/voice.md` in the current project if it exists - never
`~/.claude/youtube/`. Chapter titles are short, but they are still the channel talking: the same
address (tú, usted, vos), none of the banned words. No `voice.md` is not a reason to stop - write
the titles plainly and mention `/yt-voice`. Never invent a number for a title.

## The rules, which are not optional

A chapter list that breaks any of these silently does not become chapters at all - the block just
sits in the description doing nothing:

- The first entry must be **00:00**.
- There must be **at least three**.
- Each must be **at least 10 seconds** long.

The tool checks all three and tells you when a list is invalid rather than letting you paste it.

## Retitle every line

`chapters.py` finds the BOUNDARIES well - it scores the pauses you actually took by how much the
vocabulary shifts across them. The titles it emits are the topic words, and they are a draft. A
chapter called "Thumbnails Titles Packaging" is a placeholder. Rewrite each one as the promise of
that section, in the user's voice, three to five words.

**Search videos** are the exception to the five words: a chapter can be the sub-question it
answers - "How much to set aside for taxes?" - because that is the label search and AI answers
lift out of the video. Feed videos keep the promise form.

Chapters are also a retention diagnostic: if a section cannot be named in five words, it is two
sections or it is filler.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
