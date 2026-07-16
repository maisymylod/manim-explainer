"""
Shared style + reusable mobjects for the 3b1b-style explainer project.

Everything here exists so individual scene files stay short and read like a
storyboard. Import it at the top of a scene with:

    from helpers import PALETTE, title_text, labeled_equation, BG_COLOR

The goal is to reproduce Grant Sanderson's *look* on top of Manim Community:
a near-black stage, a small cool-toned palette with a warm accent for the one
thing you want the eye on, and clean typography.
"""

from __future__ import annotations

from manim import (
    BLUE_D,
    BLUE_E,
    TEAL,
    GREEN,
    YELLOW,
    RED,
    GREY_A,
    GREY_B,
    GREY_C,
    WHITE,
    UP,
    DOWN,
    Text,
    Tex,
    MathTex,
    VGroup,
)

# ---------------------------------------------------------------------------
# Color: a deliberately small palette.
# ---------------------------------------------------------------------------
# 3b1b's visual grammar leans on cool blues/teals for "structure" and reserves
# warm yellow for the single quantity currently under the spotlight. Keeping the
# set tiny is what makes frames feel composed rather than busy.
BG_COLOR = "#000000"          # the stage: pure black, like his final renders

PALETTE = {
    "bg": BG_COLOR,
    "structure": BLUE_D,      # axes, scaffolding, the "known" world
    "structure_dim": BLUE_E,  # a quieter blue for secondary scaffolding
    "wave": TEAL,             # individual components (each sine / each vector)
    "sum": YELLOW,            # the star: the running sum / target curve
    "accent": GREEN,          # occasional second highlight
    "warn": RED,              # error / difference, used sparingly
    "muted": GREY_B,          # de-emphasized labels
    "ink": WHITE,             # default text
}

# A repeatable set of distinct colors for "the k-th component" so that harmonic
# 1, 2, 3... each get a stable, legible hue as they stack up.
COMPONENT_COLORS = [TEAL, BLUE_D, GREEN, "#C59FF0", "#FF8FA3", GREY_A]


def component_color(k: int):
    """Stable color for the k-th component (harmonic, vector, term...)."""
    return COMPONENT_COLORS[k % len(COMPONENT_COLORS)]


# ---------------------------------------------------------------------------
# Typography helpers.
# ---------------------------------------------------------------------------
def title_text(s: str, **kwargs) -> Text:
    """A screen title in the 3b1b spirit: plain, confident, top of frame.

    Uses Manim's Pango `Text` (no LaTeX needed) so titles render even before a
    TeX distribution is installed.
    """
    return Text(s, weight="MEDIUM", color=PALETTE["ink"], **kwargs).to_edge(UP)


def caption(s: str, **kwargs) -> Text:
    """A small muted line of prose, e.g. a one-sentence intuition."""
    return Text(s, font_size=28, color=PALETTE["muted"], **kwargs)


def labeled_equation(tex: str, color=None, **kwargs) -> MathTex:
    """A LaTeX equation in the body font. Requires a TeX install at render time.

    Kept as a thin wrapper so every equation in the project shares one place to
    tweak size/color later.
    """
    return MathTex(tex, color=color or PALETTE["ink"], **kwargs)


def equation_with_note(tex: str, note: str) -> VGroup:
    """An equation with a small muted caption stacked beneath it."""
    eq = labeled_equation(tex)
    note_mob = caption(note).next_to(eq, DOWN, buff=0.35)
    return VGroup(eq, note_mob)
