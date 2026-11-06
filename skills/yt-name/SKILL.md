---
name: yt-name
description: >-
  Name a new YouTube channel - five names of different kinds, each with a
  handle that follows YouTube's rules and has been checked against what is
  already taken. Use for "name my channel", "channel name ideas", "what
  should my handle be", "is this name taken", or after /yt-refs. En
  español: "nombre para mi canal", "ideas de nombre", "qué handle uso",
  "está ocupado este nombre".
---

# yt-name

Five names that are five versions of the same idea are one name. Five names means five different
bets on what the channel will become, and the user picks the bet.

```bash
python3 handle.py "Name One" "Name Two" --check        # handles, linted, and whether they answer
python3 handle.py --file names.txt --suffix tv,hq,mx --check
```

## Before you start

1. Read `.claude/youtube/channel.md` in the current project; never `~/.claude/youtube/`. This needs
   `## Sub-niche` - the name has to fit it - and reads two things closely: the note from
   `/yt-niche` on **how wide the name must stay**, and `## Reference channels`, because a name that
   sounds like a reference channel sends your viewers to them. No sub-niche: run `/yt-niche` first,
   or get it in one line and mark it `unvalidated`.
2. Ask the one thing the file does not say: **will the creator's own name or face be the brand?**
   It decides whether a personal name is even on the table. A faceless `format:` usually answers
   it - no personal name, unless the narrator is a persona with a name of their own.
3. Never invent a number, a result or a source. Whether a name is taken is what `handle.py` and a
   search say, not what you remember.

## The kinds

Spread the five across at least three of these:

- **Descriptive** - says the topic. "Finanzas Sin Jefe." Found in search on day one; trapped by the
  topic forever.
- **Personal** - the creator's name. The widest door there is, and it only works if they are the
  channel.
- **Hybrid** - person plus topic. "Ana Invierte." Most of the descriptive reach, a way out later.
- **Promise** - the result. "Renuncia en 12 Meses." Clicks well, ages badly once the promise is kept.
- **Coined** - an invented word. Easy to own, means nothing until the videos give it meaning.

## The tests

Draft fifteen to twenty, then cut. Every survivor passes all of these:

- **Said once, typed right.** Read it as if heard on a podcast. Could a listener type it without
  seeing it? Spelling choices, silent letters and doubled letters fail here - `handle.py` flags
  the mechanical ones.
- **The door back out.** Does it survive the sub-niche widening into the niche? No years, no
  numbers that will date it, no format word that locks the channel ("Shorts", "Podcast") unless
  that format IS the channel.
- **Nobody already there.** Search it - `yt-dlp "ytsearch10:<name>" --flat-playlist -J` - and look
  at what comes back. A dead channel with the same name still owns the search.
- **Distinct from the references.** Not one word off any channel in `## Reference channels`.
- **Means the same everywhere it lands.** The `language:` in `## Niche` first, then the other
  regions that share it. Slang differs from one country to the next; say what you checked and
  say when you are not sure.
- **Not someone's brand.** Flag anything that is obviously a company or product. You cannot clear
  a trademark - if the channel is going to be a business, tell the user to check the trademark
  office in their country before they print anything.

## Handles

Run every survivor through `handle.py --check`. It builds the variants (joined, with a suffix, with
separators, initials), applies YouTube's own rules, adds the human ones, and asks youtube.com which
ones answer.

- **free?** means `@handle` returned a 404. Probably free, never certainly - reserved and
  terminated handles 404 too. Studio is the only final answer.
- **The plain handle taken** means the NAME is probably in use. A suffix gets you a handle, not the
  name. Look at that channel before keeping it.
- **Separators** are legal and nobody says them out loud. Prefer the joined form.

Other platforms - Instagram, TikTok, X, a domain - are not checked here: their pages hide behind
logins, so any answer would be a guess. Tell the user to check the ones they will use, by hand,
before deciding.

## What to hand back

A table of five: name, kind, best handle with its status, why it fits the sub-niche in one line,
and the risk in one line. Then ONE recommendation and why, and the runner-up.

Then the urgent part: **claim the handle today.** A free handle is free until someone else takes it,
and a handle can only be claimed by a channel - so for a new channel, claiming it means creating the
channel now. Give the steps for their case:

- **No channel yet:** on youtube.com, signed in, the profile picture menu has "Create a channel".
  The flow asks for the name and the handle - use the chosen ones.
- **Their Google account already has a personal channel** and this one should be separate: YouTube
  settings, "Add or manage your channel(s)", "Create a new channel". It gets its own name and handle,
  and can have other managers later.
- **The channel already exists:** YouTube Studio, Customization, Basic info, Handle.

YouTube moves these menus around; if a label does not match, say what to look for rather than
insisting on the path. Creating the channel publishes nothing - it is an empty channel until the
first upload - but it is the user's action, not this skill's.

## What to write

Into `## Name and handle` of `channel.md`: the chosen name and handle, the date it was checked, two
backups with their handles (in case it is gone by the time they claim it), the rejected names and
why, and the notes for the next steps - the name's tone feeds `/yt-voice`, its length and shape feed
the logo in `/yt-brand`. `status: locked` once the handle is actually claimed, not before.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
