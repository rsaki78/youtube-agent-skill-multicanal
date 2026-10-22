#!/usr/bin/env python3
"""refs.py - profile candidate reference channels from what you collected, and size them.

    python3 refs.py research/refs/
    python3 refs.py research/refs/ --small 50000 --big 500000 --min 2.0 --json
    python3 refs.py research/refs/ --rows > collected.json    # swipe.py input

Input is any mix of .json files, or folders of them:

  - yt-dlp output for a channel's videos tab, as is:
        yt-dlp "https://www.youtube.com/@handle/videos" --flat-playlist --playlist-end 30 \\
               --extractor-args "youtubetab:approximate_date" -J > handle.json
  - or a plain list, one object per video:
        [{"channel":"...","subs":12000,"title":"...","views":41200,"published":"2026-08-01","url":"..."}]

Subscriber count alone ranks fame. What a new channel needs from a reference is different: does it
still get watched (median views against subs), does it break out (share of videos at 2x its own
median or better), does it keep a rhythm (uploads per month, longest gap), and is it alive (days
since the last upload). Under four videos per channel none of that means anything, and the tool
says so rather than ranking on noise.

Dates from approximate_date are approximate. Good enough for cadence, not for "posted on a Tuesday".
"""
import datetime, glob, json, os, statistics, sys

TODAY = datetime.date.today()

def _date(e):
    d = e.get("upload_date") or e.get("published")
    if d:
        d = str(d).replace("-", "")[:8]
        try: return datetime.date(int(d[:4]), int(d[4:6]), int(d[6:8]))
        except ValueError: return None
    t = e.get("timestamp") or e.get("release_timestamp")
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).date() if t else None

def _entries(d):
    for e in d.get("entries") or []:
        if not e: continue
        if e.get("entries") is not None: yield from _entries(e)   # channel URL without /videos
        else: yield e

def _files(paths):
    for p in paths:
        if os.path.isdir(p):
            for f in sorted(glob.glob(os.path.join(p, "**", "*.json"), recursive=True)): yield p, f
        else:
            for f in sorted(glob.glob(p)) or [p]: yield None, f

def load(paths):
    """Every video as a flat row. A folder's subfolders become the row's niche."""
    rows = []
    for root, f in _files(paths):
        if not os.path.exists(f): continue
        rel = os.path.relpath(os.path.dirname(f), root) if root else "."
        folder = rel.split(os.sep)[0] if rel != "." else ""
        d = json.load(open(f, encoding="utf-8"))
        if isinstance(d, dict) and "entries" in d:
            ch = d.get("channel") or d.get("uploader") or d.get("title") or "?"
            subs = d.get("channel_follower_count")
            for e in _entries(d):
                rows.append({"niche": folder, "channel": e.get("channel") or e.get("uploader") or ch,
                             "subs": e.get("channel_follower_count") or subs, "title": e.get("title", ""),
                             "views": e.get("view_count"), "duration": e.get("duration"),
                             "url": e.get("url") or e.get("webpage_url") or "", "date": _date(e)})
        else:
            for r in (d.get("videos", []) if isinstance(d, dict) else d):
                rows.append({"niche": r.get("niche") or folder, "channel": r.get("channel", "?"),
                             "subs": r.get("subs"), "title": r.get("title", ""), "views": r.get("views"),
                             "duration": r.get("duration"), "url": r.get("url", ""), "date": _date(r)})
    return rows

def band(subs, small, big):
    if not subs: return "?"
    return "big" if subs >= big else "small" if subs < small else "mid"

def channel_stats(rows, lo=2.0, small=50000, big=500000):
    by = {}
    for r in rows: by.setdefault(r["channel"], []).append(r)
    out = []
    for ch, vids in by.items():
        views = [float(v["views"]) for v in vids if v["views"] is not None]
        subs = max([int(v["subs"]) for v in vids if v["subs"]] or [0]) or None
        s = {"channel": ch, "niche": vids[0]["niche"], "videos": len(vids), "subs": subs,
             "band": band(subs, small, big), "thin": len(views) < 4}
        if s["thin"]: out.append(s); continue
        med = statistics.median(views)
        mult = [(v["views"] / med if med else 0, v) for v in vids if v["views"] is not None]
        top_m, top = max(mult, key=lambda x: x[0])
        dates = sorted(v["date"] for v in vids if v["date"])
        s.update({"median": int(med), "reach": round(med / subs, 3) if subs else None,
                  "outliers": [{"multiple": round(m, 2), "title": v["title"], "views": int(v["views"]),
                                "date": v["date"].isoformat() if v["date"] else None, "url": v["url"]}
                               for m, v in sorted(mult, key=lambda x: -x[0]) if m >= lo],
                  "top": {"multiple": round(top_m, 2), "title": top["title"]}})
        s["outlier_rate"] = round(len(s["outliers"]) / len(mult), 2)
        if len(dates) >= 2:
            span = max((dates[-1] - dates[0]).days, 1)
            s["per_month"] = round((len(dates) - 1) * 30 / span, 1)
            s["longest_gap"] = max((b - a).days for a, b in zip(dates, dates[1:]))
        if dates: s["days_since"] = (TODAY - dates[-1]).days
        out.append(s)
    return out

def _arg(a, flag, default):
    return float(a[a.index(flag) + 1]) if flag in a else default

def main():
    a = sys.argv[1:]
    lo, small, big = _arg(a, "--min", 2.0), _arg(a, "--small", 50000), _arg(a, "--big", 500000)
    paths = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--min", "--small", "--big"))]
    rows = load(paths)
    if not rows: print(__doc__); sys.exit(1)
    if "--rows" in a:
        print(json.dumps([{**r, "date": r["date"].isoformat() if r["date"] else None, "published":
                           r["date"].isoformat() if r["date"] else None} for r in rows], indent=1)); return
    stats = channel_stats(rows, lo, small, big)
    if "--json" in a: print(json.dumps(stats, indent=1)); return
    good = sorted([s for s in stats if not s["thin"]], key=lambda s: (-s["outlier_rate"], -(s["reach"] or 0)))
    print(f"\n  {len(rows)} videos across {len(stats)} channels   small < {int(small):,}   big >= {int(big):,}   outlier >= {lo}x\n")
    print(f"    {'channel':<24} {'band':<5} {'subs':>9} {'median':>9} {'reach':>6} {'out%':>5} {'/mo':>5} {'gap':>4} {'last':>5}")
    for s in good:
        f = lambda k, fmt: format(s[k], fmt) if s.get(k) is not None else "?"
        flag = "  dormant" if (s.get("days_since") or 0) > 90 else ""
        print(f"    {s['channel'][:24]:<24} {s['band']:<5} {f('subs', ','):>9} {s['median']:>9,} {f('reach', '.0%'):>6} "
              f"{s['outlier_rate']:>5.0%} {f('per_month', ''):>5} {f('longest_gap', ''):>4} {f('days_since', ''):>5}{flag}")
        print(f"      top {s['top']['multiple']:.1f}x  {s['top']['title'][:70]}")
    thin = [s for s in stats if s["thin"]]
    if thin:
        print(f"\n  skipped {len(thin)} channel(s) with under 4 videos with views - collect more: "
              + ", ".join(f"{s['channel']} ({s['videos']})" for s in thin[:6]))
    if any(s["band"] == "?" for s in good):
        print("\n  no subscriber count for some channels - band and reach show ?; add \"subs\" by hand from the channel page")
    print("\n  reach = median views / subs.  out% = share of videos at the outlier multiple.  gap and last in days.\n")

if __name__ == "__main__":
    main()
