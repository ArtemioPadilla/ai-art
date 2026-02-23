# CLAUDE.md

## Project Overview

Generative algorithmic art repository. Contains 60 sacred geometry PDF posters (A3 vector), 15 perfectly looping animated GIFs, 6 standalone art pieces, and the Python scripts that generate them.

**Live gallery**: https://artemiopadilla.github.io/ai-art/

## Repo Structure

```
index.html                          — Gallery showcase (GitHub Pages)
README.md                           — Repo overview
01-flow-field.png                   — Standalone: flow field (1600x1100)
02-particle-vortex.gif              — Standalone: animated vortex (36 frames)
03-sacred-geometry.pdf              — Standalone: Flower of Life + Metatron's Cube
04-flow-field.html                  — Standalone: interactive flow field (p5.js-like)
05-geometric-poster.svg             — Standalone: hexagonal neon poster
06-cosmic-particles.html            — Standalone: interactive cosmic sky
geometria-sacred-patterns/
├── gen_001_015.py                  — Generator: PDFs 001–015
├── gen_016_030.py                  — Generator: PDFs 016–030
├── gen_031_045.py                  — Generator: PDFs 031–045
├── gen_046_060.py                  — Generator: PDFs 046–060
├── gen_gifs.py                     — Generator: 15 animated GIFs
├── README.md                       — Detailed documentation
├── 001-flower-of-life.pdf … 060-cosmic-web.pdf
└── gif/
    └── 01-flower-of-life.gif … 15-geodesic-sphere.gif
.github/workflows/pages.yml        — Auto-deploy to GitHub Pages on push
```

## Tech Stack

- **Python 3.10+**
- **ReportLab** — PDF generation (canvas API, Color with alpha, bezier paths)
- **Pillow (PIL)** — PNG/GIF generation (ImageDraw, ImageFilter, frame animation)
- **Vanilla HTML/CSS/JS** — Gallery page (no build step, no frameworks)
- **GitHub Actions** — Static site deployment to GitHub Pages

## Key Conventions

### PDF Generation (gen_XXX_YYY.py)

- Page size: A3 (842 x 1191 PDF points)
- Dark backgrounds with transparency-based layering
- Each `gen_NNN()` function: `bg()` → geometry → `scatter_stars()` → `title_block()`
- Fonts: only `Helvetica` and `Courier` (ReportLab built-ins)
- **Never** use `A3` as a local variable name (conflicts with pagesize import)
- `gen_046_060.py` uses `cv` for canvas variable (instead of `c`) to avoid naming conflicts
- OUT path: `os.path.dirname(os.path.abspath(__file__))` for portability

### GIF Generation (gen_gifs.py)

- Size: 540 x 540 px, 60 frames, 50ms per frame (20 FPS, 3s loop)
- Perfect loop: `loop_t(frame, n_frames) = frame / n_frames` → `phase = t * 2π`
- Output goes to `gif/` subdirectory
- GIF saved with `loop=0` (infinite)

### Gallery (index.html)

- Pure static HTML — no build step, no dependencies
- Data-driven: all content defined in JS arrays, rendered dynamically
- Dark theme with CSS custom properties
- Intersection Observer for scroll animations
- Hero section has animated canvas particle background
- PDF filter tabs by series (001–015, 016–030, etc.)

## Regenerating Art

```bash
cd geometria-sacred-patterns
python3 -m venv .venv
source .venv/bin/activate
pip install reportlab Pillow

python3 gen_001_015.py
python3 gen_016_030.py
python3 gen_031_045.py
python3 gen_046_060.py
python3 gen_gifs.py
```

## Adding New Pieces

### New PDF

Add a `gen_NNN()` function following the pattern in existing scripts. See `geometria-sacred-patterns/README.md` for the full template and design rules.

### New GIF

Add a function to `gen_gifs.py`. Use `loop_t()` for seamless looping. Return a list of PIL Image frames and call `make_gif(frames, name)`.

### Gallery

Update the `pdfs`, `gifs`, or `standalone` arrays in `index.html` to include new pieces.

## Known Gotchas

- `Helvetica-Light` is not available in ReportLab — use `Helvetica`
- Local variable `A3` shadows the pagesize import — use lowercase for local vars
- System Python on macOS is externally-managed (PEP 668) — always use a venv
- Large PDFs with many transparent layers can be slow to render in viewers
