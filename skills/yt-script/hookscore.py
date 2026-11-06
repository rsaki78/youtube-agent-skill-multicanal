#!/usr/bin/env python3
"""hookscore.py - score a YouTube hook before you waste a take on it.

Five properties, 0-100 each, and a verdict that is 60% the mean and 40% the weakest one. The
weakest-link weighting is deliberate: a hook with four strong properties and one dead one is a hook
that leaks at the dead one, and averaging hides that.

    python3 hookscore.py hooks.txt            # one hook per line, ranked
    python3 hookscore.py --hook "one line"    # score a single hook
    python3 hookscore.py --json hooks.txt     # machine-readable
    python3 hookscore.py hooks.txt --lang es-MX --address none --wpm 127

--lang is the channel's `language:` (en or es; guessed from the text without it). --address none is
for a channel whose narrator never speaks to the viewer - third-person documentary, say: ADDRESS is
still shown but leaves the verdict, because a channel cannot be marked down every time for a rule
it chose not to follow. --wpm is the pace from voice.md; BREVITY's band moves with it.

WHAT THIS CAN AND CANNOT TELL YOU. Measured against 74 real short-form hooks (first 15 seconds of
auto-captions, top-8 and bottom-8 by views across five channels): it separates deliberately bad
hooks from real ones well, and it separates a creator's own hits from their own misses barely at
all. Treat a low score as a reason to look again, never a high score as a promise. The Spanish
lists were written, not calibrated: no Spanish sample has been measured the way the English one was.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "yt-voice"))
from lang import fold, pick, utf8_out, words as lang_words  # noqa: E402
FORMULAS = json.load(open(os.path.join(HERE, "hooks.json"), encoding="utf-8"))["hooks"]

FILLER = {"basically","actually","literally","just","really","very","so","kind","sort","like",
          "guys","hey","welcome","today","video","subscribe","channel"}
VAGUE = {"amazing","incredible","insane","crazy","huge","massive","game","changer","secret",
         "powerful","ultimate","best","revolutionary","mind","blowing","unbelievable"}
CONCRETE = re.compile(r"\b(\d[\d,.]*\s?(%|k|m|x|s|m|h)?|\$\d|\d+\s?(second|minute|hour|day|week|month|year)s?)\b", re.I)
YOU = re.compile(r"\b(you|your|you're|youre|yourself)\b", re.I)
STAKE = re.compile(r"\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead)\b", re.I)
CURIOSITY = re.compile(r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually)\b", re.I)
CLOSED = re.compile(r"\b(because|so that|which means)\b", re.I)

# Spanish: matched against the folded text (no accents), except curiosity, which needs them -
# "qué" and "cómo" ask, "que" and "como" do not.
SIGNALS = {
 "en": dict(filler=FILLER, vague=VAGUE, you=YOU, stake=STAKE, curiosity=CURIOSITY, closed=CLOSED,
            unit=None),
 "es": dict(
  filler={"hola","bienvenidos","bienvenido","bienvenida","hoy","video","suscribete","suscribanse",
          "canal","tema","basicamente","literalmente","realmente","simplemente","muy","pues","bueno",
          "quedate","final","veremos","hablaremos","vamos"},
  vague={"increible","impresionante","brutal","loco","locura","enorme","masivo","secreto","poderoso",
         "definitivo","mejor","revolucionario","alucinante","epico","interesante","sorprendente",
         "tremendo","fascinante","misterioso"},
  you=re.compile(r"\b(tu|tus|te|ti|contigo|usted|ustedes|vos|tienes|puedes|quieres|sabes|eres|haces|"
                 r"necesitas|imagina|imaginate|tenes|podes|sos)\b"),
  stake=re.compile(r"\b(perd\w*|pierde\w*|desperdici\w*|renunci\w*|fall\w*|fracas\w*|quiebra|"
                   r"cuest[ae]n?|cost\w*|riesgo\w*|antes|nunca|jamas|muri\w*|muert\w*|mor(ir|ia)\w*|"
                   r"mat(o|aron|ar|ado|ados)|asesin\w*|fusil\w*|quem\w*|ejecut\w*|tortur\w*|prohib\w*|"
                   r"conden\w*|castig\w*|desapare\w*|carcel|pres[oa]s?|peligr\w*|sangre|deja de|detente)\b"),
  curiosity=re.compile(r"(?<!\w)(qué|cómo|cuál|quién|quien|dónde|cuándo|por qué|hasta que|pero|nadie|"
                       r"casi|excepto|salvo|razón|en realidad|ni siquiera|sin saber|todavía|aún|"
                       r"lo que nadie|nunca supo|nunca supieron)(?!\w)", re.I),
  closed=re.compile(r"\b(porque|asi que|lo que significa|para que|por eso)\b"),
  unit=re.compile(r"\b\d+\s?(segundos?|minutos?|horas?|dias?|semanas?|mes|meses|anos?|siglos?)\b")),
}
L = "en"   # set from --lang in main()

def words(t):
    # English keeps its original tokens so its scores do not move; Spanish uses the shared folding
    return re.findall(r"[a-z0-9'%$.]+", t.lower()) if L == "en" else lang_words(t, keep="'%$.")

def text(t): return t if L == "en" else fold(t)

def specificity(t):
    w = words(t)
    if not w: return 0
    sg = SIGNALS[L]
    nums = len(CONCRETE.findall(t)) + (len(sg["unit"].findall(text(t))) if sg["unit"] else 0)
    vague = sum(1 for x in w if x in sg["vague"])
    filler = sum(1 for x in w if x in sg["filler"])
    s = 34 + nums * 22 - vague * 16 - filler * 5
    # proper nouns that are not sentence-initial read as named things
    s += min(18, 6 * sum(1 for x in t.split()[1:] if x[:1].isupper()))
    return max(0, min(100, s))

def address(t):
    you = SIGNALS[L]["you"]
    n = len(you.findall(text(t)))
    first = 30 if you.search(text(" ".join(t.split()[:6]))) else 0
    return max(0, min(100, 26 + n * 20 + first))

def stakes(t):
    n = len(SIGNALS[L]["stake"].findall(text(t)))
    return max(0, min(100, 22 + n * 26 + (14 if CONCRETE.search(t) else 0)))

def curiosity(t):
    n = len(SIGNALS[L]["curiosity"].findall(t))
    q = 18 if t.strip().endswith("?") else 0
    # a hook that resolves itself has no gap left
    closed = -18 if SIGNALS[L]["closed"].search(text(t)) else 0
    return max(0, min(100, 24 + n * 17 + q + closed))

WPM = 150   # set from --wpm in main()

def brevity(t):
    n = len(words(t))
    if n == 0: return 0
    # 9-24 words is the band a spoken hook lands in at ~150wpm inside 10 seconds; a slower narrator
    # gets a narrower band, a faster one a wider one
    lo, hi = round(9 * WPM / 150), round(24 * WPM / 150)
    if lo <= n <= hi: return 100
    if n < lo: return max(30, 100 - (lo - n) * 11)
    return max(10, 100 - (n - hi) * 7)

PROPS = [("SPECIFICITY", specificity), ("ADDRESS", address), ("STAKES", stakes),
         ("CURIOSITY", curiosity), ("BREVITY", brevity)]

def classify(t):
    best, hits = None, 0
    key, tt = ("match", t) if L == "en" else ("match_" + L, fold(t))
    for f in FORMULAS:
        n = sum(1 for p in f.get(key, []) if re.search(p, tt, re.I))
        if n > hits: best, hits = f, n
    return (best["name"] if best else "Unclassified"), hits

ADDRESS_OFF = False   # set from --address none in main()

def score(t):
    parts = {n: fn(t) for n, fn in PROPS}
    vals = [v for k, v in parts.items() if not (ADDRESS_OFF and k == "ADDRESS")]
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    name, hits = classify(t)
    return parts, verdict, name, hits

def band(v): return "STRONG" if v >= 72 else "WORKABLE" if v >= 55 else "WEAK"

def report(t, parts, verdict, name, hits):
    print(f"\n  {t.strip()}")
    print(f"  {'-' * min(72, max(20, len(t.strip())))}")
    for k, v in parts.items():
        off = ADDRESS_OFF and k == "ADDRESS"
        print(f"    {k:<12} {v:3d}  {'#' * (v // 5)}" + ("  (off - not in the verdict)" if off else ""))
    print(f"    {'VERDICT':<12} {verdict:3d}  {band(verdict)}")
    print(f"    formula      {name}" + (f"  ({hits} pattern{'s' if hits != 1 else ''} matched)" if hits else "  (no formula matched - that is usually a summary, not a hook)"))
    counted = {k: v for k, v in parts.items() if not (ADDRESS_OFF and k == "ADDRESS")}
    low = min(counted, key=counted.get)
    fix = FIX_ES.get(low, FIX[low]) if L == "es" else FIX[low]
    print(f"    weakest      {low} - {fix}")

FIX = {
 "SPECIFICITY": "swap one adjective for a number, a name or a date",
 "ADDRESS": "say 'you' in the first six words",
 "STAKES": "name what it costs them to keep doing it the current way",
 "CURIOSITY": "cut the half of the sentence that answers itself",
 "BREVITY": "9 to 24 words. Read it out loud and stop where you run out of breath",
}
FIX_ES = {
 "ADDRESS": "talk to the viewer in the first six words, with the address voice.md uses (tu, usted, vos)",
}

def main():
    global L, WPM, ADDRESS_OFF
    utf8_out()
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    if "--address" in a:
        i = a.index("--address"); ADDRESS_OFF = a[i + 1].lower() in ("none", "off", "third"); a = a[:i] + a[i + 2:]
    if "--wpm" in a:
        i = a.index("--wpm"); WPM = float(a[i + 1]); a = a[:i] + a[i + 2:]
    lang_given = "--lang" in a
    L, a = pick(a)
    if "--hook" in a:
        lines = [a[a.index("--hook") + 1]]
    elif a and os.path.exists(a[0]):
        lines = [l for l in open(a[0], encoding="utf-8-sig").read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1 if not a else 0)
    if not lang_given: L = pick([], " ".join(lines))[0]
    out = []
    for t in lines:
        parts, verdict, name, hits = score(t)
        out.append({"hook": t.strip(), "properties": parts, "verdict": verdict,
                    "band": band(verdict), "formula": name, "matched": hits})
    out.sort(key=lambda r: -r["verdict"])
    if as_json:
        print(json.dumps([{k: v for k, v in r.items() if k != "matched"} for r in out], indent=1)); return
    for r in out:
        report(r["hook"], r["properties"], r["verdict"], r["formula"], r["matched"])
    if len(out) > 1:
        print(f"\n  winner: {out[0]['hook'].strip()}  ({out[0]['verdict']}, {out[0]['band']})\n")

if __name__ == "__main__":
    main()
