# The YouTube agent skill

Twenty Claude skills for a YouTube channel: seven that take it from nothing to ready for its first
upload, eleven that run it once it exists, and two for channels whose videos come out of a
production pipeline. Free, MIT, no signup, no API key, nothing to connect.

One of them writes your script off 21 hook formulas and scores the hook before you waste a take on
it. One lints the title and the thumbnail as a single pairing, because writing them separately is
why half of your click surface says the same thing twice. One reads your audience-retention export
and tells you the exact second people left and what you were saying when they did. One turns a
transcript into an edit decision list. One finds the Shorts already hiding inside a long video. One
goes and finds what is working in your niche and ranks it by how far each video beat its own
channel, not by how big the channel is.

And if there is no channel yet, `/yt-launch` builds one in order: the niche and sub-niche, checked
for whether small channels still break out there; the reference channels; five names with handles
checked against YouTube; the voice, measured from a recording of you talking; the logo and banner,
previewed at the size people actually see them; and the description.

**Nothing gets published until you do it.** These skills write. You upload.

## Install

This is the multi-channel fork of [Jake Schincariol's YouTube agent skill](https://github.com/Jakeschincariol/youtube-agent-skill).
Each channel lives in its own project folder, and everything about it - `channel.md`, `voice.md`,
`style.md`, the research, the brand files - lives in that folder's `.claude/youtube/`. The skills are
the same for every channel; where you install them is up to you.

Open Claude Code in the channel's folder and paste this:

```
https://github.com/rsaki78/youtube-agent-skill-multicanal

Install the skills from this repo into .claude/skills/ of the current project, not into
~/.claude/skills/, then confirm /yt-launch works.
```

Or do it yourself, per channel:

```bash
git clone https://github.com/rsaki78/youtube-agent-skill-multicanal.git
mkdir -p <channel-folder>/.claude/skills
cp -r youtube-agent-skill-multicanal/skills/yt-* <channel-folder>/.claude/skills/
```

Or as a plugin. Run it from the channel's folder with `--scope project` to keep it to that channel,
or leave the scope out to install it once for every project - the channel's data stays per folder
either way:

```bash
claude plugin marketplace add rsaki78/youtube-agent-skill-multicanal
claude plugin install youtube-agent-multicanal@youtube-agent-skill-multicanal --scope project
```

The first skill that needs `.claude/youtube/channel.md` or `voice.md` creates it from the templates
in [`skills/yt-launch/templates/`](skills/yt-launch/templates/).

The tools are run as `python3`. On Windows, if that command does not exist, use `py` or `python`.

No Claude Code at all? Paste any single `SKILL.md` at the top of a chat and it runs as a mode. You lose the twelve
Python tools, which is most of the point of `/yt-script`, `/yt-retention` and `/yt-edit`, but the
rest works.

Then spend ten minutes on [`voice.md`](skills/yt-launch/templates/voice.md). Fill in the channel's
`.claude/youtube/voice.md`, or open Claude Code in the channel folder, send it three of the channel's
videos and say "write my voice.md from these". Every skill reads that file, and only the one in the
current project, so two channels never share a voice. It matters more here than anywhere else,
because you have to say the words out loud. No videos yet? `/yt-voice` writes it from a two-minute
recording of you explaining something to a friend.

## Starting from zero

Run `/yt-launch` and it walks these in order, keeping its place in `.claude/youtube/channel.md` so
it can take a week of evenings. Each one also runs on its own. First time? The walkthrough, in
Spanish, is [`docs/empezar-desde-cero.md`](docs/empezar-desde-cero.md).

| command | what it does |
| --- | --- |
| `/yt-launch` | Where you are, what is next, and the step itself. Picks up where you stopped. |
| `/yt-niche` | Niche, then sub-niche, scored, with room measured: are small channels breaking out there, recently? |
| `/yt-refs` | Reference channels in three tiers - aspirational, peers at your size, adjacent - and what to take from each. |
| `/yt-name` | Five names of different kinds, each with a handle linted against YouTube's rules and checked against what is taken. |
| `/yt-voice` | `voice.md` measured from you talking, and `style.md`: format, cadence, pillars, the numbers worth watching. |
| `/yt-brand` | Palette, logo and banner as prompts for any image generator, previewed at desktop, mobile, TV and comment size. |
| `/yt-about` | The channel description in 1,000 characters, linted, and the rest of the Studio setup. |

## Running the channel

| command | what it does |
| --- | --- |
| `/yt-script` | One idea into a script. Five hooks off [21 formulas](skills/yt-script/hooks.json), scored, then the spoken script with the retention beats marked. |
| `/yt-package` | Title and thumbnail as one pairing, linted for truncation, duplication and vagueness. |
| `/yt-edit` | A transcript into an edit decision list: dead air, filler cues, retakes, with timecodes. |
| `/yt-comment` | The comment section triaged into four piles, then replies in your voice. Says which one to pin. |
| `/yt-plan` | A week that fits the hours you actually have. One anchor, one cheap one, three Shorts. |
| `/yt-viral` | What is working in your niche, ranked by multiple over each channel's own median. |
| `/yt-retention` | Your retention export read properly: hook leak, the cliffs, the slide, and what to change. |
| `/yt-shorts` | The Shorts already inside a long video, with a new first line written for each. |
| `/yt-seo` | The description, the tags that are worth having, and the three queries this should win. |
| `/yt-chapters` | Chapters from a transcript, validated against YouTube's own rules so they render. |
| `/yt-audit` | The whole channel, ending in ONE fix rather than twenty. |

## With a pipeline

For a channel whose scripts and audio come out of n8n, Make or a script of your own. Optional: they
read `.claude/youtube/pipeline.md` - where the script lives, its format, the sources file, what
to update after publishing ([template](skills/yt-launch/templates/pipeline.md)) - and without it
they work on what you paste.

| command | what it does |
| --- | --- |
| `/yt-review` | Before production: title, thumbnail and hook against a finished script, every fact checked against the sources. Changes nothing else. |
| `/yt-ship` | After the edit: chapters, description, tags and Shorts in one file in the video's folder. |

## The twelve tools

Every one of these runs on a clean Python 3 with no dependencies. They are the reason the skills are
not just prompts.

```bash
python3 skills/yt-script/hookscore.py --hook "one line"        # 5-property hook panel
python3 skills/yt-package/title.py --title "..." --thumb "..." # title + thumbnail linter
python3 skills/yt-edit/deadair.py transcript.srt               # edit decision list
python3 skills/yt-chapters/chapters.py transcript.srt          # validated chapters
python3 skills/yt-retention/retention.py retention.csv         # where they left, and why
python3 skills/yt-viral/swipe.py collected.json --min 2.0      # outliers by own-channel multiple
python3 skills/yt-niche/room.py research/niche/                # is there room, niche by niche
python3 skills/yt-refs/refs.py research/refs/                  # reference channels profiled
python3 skills/yt-name/handle.py "Channel Name" --check        # handles, linted and looked up
python3 skills/yt-voice/voiceprint.py voicetest.srt            # how you actually talk
python3 skills/yt-brand/brandkit.py --name "..." --palette ... # logo, banner and palette preview
python3 skills/yt-about/about.py description.txt               # channel description linter
```

The tools that read words - hooks, titles, chapters, cuts, formulas - work in English and Spanish.
The channel's `language:` in `channel.md` (`es-MX`, `en-US`...) is set at `/yt-niche` and passed
to them as `--lang`; the word lists live in one place, [`skills/yt-voice/lang.py`](skills/yt-voice/lang.py),
so another language is a list away.

`room.py` and `refs.py` read what `yt-dlp` collects. yt-dlp is the one outside tool the from-zero
research uses; the twelve tools themselves still need nothing but Python.

## The fine print

The part most packs leave out.

**It does not publish.** YouTube's Data API would allow it with your own OAuth, which makes this
pack different from the LinkedIn and Instagram ones, where posting is not available at all. It is
still not built here: every skill ends in a block you copy and a question — ship it, or change it?
Anything that claims to run your channel unattended should be read with that distinction in mind.

**`hookscore.py` is a heuristic, not a predictor.** The panel was built and calibrated against 74
real short-form hooks (the first 15 seconds of auto-captions, top-8 and bottom-8 by views across
five channels). It separates deliberately bad hooks from real ones well. It separates a given
creator's hits from their own misses barely at all. A low score is a reason to look again; a high
score is not a promise. The Spanish lists were written, not calibrated: no Spanish sample has been
measured the same way yet.

**The formula classifier is about the words, not the result.** When `/yt-viral` says a title used
The Statistic, that is a judgement about the title you can see, not a claim about why the video got
its views.

**`/yt-viral` reads, it does not scrape.** Public listings only. It never logs in as you and never
touches your credentials.

**`room.py` is about your sample, not the market.** It says whether the small channels you collected
are breaking out. Collect only big channels and every niche looks closed.

**A free handle is a hint, not a reservation.** `handle.py --check` reads a 404 from
`youtube.com/@handle` as "probably free"; reserved and terminated handles 404 too. Studio has the
final word, and nothing here checks Instagram, TikTok or domains, because their pages hide behind
logins and any answer would be a guess.

**It does not make your logo.** `/yt-brand` writes the prompts and checks what comes back; the image
generator is yours to choose.

**Nobody can see why an AI answer cites a video.** `/yt-seo` makes the text around a search video
say its answer plainly - captions, title, chapters, description, pinned comment - because that is
what those answers read. It is a working rule, not a measured one, and the skill says so.

**Tags barely matter** and this pack says so instead of selling you a tag generator.

**Nothing invents a number.** If a skill wants a figure it does not have, it asks you for it or
writes the line without it.

## Licence

MIT. Use it, change it, ship it.
