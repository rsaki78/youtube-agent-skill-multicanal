---
name: yt-voice
description: >-
  Build the channel's voice.md and style.md - how the creator actually
  sounds, measured from them talking, and how the channel is made: format,
  cadence, pillars, packaging rules and the numbers worth watching. Works
  for a channel with no videos yet. Use for "write my voice.md", "define
  my style", "how should my videos sound", a new channel, or after
  /yt-name. En español: "define mi voz", "escribe mi voice.md", "mi
  estilo", "cómo deben sonar mis videos".
---

# yt-voice

Two files every other skill in this pack reads. `voice.md` is how the creator sounds. `style.md` is
how the channel is made. Both get built from evidence: a voice described from what the creator
wishes they sounded like turns into scripts they cannot say out loud.

```bash
python3 voiceprint.py voicetest.srt                          # how they actually talk
python3 voiceprint.py voicetest.srt --against draft.txt      # does a script sound like them
```

## Before you start

1. Read `.claude/youtube/channel.md` in the current project; never `~/.claude/youtube/`. Use the
   viewer from `## Sub-niche`, the take/leave lines from `## Reference channels`, and the tone of
   the name from `## Name and handle`. Both files are written in the `language:` from `## Niche`,
   and `voiceprint.py` should report that same language - if it does not, ask. Missing sections are not a blocker for the voice - they are
   for the style.
2. If `.claude/youtube/voice.md` exists and is filled in - not the blank template - ask whether to
   rebuild it or only measure against it. Never overwrite it silently.
3. Never invent a number, a result or a source.

## voice.md - measured, then interviewed

### The source, best first

1. **Their own videos**, on any channel. Three, unscripted moments preferred.
2. **Any unscripted speech** - a podcast, a live, a talk, long voice notes.
3. **The voice test**, for a channel with nothing yet. Two recordings, two to three minutes each,
   phone is fine, no script:
   - explain one of the ten titles in `channel.md` to a friend who knows nothing about it;
   - tell the story of something in the niche that went wrong for them.
   Transcribe it however is easiest: the phone's dictation, an unlisted YouTube upload and its
   auto-captions (`yt-dlp --write-auto-subs --skip-download --sub-langs es <url>`), any transcriber.
4. **Their writing** - messages, posts. Last resort, and say so in the file: it measures how they
   write, which is not how they talk.

### Faceless

Read `format:` in `## Niche`. `voice` - their own voice, no face - is the flow above: it is still
their voice, so measure it. `narrator` and `ai-voice` are different: the voice is designed, not
discovered.

- **The character.** Write it like a casting brief: who they are, the energy, the address (tú,
  usted, vos), the pace, what they never say. Drawn from the viewer and the references, never
  from a generic "friendly narrator".
- **`ai-voice`: the settings, in `voice.md` under `## Voice settings`.** The provider, the voice
  and model, the speed and whatever else that provider exposes, how it marks a pause, and a
  pronunciation list: the channel name, the niche's terms, anglicisms, how numbers and currency
  are read. Take the setting names from the user or the provider's own docs - never from memory.
- **`narrator`:** the casting brief, plus a one-minute audition script with the hard words in it.
- **Then measure the first real narration** - two minutes, generated or recorded from a script -
  with `voiceprint.py` on its timed transcript. The words are the script's, so what it tells you is
  the pace; that sets how long the script's lines can be.

### Measure

Run `voiceprint.py` on everything you have. Under 300 words it says not to trust it; get more.

- **Address** goes on the first line of `voice.md`, in bold: tú, usted, vos or ustedes. A script in
  the wrong one is unreadable on camera, and it is the mistake every generic script makes.
- **Repeats** are the tics. Keep the ones that are theirs. Drop the ones that are just the topic.
- **Fillers** are for the edit (`/yt-edit`) to cut. Never write them into a script.
- **Sentence length** and **pace** set how long a script's lines can be.

### Interview

What a transcript cannot show. Ask, in one message:

- Words they would never say. Offer the usual suspects in their language to react to.
- What they will not claim: numbers they cannot show, results that are not theirs, tools they
  have not used.
- The viewer, if `channel.md` does not have it yet - one person, named properly.

### Write it

Follow the sections of `../yt-launch/templates/voice.md`. Add `## Measured` at the end: the voiceprint, the
source, and the date. Paste the best two minutes of transcript into "How I actually talk".

## style.md - how the channel is made

Write `.claude/youtube/style.md` with these sections:

- **Format.** Long-form length range, Shorts or not and how many per long video, the shape of an
  episode (cold open, intro or none, sign-off), the `format:` from `channel.md`, the setup they actually own. Faceless: what carries the
  screen - stock or own B-roll, screen recordings, graphics, generated images, animation - and the
  tools they have for it. Take
  it from the peers in `## Reference channels`, sized to the hours from `/yt-niche`.
- **Cadence.** Uploads a week that fit those hours - fewer than they want. One fixed day, marked
  provisional until their own analytics pick a better one. Consistency beats frequency.
- **Pillars.** Three or four recurring kinds of video, each with one title from the ten. A video
  that fits no pillar is a reason to ask why it is being made.
- **Packaging rules.** The title shapes the peers' outliers use (from `swipe.py` in `/yt-refs`),
  the words banned by `voice.md`, and thumbnail rules: words on it, face or not. Colours and type
  stay `pending /yt-brand`.
- **Numbers.** No invented benchmarks - no "a good CTR is". For the first ten videos the only target
  is shipping them on the cadence. After ten, the baseline is the channel's OWN median: views,
  click-through rate, average percentage viewed, retention at 30 seconds. Every video after that is
  judged against it, the way `/yt-viral` judges everyone else's. For context only, the peers'
  medians from `refs.py`, with the date they were collected.
- **The review loop.** `/yt-retention` on every long video, `/yt-audit` every ten.
- **What this channel does not do.** Three lines. The promises it will not make, the formats it will
  not chase.

## What to hand back

The address and the three tics worth keeping, the fillers the edit should cut, and a short summary
of `style.md`: format, cadence, pillars, the one number to watch first. Then update
`## Voice and style` in `channel.md` with a pointer to both files, the date, and `status: locked`
once the user agrees. Next step: `/yt-brand`.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
