# channel.md

The channel before it exists. Lives at `.claude/youtube/channel.md` inside the channel's project
folder, next to `voice.md`. One file per channel. Each from-zero skill writes its own section and
reads the ones before it, so a section left `pending` is where the next run picks up.

A status is `pending`, `unvalidated` (brought by the user, not checked), `review` (something it
depends on changed) or `locked`. `/yt-launch` reads them to know where you are.

Do not edit a `locked` section by hand and expect the others to follow - re-run the skill that owns
it, so whatever depends on it gets flagged.

## Niche
status: pending   <!-- owner: /yt-niche -->

## Sub-niche
status: pending   <!-- owner: /yt-niche -->

## Reference channels
status: pending   <!-- owner: /yt-refs -->

## Name and handle
status: pending   <!-- owner: /yt-name -->

## Voice and style
status: pending   <!-- owner: /yt-voice, writes voice.md and style.md -->

## Brand
status: pending   <!-- owner: /yt-brand -->

## About
status: pending   <!-- owner: /yt-about -->
