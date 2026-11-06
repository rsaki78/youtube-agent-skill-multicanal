---
name: yt-refs
description: >-
  Find the reference channels for a new or young YouTube channel - the
  aspirational ones, the peers growing at your size, and the adjacent ones
  ideas get borrowed from - and say what to take from each. Use for "find
  channels like mine", "who should I study", "reference channels",
  "competitors", or after /yt-niche. En español: "canales de referencia",
  "canales como el mío", "a quién estudio".
---

# yt-refs

A reference channel is not a channel you admire. It is one you can learn something specific from
this month. The list needs three kinds, and most people only collect the first:

- **Aspirational, one or two.** Big channels that define the format in the sub-niche. Take the
  packaging and the production bar. Do not take their cadence or their budget.
- **Peers, three to five.** Small or mid channels that broke out recently. The most useful ones,
  because what worked for them worked at your size, with your resources.
- **Adjacent, one to three.** Same viewer, different topic - or same format, different niche. This is
  where the ideas nobody in your niche has done yet come from.

```bash
python3 refs.py .claude/youtube/research/refs/ --small 50000
python3 refs.py .claude/youtube/research/refs/ --rows > refs-rows.json
python3 ../yt-viral/swipe.py refs-rows.json --min 2.0
```

On Windows, if `python3` is not found, run the same line with `py` or `python`.

## Before you start

1. Read `.claude/youtube/channel.md` in the current project. Each channel lives in its own project
   folder, so never read or write `~/.claude/youtube/`. This needs `## Sub-niche` filled. If it is
   not, run `/yt-niche` first - or, if the user already knows, get the sub-niche in one line and
   mark it `unvalidated` in the file.
2. Never invent a number, a result or a source. Subscriber counts, views and dates come from what
   was collected, never from memory.

## Finding them

1. **Start from what exists.** The channels collected under `research/niche/` and
   `research/subniche/` by `/yt-niche` are the first candidates. Copy the relevant ones into
   `research/refs/`.
2. **Ask the user** which channels they already watch in this space. Their own taste is a source,
   and a reference they do not enjoy watching will not get studied.
3. **Search** the queries the viewer would type, in the viewer's language:
   `yt-dlp "ytsearch30:<query>" --flat-playlist -J`. For adjacent ones, search the viewer's OTHER
   problems, not this topic.
4. **Collect** ten to fifteen candidates, each into `research/refs/<handle>.json`:
   ```bash
   yt-dlp "https://www.youtube.com/@handle/videos" --flat-playlist --playlist-end 30 \
          --extractor-args "youtubetab:approximate_date" -J > .claude/youtube/research/refs/<handle>.json
   ```

**Read, do not scrape.** Public listings only, never a logged-in session, never the user's
credentials. No yt-dlp: `pip install yt-dlp`, or the plain list in `refs.py` written by hand.

## Reading refs.py

Per channel: size band, median views, **reach** (median views over subscribers - an audience that
still watches), **out%** (share of videos at 2x its own median or better), uploads a month, the
longest gap and the days since the last upload. It flags dormant channels. A dormant channel can
still be aspirational; it cannot be a peer.

Then the tiers. Size band is a start, not the answer - the role is a judgement:

- A **peer** is small or mid, has an outlier in the last six months, is alive, and is made the
  same way - the `format:` in `## Niche`. A faceless channel learns little about holding attention
  from someone whose face does it for them.
- **Aspirational** is big, and actually sets the format - not just big in the parent niche.
- **Adjacent** is never decided by the numbers. Say why the viewer overlaps.

Then `swipe.py` across the chosen set, for which title formulas the outliers used. The formula is a
judgement about the title, not a claim about why it worked - say so when you present it.

## What to hand back

Six to ten channels, a table: name and handle, tier, size, the top outlier with its multiple, and
two lines each -

- **Take:** one specific thing. "Titles open with the amount in pesos." "Cold open on the result,
  intro after." Never "good energy" or "great editing".
- **Leave:** what not to copy, and why it would not work at this size.

Then the ONE structural thing the peers share. Then their visual conventions, for `/yt-brand`: face
or symbol in the avatar, banner style, colour - what the niche looks like, so the user can choose to
match it or stand out on purpose.

## What to write

Into `## Reference channels` of `channel.md`: the table, the take/leave lines, the shared pattern,
the visual conventions, and **the date collected**. Peers change fast - suggest re-running in three
months. Mark it `status: locked` once the user agrees. Next step: `/yt-name`.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
