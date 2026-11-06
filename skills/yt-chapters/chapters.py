#!/usr/bin/env python3
"""chapters.py - YouTube chapters from a timestamped transcript.

    python3 chapters.py transcript.srt            # or .vtt / whisper .json
    python3 chapters.py transcript.srt --target 8 --json
    python3 chapters.py transcript.srt --lang es-MX     # the channel's language: from channel.md
    python3 chapters.py transcript.srt --scenes scenes.json   # from timeline.py, or one time per line

Prints a description block you can paste straight under a video. YouTube's own rules, enforced here
rather than assumed: the list must start at 00:00, needs at least three entries, and each chapter
must be at least 10 seconds long. A block that breaks any of those silently does not become
chapters, which is why this checks instead of trusting.

Boundaries come from the gaps - the pauses you actually took between sections - scored by how long
the pause was and how much the vocabulary changes across it. It is a first draft you retitle, not a
summariser. With --scenes, only scene starts are candidates: in a video built scene by scene, a
chapter that starts mid-scene is wrong however good the pause looks. The draft titles leave out the language's small words - English or Spanish, from --lang
or guessed from the transcript - and keep the accents as spoken.
"""
import collections, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "yt-edit"))
sys.path.insert(0, os.path.join(HERE, "..", "yt-voice"))
from deadair import load, parse_ts  # noqa: E402  (same parser, one implementation)
from lang import STOP as LANG_STOP, pick, tokens, utf8_out  # noqa: E402

STOP = set("the a an of for to in on and or is are was were be been with this that it as at by from "
           "you your i my we our they them he she but so if then than there here what which who how "
           "when where why not no yes do does did just really very like about into over out up down "
           "can could will would should have has had get got make made go going went one two".split())

# Spanish adds the words that are long enough to pass the four-letter cut and still say nothing
STOP_ES = LANG_STOP["es"] | set("""para donde cuando como porque sobre entre hasta desde durante
 todo toda todos todas esos esas este esta estos estas aquel aquella usted ustedes ellos ellas
 nosotros habia hubo fueron eran estaba estaban tenia tenian sido estar hacer tener puede pueden
 dijo dice decir asi alla aqui alli ahora entonces luego despues antes nunca siempre tambien
 solo mismo misma mucho mucha muchos muchas poco otra otro otros otras cada algo nada hace hizo
 vamos tiene tienen quien quienes cual cuales mientras aunque segun pero sino ademas casi""".split())
L = "en"   # set from --lang in main()
SURFACE = collections.Counter()   # folded word -> how it was written, for the draft titles

def keywords(text):
    if L == "en":
        return {w for w in re.findall(r"[a-z']{4,}", text.lower()) if w not in STOP}
    out = set()
    for raw, w in tokens(text):
        if len(w) >= 4 and w not in STOP_ES and not w.isdigit():
            out.add(w); SURFACE[(w, raw.lower())] += 1
    return out

def written(w):
    if L == "en": return w
    forms = [(c, f) for (k, f), c in SURFACE.items() if k == w]
    return max(forms)[1] if forms else w

def mmss(t):
    t = int(t); h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def scene_starts(path):
    """Scene starts in seconds, from timeline.py's --json or a file with one time per line
    (seconds, m:ss or h:mm:ss)."""
    raw = open(path, encoding="utf-8-sig").read()
    if path.endswith(".json"):
        d = json.loads(raw)
        return sorted(float(s["start"]) for s in (d["scenes"] if isinstance(d, dict) else d))
    out = []
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]*)", line)
        if m: out.append(parse_ts(m.group(1)) if ":" in m.group(1) else float(m.group(1).replace(",", ".")))
    return sorted(out)

def main():
    global L
    utf8_out()
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    lang_given = "--lang" in a
    L, a = pick(a)
    target = int(a[a.index("--target") + 1]) if "--target" in a else 7
    scenes = None
    if "--scenes" in a:
        i = a.index("--scenes"); scenes = scene_starts(a[i + 1]); a = a[:i] + a[i + 2:]
    a = [x for x in a if not x.startswith("--") and not x.isdigit()]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cues = load(a[0])
    if len(cues) < 6: print("too few cues to chapter"); sys.exit(1)
    if not lang_given: L = pick([], " ".join(c[2] for c in cues))[0]
    dur = cues[-1][1]
    cand = []
    # each candidate is a time and the first cue at or after it
    if scenes:
        points = [(t, next((i for i, c in enumerate(cues) if c[0] >= t - 0.5), None)) for t in scenes]
        points = [(t, i) for t, i in points if i and t > 0]
    else:
        points = [(cues[i][0], i) for i in range(1, len(cues))]
    for t, i in points:
        gap = cues[i][0] - cues[i - 1][1]
        before = " ".join(c[2] for c in cues[max(0, i - 12):i])
        after = " ".join(c[2] for c in cues[i:i + 12])
        kb, ka = keywords(before), keywords(after)
        shift = 1 - (len(kb & ka) / len(kb | ka)) if (kb | ka) else 0
        cand.append((gap * 1.6 + shift * 3.2, t, i))
    cand.sort(reverse=True)
    picked, MIN = [0.0], 10.0
    for _, t, i in cand:
        if len(picked) >= target: break
        if all(abs(t - p) >= MIN for p in picked) and dur - t >= MIN:
            picked.append(t)
    picked.sort()
    chapters = []
    for n, t in enumerate(picked):
        end = picked[n + 1] if n + 1 < len(picked) else dur
        text = " ".join(c[2] for c in cues if c[0] >= t and c[1] <= end)
        kw = [w for w in keywords(text)]
        if L == "en":
            kw.sort(key=lambda w: (-text.lower().count(w), w))   # ties alphabetical, so a run repeats
        else:
            n = collections.Counter(w for _, w in tokens(text))
            kw.sort(key=lambda w: (-n[w], w))
        title = " ".join(written(w).capitalize() for w in kw[:3]) or "Section"
        chapters.append({"start": round(t, 2), "label": mmss(t), "draft_title": title,
                         "seconds": round(end - t, 2)})
    ok = len(chapters) >= 3 and chapters[0]["start"] == 0 and all(c["seconds"] >= MIN for c in chapters)
    if as_json:
        print(json.dumps({"valid": ok, "chapters": chapters}, indent=1)); return
    print()
    for c in chapters: print(f"  {c['label']} {c['draft_title']}")
    print(f"\n  {len(chapters)} chapters"
          f"{'' if ok else '  -- INVALID: YouTube needs 3+, a 00:00 first entry and 10s minimum each'}")
    print("  Retitle every line before pasting. These are the topic words, not your words.\n")

if __name__ == "__main__":
    main()
