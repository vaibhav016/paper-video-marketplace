#!/bin/bash
# paper-video environment: creates (once) a persistent venv with manim and prints its path on stdout.
# Re-running is a no-op once it works. Location: $PAPER_VIDEO_VENV or ~/.local/share/paper-video/venv.
#   setup_env.sh                 # venv + manim; reports missing LaTeX
#   setup_env.sh --install-tex   # also installs TinyTeX (user-level, no sudo) with the packages the videos need
# Needs python >= 3.10. ffmpeg: the system one if present, else a pip-provided binary linked into the venv.
set -e
log(){ echo "[paper-video] $*" >&2; }
VENV=${PAPER_VIDEO_VENV:-$HOME/.local/share/paper-video/venv}
TEXPKGS="standalone preview doublestroke relsize everysel ragged2e fundus-calligra microtype wasysym physics dvisvgm.x86_64-linux \
  rsfs wasy cm-super jknapltx mathastext psnfss times mathtools amsfonts amsmath babel-english ms setspace xcolor bm"

if [ "$1" = "--install-tex" ] && ! command -v latex >/dev/null; then
  log "installing TinyTeX into ~/.TinyTeX (user-level)"
  curl -sL "https://yihui.org/tinytex/install-bin-unix.sh" | sh >&2
  export PATH="$HOME/bin:$HOME/.TinyTeX/bin/x86_64-linux:$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
  tlmgr install $TEXPKGS >&2 || true
fi

if [ ! -x "$VENV/bin/manim" ] || ! "$VENV/bin/python" -c "import manim" 2>/dev/null; then
  PY=""
  for p in python3.12 python3.11 python3.10 python3; do
    command -v $p >/dev/null && $p -c 'import sys; sys.exit(sys.version_info < (3,10))' && { PY=$p; break; }
  done
  [ -z "$PY" ] && { log "need python >= 3.10"; exit 1; }
  log "creating venv at $VENV with $PY (first run takes a few minutes)"
  mkdir -p "$(dirname "$VENV")"
  $PY -m venv "$VENV"
  "$VENV/bin/pip" install -q --upgrade pip >&2
  # click/cloup pins: some cluster wheelhouses (e.g. Compute Canada's click 8.5.0+computecanada) break cloup
  "$VENV/bin/pip" install -q "manim>=0.19" "click==8.1.7" "cloup<3.1" imageio-ffmpeg >&2
fi

# ffmpeg for concat / cuts: system binary, else imageio-ffmpeg's static build
if ! command -v ffmpeg >/dev/null && [ ! -e "$VENV/bin/ffmpeg" ]; then
  "$VENV/bin/pip" install -q imageio-ffmpeg >&2
  ln -sf "$("$VENV/bin/python" -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" "$VENV/bin/ffmpeg"
  log "linked a pip-provided ffmpeg into the venv"
fi

missing=""
for t in latex dvisvgm; do command -v $t >/dev/null || missing="$missing $t"; done
if [ -n "$missing" ]; then
  log "MISSING:$missing. Run: bash $(cd "$(dirname "$0")" && pwd)/setup_env.sh --install-tex"
  log "  (or install TeX Live / MacTeX with your package manager)"
  exit 2
fi
if ! kpsewhich times.sty >/dev/null 2>&1; then log "WARNING: times.sty not found (tlmgr install psnfss)"; fi
"$VENV/bin/python" -c "import manim" && echo "$VENV"
