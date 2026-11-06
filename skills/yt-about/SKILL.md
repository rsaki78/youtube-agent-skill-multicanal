---
name: yt-about
description: >-
  Write a YouTube channel's description - 1,000 characters at most, first
  line written to stand alone - plus the links, the contact email and the
  rest of the Studio fields a new channel needs filled before its first
  upload. Use for "channel description", "about section", "write my
  channel bio", "set up my channel", or after /yt-brand. En español:
  "descripción del canal", "sección acerca de", "bio del canal",
  "configura mi canal".
---

# yt-about

A channel description gets read by two kinds of stranger: someone deciding in two seconds whether
this channel is for them, and YouTube deciding what the channel is about. Both read the first line
hardest. Most descriptions spend it on "Welcome to my channel".

```bash
python3 about.py description.txt --keywords "word one,word two" --voice .claude/youtube/voice.md
python3 about.py a.txt b.txt --keywords "..." --voice .claude/youtube/voice.md     # compare drafts
```

On Windows, if `python3` is not found, run the same line with `py` or `python`.

## Before you start

1. Read `.claude/youtube/channel.md`, `voice.md` and `style.md` in the current project; never
   `~/.claude/youtube/`. The description is the sub-niche's one-line statement, the viewer, the
   pillars and the cadence, said in the creator's voice - it should invent nothing those files do
   not already hold, in the `language:` from `## Niche`. Anything missing, ask; or run the skill that owns it.
2. Never invent a number, a result or a source. No subscriber counts, years of experience,
   clients or results that the user has not given you - and nothing `voice.md` says they will not
   claim.

## The description

1,000 characters. That is YouTube's only hard rule; `about.py` counts it.

1. **The first line stands alone.** Who it is for and what they get, with the words that viewer
   would search. It is what the channel header shows before "more". Never a greeting.
2. **What the videos are.** The pillars from `style.md`, in plain words, not a list of hashtags.
3. **Who is behind it.** Only what is true and checkable. One line. Skip it for a faceless channel
   unless the persona has something real to say.
4. **When.** The upload day - only if `style.md` has a cadence they keep.
5. **Contact.** One line pointing to the contact section, not an email typed into the text.

Write TWO drafts - one search-first, one voice-first - run both through `about.py` with the
sub-niche's search words as `--keywords` and `--voice` pointing at `voice.md`, fix what it flags,
and show both with their counts. Errors are fixed before showing; warnings are explained or fixed.
The 120-character warning on the first line is a heuristic - the header cut depends on the screen
- not a YouTube rule.

## The rest of the setup

What a new channel needs filled before the first upload. Hand it over as a checklist, with the value
for each line already written:

- **Links** - up to 14; the first one shows by the subscribe button, so choose it on purpose. Not
  the creator's personal Instagram by default - whatever the channel actually sends people to.
- **Contact email** - for business. A separate address from the personal one.
- **Channel keywords** - Settings, Channel. They barely matter; five honest ones and move on.
- **Country and language** - the market from `/yt-niche`.
- **Upload defaults** - Settings, Upload defaults: the default video description footer (links,
  the contact line) so it is never typed by hand again, the category, the video language.
- **Name and handle** - already claimed in `/yt-name`. Note it: the name can be changed twice in
  fourteen days, and changing it removes a verification badge.

## What to write

Into `## About` of `channel.md`: the chosen description, its count, both drafts, the links in
order, and the date. `status: locked` once it is in Studio. Next step: the first video -
`/yt-plan`, then `/yt-script`.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
