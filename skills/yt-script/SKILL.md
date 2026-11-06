---
name: yt-script
description: >-
  Write a YouTube video script from a raw idea - hook options off 21
  formulas, scored, then the full spoken script with the retention beats
  marked. Use whenever the user wants a video script, a hook, an opening
  line, "what should I say", "write my next video", or is about to record
  and does not have the first fifteen seconds yet. En español: "escríbeme
  un guion", "dame un hook", "cómo empiezo el video", "mi próximo video".
---

# yt-script

One idea into a script somebody finishes.

Two tools live in this folder and both actually run. Use them. Do not eyeball the hook.

```bash
python3 hookscore.py hooks.txt              # rank your hook options
python3 hookscore.py --hook "one line"      # score a single one
```

## Before you write

1. Read `.claude/youtube/voice.md` in the current project if it exists. Each channel lives in its
   own project folder with its own profile, so never read or write `~/.claude/youtube/voice.md`.
   That is the user's voice profile: how they talk on camera, the words they never use, who they
   are talking to, what they will not claim. If it does not exist, or is still the blank
   template, run `/yt-voice`: it builds the file from the user's own videos or, for a channel with
   none yet, from a recorded voice test. Read `.claude/youtube/style.md` too if it exists - the
   format, cadence and packaging rules for this channel. A script in the wrong voice is worse than no script, because they have to
   read it out loud.
   Read `language:` under `## Niche` in `.claude/youtube/channel.md` too: everything this writes
   is in that language and region. No `language:` line - a channel set up before it existed -
   take it from `voice.md` or the channel's own videos, confirm it with the user once, and write
   it in.
2. Never invent a number, a result or a source. If a figure would strengthen it and you do not have
   one, ask for it or write the line without it.

## The shape

**The first 15 seconds is the whole job.** It does three things or the video leaks: confirm the
click the title promised, open a question the viewer cannot close, and prove the payoff exists.

1. **Hook.** Write FIVE against [the 21 formulas](hooks.json), run them through `hookscore.py`,
   keep the top two, and show the user both with their scores. Never hand over one hook.
2. **The turn** (0:15-0:45). Say what the video is going to do, in one sentence, and start doing it.
   No channel intro, no "before we get started", no subscribe pitch. Those are the single most
   common cause of the 0:30 cliff.
3. **The body.** One idea per beat. Mark each beat with what is ON SCREEN, not just what is said -
   a talking head with nothing to look at is a podcast.
4. **The payoff.** Deliver the thing the hook promised, explicitly, and say that you are delivering
   it: "that is the prompt, it is in the description". Say the answer once as a complete sentence
   that still makes sense quoted on its own, and say the names that matter - the tool, the place,
   the term - out loud, not only on screen. Captions, search and AI answers only get what was said.
5. **The close.** One ask. Not three.
6. **Say it in their voice.** Save the script as plain text and run
   `../yt-voice/voiceprint.py <their transcripts> --against script.txt`. Fix the address first if it
   does not match, then every phrase it lists under "never said" that does not sound like them.

## Faceless

Read `format:` in `.claude/youtube/channel.md`. Anything but `camera` changes three things:

- **Every beat names the source of its visual**, not just what is on screen: `[ON SCREEN: B-roll -
  ...]`, `screen recording`, `graphic`, `on-screen text`, `generated image`. Nothing else holds the
  frame. If one visual would sit through a whole long beat, split the beat or add a second visual.
- **`ai-voice`: write for the engine.** No fillers, no stage directions it would read aloud, pauses
  marked the way `## Voice settings` in `voice.md` says, and every word on its pronunciation list
  spelled the way it needs to be said.
- **The hook cannot lean on a face.** The first visual has to do the job a face does: show the
  payoff, or the problem, in the first second.

If the HyperFrames `faceless-explainer` skill is available here, it works scene by scene too -
hand it the beats as they are. Never required.

## What to hand back

- the two best hooks with their scored panels
- the script, beat by beat, with `[ON SCREEN: ...]` on every beat
- the runtime estimate at the pace measured in `voice.md`, or 150 words per minute without one
- what `voiceprint.py --against` caught, and what you changed
- one line naming which formula the winning hook used and why it fits this idea

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
