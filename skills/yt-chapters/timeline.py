#!/usr/bin/env python3
"""timeline.py - where each scene starts in the final video, from the audio of each scene.

    python3 timeline.py videos/0412/audio/                      # one mp3 or wav per scene
    python3 timeline.py videos/0412/audio/ --style .claude/youtube/style.md
    python3 timeline.py videos/0412/audio/ --start 1.5 --gap 1 --fps 24 --json > scenes.json
    python3 chapters.py subtitles.srt --scenes scenes.json      # scenes as chapter candidates

For videos assembled from one audio file per scene, laid end to end with a fixed silence before the
first and between each pair. The settings are the channel's, in the `## Timeline` section of
style.md:

    ## Timeline
    start_silence: 1.5     # seconds before scene 1
    scene_gap: 1           # seconds between scenes
    fps: 24                # the edit's frame rate; each scene adds one frame (a clip fills whole frames)

    start of scene k = start_silence + sum over the scenes before it of (audio + scene_gap + 1/fps)

The audio length is the whole file, counted in MP3 frames - not the end of the last word. Generated
voice files carry silence at the end, and leaving it out drifts seconds by the last scene. Flags
override style.md. Without fps the frame term is left out.

--gapless takes off the encoder delay and padding a LAME tag records (about 0.04s a file), for an
edit that trims them - ffmpeg does when it decodes. Which one your edit does is a question for one
real video: run both, and keep the one whose starts land on the scene changes. Then write
`gapless: 1` into `## Timeline` so nobody has to ask again.

It computes; it does not measure. To check it against a real video, compare a few starts by ear
once, and fix the settings rather than the output. MP3 (MPEG audio, CBR or VBR) and WAV, no
dependencies.
"""
import json, os, re, struct, sys, wave

BITRATES = {  # kbps by (mpeg1?, layer)
 (True, 1): [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448],
 (True, 2): [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],
 (True, 3): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
 (False, 1): [0, 32, 48, 56, 64, 80, 96, 112, 128, 144, 160, 176, 192, 224, 256],
 (False, 2): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
 (False, 3): [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160],
}
RATES = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000]}

def header(b, i):
    """(frame length, samples, sample rate) of the MPEG audio frame at i, or None."""
    if i + 4 > len(b) or b[i] != 0xFF or (b[i + 1] & 0xE0) != 0xE0: return None
    ver, layer = (b[i + 1] >> 3) & 3, 4 - ((b[i + 1] >> 1) & 3)
    br_i, sr_i, pad = b[i + 2] >> 4, (b[i + 2] >> 2) & 3, (b[i + 2] >> 1) & 1
    if ver == 1 or layer == 4 or br_i in (0, 15) or sr_i == 3: return None
    mpeg1 = ver == 3
    br, sr = BITRATES[(mpeg1, layer)][br_i] * 1000, RATES[ver][sr_i]
    if layer == 1: return (12 * br // sr + pad) * 4, 384, sr
    samples = 1152 if (layer == 2 or mpeg1) else 576
    return samples // 8 * br // sr + pad, samples, sr

def lame_trim(head, j):
    """Encoder delay + padding, in samples, from the LAME tag after a Xing/Info header, or 0."""
    flags = struct.unpack(">I", head[j + 4:j + 8])[0]
    k = j + 8 + 4 * bool(flags & 1) + 4 * bool(flags & 2) + 100 * bool(flags & 4) + 4 * bool(flags & 8)
    if head[k:k + 4] not in (b"LAME", b"Lavc", b"Lavf", b"GOGO") or len(head) < k + 24: return 0
    d = head[k + 21:k + 24]
    return ((d[0] << 4) | (d[1] >> 4)) + (((d[1] & 0x0F) << 8) | d[2])

def mp3_seconds(path, gapless=False):
    b = open(path, "rb").read()
    i = 0
    if b[:3] == b"ID3":
        i = 10 + ((b[6] << 21) | (b[7] << 14) | (b[8] << 7) | b[9]) + (10 if b[5] & 0x10 else 0)
    while i < len(b) and not header(b, i): i += 1          # junk before the first frame
    first = header(b, i)
    if not first: raise ValueError("no MPEG audio frames found")
    length, samples, sr = first
    head = b[i:i + length]
    for tag in (b"Xing", b"Info"):                          # VBR header: the frame count, exact
        j = head.find(tag)
        if j >= 0 and struct.unpack(">I", head[j + 4:j + 8])[0] & 1:
            trim = lame_trim(head, j) if gapless else 0
            return (struct.unpack(">I", head[j + 8:j + 12])[0] * samples - trim) / sr
    j = head.find(b"VBRI")
    if j >= 0: return struct.unpack(">I", head[j + 14:j + 18])[0] * samples / sr
    frames = 0                                              # no header: count every frame
    while True:
        h = header(b, i)
        if not h: break
        frames += 1; i += h[0]
    return frames * samples / sr

def seconds(path, gapless=False):
    if path.lower().endswith(".wav"):
        with wave.open(path) as w: return w.getnframes() / w.getframerate()
    return mp3_seconds(path, gapless)

def style_timeline(path):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"^## Timeline\s*\n(.*?)(?=^## |\Z)", t, re.S | re.M)
    if not m: return {}
    return {k: float(v) for k, v in re.findall(r"^\s*(\w+)\s*:\s*([\d.]+)", m.group(1), re.M)}

def natural(name): return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", name)]

def stamp(t): return f"{int(t // 60)}:{t % 60:06.3f}"

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    gapless = "--gapless" in a; a = [x for x in a if x != "--gapless"]
    opt = {}
    for flag in ("--start", "--gap", "--fps", "--style"):
        if flag in a:
            i = a.index(flag); opt[flag] = a[i + 1]; a = a[:i] + a[i + 2:]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cfg = style_timeline(opt["--style"]) if "--style" in opt else {}
    start = float(opt.get("--start", cfg.get("start_silence", 0)))
    gap = float(opt.get("--gap", cfg.get("scene_gap", 0)))
    fps = float(opt.get("--fps", cfg.get("fps", 0)))
    gapless = gapless or bool(cfg.get("gapless"))
    if os.path.isdir(a[0]):
        files = sorted((f for f in os.listdir(a[0]) if f.lower().endswith((".mp3", ".wav"))), key=natural)
        files = [os.path.join(a[0], f) for f in files]
    else:
        files = a
    if not files: print("no .mp3 or .wav files there"); sys.exit(1)
    frame = 1 / fps if fps else 0
    scenes, t = [], start
    for n, f in enumerate(files, 1):
        d = seconds(f, gapless)
        scenes.append({"scene": n, "file": os.path.basename(f), "audio": round(d, 3), "start": round(t, 3)})
        t += d + gap + frame
    end = round(t - gap - frame, 3)
    settings = {"start_silence": start, "scene_gap": gap, "fps": fps or None, "gapless": gapless}
    if as_json:
        print(json.dumps({"settings": settings, "scenes": scenes, "end": end}, indent=1)); return
    print(f"\n  {len(scenes)} scenes   start {start}s, gap {gap}s" + (f", +1 frame at {fps:g} fps" if fps else ", no frame term"))
    if not (start or gap): print("  no settings - pass --style with a ## Timeline section, or the flags")
    print()
    for s in scenes:
        print(f"    {s['scene']:3d}  {stamp(s['start'])}  {s['audio']:8.3f}s  {s['file']}")
    print(f"\n  last scene ends at {stamp(end)}\n")

if __name__ == "__main__":
    main()
