"""paperstyle: shared look and helpers for research-paper explainer videos (manim CE >= 0.19).

Usage in a video file:
    import sys; sys.path.insert(0, "<skill>/lib")      # or copy this file next to the video
    from paperstyle import *

    class Hook(Base):
        def construct(self):
            h = header("RL post-training")
            cap = caption("Reward only on the [[finished]] answer.")
            self.play(Write(h), run_time=1.2)
            self.play(FadeIn(cap), run_time=0.8); self.emph(cap); self.wait(READ)
            self.clear_all()

Design rules this module encodes (see reference/design_rules.md):
  cream background, ALL text pure black (never grey), coloured text uses the darker *_T shades,
  thin black outlines on boxes, Times text + Computer Modern math (matches most papers),
  bottom captions >= 40 pt on one line with [[key words]] in bold blue, honest chart axes.
"""
from manim import *
import numpy as np
import re

# ---------------------------------------------------------------- palette (paper-like, on cream)
BG = "#FAF7F0"
TXT = "#000000"
DIM = "#8C8476"    # strokes only (arrows, frames, axes); NEVER text
FAINT = "#DCD5C6"
CELL = "#F0EBE0"
BLUE = "#2A63C7"   # cobalt: the paper's own method ("ours")
TEAL = "#23948A"
AMBER = "#E2725B"  # coral: the method's key quantity
VIOLET = "#7457AE"
RED = "#B8324F"    # rose: bad / loss / failure
GREEN = "#2F9A60"  # good / correct
BLUE_T = "#1B4A9C"   # darker shades for coloured TEXT and equations; fills keep BLUE / AMBER
AMBER_T = "#B4462E"
BASE_A = "#BCCDEB"   # baseline family A bars
BASE_B = "#D5C8EA"   # baseline family B bars
UNTUNED = "#D3CBBB"  # untuned / base model bars
OURS = BLUE

config.background_color = BG

TPL = TexTemplate()
TPL.add_to_preamble(r"\usepackage[T1]{fontenc}\usepackage{times}\usepackage{amsmath,amssymb,bm,mathtools}"
                    r"\hyphenpenalty=10000\exhyphenpenalty=10000")

SAFE_X = config.frame_width / 2 - 0.35
SAFE_Y = config.frame_height / 2 - 0.15
READ = 2.4   # default hold after a beat, so the viewer can read it
ANIM = 0.75  # non-text animations play at this fraction of their written run_time ...
HOLD = 1.3   # ... and reading pauses (>= 1 s) are stretched by this factor plus 0.4 s


# ---------------------------------------------------------------- text
def T(*args, size=38, color=TXT, **kw):
    """T(tex..., [size], [colour]). Colours MUST be '#rrggbb' strings (manim names like WHITE break the tex)."""
    texs = []
    for a in args:
        if isinstance(a, (int, float)):
            size = a
        elif isinstance(a, str) and a.startswith("#"):
            color = a
        else:
            texs.append(a)
    if len(texs) == 1 and r"\\" not in texs[0]:
        texs = [r"\mbox{" + texs[0] + "}"]
    return Tex(*texs, tex_template=TPL, font_size=size, color=color, **kw)


def M(*s, size=42, color=TXT, **kw):
    return MathTex(*s, tex_template=TPL, font_size=size, color=color, **kw)


def fit(m, w=None, h=None):
    if w is not None and m.width > w:
        m.scale_to_fit_width(w)
    if h is not None and m.height > h:
        m.scale_to_fit_height(h)
    return m


def header(s, size=46):
    """Centred bold heading at the top. No chapter tags."""
    h = T(r"\textbf{" + s + "}", size)
    fit(h, w=2 * SAFE_X - 0.2)
    h.move_to([0, 3.2, 0])
    return h


def caption(s, size=40, color=TXT, y=-3.3):
    """Bottom caption, always one line. [[...]] marks key words: bold BLUE_T, and they grow when emph() runs."""
    size = max(size, 40)
    pieces, keys = [], []
    for part in re.split(r"(\[\[.*?\]\])", s):
        if not part:
            continue
        key = part.startswith("[[")
        txt = part[2:-2] if key else part
        txt = "$".join(seg if i % 2 else seg.replace(" ", "~") for i, seg in enumerate(txt.split("$")))
        pieces.append(txt)
        keys.append(key)

    def build(grow):
        args = [(r"\textbf{" + (r"\large " if grow else "") + t + "}") if k else t for t, k in zip(pieces, keys)]
        args = [r"\mbox{" + x + "}" for x in args]
        m = Tex(*args, arg_separator="", tex_template=TPL, font_size=size, color=color)
        for sub, k in zip(m, keys):
            if k:
                sub.set_color(BLUE_T)
        return m

    c = build(False)
    big = build(True)
    sc = min(1.0, 12.6 / c.width, 12.6 / big.width)
    c.scale(sc).move_to([0, y, 0])
    big.scale(sc).move_to([0, y, 0])
    c.big = big if any(keys) else None
    return c


# ---------------------------------------------------------------- backdrop
def background():
    g = VGroup()
    for x in np.arange(-7.0, 7.01, 0.5):
        for y in np.arange(-4.0, 4.01, 0.5):
            g.add(Dot([x, y, 0], radius=0.011, color=FAINT))
    for r in np.linspace(4.5, 0.5, 8):
        g.add(Circle(r, stroke_width=0).set_fill(BLUE, 0.006).move_to([-6, 3.6, 0]))
        g.add(Circle(r, stroke_width=0).set_fill(AMBER, 0.008).move_to([6, -3.6, 0]))
    g.set_z_index(-10)
    return g


# ---------------------------------------------------------------- tokens / boxes
def box(w, h, fill=CELL, opacity=1.0, r=0.1):
    """Rounded box with the house style: light fill, thin black edge."""
    return RoundedRectangle(corner_radius=r, width=w, height=h).set_fill(fill, opacity).set_stroke(TXT, 1.4)


def labelled_box(label, w=None, h=0.9, fill=CELL, opacity=1.0, size=32, color=TXT):
    t = T(label, size, color)
    b = box(w or t.width + 0.5, h, fill, opacity)
    t.move_to(b)
    return VGroup(b, t)


def word_tokens(words, h=0.82, size=46):
    """One masked box per word (text hidden, three dots shown); words share one baseline."""
    sent = T(*words, size=size, color=TXT)
    toks = VGroup()
    for i in range(len(words)):
        txt = sent[i].copy()
        b = RoundedRectangle(corner_radius=0.1, width=max(0.75, txt.width + 0.36), height=h)
        b.set_fill(CELL, 1).set_stroke(FAINT, 1.8)
        dy = sent[i].get_y() - sent.get_y()
        txt.move_to(b).shift(UP * dy).set_opacity(0)
        dot = VGroup(*[Dot(radius=0.035, color=DIM) for _ in range(3)]).arrange(RIGHT, buff=0.07).move_to(b)
        toks.add(VGroup(b, txt, dot))
    return toks


def shown(tok, color):
    tok[0].set_fill(color, 0.16).set_stroke(TXT, 1.4)
    tok[1].set_opacity(1)
    tok[2].set_opacity(0)
    return tok


def reveal_anims(tok, color):
    b, txt, dot = tok
    return [b.animate.set_fill(color, 0.16).set_stroke(TXT, 1.4),
            txt.animate.set_opacity(1), dot.animate.set_opacity(0)]


def strip(n, filled, color=BLUE, s=0.26, buff=0.05, new=()):
    """Row of n small squares; `filled` indices coloured, `new` ones in AMBER (e.g. a sequence state)."""
    g = VGroup()
    for i in range(n):
        sq = RoundedRectangle(corner_radius=0.05, width=s, height=s)
        if i in new:
            sq.set_fill(AMBER, 0.9).set_stroke(TXT, 1)
        elif i in filled:
            sq.set_fill(color, 0.85).set_stroke(TXT, 1)
        else:
            sq.set_fill(CELL, 1).set_stroke(DIM, 1.1, 0.6)
        g.add(sq)
    return g.arrange(RIGHT, buff=buff)


def gauge(value, height=1.0, width=0.22, color=None):
    """Vertical meter, value in [0,1]; red -> coral -> green unless a colour is given."""
    frame = RoundedRectangle(corner_radius=0.05, width=width, height=height).set_stroke(DIM, 1.4).set_fill(CELL, 1)
    if color is None:
        col = interpolate_color(ManimColor(RED), ManimColor(AMBER), 2 * value) if value < 0.5 else \
            interpolate_color(ManimColor(AMBER), ManimColor(GREEN), 2 * value - 1)
    else:
        col = color
    fill = RoundedRectangle(corner_radius=0.04, width=width - 0.06, height=max(0.02, (height - 0.06) * value))
    fill.set_fill(col, 0.9).set_stroke(width=0)
    fill.align_to(frame, DOWN).shift(UP * 0.03)
    return VGroup(frame, fill)


def arrow(a, b, color=DIM, width=2.5, buff=0.1):
    return Arrow(a, b, buff=buff, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=0.25, max_stroke_width_to_length_ratio=8)


def delta_label(d, size=30, fmt="{:.2f}"):
    c = GREEN if d > 0 else RED
    return T(("+" if d > 0 else r"$-$") + fmt.format(abs(d)), size, c)


def axis_break(x, y, color=DIM):
    """Two short slanted strokes: mark an axis that does not start at 0. Use whenever an axis is truncated."""
    return VGroup(Line([x - 0.09, y, 0], [x + 0.09, y + 0.08, 0], stroke_width=1.8, color=color),
                  Line([x - 0.09, y + 0.08, 0], [x + 0.09, y + 0.16, 0], stroke_width=1.8, color=color))


# ---------------------------------------------------------------- charts
def hbar_chart(rows, v0=0.0, x0=-2.3, scale=None, pitch=0.385, ytop=2.25, vmax=None, width=7.0,
               name_size=27, fmt="%.1f", group_colors=None):
    """Horizontal bar chart. rows = [(kind, name, value, family)], kind 'row' or 'group' (a family heading).
    family 'ours' is drawn bold in OURS; others use group_colors[family] (fill colour).
    v0 > 0 truncates the axis; an axis_break is added automatically (honest axes).
    Returns (VGroup axis, dict family -> [(name, bar, value_label)], dict family -> group label, dict name -> bar)."""
    group_colors = group_colors or {}
    vals = [v for k, _, v, _ in rows if k == "row"]
    vmax = vmax or max(vals)
    scale = scale or width / (vmax - v0)
    by_fam, glabels, bar_of = {}, {}, {}
    for k, (kind, nm, v, fam) in enumerate(rows):
        y = ytop - k * pitch
        if kind == "group":
            g = T(r"\textbf{\textit{" + nm + "}}", name_size + 1, group_colors.get(fam + "_text", BLUE_T))
            g.move_to([x0 - 0.2 - g.width / 2, y, 0])
            glabels[fam] = g
            continue
        ours = fam == "ours"
        n = T((r"\textbf{" + nm + "}") if ours else nm, name_size, BLUE_T if ours else TXT)
        n.move_to([x0 - 0.2 - n.width / 2, y, 0])
        fill = OURS if ours else group_colors.get(fam, BASE_A)
        bar = Rectangle(width=max(0.02, (v - v0) * scale), height=pitch * 0.68).set_fill(fill, 0.95).set_stroke(width=0)
        bar.move_to([x0 + (v - v0) * scale / 2, y, 0])
        t = T((r"\textbf{" + fmt % v + "}") if ours else fmt % v, name_size, BLUE_T if ours else TXT)
        t.next_to(bar, RIGHT, buff=0.12)
        by_fam.setdefault(fam, []).append((n, bar, t))
        bar_of[nm] = bar
    ybot = ytop - (len(rows) - 1) * pitch - 0.25
    axis = VGroup(Line([x0, ytop + 0.25, 0], [x0, ybot, 0], color=DIM, stroke_width=1.5))
    if v0 > 0:
        axis.add(axis_break(x0, ybot + 0.1))
    return axis, by_fam, glabels, bar_of


# ---------------------------------------------------------------- base scene
class Base(Scene):
    """Every scene subclasses this. Per-scene pacing knobs:
    anim_scale (non-text animations), text_scale (Write of text), hold_scale (pauses >= 1 s)."""
    anim_scale = ANIM
    hold_scale = HOLD
    text_scale = 1.15

    def setup(self):
        self.bg = background()
        self.add(self.bg)

    def play(self, *args, **kwargs):
        if "run_time" in kwargs:
            writes_text = any(isinstance(a, Write) for a in args)
            kwargs["run_time"] *= self.text_scale if writes_text else self.anim_scale
        super().play(*args, **kwargs)
        self._check_bounds()

    def wait(self, duration=1.0, *args, **kwargs):
        if duration >= 1.0:
            duration = duration * self.hold_scale + (0.4 if self.hold_scale > 1.0 else 0.2)
        super().wait(duration, *args, **kwargs)

    def _check_bounds(self):
        """Prints '!! BOUNDS' whenever something leaves the safe frame; render.sh greps for it."""
        for m in self.mobjects:
            if m is self.bg:
                continue
            pts = [sm for sm in m.get_family() if isinstance(sm, VMobject) and sm.has_points()
                   and (sm.get_fill_opacity() > 0.01 or sm.get_stroke_opacity() > 0.01)]
            if not pts:
                continue
            g = VGroup(*pts)
            if g.get_left()[0] < -SAFE_X - 0.15 or g.get_right()[0] > SAFE_X + 0.15 or \
               g.get_bottom()[1] < -SAFE_Y - 0.1 or g.get_top()[1] > SAFE_Y + 0.1:
                print(f"!! BOUNDS {type(self).__name__} t={self.renderer.time:.1f}s {type(m).__name__} "
                      f"x[{g.get_left()[0]:.2f},{g.get_right()[0]:.2f}] y[{g.get_bottom()[1]:.2f},{g.get_top()[1]:.2f}]")

    def emph(self, mob):
        """Key words of a caption grow, then a blue rectangle runs around the claim."""
        if getattr(mob, "big", None) is not None:
            self.play(Transform(mob, mob.big), run_time=0.8)
        self.play(Circumscribe(mob, color=BLUE, buff=0.15, time_width=0.6, stroke_width=3), run_time=1.6)

    def clear_all(self, run_time=1.0, keep=()):
        mobs = [m for m in self.mobjects if m is not self.bg and m not in keep]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def grow_bars(self, items, run_time=1.0, extra=()):
        """Animate [(name, bar, value_label)] from hbar_chart, staggered."""
        anims = [AnimationGroup(FadeIn(n), GrowFromEdge(b, LEFT), FadeIn(t)) for n, b, t in items]
        self.play(*extra, LaggedStart(*anims, lag_ratio=0.12), run_time=run_time)


def title_card(scene, acronym, title, authors=None, affiliation=None, colors=None):
    """Outro: big acronym, title, optional authors. Ends on the card (no fade to blank).
    Leave authors=None while the paper is under double-blind review."""
    colors = colors or [OURS] * len(acronym)
    letters = VGroup(*[T(r"\textbf{" + c + "}", 170, col) for c, col in zip(acronym, colors)])
    letters.arrange(RIGHT, buff=0.25).move_to([0, 1.3, 0])
    fit(letters, w=12.0)
    t = T(r"\textbf{" + title + "}", 44)
    fit(t, w=12.4).move_to([0, -0.5, 0])
    line = Line(LEFT * 4, RIGHT * 4, stroke_width=2, color=OURS).next_to(t, DOWN, buff=0.4)
    scene.play(LaggedStart(*[FadeIn(l, scale=0.6) for l in letters], lag_ratio=0.15), run_time=1.4)
    scene.play(Write(t), run_time=1.8)
    extra = []
    if authors:
        a = T(authors, 36, TXT).next_to(line, DOWN, buff=0.4)
        extra.append(FadeIn(a, shift=UP * 0.1))
        if affiliation:
            extra.append(FadeIn(T(r"\textit{" + affiliation + "}", 30, TXT).next_to(a, DOWN, buff=0.2), shift=UP * 0.1))
    scene.play(Create(line), *extra, run_time=1.2)
    scene.wait(1.2)
