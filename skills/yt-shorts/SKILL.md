---
name: yt-shorts
description: >-
  Find the Shorts hiding inside a long video and write them, using the
  transcript to pick self-contained moments. Use for "cut this into
  shorts", "clip this", "repurpose this video", "what should I clip". En
  español: "sácale shorts", "recorta este video", "qué clips saco".
---

# yt-shorts

A Short cut out of a long video is not a clip of the best moment. It is a moment that **survives
without the video around it**, which is a much smaller set.

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
3. Every new first line and every piece of on-screen text uses the address in `voice.md` (tú,
   usted, vos) and none of its banned words. Time each Short at the pace in its `## Measured`
   section, or 150 words a minute without one.

## Picking

Read the transcript and find spans of 20-55 seconds where all three are true:

1. It opens on a complete thought. If the first sentence needs the previous minute, it is not a Short.
2. There is a turn in it - a claim, then something that complicates or proves it.
3. It ends on a line, not a trail-off.

Rank the candidates and show the user the top five with their timecodes and first line, so they can
reject one without reading the whole transcript.

## Writing each one

- **A NEW first line.** The long video's line assumes context this viewer does not have. Write the
  replacement and run it through `../yt-script/hookscore.py`.
- **On-screen text for the first two seconds**, different words from the spoken line.
- **A loop point**: what the last line sets up so the first line answers it.
- Vertical framing note - what gets cropped out of a 16:9 frame and whether that matters.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
