#!/usr/bin/env python3
"""brandkit.py - check a channel's logo, banner and palette, and preview them where YouTube shows them.

    python3 brandkit.py --name "Finanzas Sin Jefe" --handle finanzassinjefe \\
        --palette "#0F172A,#F59E0B,#F8FAFC" --font "Poppins" --out .claude/youtube/brand/
    python3 brandkit.py ... --logo logo.png --banner banner.jpg

Writes into --out:
  preview.html          the channel page at desktop, mobile and TV crops, the avatar from header to
                        comment size on light and dark, the palette with its contrast. Open it.
  banner-template.svg   2560x1440 with the safe area and the desktop band drawn on a "guides" layer
                        - put the art under it, the text inside the safe area, hide the layer, export.

Without --logo or --banner it draws placeholders from the name and the palette, so the layout can be
judged before anything is generated.

YouTube's own numbers (support.google.com/youtube/answer/10456525): the profile picture renders at
98x98, as a circle, JPG/GIF/BMP/PNG, 15 MB at most. The banner is at least 2048x1152 at 16:9,
2560x1440 recommended, 6 MB at most, and only the centre 1235x338 of a 2048x1152 image - about
1546x423 at 2560 wide - is guaranteed to show everywhere. The desktop and tablet crops drawn here
are approximate; the safe area is the only promise.
"""
import base64, html, json, os, struct, sys

W, H = 2560, 1440
SAFE = (1546, 423)
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".bmp": "image/bmp"}

def size(path):
    """Width and height from the file header - PNG, JPEG, GIF, BMP - without any library."""
    b = open(path, "rb").read(1 << 20)
    if b[:8] == b"\x89PNG\r\n\x1a\n": return struct.unpack(">II", b[16:24])
    if b[:6] in (b"GIF87a", b"GIF89a"): return struct.unpack("<HH", b[6:10])
    if b[:2] == b"BM": w, h = struct.unpack("<ii", b[18:26]); return w, abs(h)
    if b[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(b):
            if b[i] != 0xFF: i += 1; continue
            m = b[i + 1]
            if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
                h, w = struct.unpack(">HH", b[i + 5:i + 9]); return w, h
            i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
    return None

def check_image(path, kind):
    problems = []
    ext = os.path.splitext(path)[1].lower()
    if ext not in MIME: problems.append(f"{ext or 'no extension'} - YouTube takes JPG, PNG, GIF (not animated) or BMP")
    mb = os.path.getsize(path) / 1e6
    dims = size(path)
    if not dims: return problems + ["could not read the dimensions"], None
    w, h = dims
    if kind == "logo":
        if mb > 15: problems.append(f"{mb:.1f} MB - the limit is 15 MB")
        if w != h: problems.append(f"{w}x{h} is not square - YouTube will crop it")
        if min(w, h) < 800: problems.append(f"{min(w, h)} px - 800x800 is the usual recommendation; it renders at 98x98 but gets reused larger")
    else:
        if mb > 6: problems.append(f"{mb:.1f} MB - the limit is 6 MB")
        if w < 2048 or h < 1152: problems.append(f"{w}x{h} - the minimum is 2048x1152")
        if abs(w / h - 16 / 9) > 0.01: problems.append(f"{w}x{h} is not 16:9")
        if w < 2560: problems.append(f"{w} wide - 2560x1440 is recommended, for TV")
    return problems, dims

def lum(hexc):
    c = [int(hexc.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)

def data_uri(path):
    return f"data:{MIME.get(os.path.splitext(path)[1].lower(), 'image/png')};base64," + base64.b64encode(open(path, "rb").read()).decode()

def initials(name):
    ws = [w for w in name.split() if w[:1].isalnum()]
    big = [w for w in ws if len(w) > 3] or ws
    return "".join(w[0] for w in big[:2]).upper() or "?"

def text_on(bg, pal):
    return max(pal + ["#FFFFFF", "#000000"], key=lambda c: contrast(bg, c))

def banner_svg(name, pal, font, guides):
    bg, accent = pal[0], pal[1] if len(pal) > 1 else pal[0]
    sx, sy = (W - SAFE[0]) / 2, (H - SAFE[1]) / 2
    g = (f'<g id="guides" fill="none" stroke-width="4" stroke-dasharray="24 16">'
         f'<rect x="0" y="{sy:.0f}" width="{W}" height="{SAFE[1]}" stroke="#888"/>'
         f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{SAFE[0]}" height="{SAFE[1]}" stroke="#E11D48"/>'
         f'<text x="{sx + 12:.0f}" y="{sy - 16:.0f}" fill="#E11D48" stroke="none" font-size="36" font-family="sans-serif">safe area {SAFE[0]}x{SAFE[1]} - text and logo go here</text>'
         f'<text x="16" y="{sy - 16:.0f}" fill="#888" stroke="none" font-size="36" font-family="sans-serif">desktop band (approx.)</text></g>') if guides else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{bg}"/>'
            f'<stop offset="1" stop-color="{accent}" stop-opacity="0.55"/></linearGradient></defs>'
            f'<g id="art"><rect width="{W}" height="{H}" fill="{bg}"/><rect width="{W}" height="{H}" fill="url(#g)"/></g>'
            f'<g id="text"><text x="{W / 2}" y="{H / 2 + 40}" text-anchor="middle" font-size="120" font-weight="700" '
            f'font-family="{html.escape(font)}, sans-serif" fill="{text_on(bg, pal)}">{html.escape(name)}</text></g>{g}</svg>')

def logo_svg(name, pal, font):
    bg = pal[1] if len(pal) > 1 else pal[0]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800"><rect width="800" height="800" fill="{bg}"/>'
            f'<text x="400" y="400" dy="0.35em" text-anchor="middle" font-size="320" font-weight="700" '
            f'font-family="{html.escape(font)}, sans-serif" fill="{text_on(bg, pal)}">{html.escape(initials(name))}</text></svg>')

def svg_uri(svg):
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()

PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} - brand preview</title>{fontlink}
<style>
:root{{--bg:#fff;--fg:#0f0f0f;--muted:#606060;--line:#e5e5e5}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0f0f0f;--fg:#f1f1f1;--muted:#aaa;--line:#303030}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 Roboto,Arial,sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:24px 16px 64px}}
h2{{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin:40px 0 12px}}
.band{{position:relative;width:100%;border-radius:12px;background:var(--b) center/100% auto no-repeat;overflow:hidden}}
.desk{{aspect-ratio:2560/423}} .mob{{aspect-ratio:1546/423;background-size:165.6% auto}}
.tv{{aspect-ratio:16/9;background-size:cover}}
.safe{{position:absolute;border:2px dashed #E11D48;left:19.8%;width:60.4%;top:35.3%;height:29.4%;display:var(--g,block)}}
.head{{display:flex;gap:16px;align-items:center;margin-top:16px}}
.av{{border-radius:50%;object-fit:cover;flex:none}}
.name{{font-size:28px;font-weight:700}} .meta{{color:var(--muted)}}
.phone{{max-width:390px;border:1px solid var(--line);border-radius:24px;padding:12px}}
.phone .name{{font-size:20px}}
.sizes{{display:flex;gap:24px;flex-wrap:wrap}} .sizes>div{{padding:20px;border-radius:12px;display:flex;gap:20px;align-items:center}}
.comment{{display:flex;gap:10px;align-items:flex-start;font-size:14px}}
.sw{{display:flex;gap:12px;flex-wrap:wrap}} .sw div{{width:150px;border-radius:10px;padding:14px;font-size:13px}}
.warn{{border-left:3px solid #E11D48;padding:4px 12px;margin:6px 0}}
label{{user-select:none;cursor:pointer}}
</style></head><body><main>
<label><input type="checkbox" checked onchange="document.body.style.setProperty('--g',this.checked?'block':'none')"> show the safe area</label>
{warnings}
<h2>Desktop channel page (approximate crop)</h2>
<div class="band desk" style="--b:url('{banner}')"><div class="safe" style="left:19.8%;width:60.4%;top:0;height:100%"></div></div>
<div class="head"><img class="av" src="{logo}" width="98" height="98" alt=""><div><div class="name">{name}</div>
<div class="meta">@{handle} &middot; subscribers &middot; videos</div></div></div>
<h2>Mobile - the safe area, and nothing else</h2>
<div class="phone"><div class="band mob" style="--b:url('{banner}')"></div>
<div class="head"><img class="av" src="{logo}" width="72" height="72" alt=""><div><div class="name">{name}</div><div class="meta">@{handle}</div></div></div></div>
<h2>TV - the whole image</h2>
<div class="band tv" style="--b:url('{banner}')"><div class="safe"></div></div>
<h2>The avatar where it actually appears</h2>
<div class="sizes">
<div style="background:#fff;color:#0f0f0f">{avs}</div><div style="background:#0f0f0f;color:#f1f1f1">{avs}</div></div>
<h2>In a comment and in search, the size most people see it</h2>
<div class="comment"><img class="av" src="{logo}" width="40" height="40" alt=""><div><b>@{handle}</b> <span class="meta">2 hours ago</span><br>
Thanks for watching - the spreadsheet is in the description.</div></div>
<h2>Palette contrast (WCAG: 4.5 body text, 3 large text)</h2><div class="sw">{swatches}</div>
</main></body></html>"""

def main():
    a = sys.argv[1:]
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    name, out = opt("--name"), opt("--out", ".")
    if not name: print(__doc__); sys.exit(1)
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    handle = opt("--handle", "".join(c for c in name.lower() if c.isalnum()))
    pal = [c.strip() if c.strip().startswith("#") else "#" + c.strip() for c in opt("--palette", "#0F172A,#F59E0B,#F8FAFC").split(",")]
    font, logo, banner = opt("--font", "Inter"), opt("--logo"), opt("--banner")
    os.makedirs(out, exist_ok=True)
    report, warnings = {"images": {}, "contrast": []}, []
    for kind, path in (("logo", logo), ("banner", banner)):
        if not path: continue
        if not os.path.exists(path): warnings.append(f"{kind}: {path} not found"); continue
        probs, dims = check_image(path, kind)
        report["images"][kind] = {"path": path, "size": dims, "problems": probs}
        warnings += [f"{kind}: {p}" for p in probs]
    for i, bgc in enumerate(pal):
        for fg in pal[i + 1:]:
            report["contrast"].append({"pair": [bgc, fg], "ratio": contrast(bgc, fg)})
    open(os.path.join(out, "banner-template.svg"), "w", encoding="utf-8").write(banner_svg(name, pal, font, True))
    logo_src = data_uri(logo) if logo and os.path.exists(logo) else svg_uri(logo_svg(name, pal, font))
    banner_src = data_uri(banner) if banner and os.path.exists(banner) else svg_uri(banner_svg(name, pal, font, False))
    avs = "".join(f'<img class="av" src="{logo_src}" width="{s}" height="{s}" alt="" title="{s}px">' for s in (98, 48, 40, 32, 24))
    sw = "".join(f'<div style="background:{c};color:{text_on(c, pal)}"><b>{c}</b><br>'
                 + "<br>".join(f"on it: {o} {contrast(c, o)}" for o in pal if o != c) + "</div>" for c in pal)
    fontlink = (f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family={font.replace(" ", "+")}:wght@400;700&display=swap">'
                if font else "")
    page = PAGE.format(name=html.escape(name), handle=html.escape(handle), banner=banner_src, logo=logo_src, avs=avs,
                       swatches=sw, fontlink=fontlink, warnings="".join(f'<p class="warn">{html.escape(w)}</p>' for w in warnings))
    open(os.path.join(out, "preview.html"), "w", encoding="utf-8").write(page)
    if "--json" in a: print(json.dumps(report, indent=1)); return
    print(f"\n  {name}  @{handle}   font {font}   palette {' '.join(pal)}\n")
    for kind in ("logo", "banner"):
        r = report["images"].get(kind)
        if not r: print(f"    {kind:<7} placeholder - pass --{kind} when there is one"); continue
        print(f"    {kind:<7} {r['size'][0]}x{r['size'][1]}  " + ("ok" if not r["problems"] else "; ".join(r["problems"])) if r["size"]
              else f"    {kind:<7} " + "; ".join(r["problems"]))
    print("\n    contrast")
    for c in report["contrast"]:
        verdict = "body text" if c["ratio"] >= 4.5 else "large text only" if c["ratio"] >= 3 else "not for text"
        print(f"      {c['pair'][0]} / {c['pair'][1]}   {c['ratio']:>5}   {verdict}")
    for w in warnings:
        if w.endswith("not found"): print(f"\n    {w}")
    print(f"\n  wrote {os.path.join(out, 'preview.html')} and banner-template.svg - open the preview\n")

if __name__ == "__main__":
    main()
