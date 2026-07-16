# manim-explainer

Short, 3Blue1Brown-style animated math explainers built on
[Manim Community](https://www.manim.community/) (ManimCE).

The aim is to reproduce Grant Sanderson's *visual grammar* — near-black stage, a
small cool-toned palette with a warm accent for the quantity under the spotlight,
equations animated in lockstep with the geometry they describe, and smooth
`Transform`s instead of hard cuts — on top of the better-documented, more stable
community engine rather than his personal `manimgl`.

## Project layout

```
manim-explainer/
├── helpers.py          # shared palette, typography + reusable mobjects
├── manim.cfg           # project-wide render defaults (black bg, 60fps, media dir)
├── requirements.txt    # top-level dependency (manim==0.20.1)
├── requirements.lock   # exact frozen dependency set
├── scenes/
│   └── hello.py        # Phase-2 smoke test (no LaTeX required)
└── media/              # rendered output (git-ignored)
```

## Setup

Requires **Python 3.14** (pinned in `.python-version`), plus **ffmpeg** and a
**LaTeX** distribution.

> **Why 3.14 and not 3.13?** This machine's Homebrew `python@3.13` bottle has a
> mis-linked `pyexpat` (it resolves to the old system `libexpat.1.dylib`, which
> lacks a symbol the bottle was built against, so `pip` can't even bootstrap).
> Python 3.14 builds every native manim dependency (pycairo, moderngl,
> manimpango) cleanly and renders fine, so the project targets 3.14.

```bash
# 1. system deps (Homebrew)
brew install ffmpeg
brew install --cask basictex            # small LaTeX; needs admin password

# 2. LaTeX packages ManimCE needs (fresh terminal so tlmgr is on PATH)
sudo tlmgr update --self && sudo tlmgr install \
  amsmath babel-english cbfonts-fd cm-super count1to ctex doublestroke \
  dvisvgm everysel fontspec frcursive fundus-calligra gnu-freefont jknapltx \
  latex-bin mathastext microtype multitoc physics preview prelim2e ragged2e \
  relsize rsfs setspace standalone tipa wasy wasysym xcolor xetex xkeyval

# 3. Python env
python3.14 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

## Rendering

Run from the project root so `manim.cfg` is picked up:

```bash
# quick preview (low quality, opens when done)
./.venv/bin/manim -pql scenes/hello.py HelloScene

# quality flags: -ql (480p) · -qm (720p) · -qh (1080p) · -qk (4k)
```

Output mp4s land under `media/videos/<scene-file>/<resolution>/`.

## Extending with new scenes

1. Add a file under `scenes/`, e.g. `scenes/my_topic.py`.
2. Start it with the same 3 lines every scene here uses so it can import the
   shared style from the project root:
   ```python
   import sys; from pathlib import Path
   sys.path.append(str(Path(__file__).resolve().parent.parent))
   from helpers import PALETTE, title_text, labeled_equation
   ```
3. Subclass `Scene`, put the animation in `construct()`, and reuse `PALETTE`
   (`structure`/`wave`/`sum`/`accent`) so new scenes stay visually consistent.
4. Render with `manim -pql scenes/my_topic.py MySceneClass`.

<!-- Phase 3/4 will add the main explainer scene + its exact render command here. -->
