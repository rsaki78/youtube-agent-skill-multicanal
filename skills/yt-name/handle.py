#!/usr/bin/env python3
"""handle.py - turn channel names into YouTube handles, lint them, and optionally see if they answer.

    python3 handle.py "Finanzas Sin Jefe" "El Freelance Rico"
    python3 handle.py --file names.txt --check
    python3 handle.py "Finanzas Sin Jefe" --suffix tv,hq,mx --check --json

YouTube's rules (support.google.com/youtube/answer/11585688): 3 to 30 characters; letters and
numbers from a supported language, plus underscore, hyphen, period and the Latin middle dot; no
separator at the start or end; not URL-like, not phone-number-like, not already taken. Not case
sensitive. This tool enforces those, then adds the ones YouTube does not: a handle is said out loud
("arroba ...") and typed on a phone, so it warns on length, on accents it had to strip, on letters
that double at a word joint, and on characters that read as each other.

--check asks youtube.com/@handle, one request a second. A 200 means taken. A 404 means probably
free, never certainly: terminated and reserved handles also 404. The only final answer is the
handle field in YouTube Studio, so treat "free?" as worth trying, nothing more.
"""
import json, re, sys, time, unicodedata, urllib.error, urllib.request

SEPS = "._-·"
URLISH = re.compile(r"(^www|https?|\.(com|net|org|io|tv|co|app|me|ly|es|mx|ar|cl|pe|us|uk|info)$)")
LOOKALIKE = re.compile(r"(l1|1l|il|li|o0|0o|rn|vv)")

def words(name):
    plain = unicodedata.normalize("NFKD", name)
    plain = "".join(c for c in plain if not unicodedata.combining(c))
    return [w for w in re.split(r"[^0-9a-zA-Z]+", plain.lower()) if w], plain != unicodedata.normalize("NFKD", name) or name != plain

def variants(name, suffixes):
    ws, _ = words(name)
    if not ws: return []
    out = ["".join(ws)]
    out += ["".join(ws) + s for s in suffixes]
    if len(ws) > 1:
        out += [".".join(ws), "_".join(ws)]
        out.append("".join(w[0] for w in ws[:-1]) + ws[-1])       # initials + last word, for long names
    seen, uniq = set(), []
    for v in out:
        if v not in seen: seen.add(v); uniq.append(v)
    return uniq

def lint(h, name):
    errors, warns = [], []
    if not 3 <= len(h) <= 30: errors.append(f"{len(h)} characters, must be 3-30")
    if any(not (c.isalnum() or c in SEPS) for c in h): errors.append("characters outside letters, numbers and . _ - ·")
    if h[:1] in SEPS or h[-1:] in SEPS: errors.append("separator at the start or end")
    if URLISH.search(h): errors.append("URL-like")
    digits = sum(c.isdigit() for c in h)
    if digits >= 7 or (h and digits / len(h) > 0.6): errors.append("phone-number-like")
    if re.search(r"[._\-·]{2}", h): warns.append("two separators in a row")
    if len(h) > 18: warns.append(f"{len(h)} characters - long to say and to type")
    ws, stripped = words(name)
    if stripped: warns.append("accents stripped (n for the tilde n too) - check the word still means the same thing")
    joints = ["".join(ws)[sum(map(len, ws[:i])) - 1:sum(map(len, ws[:i])) + 1] for i in range(1, len(ws))]
    if any(len(j) == 2 and j[0] == j[1] for j in joints) and "".join(ws) in h:
        warns.append("a letter doubles where two words join - easy to mistype")
    if len(ws) > 1 and ws[0] not in h: warns.append("initials - nobody gets from the name to this handle")
    if LOOKALIKE.search(h): warns.append("letters that read as each other (l/1/i, o/0, rn/m)")
    if any(c in h for c in SEPS): warns.append("separator - nobody says it out loud, people will type it without")
    return errors, warns

def check(h):
    req = urllib.request.Request(f"https://www.youtube.com/@{h}", headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            if "consent." in r.geturl(): return "unknown (consent page)"
            return "taken"
    except urllib.error.HTTPError as e:
        return "free?" if e.code == 404 else f"unknown ({e.code})"
    except Exception as e:
        return f"unknown ({type(e).__name__})"

def main():
    a = sys.argv[1:]
    as_json, online = "--json" in a, "--check" in a
    suffixes = a[a.index("--suffix") + 1].split(",") if "--suffix" in a else ["tv", "hq"]
    names = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--suffix", "--file"))]
    if "--file" in a: names += [l.strip() for l in open(a[a.index("--file") + 1], encoding="utf-8") if l.strip()]
    if not names: print(__doc__); sys.exit(1)
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    report, first = [], True
    for name in names:
        rows = []
        for h in variants(name, suffixes):
            errors, warns = lint(h, name)
            status = None
            if online and not errors:
                if not first: time.sleep(1)
                first, status = False, check(h)
            rows.append({"handle": h, "errors": errors, "warnings": warns, "status": status})
        plain = rows[0] if rows else None
        if plain and plain["status"] == "taken":
            for r in rows[1:]:
                if r["status"] == "free?":
                    r["warnings"].append(f"@{plain['handle']} is someone else's - people who search the name find them first")
        usable = [r for r in rows if not r["errors"] and r["status"] != "taken"]
        best = min(usable, key=lambda r: (r["status"] != "free?" if online else 0, len(r["warnings"]), rows.index(r)), default=None)
        report.append({"name": name, "best": best["handle"] if best else None, "handles": rows,
                       "name_in_use": bool(plain and plain["status"] == "taken")})
    if as_json: print(json.dumps(report, indent=1, ensure_ascii=False)); return
    for r in report:
        print(f"\n  {r['name']}   ->   " + (f"@{r['best']}" if r["best"] else "no usable handle - change the name or add --suffix"))
        for h in r["handles"]:
            mark = "x" if h["errors"] else ("-" if h["status"] == "taken" else "*" if h["handle"] == r["best"] else " ")
            st = f"[{h['status']}]" if h["status"] else ""
            print(f"    {mark} @{h['handle']:<32}{st:<26}" + "; ".join(h["errors"] + h["warnings"]))
        if r["name_in_use"]: print("    the plain handle is taken - the NAME is probably in use. Look at that channel before keeping it.")
    if online: print("\n  free? = youtube.com/@handle returned 404. Probably free, not certainly - confirm in YouTube Studio.")
    print()

if __name__ == "__main__":
    main()
