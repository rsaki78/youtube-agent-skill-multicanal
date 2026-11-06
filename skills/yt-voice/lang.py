#!/usr/bin/env python3
"""lang.py - the language layer every tool in this pack shares.

    from lang import pick, words, fold, STOP

One place for the word lists and the normalisation, so a fix for Spanish is made once and not in
twelve tools. Not a command - the tools import it.

The language comes from the channel: `language:` under `## Niche` in `.claude/youtube/channel.md`
(es-MX, en-US...). The skills pass it to each tool as `--lang`; only the first two letters matter
here. Without `--lang` a tool guesses from the text it was given, and a short text - one title -
is a weak guess, so the skills always pass it.

Adding a language is adding its lists below and its patterns in yt-script/hooks.json.
"""
import re, sys, unicodedata

LANGS = ("en", "es")

def fold(text):
    """Lower case, accents off: "MURIÓ" -> "murio", "Sabás" -> "sabas". For comparing, never for
    printing - keep the original text for anything the user reads."""
    t = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")

WORD = re.compile(r"[^\W_]+(?:'[^\W_]+)*")

def words(text, keep=""):
    """Folded words, accents and ñ included. `keep` adds characters that belong to a token in that
    tool - "%$." for figures."""
    t = fold(text)
    if not keep: return WORD.findall(t)
    return re.findall(r"(?:[^\W_]|['" + re.escape(keep) + r"])+", t)

def tokens(text):
    """The words as written, with their folded form: [("Murió", "murio"), ...]."""
    return [(m.group(0), fold(m.group(0))) for m in WORD.finditer(text)]

# Folded. Spanish keeps "este" out: it is a filler in Mexico and a word everywhere else.
STOP = {
 "en": set("""the a an and or but of to in on at for with is are was were be been it this that these
 those i you he she we they me my your our their as by from so if not no do does did have has had
 just then than there here what which who about into out up""".split()),
 "es": set("""de la que el en y a los se del las un por con no una su para es al lo como mas pero sus
 le ya o si porque esta entre cuando muy sin sobre tambien me hasta hay donde quien desde todo nos
 durante todos uno les ni contra otros ese eso esos esas ante ellos e esto mi antes algunos unos yo
 otro otras otra tanto estos mucho quienes nada muchos cual poco ella estar estas algunas algo
 nosotros mis tu te ti tus ellas nosotras vosotros os mio mia tuyo suyo son fue era ser va voy van
 hacer tiene tengo usted ustedes aqui alli asi entonces despues luego ahora hoy cada mismo misma
 tan ademas aunque mientras segun tras hacia cuyo cuya sea han ha habia hubo fueron eran estaba
 estaban sido puede pueden dijo dice hace hizo solo vez veces aquel aquella aquellos aquellas
 cuales cuyos sus nuestro nuestra nuestros nuestras vuestro vuestra le les lo los la las""".split()),
}

FILLERS = {
 "es": ["o sea", "este", "eh", "em", "bueno", "pues", "como que", "digamos", "basicamente",
        "literalmente", "tipo", "verdad?", "no?", "vale"],
 "en": ["um", "uh", "like", "you know", "basically", "actually", "literally", "kind of", "sort of",
        "i mean", "right?"],
}

def detect(text, default="en"):
    w = words(text)
    es = sum(x in STOP["es"] for x in w); en = sum(x in STOP["en"] for x in w)
    if es == en: return default
    return "es" if es > en else "en"

def code(value):
    """"es-MX" -> "es". A language with no lists here falls back to English, and says so."""
    c = (value or "").strip().lower()[:2]
    if c in LANGS: return c
    if c: print(f"  no word lists for '{value}' - using English. Add them to yt-voice/lang.py.", file=sys.stderr)
    return "en"

def pick(argv, text="", default="en"):
    """The tool's language: --lang if given, else a guess from the text. Returns (lang, argv
    without --lang and its value)."""
    if "--lang" in argv:
        i = argv.index("--lang")
        value = argv[i + 1] if i + 1 < len(argv) else ""
        return code(value), argv[:i] + argv[i + 2:]
    return detect(text, default), argv

def utf8_out():
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
