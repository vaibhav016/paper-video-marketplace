#!/usr/bin/env python3
"""Run with the paper-video venv python (it has PyAV): $(setup_env.sh)/bin/python social_cuts.py ...

Social-media cuts from rendered scene files.

Per-post clips (one scene, or several joined, per post):
  social_cuts.py clips MEDIA_DIR STEM OUT_DIR "1_hook=Hook" "2_problem=Problem@0-27.8" "8_results=Results+Outro"
     Scene@a-b trims to [a,b] seconds (either end optional). Cut at scene changes or after a fade
     completes; check the first frame of each clip.
Short teaser with crossfades (e.g. a 40 s cut for X's first post):
  social_cuts.py teaser MEDIA_DIR STEM OUT.mp4 "Results@4.9-8.6" "Problem@40.5-53" ... [--hold 2.5] [--xfade 0.4]
     Start on a fully drawn frame (muted autoplay decides in ~2 s). The last frame is held --hold seconds.
Resolution: --res 1080p60 (default) | 720p30.
"""
import subprocess, sys, os, re, tempfile

def dur(f):
    import av
    with av.open(f) as c:
        return c.duration / 1e6

def parse(spec):
    m = re.match(r"(\w+)(?:@([\d.]*)-([\d.]*))?$", spec)
    return m.group(1), float(m.group(2)) if m.group(2) else None, float(m.group(3)) if m.group(3) else None

ENC = ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart"]

def src(media, stem, scene, res):
    return os.path.join(media, scene, "videos", stem, res, scene + ".mp4")

def main():
    a = sys.argv[1:]
    opt = lambda k, d: (a.pop(a.index(k) + 1), a.remove(k))[0] if k in a else d
    res = opt("--res", "1080p60"); hold = float(opt("--hold", "2.5")); X = float(opt("--xfade", "0.4"))
    mode, media, stem, out, specs = a[0], os.path.abspath(a[1]), a[2], os.path.abspath(a[3]), a[4:]
    if mode == "clips":
        os.makedirs(out, exist_ok=True)
        for item in specs:
            name, parts = item.split("=")
            tmp = []
            for p in parts.split("+"):
                s, t0, t1 = parse(p)
                f = src(media, stem, s, res)
                if t0 is None and t1 is None:
                    tmp.append(f); continue
                o = tempfile.mktemp(suffix=".mp4")
                cmd = ["ffmpeg", "-y", "-loglevel", "error"] + (["-ss", str(t0)] if t0 else []) + \
                      (["-t", str(t1 - (t0 or 0))] if t1 else []) + ["-i", f] + ENC + [o]
                subprocess.run(cmd, check=True); tmp.append(o)
            lst = tempfile.mktemp(suffix=".txt")
            open(lst, "w").write("".join(f"file '{x}'\n" for x in tmp))
            dst = os.path.join(out, name + ".mp4")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst] + ENC + [dst], check=True)
            print(f"{dst} {dur(dst):.1f}s")
    elif mode == "teaser":
        inp, fl, segs = [], [], [parse(s) for s in specs]
        lens = []
        for i, (s, t0, t1) in enumerate(segs):
            f = src(media, stem, s, res)
            t0 = t0 or 0.0; t1 = t1 or dur(f)
            inp += ["-ss", str(t0), "-t", str(t1 - t0), "-i", f]
            fl.append(f"[{i}:v]settb=AVTB,fps={res[-2:]},format=yuv420p[v{i}]")
            lens.append(t1 - t0)
        prev, cur = "v0", lens[0]
        for i in range(1, len(segs)):
            off = cur - X
            fl.append(f"[{prev}][v{i}]xfade=transition=fade:duration={X}:offset={off:.3f}[x{i}]")
            prev, cur = f"x{i}", off + lens[i]
        tmp = tempfile.mktemp(suffix=".mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inp, "-filter_complex", ";".join(fl), "-map", f"[{prev}]",
                        "-c:v", "libx264", "-crf", "14", "-preset", "medium", tmp], check=True)
        # ffmpeg 4.x: tpad inside an xfade chain fails to open the encoder, so hold the last frame in a 2nd pass
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-vf", f"tpad=stop_mode=clone:stop_duration={hold}"] + ENC + [out], check=True)
        print(f"{out} {dur(out):.1f}s")

if __name__ == "__main__":
    main()
