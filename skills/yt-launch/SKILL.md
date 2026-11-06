---
name: yt-launch
description: >-
  Take a YouTube channel from nothing to ready-for-the-first-upload, one
  step at a time - niche, references, name and handle, voice and style,
  brand, description - picking up wherever it was left. Use for "start a
  YouTube channel", "create a channel from scratch", "where was I",
  "what's next for my channel", or a new channel folder with no
  channel.md. En español: "empezar un canal", "crear un canal desde cero",
  "qué sigue en mi canal", "dónde me quedé".
---

# yt-launch

Starting a channel is six decisions, and each one is built on the one before it. A name chosen
before the sub-niche gets renamed. A logo designed before the name gets redesigned. This runs them in
order, one at a time, and remembers where it stopped - so it can take a week of evenings instead of
one heroic afternoon.

## The order

| # | step | skill | writes | locked when |
| --- | --- | --- | --- | --- |
| 1 | Niche and sub-niche | `/yt-niche` | `## Niche`, `## Sub-niche` | the user agrees the one-line statement |
| 2 | Reference channels | `/yt-refs` | `## Reference channels` | the user agrees the list |
| 3 | Name and handle | `/yt-name` | `## Name and handle` | the handle is claimed in Studio |
| 4 | Voice and style | `/yt-voice` | `voice.md`, `style.md`, `## Voice and style` | the user agrees both files |
| 5 | Brand | `/yt-brand` | `brand/`, `## Brand` | logo and banner are uploaded |
| 6 | Description and setup | `/yt-about` | `## About` | the description is in Studio |

Step 1 also records the channel's `format:` - on camera, or one of three faceless ways - and its
`language:` with the region, and every later step reads both.

Everything lives in `.claude/youtube/` inside the channel's project folder - never in
`~/.claude/youtube/`. `channel.md` is the memory: each section carries a status.

- `pending` - not started.
- `unvalidated` - the user brought it without running the step. Usable, flagged.
- `review` - an earlier section changed after this one was locked. Check it still fits.
- `locked` - done.

## Every run

1. **Read `.claude/youtube/channel.md`.** If it does not exist, create it from
   `templates/channel.md` in this skill's folder, and copy `templates/voice.md` from there to
   `.claude/youtube/` if that is missing too.
2. **Say where they are.** One line per step with its status, then the next one, named. Not a
   lecture - a position.
3. **Run the next step** by following its skill. ONE step per run unless the user asks for more:
   each step ends with something the user has to decide or do outside the conversation, and the
   next step is better for it.
4. **Lock it** only when the "locked when" column is true. A handle that is free but not yet
   claimed is not locked.

## What the user already has

Most people arrive with something - a name they love, a logo a friend made, a niche they are sure
of. Do not throw it away, and do not wave it through:

- Record it in its section as `unvalidated`, with "brought by the user".
- Run that step's checks on it anyway - `room.py` on the niche, `handle.py` on the name,
  `brandkit.py` on the logo, `about.py` on the description. Show what they find.
- If a check finds a real problem - the handle is taken, the logo vanishes at comment size - say
  so plainly once, and let the user decide.

## Going back

When the user changes a locked section, mark every LATER section that depends on it `review`, and
say which ones and why: a new sub-niche puts the name, the voice's viewer, the brand direction and
the description up for review; a new name puts the brand and the description up. Never rewrite a
later section silently to match.

## After step 6

The channel exists; it is not launched yet. Hand back the last checklist:

- Handle claimed, logo and banner uploaded, description and links in, upload defaults set.
- `/yt-plan` for the first month - sized to the hours in `style.md`.
- `/yt-script` for the first video, off one of the ten titles from `/yt-niche`.
- The second video made before the first goes out. A cadence that breaks in week two is the most
  common way a new channel ends.

From here the other skills in the pack take over, and `channel.md` stays as the record of why the
channel is what it is.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
