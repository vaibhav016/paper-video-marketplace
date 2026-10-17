"""Reference template for a paper explainer video. Every number and claim here is ILLUSTRATIVE.
Copy to video/video.py (with lib/paperstyle.py next to it) and replace the content scene by scene.

It shows the patterns a full video needs:
  Hook     heading + running toy example revealed token by token + emphasised caption
  Problem  a chain of intermediate states, a value curve with one bad step boxed, the named concept
  Idea     gauges for "before / after", good vs bad branch, the key rule as a caption
  Method   labelled boxes + arrows (a mechanism diagram) and the objective in the video's own symbols
  Results  grouped bar chart with a truncated axis (break mark) and a margin bracket; per-task zoomed panels
  Outro    title card (authors left off, e.g. during double-blind review)

Smoke test:  bash $SKILL/scripts/render.sh $SKILL/examples/template_video.py m
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))                     # paperstyle copied next to the video
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))  # or the skill's lib/
from paperstyle import *  # noqa: E402,F403


# ================================================================= 1. HOOK
class Hook(Base):
    anim_scale = 1.0

    def construct(self):
        h = header("A model is graded only on its final answer")
        toks = word_tokens(["12", "+", "30", "=", "42"]).arrange(RIGHT, buff=0.08).move_to([0, 0.9, 0])
        self.play(Write(h), run_time=1.2)
        self.play(FadeIn(toks), run_time=0.6)
        for i, c in zip(range(5), [BLUE] * 4 + [GREEN]):
            self.play(*reveal_anims(toks[i], c), run_time=0.35)
        reward = labelled_box(r"reward $=1$", h=0.8, fill=GREEN, opacity=0.16, size=34).next_to(toks, DOWN, buff=0.9)
        self.play(GrowArrow(arrow(toks.get_bottom(), reward.get_top())), FadeIn(reward), run_time=0.8)
        cap = caption(r"One number for the whole answer. Which [[steps]] earned it?")
        self.play(FadeIn(cap), run_time=0.8)
        self.emph(cap)
        self.wait(READ)
        self.clear_all()


# ================================================================= 2. PROBLEM
class Problem(Base):
    def construct(self):
        h = header("Every step gets the same credit")
        xs = np.linspace(-5.0, 5.0, 6)
        orders = [[], [1], [1, 3], [0, 1, 3], [0, 1, 2, 3], [0, 1, 2, 3, 4]]
        states = VGroup(*[strip(5, set(o), s=0.24).move_to([x, 1.6, 0]) for x, o in zip(xs, orders)])
        arrows = VGroup(*[arrow(a.get_right(), b.get_left(), width=2) for a, b in zip(states[:-1], states[1:])])
        credit = VGroup(*[labelled_box(r"$+A$", w=0.7, h=0.45, fill=RED, opacity=0.12, size=26)
                          .next_to(a, UP, buff=0.15) for a in arrows])
        self.play(Write(h), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(s) for s in states], lag_ratio=0.15), Create(arrows), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in credit], lag_ratio=0.1), run_time=1.0)

        # value of each intermediate state; one step goes down
        vals = [0.40, 0.55, 0.30, 0.50, 0.70, 0.90]
        y0, H = -2.4, 2.0
        pts = [np.array([x, y0 + v * H, 0]) for x, v in zip(xs, vals)]
        label = T(r"\textit{expected reward of the partial answer}", 26).move_to([0, 0.75, 0])
        segs = VGroup(*[Line(a, b, stroke_width=4, color=GREEN if vb > va else RED)
                        for a, b, va, vb in zip(pts[:-1], pts[1:], vals[:-1], vals[1:])])
        dots = VGroup(*[Dot(p, radius=0.06, color=TXT) for p in pts])
        deltas = VGroup(*[delta_label(vb - va, 26).move_to((a + b) / 2 + UP * 0.3)
                          for a, b, va, vb in zip(pts[:-1], pts[1:], vals[:-1], vals[1:])])
        self.play(FadeIn(label), FadeIn(dots), run_time=0.6)
        self.play(Create(segs), FadeIn(deltas), run_time=1.4)
        bad = SurroundingRectangle(VGroup(credit[1], segs[1], deltas[1]), color=RED, buff=0.12, stroke_width=3)
        cap = caption(r"A step that [[hurt]] the answer still receives the same $+A$.")
        self.play(Create(bad), FadeIn(cap), run_time=1.0)
        self.emph(cap)
        self.wait(READ)
        self.clear_all(run_time=0.8)
        name = T(r"\textbf{the named failure mode}", 60, RED).move_to([0, 0.4, 0])
        self.play(FadeIn(name, scale=0.9), run_time=1.0)
        self.wait(1.5)
        self.clear_all()


# ================================================================= 3. IDEA
class Idea(Base):
    def construct(self):
        h = header("What if we scored every step?")

        def eq(last, col=None):
            t = word_tokens(["12", "+", "30", "=", last], h=0.7, size=38).arrange(RIGHT, buff=0.07)
            for k in t[:4]:
                shown(k, BLUE)
            if col:
                shown(t[4], col)
            return t

        start = eq("?").move_to([-3.4, 0.2, 0])
        g0 = gauge(0.5, height=1.4).next_to(start, LEFT, buff=0.35)
        good = eq("42", GREEN).move_to([2.4, 1.4, 0])
        bad = eq("32", RED).move_to([2.4, -1.0, 0])
        g1 = gauge(0.95, height=1.4).next_to(good, RIGHT, buff=0.35)
        g2 = gauge(0.1, height=1.4).next_to(bad, RIGHT, buff=0.35)
        a1 = arrow(start.get_right(), good.get_left(), color=GREEN)
        a2 = arrow(start.get_right(), bad.get_left(), color=RED)
        l1 = T(r"\textbf{good step:} score $3 \to 6$", 28, GREEN).next_to(good, UP, buff=0.2)
        l2 = T(r"\textbf{bad step:} score $3 \to 1$", 28, RED).next_to(bad, DOWN, buff=0.2)
        self.play(Write(h), run_time=1.2)
        self.play(FadeIn(start), FadeIn(g0), run_time=0.8)
        self.play(GrowArrow(a1), FadeIn(good), FadeIn(g1), FadeIn(l1), run_time=1.0)
        self.play(GrowArrow(a2), FadeIn(bad), FadeIn(g2), FadeIn(l2), run_time=1.0)
        cap = caption(r"Judge each step by whether it [[raises]] or [[lowers]] the score.")
        self.play(FadeIn(cap), run_time=0.8)
        self.emph(cap)
        self.wait(READ)
        self.clear_all()


# ================================================================= 4. METHOD
class Method(Base):
    def construct(self):
        h = header("How the method trains on one step")
        model = labelled_box(r"\textbf{model}", w=2.6, h=0.8, fill=BLUE, opacity=0.18, size=34).move_to([0, 1.9, 0])
        head = labelled_box("score head", w=2.6, h=0.75, fill=AMBER, opacity=0.18, size=30).move_to([-3.2, 0.4, 0])
        probs = labelled_box("token probabilities", w=3.4, h=0.75, fill=BLUE, opacity=0.10, size=30).move_to([3.2, 0.4, 0])
        gain = M(r"\text{gain}", size=38, color=AMBER_T).next_to(head, DOWN, buff=0.5)
        boost = M(r"\text{boost}", size=38, color=BLUE_T).next_to(probs, DOWN, buff=0.5)
        self.play(Write(h), run_time=1.2)
        self.play(FadeIn(model), run_time=0.6)
        self.play(GrowArrow(arrow(model.get_left(), head.get_top())), FadeIn(head),
                  GrowArrow(arrow(model.get_right(), probs.get_top())), FadeIn(probs), run_time=1.0)
        self.play(GrowArrow(arrow(head.get_bottom(), gain.get_top())), Write(gain),
                  GrowArrow(arrow(probs.get_bottom(), boost.get_top())), Write(boost), run_time=1.0)
        loss = M(r"\mathcal{L} = (\,", r"\text{boost}", r" - ", r"\text{gain}", r"\,)^2", size=46)
        loss[1].set_color(BLUE_T)
        loss[3].set_color(AMBER_T)
        loss.move_to([0, -1.9, 0])
        self.play(Write(loss), run_time=1.4)
        cap = caption(r"Training shrinks the [[mismatch]] on every sampled step.")
        self.play(FadeIn(cap), run_time=0.8)
        self.emph(cap)
        self.wait(READ)
        self.clear_all()


# ================================================================= 5. RESULTS
class Results(Base):
    anim_scale = 0.55
    text_scale = 0.9
    hold_scale = 1.0

    def construct(self):
        h = header("Best average accuracy among the compared methods")
        rows = [("row", "Ours", 70.0, "ours"),
                ("group", "Family A", None, "a"), ("row", "Method A1", 66.0, "a"), ("row", "Method A2", 58.0, "a"),
                ("group", "Family B", None, "b"), ("row", "Method B1", 64.5, "b"), ("row", "Method B2", 55.0, "b"),
                ("row", "Base model", 42.0, "base")]
        axis, fam, glab, bar_of = hbar_chart(rows, v0=40, x0=-2.3, ytop=2.1, pitch=0.48, width=6.0,
                                             group_colors={"a": BASE_B, "b": BASE_A, "base": UNTUNED,
                                                           "a_text": VIOLET, "b_text": BLUE_T})
        sub = T(r"\textit{illustrative numbers; state model, benchmark and metric here}", 26)
        fit(sub, w=12.4).move_to([0, -3.55, 0])
        self.play(Write(h), run_time=1.2)
        self.play(Create(axis), FadeIn(sub), run_time=0.6)
        for f in ["base", "b", "a"]:
            self.grow_bars(fam[f], run_time=1.0, extra=[FadeIn(glab[f])] if f in glab else [])
        self.wait(0.6)
        self.grow_bars(fam["ours"], run_time=0.9)
        top, nxt = bar_of["Ours"], bar_of["Method A1"]
        xr = top.get_right()[0] + 0.95
        br = VGroup(Line([xr, top.get_y(), 0], [xr + 0.2, top.get_y(), 0]),
                    Line([xr + 0.2, top.get_y(), 0], [xr + 0.2, nxt.get_y(), 0]),
                    Line([xr, nxt.get_y(), 0], [xr + 0.2, nxt.get_y(), 0])).set_stroke(BLUE, 2.5)
        gain = VGroup(T(r"\textbf{+4.0}", 40, BLUE_T), T("over the next best", 24, BLUE_T)).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
        gain.next_to(br, RIGHT, buff=0.15)
        self.play(Create(br), FadeIn(gain), run_time=0.8)
        self.wait(READ)
        self.clear_all()

        # per-task panels, each zoomed to its own range with a break mark (honest axes)
        h2 = header("Task by task, against the strongest other method")
        self.play(Write(h2), run_time=1.2)
        tasks = [("Task 1", 80.0, 77.5, "A1", 70, 85), ("Task 2", 45.0, 43.0, "B1", 35, 50),
                 ("Task 3", 72.0, 74.0, "A1", 65, 80)]
        y0, H = -1.3, 3.2
        panels = []
        for x, (tn, ours, other, on, lo, hi) in zip([-4.2, 0.0, 4.2], tasks):
            def hgt(v, lo=lo, hi=hi):
                return max(0.04, (v - lo) / (hi - lo) * H)
            ob = Rectangle(width=0.7, height=hgt(other)).set_fill(BASE_A, 0.95).set_stroke(width=0)
            ob.move_to([x - 0.5, y0 + hgt(other) / 2, 0])
            pb = Rectangle(width=0.7, height=hgt(ours)).set_fill(OURS, 0.95).set_stroke(width=0)
            pb.move_to([x + 0.5, y0 + hgt(ours) / 2, 0])
            ax_x = x - 1.2
            frame = VGroup(Line([ax_x, y0, 0], [ax_x, y0 + H, 0], stroke_width=1.5, color=DIM),
                           Line([ax_x, y0, 0], [x + 1.1, y0, 0], stroke_width=1.5, color=DIM),
                           axis_break(ax_x, y0 + 0.12))
            for v in (lo, hi):
                yy = y0 + (v - lo) / (hi - lo) * H
                frame.add(T(str(v), 20).next_to([ax_x, yy, 0], LEFT, buff=0.08))
            texts = VGroup(T("%.1f" % other, 28).next_to(ob, UP, buff=0.1),
                           T(r"\textbf{%.1f}" % ours, 30, BLUE_T).next_to(pb, UP, buff=0.1),
                           T(on, 24).next_to(ob, DOWN, buff=0.12), T("Ours", 24, BLUE_T).next_to(pb, DOWN, buff=0.12),
                           T(r"\textbf{" + tn + "}", 32).move_to([x, y0 - 0.8, 0]))
            panels.append((frame, ob, pb, texts))
        self.play(*[FadeIn(p[0]) for p in panels], run_time=0.8)
        for frame, ob, pb, texts in panels:
            self.play(GrowFromEdge(ob, DOWN), GrowFromEdge(pb, DOWN), FadeIn(texts), run_time=0.7)
        cap = caption(r"Best on [[Task 1]] and [[Task 2]]; A1 leads on Task 3 by 2.0.", y=-3.15)
        self.play(FadeIn(cap), run_time=0.8)
        self.emph(cap)
        self.wait(1.2)
        self.clear_all()


# ================================================================= 6. OUTRO
class Outro(Base):
    anim_scale = 0.6

    def construct(self):
        title_card(self, "DEMO", "A Template for Paper Explainer Videos")   # authors=None during double-blind review
