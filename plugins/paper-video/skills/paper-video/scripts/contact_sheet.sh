#!/bin/bash
# Usage: contact_sheet.sh VIDEO.mp4 OUT.png [every_seconds=2] [cols=6]
# One tiled PNG of frames (timestamped when ffmpeg has drawtext): Read it to review a render without watching it.
SKILL=$(cd "$(dirname "$0")/.." && pwd)
VENV=$(bash "$SKILL/scripts/setup_env.sh" 2>/dev/null); [ -n "$VENV" ] && export PATH="$VENV/bin:$PATH"
IN=$1; OUT=$2; E=${3:-2}; C=${4:-6}
N=$(python -c "import math,sys; d=float(sys.argv[1]); print(max(1, math.ceil(d/$E/$C)))" "$(python "$SKILL/scripts/vdur.py" "$IN")")
TS="drawtext=text='%{pts\\:hms}':x=5:y=5:fontsize=20:fontcolor=red,"
ffmpeg -y -loglevel error -i "$IN" -vf "fps=1/$E,scale=384:-1,${TS}tile=${C}x${N}" -frames:v 1 -threads 1 "$OUT" 2>/dev/null || \
ffmpeg -y -loglevel error -i "$IN" -vf "fps=1/$E,scale=384:-1,tile=${C}x${N}" -frames:v 1 -threads 1 "$OUT"
echo "$OUT"
