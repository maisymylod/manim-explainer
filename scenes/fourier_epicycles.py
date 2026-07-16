"""
Fourier series, the 3Blue1Brown way: a square wave built from rotating vectors.

The whole scene follows one arc — *feel it before you formalize it*:

    1. ONE vector rotating, its tip tracing a circle.
    2. A second, then a third vector chained tip-to-tip: "a sum of rotations".
    3. The tip of the last vector drives a pen that draws a curve over time.
       With enough odd harmonics that curve snaps into a square wave. (payoff)
    4. Only now does the equation appear, and each term lights up in sync with
       the vector it stands for.

Everything cool-toned is scaffolding; the warm yellow is always "the answer"
(the traced wave). Run:

    manim -qh scenes/fourier_epicycles.py FourierEpicycles
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np  # noqa: E402
from manim import (  # noqa: E402
    Scene,
    Circle,
    Arrow,
    Line,
    DashedVMobject,
    VMobject,
    VGroup,
    MathTex,
    Dot,
    TracedPath,
    Create,
    Write,
    FadeIn,
    FadeOut,
    Indicate,
    always_redraw,
    ValueTracker,
    linear,
    PI,
    LEFT,
    RIGHT,
    DOWN,
    UP,
    config,
)
from helpers import PALETTE, component_color, title_text, caption  # noqa: E402

config.background_color = PALETTE["bg"]

# --- Fixed geometry for the whole scene ------------------------------------
CENTER = np.array([-4.3, 0.0, 0.0])   # where the epicycle chain is pinned
GRAPH_X0 = -1.4                        # x where the drawn wave begins
H_SCALE = 0.55                         # world-x per unit of angle (time -> x)
N_FULL = 7                             # harmonics used for the final square wave


def freq(k: int) -> int:
    """Odd frequencies 1, 3, 5, ... — a square wave has only odd harmonics."""
    return 2 * k + 1


def amp(k: int) -> float:
    """Amplitudes fall off like 1/n: the 4/(pi n) Fourier coefficients."""
    return 4 / (PI * freq(k))


class FourierEpicycles(Scene):
    def construct(self):
        # A single clock that drives every rotation. Advancing it turns all the
        # vectors at once; every mobject below reads its value each frame.
        self.t = ValueTracker(0.0)

        self.intro()
        self.one_vector()
        self.add_more_vectors()
        self.draw_the_wave()
        self.reveal_equation()
        self.outro()

    # ------------------------------------------------------------------ utils
    def tip_after(self, n: int, time: float) -> np.ndarray:
        """Where the chain of the first n vectors ends at a given time."""
        p = CENTER.copy()
        for k in range(n):
            ang = freq(k) * time
            p = p + amp(k) * np.array([np.cos(ang), np.sin(ang), 0.0])
        return p

    def build_chain(self, n: int, time: float) -> VGroup:
        """A static snapshot of n vectors chained tip-to-tip, each on its
        faint guide circle. Returned as a VGroup of per-harmonic VGroups so a
        single harmonic can later be indexed and highlighted."""
        chain = VGroup()
        p = CENTER.copy()
        for k in range(n):
            ang = freq(k) * time
            nxt = p + amp(k) * np.array([np.cos(ang), np.sin(ang), 0.0])
            guide = Circle(
                radius=amp(k),
                color=PALETTE["structure_dim"],
                stroke_width=1.5,
                stroke_opacity=0.45,
            ).move_to(p)
            vec = Arrow(
                p, nxt, buff=0,
                color=component_color(k),
                stroke_width=3.5,
                max_tip_length_to_length_ratio=0.22,
                max_stroke_width_to_length_ratio=8,
            )
            chain.add(VGroup(guide, vec))
            p = nxt
        return chain

    def live_chain(self, n: int) -> VGroup:
        """The same chain, but redrawn every frame as the clock turns."""
        return always_redraw(lambda: self.build_chain(n, self.t.get_value()))

    def spin(self, revolutions: float, run_time: float):
        """Advance the fundamental by whole turns at constant angular speed."""
        self.play(
            self.t.animate.set_value(self.t.get_value() + revolutions * 2 * PI),
            run_time=run_time,
            rate_func=linear,
        )

    # ----------------------------------------------------------------- beats
    def intro(self):
        # Set the question before any machinery appears.
        self.title = title_text("A square wave from spinning arrows")
        self.play(Write(self.title))
        self.wait(0.8)

    def one_vector(self):
        # ONE rotating vector. Its tip traces a circle — the atom of the whole
        # idea. We let the tip's own path draw itself so the circle feels earned.
        self.chain = self.live_chain(1)
        tip_trace = TracedPath(
            lambda: self.tip_after(1, self.t.get_value()),
            stroke_color=PALETTE["sum"],
            stroke_width=3,
        )
        self.add(tip_trace, self.chain)
        note = caption("one arrow, turning at a steady rate").to_edge(DOWN)
        self.play(FadeIn(note, shift=0.3 * UP))
        self.spin(1, run_time=4.0)     # exactly one revolution -> a full circle
        self.wait(0.6)
        self.play(FadeOut(note), FadeOut(tip_trace))

    def add_more_vectors(self):
        # Add a second, then a third vector, each pinned to the tip of the last.
        # The combined tip now traces a lumpier curve: a *sum of rotations*.
        note = caption("stack a faster, smaller arrow on its tip").to_edge(DOWN)
        self.play(FadeIn(note, shift=0.3 * UP))

        for n in (2, 3):
            new_chain = self.live_chain(n)
            # Swap the live chain for one with an extra vector, in place.
            self.remove(self.chain)
            self.chain = new_chain
            tip_trace = TracedPath(
                lambda n=n: self.tip_after(n, self.t.get_value()),
                stroke_color=PALETTE["sum"],
                stroke_width=3,
            )
            self.add(tip_trace, self.chain)
            self.spin(1, run_time=4.0)
            self.wait(0.4)
            self.play(FadeOut(tip_trace))

        self.play(FadeOut(note))
        self.wait(0.3)

    def draw_the_wave(self):
        # THE PAYOFF. Grow the chain to many harmonics, then carry the tip's
        # HEIGHT rightward over time: the pen's vertical position is the sum of
        # sines, and sweeping it in x draws the wave. With odd harmonics and a
        # 1/n falloff, the curve converges to a square wave.
        self.remove(self.chain)
        self.chain = self.live_chain(N_FULL)
        self.add(self.chain)

        # A faint dashed reference of the ideal square wave, so the convergence
        # of the drawn curve is visible against its target.
        ref = self.square_wave_reference()
        self.play(Create(ref), run_time=1.2)

        # The pen: same height as the chain's tip, marching right as time runs.
        t0 = self.t.get_value()
        pen_point = lambda: np.array([
            GRAPH_X0 + H_SCALE * (self.t.get_value() - t0),
            self.tip_after(N_FULL, self.t.get_value())[1],
            0.0,
        ])
        pen = always_redraw(lambda: Dot(pen_point(), color=PALETTE["sum"], radius=0.06))
        # A horizontal tie-line linking the chain's tip to the pen.
        link = always_redraw(lambda: Line(
            self.tip_after(N_FULL, self.t.get_value()),
            pen_point(),
            color=PALETTE["muted"], stroke_width=1.5, stroke_opacity=0.6,
        ))
        wave = TracedPath(pen_point, stroke_color=PALETTE["sum"], stroke_width=4)

        note = caption("carry the tip's height sideways as it turns").to_edge(DOWN)
        self.add(link, wave, pen)
        self.play(FadeIn(note, shift=0.3 * UP))
        self.spin(2, run_time=11.0)    # two periods drawn across the frame
        self.wait(0.6)
        self.play(FadeOut(note), FadeOut(link), FadeOut(pen))
        self.wave = wave
        self.ref = ref

    def square_wave_reference(self) -> VMobject:
        """The ideal square wave (amplitude 1) the partial sums approach."""
        xs = np.linspace(GRAPH_X0, GRAPH_X0 + H_SCALE * 4 * PI, 600)
        pts = []
        t0 = self.t.get_value()
        for x in xs:
            theta = (x - GRAPH_X0) / H_SCALE + t0
            y = 1.0 if np.sin(theta) >= 0 else -1.0
            pts.append([x, y, 0.0])
        wave = VMobject()
        wave.set_points_as_corners([np.array(p) for p in pts])
        wave.set_stroke(PALETTE["muted"], width=2, opacity=0.55)
        return DashedVMobject(wave, num_dashes=120)

    def reveal_equation(self):
        # Now — and only now — the formula. Freeze the spin and swap the live
        # chain for a static copy so individual vectors can be highlighted.
        static = self.build_chain(N_FULL, self.t.get_value())
        self.remove(self.chain)
        self.add(static)

        # Terms are pre-colored to match their vectors, so the eye pairs them
        # before any words are spoken.
        eq = MathTex(
            r"f(\theta)=\frac{4}{\pi}\left(",
            r"\frac{\sin\theta}{1}", "+",
            r"\frac{\sin 3\theta}{3}", "+",
            r"\frac{\sin 5\theta}{5}", "+",
            r"\cdots", r"\right)",
        ).scale(0.95).to_edge(DOWN, buff=0.6)
        term_index = {0: 1, 1: 3, 2: 5}     # k -> position in the MathTex list
        for k, idx in term_index.items():
            eq[idx].set_color(component_color(k))
        self.play(Write(eq), run_time=2.0)
        self.wait(0.5)

        # Walk term-by-term: light up each fraction together with its arrow.
        for k, idx in term_index.items():
            col = component_color(k)
            self.play(
                Indicate(eq[idx], color=col, scale_factor=1.25),
                Indicate(static[k], color=col, scale_factor=1.1),
                run_time=1.1,
            )
            self.wait(0.25)
        # The "+ ..." stands for every remaining harmonic.
        self.play(
            Indicate(eq[7], color=PALETTE["ink"]),
            Indicate(VGroup(*static[3:]), color=PALETTE["ink"]),
            run_time=1.1,
        )
        self.wait(0.6)
        self.eq = eq
        self.static = static

    def outro(self):
        # Land the idea in one muted line, leaving the wave on screen.
        closer = caption(
            "more arrows, sharper corners — that's a Fourier series"
        ).to_edge(DOWN, buff=0.25)
        self.play(FadeOut(self.eq), FadeIn(closer, shift=0.3 * UP))
        self.wait(2.0)
