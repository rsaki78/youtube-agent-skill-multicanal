#!/usr/bin/env python3
"""about.py - lint a channel description before it goes in the box.

    python3 about.py description.txt
    python3 about.py description.txt --keywords "finanzas,freelancers" --voice .claude/youtube/voice.md
    python3 about.py a.txt b.txt --json            # compare drafts

The box takes 1,000 characters. That is the only hard rule, and the tool counts it two ways - by
character and by UTF-16 unit, because an emoji is one character to you and may be two to a text
box. Past that, the things that make a description fail quietly:

  - the first line has to stand on its own: it is the part the channel header shows before "more",
    and the part that tells a stranger whether this channel is for them
  - the words the viewer would search should be in it, early - --keywords checks where they land
  - the same word five times is keyword stuffing, which YouTube's spam policy names outright
  - links belong in the links section (up to 14, the first one shown by the subscribe button),
    where they are clickable buttons, not in the text
  - "<" and ">" are rejected in YouTube descriptions
  - with --voice: the words voice.md bans, and the same address (tu, usted, vos) as the speaker
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "yt-voice"))
from voiceprint import ADDRESS, STOP, lang

LIMIT = 1000
URL = re.compile(r"(https?://\S+|www\.\S+|\b\S+\.(com|net|org|io|tv|co|mx|es|ar|cl|pe|app|me|ly)\b\S*)", re.I)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️]")

def voice_rules(path):
    t = open(path, encoding="utf-8").read()
    reg = re.search(r"\*\*(tú|tu|usted|ustedes|vos|vosotros)\*\*", t, re.I)
    sec = re.search(r"## Words I never use\s*\n(.*?)(\n## |\Z)", t, re.S)
    banned = []
    if sec:
        body = re.sub(r"<!--.*?-->", "", sec.group(1), flags=re.S)
        banned = [w.strip().strip('"“”\'').lower() for w in re.findall(r'"([^"]+)"|“([^”]+)”|^[-*]\s*(.+)$', body, re.M)
                  for w in w if w.strip()]
    r = reg.group(1).lower().replace("ú", "u") if reg else None
    return ("usted" if r == "ustedes" else r), banned

def lint(text, keywords=(), voice=None):
    t = text.strip()
    utf16 = len(t.encode("utf-16-le")) // 2
    first = t.splitlines()[0].strip() if t else ""
    words = re.findall(r"[\wáéíóúüñ']+", t.lower())
    lg = lang(words) if words else "es"
    r = {"chars": len(t), "utf16": utf16, "first_line": first, "errors": [], "warnings": [], "keywords": {}}
    if max(len(t), utf16) > LIMIT: r["errors"].append(f"{max(len(t), utf16)} characters - the box takes {LIMIT}")
    if "<" in t or ">" in t: r["errors"].append("contains < or > - YouTube rejects them in descriptions")
    if len(first) > 120: r["warnings"].append(f"first line is {len(first)} characters - the header cuts it; say who it is for and what they get, sooner")
    if len(t) < 200: r["warnings"].append("under 200 characters - room left for what the channel is, who is behind it, when it posts")
    for k in keywords:
        pos = t.lower().find(k.lower())
        r["keywords"][k] = pos
        if pos < 0: r["warnings"].append(f'"{k}" is not in it')
        elif pos > len(first): r["warnings"].append(f'"{k}" first appears at character {pos}, after the first line')
    counts = {}
    for w in words:
        if len(w) > 3 and w not in STOP[lg]: counts[w] = counts.get(w, 0) + 1
    stuffed = [f"{w} x{c}" for w, c in sorted(counts.items(), key=lambda x: -x[1]) if c >= 5]
    if stuffed: r["warnings"].append("repeated - reads as keyword stuffing: " + ", ".join(stuffed[:5]))
    urls = URL.findall(t)
    if urls: r["warnings"].append(f"{len(urls)} link(s) in the text - put them in the links section, where they are buttons")
    caps = list(dict.fromkeys(re.findall(r"\b[A-ZÁÉÍÓÚÑ]{4,}\b", t)))
    if len(caps) > 2: r["warnings"].append("shouting: " + ", ".join(caps[:5]))
    em = len(EMOJI.findall(t))
    if em > 5: r["warnings"].append(f"{em} emoji")
    if voice:
        reg, banned = voice
        low = t.lower()
        hits = [b for b in banned if b and re.search(r"(?<!\w)" + re.escape(b) + r"(?!\w)", low)]
        if hits: r["errors"].append("voice.md bans: " + ", ".join(hits))
        used = {k: len(re.findall(v, low, re.I)) for k, v in ADDRESS.items()}
        used = {k: v for k, v in used.items() if v}
        if reg and used and reg not in used:
            r["errors"].append(f"voice.md says {reg}, this says {max(used, key=used.get)}")
    return r

def main():
    a = sys.argv[1:]
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    kw = [k.strip() for k in (opt("--keywords") or "").split(",") if k.strip()]
    vpath = opt("--voice")
    voice = voice_rules(vpath) if vpath and os.path.exists(vpath) else None
    files = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--keywords", "--voice"))]
    files = [f for f in files if os.path.exists(f)]
    if not files: print(__doc__); sys.exit(1)
    out = {f: lint(open(f, encoding="utf-8").read(), kw, voice) for f in files}
    if "--json" in a: print(json.dumps(out, indent=1, ensure_ascii=False)); return
    if vpath and not voice: print(f"\n  {vpath} not found - voice checks skipped")
    for f, r in out.items():
        n = max(r["chars"], r["utf16"])
        print(f"\n  {os.path.basename(f)}   {n}/{LIMIT}" + (f"  ({r['chars']} characters, {r['utf16']} UTF-16 units)" if r["chars"] != r["utf16"] else ""))
        print(f"    first line  {r['first_line'][:110]}")
        for e in r["errors"]: print(f"    x {e}")
        for w in r["warnings"]: print(f"    - {w}")
        if not r["errors"] and not r["warnings"]: print("    clean")
    print()

if __name__ == "__main__":
    main()
