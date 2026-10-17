#!/bin/bash
# Usage: render.sh VIDEO.py [m|h|k] [Scene ...]
#   m = 720p30 review (default), h = 1080p60 final, k = 4K. l (480p15) looks jerky: don't review with it.
# Scenes default to every `class X(Base)` in file order. Renders scenes in parallel, each with its own
# media dir (a shared Tex cache races), greps logs for errors and !! BOUNDS, concatenates <stem>_<q>.mp4.
set -e
SKILL=$(cd "$(dirname "$0")/.." && pwd)
FILE=$(readlink -f "$1"); Q=${2:-m}; shift 2 2>/dev/null || shift $#
VENV=$(bash "$SKILL/scripts/setup_env.sh") || exit 1
source "$VENV/bin/activate"
export PYTHONPATH="$SKILL/lib:$PYTHONPATH"
DIR=$(dirname "$FILE"); STEM=$(basename "$FILE" .py); MEDIA=${MEDIA:-$DIR/media}
SCENES=${*:-$(grep -oP '^class \K\w+(?=\(Base\))' "$FILE" | tr '\n' ' ')}
[ -n "$SCENE_LIST" ] && SCENES=$SCENE_LIST
echo "scenes: $SCENES"
cd "$DIR"; mkdir -p "$MEDIA"
for s in $SCENES; do
  manim -q$Q --media_dir "$MEDIA/$s" --disable_caching "$FILE" $s > "$MEDIA/log_$s.txt" 2>&1 &
done
wait   # never poll with pgrep -f loops: they match their own command line
grep -H "BOUNDS\|Error\|Traceback" "$MEDIA"/log_*.txt || echo "no errors, no bounds warnings"
case $Q in l) R=480p15;; m) R=720p30;; h) R=1080p60;; k) R=2160p60;; esac
LIST="$MEDIA/list_$Q.txt"; : > "$LIST"
for s in $SCENES; do
  f="$MEDIA/$s/videos/$STEM/$R/$s.mp4"
  [ -f "$f" ] || { echo "missing $f (see $MEDIA/log_$s.txt)"; exit 1; }
  echo "file '$f'" >> "$LIST"
  printf "%-12s %6.1fs\n" $s $(python "$SKILL/scripts/vdur.py" "$f")
done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$LIST" -c copy "$DIR/${STEM}_$Q.mp4"
printf "TOTAL %s -> %s\n" "$(python "$SKILL/scripts/vdur.py" "$DIR/${STEM}_$Q.mp4")" "$DIR/${STEM}_$Q.mp4"
