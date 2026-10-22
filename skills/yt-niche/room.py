#!/usr/bin/env python3
"""room.py - is there still room for a new channel in this niche? Compare candidates side by side.

    python3 room.py research/niche/
    python3 room.py research/niche/ --small 50000 --min 2.0 --days 180 --json

One subfolder per candidate niche, one yt-dlp (or plain-list) .json per channel inside it - the
same input refs.py reads, see ../yt-refs/refs.py:

    research/niche/finanzas-freelancers/<channel>.json
    research/niche/cocina-keto/<channel>.json

The question is not "is this niche big". It is "are SMALL channels breaking out here, recently".
A niche where only the million-subscriber channels get outliers is one a new channel enters at the
bottom of a ladder; a niche where a 6k channel put out a 10x video last month is one with a door.

So per niche: how many channels you collected, how many of the small ones have at least one video
at --min times their own median, how many outliers landed in the last --days, and how many
channels have gone quiet. The verdict is a heuristic about the sample you collected - collect only
big channels and every niche looks top-heavy. It is not a market size.
"""
import datetime, json, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "yt-refs"))
from refs import load, channel_stats, TODAY

def verdict(n):
    if n["channels"] < 4: return "too little collected", "collect at least 4 channels with 4+ videos, mixed sizes"
    if n["small"] == 0: return "unknown", "no small channels in the sample - add some before judging room"
    if n["small_breaking"] >= 2 and n["recent_small"] > 0:
        return "open", "small channels are breaking out, and recently"
    if n["small_breaking"] >= 1:
        return "narrow door", "a small channel broke out, but rarely or not lately"
    if n["outliers"] > 0: return "top-heavy", "outliers come from established channels only"
    return "flat", "nothing beats its own median - saturated, or too little collected"

def main():
    a = sys.argv[1:]
    num = lambda f, d: float(a[a.index(f) + 1]) if f in a else d
    lo, small, days = num("--min", 2.0), num("--small", 50000), int(num("--days", 180))
    paths = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--min", "--small", "--days"))]
    rows = load(paths)
    if not rows: print(__doc__); sys.exit(1)
    cutoff = (TODAY - datetime.timedelta(days=days)).isoformat()
    by = {}
    for s in channel_stats(rows, lo, small, float("inf")): by.setdefault(s["niche"] or "(no folder)", []).append(s)
    out = []
    for niche, chans in by.items():
        ok = [s for s in chans if not s["thin"]]
        sm = [s for s in ok if s["band"] == "small"]
        n = {"niche": niche, "channels": len(ok), "skipped_thin": len(chans) - len(ok), "small": len(sm),
             "small_breaking": sum(1 for s in sm if s["outliers"]),
             "outliers": sum(len(s["outliers"]) for s in ok),
             "recent": sum(1 for s in ok for o in s["outliers"] if (o["date"] or "") >= cutoff),
             "recent_small": sum(1 for s in sm for o in s["outliers"] if (o["date"] or "") >= cutoff),
             "dormant": sum(1 for s in ok if (s.get("days_since") or 0) > 90),
             "median_of_medians": int(statistics.median([s["median"] for s in ok])) if ok else 0,
             "undated": not any(o["date"] for s in ok for o in s["outliers"]),
             "examples": sorted(({"channel": s["channel"], "subs": s["subs"], **o} for s in ok for o in s["outliers"]),
                                key=lambda o: (o["subs"] or 10**12) / max(o["multiple"], 0.01))[:3]}
        n["verdict"], n["why"] = verdict(n)
        out.append(n)
    rank = {"open": 0, "narrow door": 1, "top-heavy": 2, "flat": 3, "unknown": 4, "too little collected": 5}
    out.sort(key=lambda n: (rank[n["verdict"]], -n["small_breaking"], -n["recent_small"]))
    if "--json" in a: print(json.dumps(out, indent=1)); return
    print(f"\n  {len(out)} niche(s)   small < {int(small):,} subs   outlier >= {lo}x   recent = last {days} days\n")
    for n in out:
        print(f"  {n['niche']}  ->  {n['verdict'].upper()}: {n['why']}")
        print(f"    {n['channels']} channels ({n['small']} small, {n['small_breaking']} of them breaking out)   "
              f"{n['outliers']} outliers, {n['recent']} recent ({n['recent_small']} on small)   "
              f"{n['dormant']} dormant   median of medians {n['median_of_medians']:,}")
        for o in n["examples"]:
            subs = f"{o['subs']:,} subs" if o["subs"] else "? subs"
            print(f"      {o['multiple']:5.1f}x  {subs:>13}  {o['channel'][:20]:<20} {o['title'][:56]}")
        if n["skipped_thin"]: print(f"    skipped {n['skipped_thin']} channel(s) with under 4 videos")
        if n["undated"] and n["outliers"]: print("    no dates on the outliers - collect with youtubetab:approximate_date or 'recent' means nothing")
        print()
    print("  a heuristic about the channels you collected, not a market size. Small channels with no")
    print("  subscriber count do not count as small - add \"subs\" by hand if yt-dlp did not return it.\n")

if __name__ == "__main__":
    main()
