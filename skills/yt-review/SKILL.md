---
name: yt-review
description: >-
  Review a finished script before production spends anything on it -
  title and thumbnail text, the hook, and whether the title and the first
  sentence promise the same thing - for channels whose scripts come out of
  a pipeline. Use for "review this script", "check the script before
  production", "/yt-review <code>". En español: "revisa el guion", "revisa
  antes de producir", "checa el guion".
---

# yt-review

The cheapest moment to fix a video is before the voice and the images exist. After that, every
change costs a regeneration. This runs the packaging and the hook against a finished script while
changing them is still free - and touches nothing else.

It orchestrates `/yt-package` and the hook step of `/yt-script`. It does not repeat their rules;
it follows them.

## Before you start

1. Read `.claude/youtube/channel.md`, `voice.md` and `style.md` in the current project; never
   `~/.claude/youtube/`. From them: `language:`, the address, the pace, `Thumbnail words:`, and
   anything `voice.md` says the channel will not claim. Read `.claude/youtube/plan.md` too if it
   exists - the video's slot in the plan.
2. Read `.claude/youtube/pipeline.md` if it exists: where the script is, its format, the sources
   file.
   No `pipeline.md`: offer once to create it - see **Setting up pipeline.md** below. If they say
   no, ask for the script and the sources, or work on what is pasted,
   and do not offer again this session.
3. Find the video by its code. Read the script and its sources file whole.
4. Never invent a number, a result or a source. **A fact that is not in the sources file does not
   go in** - not in the title, not in the hook, not in the thumbnail.

## Setting up pipeline.md

Start from `../yt-launch/templates/pipeline.md`. Fill in what the project already shows - the
video folders and how they are named, the script's markers read off a real script, the sources
file, the subtitle and audio files in an edited video's folder - and ask the rest in one message:
where the script lives and whether Claude can write to it, where the output goes, what has to be
updated after publishing. Show the file and write it to `.claude/youtube/pipeline.md` only when
they agree. Never guess a path that is not in the project; leave it empty and say so.

## The review

1. **Title and thumbnail.** Run the `/yt-package` flow on the script's own title and thumbnail
   text: `title.py` with `--lang` and `--thumb-max`, then ten alternatives against the same rules.
   Keep the script's title in the comparison; it may win.
2. **The hook.** The first sentence or two of the narration. Score it with `hookscore.py`, with
   `--lang`, `--wpm` and `--address none` if the voice is third person. Then write four
   alternatives the `/yt-script` way and score them too. Keep the current one in the comparison.
3. **The promise.** Title, thumbnail and first sentence must promise the same thing. If the title
   says one story and the hook opens another, that is the finding, ahead of any score.
4. **The facts.** Every name, date and figure in what you propose, checked against the sources
   file. Whatever is not there is listed under "needs a source", not used.

## The rules

- **Do not rewrite the script.** Title, thumbnail text, the hook. Anything else you notice goes in
  the review list as a note, not as a change.
- **Keep the channel's address** and whatever the script marks as a reconstruction or a
  dramatisation - a reconstructed scene stays marked as one.
- **Keep the format intact.** The pipeline parses the script; a moved marker breaks production.
  Write every change in the script's own format, field by field, so it can be pasted in place.

## What to hand back

- The changes, each as the exact line from the script and its replacement, in the script's format,
  ready to paste. If `pipeline.md` says `access: read-only`, say that the change goes into the
  original - production reads that one, not a copy.
- The scores: current title and hook against the best alternative, with the reason in a line.
- **Needs a source**: every fact you wanted and could not find in the sources file.
- **Notes**: anything else, for the creator to decide.

## The gate

Nothing here publishes or starts production. This skill writes and you decide. Every output ends
in a block the user copies, and the last line of every run is the question: **ship it, or change
it?**
