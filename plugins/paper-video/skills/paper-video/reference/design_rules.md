# Design rules

These were settled over many review rounds on real paper videos. Each rule exists because the alternative
looked worse on screen. `lib/paperstyle.py` encodes most of them; this file covers the rest.

## Look

- **Background**: cream `#FAF7F0`, with a faint dot grid and two very soft corner glows (`background()`).
- **Text is pure black (`TXT`), always.** Never use grey text, not for subtitles, axis labels or "minor" notes. `DIM` is
  for strokes only (arrows, axes, frames).
- **Fonts match the paper**: Times for text and Computer Modern for math (`TPL`). If the paper uses a different font
  (e.g. Palatino, Libertine), change the `\usepackage` in `TPL`.
- **Palette**, one meaning per colour, used consistently across scenes:
  - `BLUE #2A63C7` is the paper's method ("ours").
  - `AMBER #E2725B` (coral) is the method's key quantity (e.g. a learned score or value).
  - `RED #B8324F` is bad, loss or failure. `GREEN #2F9A60` is good or correct.
  - `TEAL` and `VIOLET` are secondary series only.
  - Baseline bars use the light fills `BASE_A`, `BASE_B` and `UNTUNED`.
- **Coloured text uses the darker shades** `BLUE_T` and `AMBER_T`. Fills keep the light colours.
- **Box outlines are thin black** (`set_stroke(TXT, 1.4)`), not the fill colour.
- **Headings** are centred, bold, at the top (`header()`). There are no chapter tags or section numbers on screen.
- Keep everything inside the safe frame. `Base` prints `!! BOUNDS` when something leaves it.

## Captions

- Captions sit at the bottom (`caption()`), at **≥ 40 pt**, and are **always one line** (each piece is `\mbox`ed and the caption
  shrinks to fit). If a caption doesn't fit at 40 pt, rewrite it shorter. Don't wrap it.
- Mark key words with `[[...]]`, which renders them in bold `BLUE_T`. `self.emph(cap)` grows the key words, then runs a blue
  `Circumscribe` around the caption. Use it on the 1–2 claims per scene that matter.
- Write plain sentences. Avoid hype words, emojis, "it's not X, it's Y", colon reveals and rhythm-driven three-item lists.

## Content

- **Broad idea only.** Name the key concept and show it with numbers on a toy example. Skip formal definitions,
  indices and derivations. For example, show a learned quantity as "a score" that goes 3 → 6 for a good step and 3 → 1 for a
  bad one, and *name* the underlying theorem without deriving it.
- If the paper has a loss, write it **in the video's own symbols** (the ones introduced on screen), not the paper's
  full notation.
- **One running example** that the viewer can track, e.g. `12 + 30 = ?` with a correct and an incorrect completion.
- Every number on screen is in `FACTS.md` with its source.

## Charts

- **Honest axes.** If an axis does not start at 0, draw `axis_break` and label the start value. Keep bar lengths
  proportional to the values. Don't make the paper's bar longer "for effect" (this was requested once and declined).
- Group baselines by family with italic coloured group labels (`hbar_chart` rows of kind `"group"`).
- Highlight "ours" by colour and bold, then add a bracket or annotation for the margin (e.g. "+4.0 over the next best").
- A per-task panel view can zoom each panel to its own range (with break marks) so small margins stay readable.
- State the evaluation setting in an italic one-line subtitle under the chart (model, length, metric).
- If the paper loses somewhere, say so in a caption ("Method A leads on Task 3 by 2.0").

## Pacing

- Target 2:30–3:00 overall. X free accounts cap video at 2:20, so plan a teaser or per-post clips anyway.
- `READ = 2.4 s` is the default hold after a beat. Holds are stretched by `hold_scale`.
- `Write` of text is never sped up (`text_scale ≥ 0.9`). Speed up shapes and bars with `anim_scale`.
- Results scenes can move faster (`anim_scale ≈ 0.55`). Concept scenes need slower holds.
- End on the title card, without fading to blank (`title_card`).

## Review checklist (run on every contact sheet)

1. No text overlaps another element, and no text is clipped at a frame edge.
2. No grey text anywhere. Coloured text uses `*_T` shades.
3. Every caption is on one line, ≥ 40 pt, and readable for at least ~2 s.
4. The first frame of each scene is not blank for more than ~0.5 s, and the final frame is not mid-fade.
5. Colours keep their meaning across scenes.
6. Charts have break marks wherever an axis is truncated, and the numbers match `FACTS.md`.
7. No `!! BOUNDS` lines and no LaTeX errors in the render logs.
