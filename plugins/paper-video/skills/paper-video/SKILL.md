---
name: paper-video
description: Make a polished, paper-styled manim explainer video for the research paper in the current directory (LaTeX sources or PDF), plus optional short social cuts, an X/Twitter thread and a LinkedIn post. Use when the user asks for a paper video, explainer animation, manim video, teaser or social-media video of their paper.
---

# paper-video

Turns the paper in the working directory into a ~2.5–3 min explainer video in a clean
"paper" look: cream background, black Times text, Computer Modern math, a small colour palette,
honest charts. The reference implementation is `examples/template_video.py`: six scenes (hook, problem,
idea, method, results, outro) with illustrative content that use every helper. **Read it before writing scenes**; reuse its patterns.

All paths below are relative to this skill's base directory (shown when the skill loads); call it `$SKILL`.

| File | Use |
|---|---|
| `scripts/setup_env.sh` | one-time install (venv + manim + ffmpeg fallback; `--install-tex` adds TinyTeX). Prints the venv path |
| `lib/paperstyle.py` | palette, text helpers, captions, tokens, gauges, bar charts, `Base` scene with pacing + bounds check, `title_card` |
| `scripts/render.sh VIDEO.py [m\|h] [Scene...]` | parallel per-scene render + concat → `<stem>_<q>.mp4` |
| `scripts/contact_sheet.sh VIDEO.mp4 OUT.png [every_s]` | tiled timestamped frames; Read the PNG to review |
| `scripts/social_cuts.py` | per-post clips and a short crossfaded teaser from scene renders |
| `scripts/count_posts.py THREAD.md` | per-post character counts (links = 23) |
| `reference/design_rules.md` | **the visual rules; follow all of them** |
| `reference/storyboard.md` | narrative arc + storyboard template |
| `reference/social.md` | thread / LinkedIn / posting guidance |

## Workflow

Work in `video/` next to the paper (create it). Keep the user in the loop at the storyboard and at the 720p review. Don't over-ask otherwise.

1. **Environment.** `VENV=$(bash $SKILL/scripts/setup_env.sh)`. The first run takes a few minutes.
   - Exit code 2 means LaTeX is missing. Ask the user before running `setup_env.sh --install-tex` (user-level TinyTeX, ~300 MB, no sudo).
   - The venv persists across projects.

2. **Read the paper.**
   - Prefer the LaTeX sources (`main.tex`, `sections/`, `\input` tree, `.bib` not needed). Otherwise use the PDF via `pdftotext -layout`, or the Read tool with pages.
   - Extract the problem, the key insight, the method (in one sentence and in one picture), why it works (theory, if any), the headline results, efficiency claims, the title and the authors.
   - Write `video/FACTS.md`: every number that will appear, with its source (`file:line` or table/figure number).
   - **Never invent or round numbers beyond the paper.** If the paper says "best on 3 of 4", the video does not say "best everywhere".

3. **Storyboard.** Write `video/STORYBOARD.md` from `reference/storyboard.md`. It has 6–9 scenes, each with its purpose, visuals, captions and a target duration. Show it to the user and revise once, then code.
   - Simplify hard. Show the broad idea, not every definition.
   - Use one running toy example across scenes, e.g. a tiny arithmetic problem the method acts on.
   - Use the paper's own words for named concepts.

4. **Write `video/video.py`.**
   - First copy `$SKILL/lib/paperstyle.py` into `video/` and start the file with `from paperstyle import *`. Don't import it from `$SKILL`: a plugin's install path changes on every update, and a self-contained `video/` keeps rendering later.
   - Write one class per scene, subclassing `Base`, in story order. `render.sh` discovers scenes in file order.
   - Tune pacing per scene with the class attributes `anim_scale`, `text_scale` and `hold_scale`, not by editing every `run_time`.

5. **Review at 720p.** Run `bash $SKILL/scripts/render.sh video/video.py m`, which takes ~30 s with scenes in parallel.
   - Fix every `!! BOUNDS` line and every error the script prints.
   - Make a contact sheet per scene: `bash $SKILL/scripts/contact_sheet.sh video/media/<S>/videos/video/720p30/<S>.mp4 /tmp/<S>.png 1`. Read each PNG and check it against the checklist in `design_rules.md`: overlaps, clipped text, grey text, captions on two lines, empty first or last frames, unreadable holds.
   - Iterate scene by scene. Pass `render.sh video/video.py m SceneName` to re-render one scene.
   - Never review at 480p15 (it looks jerky).

6. **Final.** Render `render.sh video/video.py h` (1080p60) once, after the user approves the 720p cut.

7. **Optional social package** (`reference/social.md`):
   - per-post clips cut at scene changes,
   - a ~40 s teaser that starts on a fully drawn result frame,
   - a thread checked with `count_posts.py`,
   - a LinkedIn post.

8. **Document** in `video/VIDEO_PROGRESS.md`: scenes and durations, decisions the user made, render commands and open items.

## Hard-won gotchas

- Colours passed to `T()` must be `"#rrggbb"` strings. Manim names like `WHITE` end up inside the LaTeX and break it.
- Parallel renders need separate `--media_dir` per scene; `render.sh` does this. A shared Tex cache races.
- Wait on background renders with `wait`. Never use `pgrep -f` loops, which match their own command line.
- `render.sh` passes `--disable_caching`. Stale partial-movie caches have shown old frames.
- ffmpeg 4.x: `tpad` inside an `xfade` filter chain fails to open the encoder. `social_cuts.py` pads in a second pass.
- When trimming clips, cut after a scene's fade-out completes. Check the first frame of every clip, since muted autoplay decides in about 2 s.
- If the paper is under double-blind review, leave authors off the title card (`title_card(..., authors=None)`) unless the user decides otherwise.
- Charts must not exaggerate. Truncated axes get `axis_break`, and bar lengths stay proportional to the values. Decline requests to stretch a bar while keeping its label.
