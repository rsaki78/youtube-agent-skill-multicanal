---
name: yt-brand
description: >-
  Design a YouTube channel's look - palette, typeface, logo and banner -
  as prompts for any image generator, then check the results against
  YouTube's sizes and preview them where YouTube actually shows them. Use
  for "make my logo", "channel banner", "channel art", "profile picture",
  "brand colours", or after /yt-voice. En español: "hazme el logo",
  "banner del canal", "foto de perfil", "colores del canal".
---

# yt-brand

Nobody sees a channel's logo at the size it was designed. They see it at the size of a fingernail,
next to a comment, in a feed full of other fingernails. Design for that, then check the big version
still holds up.

```bash
python3 brandkit.py --name "Channel Name" --handle handle --palette "#0F172A,#F59E0B,#F8FAFC" \
                    --font "Poppins" --out .claude/youtube/brand/
python3 brandkit.py ... --logo logo.png --banner banner.png      # once they exist
```

On Windows, if `python3` is not found, run the same line with `py` or `python`.

It writes `preview.html` - the channel page at desktop, mobile and TV crops, the avatar from header
size down to comment size on light and dark, the palette with its contrast - and
`banner-template.svg` with the safe area drawn on a layer you hide before exporting. Before any image
exists it draws placeholders from the name and the palette, so the layout is judged first.

## Before you start

1. Read `.claude/youtube/channel.md` in the current project; never `~/.claude/youtube/`. This needs
   `## Name and handle`. It reads the visual conventions in `## Reference channels` - what the
   niche looks like - and the thumbnail rules in `.claude/youtube/style.md`.
2. Read `format:` in `## Niche`. With `camera`, ask: **is the creator's face the brand?** If yes,
   the profile picture is a photo, not a logo - tight crop, plain background in a brand colour.
   Faceless, there is no face to recognise, so the logo and the thumbnail style carry the whole
   identity: the logo has to be a mark people learn, and `style.md` needs a thumbnail signature
   that repeats - a colour, a layout, a character - so a viewer knows the channel before the title.
3. Never invent a number, a result or a source. YouTube's sizes are in the header of `brandkit.py`,
   from YouTube's own help page. Use those, not remembered ones.

## Directions first, images second

Two or three directions, never one:

- **Match** - looks like the niche, so the viewer knows what kind of channel it is at a glance.
- **Stand out** - deliberately unlike the references, so it is the one that gets noticed.
- **A third** only if the voice or the name points somewhere neither covers.

Each direction: a palette of three or four hex colours (background, accent, light), one typeface
from Google Fonts - free, and in every design tool - a logo concept in a line, the mood in a line.
Run each palette through `brandkit.py` before showing it: a pair under 3:1 never carries text, and say
so.

## The logo

- **One idea.** A symbol, or one or two letters. Never the full name - at 98 pixels it is noise.
- **Inside the circle.** YouTube crops to a circle. Keep the mark well inside it, nothing in the
  corners.
- **Survives small.** Check the 24 and 40 pixel versions in the preview. If you cannot tell what
  it is, simplify - do not add detail.
- **Works on light and dark.** The preview shows both. A dark edge vanishes on dark mode.

## The banner

- **Text and logo only inside the safe area.** Everything outside it is decoration that a phone
  never shows.
- **At most three things on it:** the name, a one-line promise, and the upload day - only if
  `style.md` has a cadence they actually keep. A banner promising Thursdays on a channel that
  posts monthly is worse than none.
- **Generate the art without text,** then put the text on with `banner-template.svg` - in Figma,
  Canva, Inkscape, anything that opens SVG. Image generators mangle letters and do not know where
  the safe area is.

## The prompts

Write them into `.claude/youtube/brand/prompts.md`, two per asset, ready to paste. Each prompt
carries: the subject, the style, the composition, the colours by hex and by name, and the
constraints - square for the logo, 16:9 for the banner, "no text, no letters, no watermark" for
the banner art, "centred, simple, readable as a tiny icon" for the logo. Note the tool-specific
form where it differs: Midjourney takes `--ar 16:9 --no text`; ChatGPT, Gemini and the rest take
it in plain words. If the logo must contain letters, say to use a generator known for rendering
text, and check every letter.

Generated images usually come back smaller than 2560x1440. `brandkit.py` flags it; upscale
before uploading.

## The loop

Re-run `brandkit.py` with the real files and open the preview. Three questions, in this order:
can you tell what the avatar is at comment size, does the banner text sit whole inside the mobile
crop, and does any of it disappear in dark mode. Fix, re-run, look again.

The template SVG names the font but cannot embed it; install the font to edit it. The preview's
placeholders fall back to a plain sans-serif for the same reason.

**Optional, if the HyperFrames `motion-graphics` skill is available here:** offer a three-to-five
second logo sting for the intro or the end screen, built from the final logo and palette. Never
required, never assumed to be installed.

## What to write

Into `## Brand` of `channel.md`: the chosen direction, palette, typeface, the paths to
`prompts.md`, the final logo and banner, and the date. Replace the `pending /yt-brand` colours and
type in `style.md`'s thumbnail rules with the real ones. Then the upload steps - YouTube Studio,
Customization, Branding - and an optional watermark: square, at least 150x150, under 1 MB.
`status: locked` once both are uploaded. Next step: `/yt-about`.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
