"""
Phase-2 LaTeX smoke test: renders a real equation via MathTex.

If this produces an mp4, the LaTeX -> dvisvgm -> manim path works and the
Fourier scene (all equations) is safe to build. Uses the Fourier square-wave
sum itself as the test string so we exercise fractions, sums and Greek.

Render:
    manim -pql scenes/latex_check.py LatexCheck
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from manim import Scene, Write, config  # noqa: E402
from helpers import PALETTE, labeled_equation  # noqa: E402

config.background_color = PALETTE["bg"]


class LatexCheck(Scene):
    def construct(self):
        eq = labeled_equation(
            r"f(\theta)=\frac{4}{\pi}\sum_{k=0}^{\infty}"
            r"\frac{\sin\!\big((2k+1)\theta\big)}{2k+1}",
            color=PALETTE["sum"],
        ).scale(1.2)
        self.play(Write(eq))
        self.wait(1)
