# paper-video

A Claude Code plugin that turns the research paper in your working directory into a polished
[manim](https://www.manim.community/) explainer video. The video uses a clean paper look: cream background, black Times text,
Computer Modern math, a small consistent palette and honest charts. The plugin can also produce short social cuts, an X thread and a
LinkedIn post.

## Install

```
/plugin marketplace add <github-user>/paper-video-marketplace
/plugin install paper-video@paper-video
```

You can also install from a local clone: `/plugin marketplace add /path/to/paper-video-marketplace`.

## Use

`cd` into a paper's directory (LaTeX sources or a PDF) and ask:

> make an explainer video for this paper

Claude reads the paper and records every number it will show in `video/FACTS.md`. It writes a storyboard for your OK, then
codes the scenes. It reviews renders at 720p using contact sheets, renders the final at 1080p60, and documents the
result in `video/VIDEO_PROGRESS.md`.

## Requirements

On first use, the skill runs `scripts/setup_env.sh`. It creates a persistent venv in
`~/.local/share/paper-video/venv` (override with `PAPER_VIDEO_VENV`) with manim, and links a pip-provided
ffmpeg into it if your system has none.

You need:
- Python ≥ 3.10.
- A LaTeX install with `latex` and `dvisvgm` on PATH. If you have none, `setup_env.sh --install-tex` installs TinyTeX at user level, without sudo, together with the needed packages.
- On Linux, manim's wheels may need system cairo/pango. See the [manim install docs](https://docs.manim.community/en/stable/installation.html) if pip fails.

## What's inside

```
plugins/paper-video/skills/paper-video/
  SKILL.md                    workflow Claude follows
  lib/paperstyle.py           palette, captions, tokens, gauges, bar charts, Base scene (pacing + bounds check)
  scripts/setup_env.sh        one-time environment install
  scripts/render.sh           parallel per-scene render + concat
  scripts/contact_sheet.sh    tiled frames for review
  scripts/social_cuts.py      per-post clips and crossfaded teasers
  scripts/count_posts.py      thread character counts
  reference/                  design rules, storyboard template, social guidance
  examples/template_video.py  reference template (6 scenes, illustrative content) / smoke test
```

Smoke test: `bash plugins/paper-video/skills/paper-video/scripts/render.sh plugins/paper-video/skills/paper-video/examples/template_video.py m`

## License

MIT
