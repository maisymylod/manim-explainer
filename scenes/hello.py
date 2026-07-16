"""
Phase-2 smoke test: the smallest scene that proves the pipeline works.

Deliberately uses NO LaTeX (only Pango `Text` + a shape), so it renders as soon
as manim + ffmpeg are installed, before a TeX distribution is set up. It also
exercises the shared style module so we know `helpers.py` imports cleanly.

Render:
    manim -pql scenes/hello.py HelloScene
"""

import sys
from pathlib import Path

# Let scene files find helpers.py at the project root regardless of CWD.
sys.path.append(str(Path(__file__).resolve().parent.parent))

from manim import Scene, Circle, Create, Write, FadeIn, DOWN, config  # noqa: E402
from helpers import PALETTE, title_text, caption  # noqa: E402

config.background_color = PALETTE["bg"]


class HelloScene(Scene):
    def construct(self):
        # A title, written on stroke-by-stroke like his section headers.
        title = title_text("Hello, Manim")
        self.play(Write(title))

        # One structural shape in the 3b1b blue, drawn with `Create`.
        ring = Circle(radius=1.6, color=PALETTE["structure"], stroke_width=6)
        self.play(Create(ring))

        # A muted one-liner fades in beneath the ring — the "intuition" slot.
        line = caption("if this plays, the render pipeline works")
        line.next_to(ring, DOWN, buff=0.6)
        self.play(FadeIn(line, shift=0.3 * DOWN))

        self.wait(1.5)
