---
name: yt-niche
description: >-
  Choose the niche, then the sub-niche, for a YouTube channel that does
  not exist yet - validated against whether small channels are still
  breaking out, not against what sounds good. Use for "what should my
  channel be about", "pick a niche", "find a sub-niche", "is this niche
  saturated", or starting a channel from zero. En español: "qué nicho
  elijo", "de qué hago mi canal", "busca un subnicho", "está saturado este
  nicho".
---

# yt-niche

A niche is not a topic you like. It is a topic you can make a hundred videos about, for a person
who is already looking for it, where small channels are still breaking out. Most people choose on
the first and never check the other two.

Two passes: the niche, then the sub-niche inside it. Do not let the user skip to the sub-niche
because they "already know" - ask what they ruled out and why. If the answer is nothing, they have
not chosen, they have defaulted.

```bash
python3 room.py .claude/youtube/research/niche/      # is there room, candidate by candidate
```

## Before you start

1. Read `.claude/youtube/channel.md` in the current project. If it does not exist, create it from
   `../yt-launch/templates/channel.md`. Never read or write `~/.claude/youtube/`; each channel lives
   in its own project folder. If `## Niche` is already `locked`, ask whether they are revisiting it
   before touching it - everything after it was built on that line.
2. Never invent a number, a result or a source. That includes RPM: it moves with country, language
   and audience, and a confident figure from memory is the most common lie in niche advice. Quote
   one only from a source found this session, with its date, or from the user.

## Pass 1 - the niche

### The interview

Five questions, in one message, then wait:

1. What could you make a hundred videos about without running out? Three to five, half-serious ones
   included.
2. What do you know, do, or have access to that most people do not - job, trade, place, equipment,
   people?
3. On camera, their own voice without their face, a narrator, or an AI voice? And how many hours a
   week, honestly?
4. Who is it for - which language, which country or region?
5. What is the channel for: ad revenue, selling something of your own, authority for a business, or
   because you want to make it?

### The candidates

At most five, written as **topic for a person**, never a single word. "Finance" is a category.
"Personal finance for freelancers" is a niche. Then a table, every score with its one-line reason:

| | what it measures | how |
| --- | --- | --- |
| **Stamina** | the hundred-video test | Draft twenty titles. Ask which they would actually make. Under ten is a 2. |
| **Edge** | why them | From answer 2. "I like it" is a 1. |
| **Demand** | someone is looking | Search the queries the viewer would type, in the viewer's language. Real channels getting real views, or not. |
| **Room** | a new channel can get in | `room.py`, below. Never scored from memory. |
| **Money** | it pays the way they need it to | Against answer 5. Look at what the top channels sell, who sponsors them, what is in their descriptions. |

Answer 3 is also the channel's **format**, and every later skill reads it: write it into
`## Niche` as `format: camera`, `voice`, `narrator` or `ai-voice`. Faceless - the last three -
moves the work from the camera to the visuals, so count the hours for those, and judge Edge on
what the channel can show, not on who is in front of it.

The hours are a gate, not a score. A niche that needs forty hours a video for someone with five a week
is out, however well it scores.

### Room - measured

Collecting is the expensive part, so only the top three candidates get it.

1. **Discover.** Two or three queries per candidate, in the viewer's language:
   `yt-dlp "ytsearch30:<query>" --flat-playlist -J > .claude/youtube/research/discover-<slug>.json`.
   Pick six to ten channels per candidate, and **deliberately include small ones** - a sample of only
   big channels says "top-heavy" about every niche on earth.
2. **Collect** each channel into the candidate's folder:
   ```bash
   yt-dlp "https://www.youtube.com/@handle/videos" --flat-playlist --playlist-end 30 \
          --extractor-args "youtubetab:approximate_date" -J \
          > .claude/youtube/research/niche/<candidate-slug>/<handle>.json
   ```
3. **Run** `room.py` on the `niche/` folder.

No yt-dlp: `pip install yt-dlp`, or write the plain list from the public pages by hand - the format is
in `../yt-refs/refs.py`. **Read, do not scrape.** Public listings only, never a logged-in session,
never the user's credentials.

Reading it: **open** means small channels broke out, recently. **Narrow door**, one did, a while
ago. **Top-heavy**, only the established ones get outliers. **Flat**, nothing beats its own median.
Show the example outliers it prints - a 6k-subscriber channel with a 10x video is the most
persuasive line in this whole skill. And say what it is: a heuristic about the channels collected,
not a market size.

### The pick

Recommend ONE, with the reason in a sentence, and name the runner-up. The user decides. Write it
down before moving on.

## Pass 2 - the sub-niche

Narrow the chosen niche on **one or two** of these axes, never all four:

- **Who** - a stage, a job, an age, a place. "Freelancers paid in dollars, living in Mexico."
- **When** - the situation that makes them search. "The first year after quitting."
- **How** - a method, a constraint, a persona. "With under 100 dollars a month."
- **Format** - how it is made. "Spreadsheet walkthroughs, screen only."

Three to five sub-niches, then the tests:

- **The one person.** Can you describe the viewer as specifically as `voice.md` will ask? If not,
  it is not narrow yet.
- **Too narrow.** Fewer than thirty titles come out, or the queries return almost nothing. Widen.
- **Too broad.** The big channels in the room output already own it exactly. Narrow.
- **The door back out.** Can it widen into the parent niche later without a rename? A sub-niche so
  narrow it traps the channel name is the most expensive mistake in this whole phase. Say so in the
  notes for `/yt-name`.

Run the top one or two through `room.py` the same way, into `research/subniche/<slug>/` - most of
the channels can be copied from the niche pass. Then draft the first ten video titles for the
winner. Not a plan. A proof that the channel has a first month.

## What to write

Into `## Niche` and `## Sub-niche` of `channel.md`, each ending `status: locked` once the user agrees:

- The one-line statement - topic for a person.
- The `format:` line.
- The viewer, in a sentence.
- The scores table and the room verdict, **with the date the data was collected**.
- What was ruled out and why, so nobody relitigates it in three weeks.
- The ten titles.
- The channels collected, by folder - `/yt-refs` starts from them.
- Anything `/yt-name` needs to know: how wide the name must stay.

## What to hand back

The scored table, the room verdicts with their examples, the recommendation in one line, and the
next step: `/yt-refs`.

## The gate

Nothing here publishes. This skill writes and you publish. Every output ends in a block the user
copies, and the last line of every run is the question: **ship it, or change it?**
