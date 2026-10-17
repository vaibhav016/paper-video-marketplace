#!/usr/bin/env python3
"""vdur.py FILE...: print the duration in seconds of each video (PyAV, so no ffprobe needed)."""
import sys, av
for f in sys.argv[1:]:
    with av.open(f) as c:
        d = c.duration / 1e6 if c.duration else float(c.streams.video[0].duration * c.streams.video[0].time_base)
    print(f"{d:.3f}" if len(sys.argv) == 2 else f"{f} {d:.3f}")
