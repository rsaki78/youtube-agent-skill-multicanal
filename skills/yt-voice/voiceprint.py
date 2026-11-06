#!/usr/bin/env python3
"""voiceprint.py - measure how someone actually talks, from transcripts of them talking.

    python3 voiceprint.py voicetest.srt
    python3 voiceprint.py take1.txt take2.vtt podcast.srt --json
    python3 voiceprint.py voicetest.srt --against draft-script.txt

Input: .srt, .vtt or plain .txt - a voice test, an old video, a podcast, a voice note, anything
where they speak unscripted. Written text (posts, emails) measures how they write, which is not the
same thing, and the tool says so if you give it something with no timings and tidy punctuation.

What it measures:
  - pace, words a minute including pauses (timed input only)
  - sentence length, if the transcript is punctuated - auto-captions often are not, and then it
    says so instead of reporting one 900-word sentence
  - the phrases they repeat - their tics, which voice.md should keep
  - fillers, counted separately - the edit removes those, the script should not add them
  - how they address the viewer: tu, usted, vos, ustedes (Spanish) or you/we (English) - get this
    wrong in a script and it is unreadable on camera
  - I against we

--against scores a draft against the voiceprint: the same measures, side by side, and the phrases in
the draft that the speaker never used.
"""
import collections, json, os, re, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lang import STOP, FILLERS, fold  # noqa: E402  (one word list for the whole pack)

TIME = re.compile(r"(\d+):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d+):(\d{2}):(\d{2})[,.](\d{3})")
ADDRESS = {"tu": r"\b(tú|tienes|puedes|quieres|sabes|eres|estás|haces|necesitas|contigo)\b",
           "usted": r"\b(usted|ustedes)\b",
           "vos": r"\b(vos|tenés|podés|querés|sabés|sos|hacés|necesitás)\b",
           "vosotros": r"\b(vosotros|vosotras|tenéis|podéis|queréis|sabéis|sois)\b"}
PERSON = {"es": (r"\b(yo|me|mi|mis|conmigo)\b", r"\b(nosotros|nosotras|nuestro|nuestra|nuestros|nuestras)\b"),
          "en": (r"\b(i|me|my|mine)\b", r"\b(we|us|our|ours)\b")}

def read(path):
    raw = open(path, encoding="utf-8-sig", errors="replace").read()
    spans, text = [], []
    for line in raw.splitlines():
        m = TIME.search(line)
        if m:
            g = [int(x) for x in m.groups()]
            spans.append((g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000, g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000))
        elif line.strip() and not line.strip().isdigit() and not line.startswith(("WEBVTT", "NOTE", "Kind:", "Language:")):
            text.append(re.sub(r"<[^>]+>", "", line.strip()))
    if spans:   # auto-captions repeat rolling lines - keep each line once, in order
        text = [t for i, t in enumerate(text) if i == 0 or t != text[i - 1]]
    secs = (max(e for _, e in spans) - min(s for s, _ in spans)) if spans else None
    return " ".join(text), secs

def lang(words):
    words = [fold(w) for w in words]
    es = sum(w in STOP["es"] for w in words); en = sum(w in STOP["en"] for w in words)
    return "es" if es >= en else "en"

def count(pattern, text):
    return len(re.findall(pattern, text, re.I))

def dedupe(grams):
    """Longest form of each repeated phrase: "hoja de calculo" (5), not also "hoja de" (5) and
    "una hoja de calculo" (3)."""
    keep = []
    for g, c in sorted(grams, key=lambda x: (-x[1], -len(x[0]))):
        if not any((g in k or k in g) and c <= kc for k, kc in keep): keep.append((g, c))
    return keep

def profile(text, secs=None):
    low = text.lower()
    words = re.findall(r"[\wáéíóúüñ']+", low)
    if not words: return None
    lg = lang(words)
    p = {"language": lg, "words": len(words), "minutes": round(secs / 60, 1) if secs else None,
         "wpm": round(len(words) / (secs / 60)) if secs else None}
    marks = len(re.findall(r"[.!?¿¡]", text))
    if marks >= len(words) / 40:
        sents = [s for s in re.split(r"(?<=[.!?])\s+", text) if re.search(r"\w", s)]
        lens = [len(re.findall(r"[\wáéíóúüñ']+", s)) for s in sents]
        p["sentence_median"] = statistics.median(lens)
        p["sentence_long_share"] = round(sum(l > 25 for l in lens) / len(lens), 2)
        p["questions_share"] = round(sum(s.strip().endswith("?") for s in sents) / len(sents), 2)
    else:
        p["sentence_median"] = None
    fill = {f: count(r"(?<!\w)" + re.escape(f) + ("" if f.endswith("?") else r"(?!\w)"), fold(low)) for f in FILLERS[lg]}
    p["fillers_per_100"] = round(100 * sum(fill.values()) / len(words), 1)
    p["fillers"] = {k: v for k, v in sorted(fill.items(), key=lambda x: -x[1]) if v}
    if lg == "es":
        p["address"] = {k: count(v, low) for k, v in ADDRESS.items() if count(v, low)}
    else:
        p["address"] = {"you": count(r"\byou\b|\byour\b", low)}
    me, we = PERSON[lg]
    p["i_vs_we"] = [count(me, low), count(we, low)]
    grams = collections.Counter()
    for n in (2, 3, 4):
        for i in range(len(words) - n + 1):
            g = words[i:i + n]
            if all(fold(w) in STOP[lg] for w in g): continue
            grams[" ".join(g)] += 1
    p["phrases"] = dedupe([(g, c) for g, c in grams.items() if c >= 3 and g not in FILLERS[lg]])[:15]
    p["grams"] = grams
    return p

def show(p, title):
    print(f"\n  {title}   [{p['language']}]  {p['words']:,} words" + (f", {p['minutes']} min, {p['wpm']} wpm with pauses" if p["wpm"] else ""))
    if p["sentence_median"] is not None:
        print(f"    sentences  median {p['sentence_median']} words, {p['sentence_long_share']:.0%} over 25, {p['questions_share']:.0%} questions")
    else:
        print("    sentences  not measured - the transcript is barely punctuated (auto-captions?)")
    print(f"    fillers    {p['fillers_per_100']} per 100 words  " + ", ".join(f"{k} {v}" for k, v in list(p["fillers"].items())[:6]))
    print(f"    address    " + (", ".join(f"{k} {v}" for k, v in p["address"].items()) or "nobody addressed directly"))
    print(f"    I / we     {p['i_vs_we'][0]} / {p['i_vs_we'][1]}")
    if p["phrases"]:
        print("    repeats    " + "  |  ".join(f"{g} ({c})" for g, c in p["phrases"]))

def main():
    a = sys.argv[1:]
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    draft = a[a.index("--against") + 1] if "--against" in a else None
    files = [x for i, x in enumerate(a) if not x.startswith("--") and x != draft]
    files = [f for f in files if os.path.exists(f)]
    if not files: print(__doc__); sys.exit(1)
    texts, secs = zip(*(read(f) for f in files))
    timed = [s for s in secs if s]
    p = profile(" ".join(texts), sum(timed) if len(timed) == len(secs) else None)
    if not p: print("  no words found"); sys.exit(1)
    d = None
    if draft:
        d = profile(read(draft)[0])
        d["foreign"] = [g for g, _ in dedupe([(g, c) for g, c in d["grams"].items() if c >= 2 and g not in p["grams"]])][:12]
    if "--json" in a:
        out = {k: v for k, v in p.items() if k != "grams"}
        if d: out["draft"] = {k: v for k, v in d.items() if k != "grams"}
        print(json.dumps(out, indent=1, ensure_ascii=False)); return
    show(p, "speaker")
    if not timed: print("    no timings - if this is writing, not speech, it measures how they write. Not the same voice.")
    if p["words"] < 300: print(f"    only {p['words']} words - record more before trusting any of this")
    if d:
        show(d, "draft")
        if d["foreign"]: print("    never said " + "  |  ".join(d["foreign"]))
        pa, da = max(p["address"], key=p["address"].get, default=None), max(d["address"], key=d["address"].get, default=None)
        if pa and da and pa != da: print(f"\n  the speaker says {pa}, the draft says {da}. Fix that first.")
    print()

if __name__ == "__main__":
    main()
