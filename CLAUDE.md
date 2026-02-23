# CLAUDE.md

## Project Overview

Multi-collection generative algorithmic art hub. Currently contains one collection ("Geometria Sacred Patterns") with 60 sacred geometry PDF posters, 15 looping GIFs, 6 standalone pieces, and the Python scripts that generate them. Designed for easy addition of new collections.

**Live gallery**: https://artemiopadilla.github.io/ai-art/

## Repo Structure

```
index.html                              — Hub landing page (fetches manifest, renders collection cards)
shared/
├── styles.css                          — Shared CSS (theme, cards, grids, animations)
├── hub.css                             — Hub-page-specific styles
├── collection.css                      — Collection-page-specific styles
├── hero-canvas.js                      — Particle background (ES module)
├── scroll-animations.js                — IntersectionObserver fade-ins
├── gallery-renderer.js                 — Render functions for GIFs, PDFs, standalone, sources
└── collection-loader.js                — Orchestrates rendering a collection page
collections/
├── manifest.json                       — Central registry of all collections
└── geometria-sacred-patterns/
    ├── index.html                      — Collection detail page
    ├── data.js                         — Exports gifs[], pdfs[], standalone[], sources[]
    ├── gen_001_015.py … gen_gifs.py    — Generator scripts
    ├── README.md                       — Detailed documentation
    ├── 001-flower-of-life.pdf … 060-cosmic-web.pdf
    ├── gif/
    │   └── 01-flower-of-life.gif … 15-geodesic-sphere.gif
    └── standalone/
        └── 01-flow-field.png … 06-cosmic-particles.html
.github/workflows/pages.yml            — Auto-deploy to GitHub Pages on push
```

## Tech Stack

- **Python 3.10+**
- **ReportLab** — PDF generation (canvas API, Color with alpha, bezier paths)
- **Pillow (PIL)** — PNG/GIF generation (ImageDraw, ImageFilter, frame animation)
- **Vanilla HTML/CSS/JS** — Gallery pages (no build step, no frameworks, ES modules)
- **GitHub Actions** — Static site deployment to GitHub Pages

## Architecture

- **Multi-page with shared ES modules**: Hub page at root, collection detail pages under `collections/*/`
- **Data layers**: `collections/manifest.json` for hub summaries, per-collection `data.js` for full item arrays
- **Local dev requires HTTP server**: ES modules don't work over `file://` — use `python3 -m http.server`

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

### Gallery

- Hub page (`index.html`) fetches `collections/manifest.json` and renders collection cards
- Each collection page imports shared modules from `../../shared/` and its own `data.js`
- Shared CSS: `styles.css` (base) + `hub.css` or `collection.css` (page-specific)
- Dark theme with CSS custom properties
- Intersection Observer for scroll animations
- Hero section has animated canvas particle background

## Regenerating Art

```bash
cd collections/geometria-sacred-patterns
python3 -m venv .venv
source .venv/bin/activate
pip install reportlab Pillow

python3 gen_001_015.py
python3 gen_016_030.py
python3 gen_031_045.py
python3 gen_046_060.py
python3 gen_gifs.py
```

## Adding a New Collection

1. Create `collections/my-new-collection/`
2. Add your art files and generator scripts
3. Write `data.js` exporting item arrays (`collectionMeta`, `gifs`, `pdfs`, `standalone`, `sources`)
4. Copy any existing collection's `index.html` as template — change the `<title>` and imports
5. Add one entry to `collections/manifest.json`
6. Push — hub page automatically shows the new collection

## Adding Pieces to an Existing Collection

### New PDF

Add a `gen_NNN()` function following the pattern in existing scripts. See `collections/geometria-sacred-patterns/README.md` for the full template and design rules. Update `data.js` to include the new entry.

### New GIF

Add a function to `gen_gifs.py`. Use `loop_t()` for seamless looping. Return a list of PIL Image frames and call `make_gif(frames, name)`. Update `data.js`.

### Gallery

Update the arrays in the collection's `data.js`. If adding a new collection, also update `collections/manifest.json`.

## Known Gotchas

- `Helvetica-Light` is not available in ReportLab — use `Helvetica`
- Local variable `A3` shadows the pagesize import — use lowercase for local vars
- System Python on macOS is externally-managed (PEP 668) — always use a venv
- Large PDFs with many transparent layers can be slow to render in viewers
- ES modules require HTTP server for local dev (`python3 -m http.server`)
