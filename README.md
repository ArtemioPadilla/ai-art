# AI Art

> Generative algorithmic art — 60 sacred geometry PDF posters, 15 loopeable GIFs, and interactive pieces. All code-generated with Python + ReportLab + Pillow.

**[View the gallery](https://artemiopadilla.github.io/ai-art/)**

## What's inside

| Category | Count | Format | Description |
|---|---|---|---|
| Sacred Geometry Posters | 60 | PDF (A3 vector) | Mathematical art from Flower of Life to Cosmic Web |
| Animated Loops | 15 | GIF (540px, 60fps) | Perfectly looping sacred geometry animations |
| Standalone Pieces | 6 | PNG, GIF, PDF, SVG, HTML | Individual artworks in various formats |
| Generator Scripts | 5 | Python | Full source code to regenerate everything |

## Quick start

```bash
# Clone
git clone https://github.com/ArtemioPadilla/ai-art.git
cd ai-art/geometria-sacred-patterns

# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install reportlab Pillow

# Generate
python3 gen_001_015.py   # PDFs 001-015
python3 gen_016_030.py   # PDFs 016-030
python3 gen_031_045.py   # PDFs 031-045
python3 gen_046_060.py   # PDFs 046-060
python3 gen_gifs.py      # 15 animated GIFs
```

## Highlights

### Animated GIFs (perfect loops)

| | | |
|---|---|---|
| ![Flower of Life](geometria-sacred-patterns/gif/01-flower-of-life.gif) | ![Breathing Mandala](geometria-sacred-patterns/gif/02-breathing-mandala.gif) | ![Spiral Vortex](geometria-sacred-patterns/gif/03-spiral-vortex.gif) |
| ![Metatron's Cube](geometria-sacred-patterns/gif/04-metatrons-cube.gif) | ![Lorenz Butterfly](geometria-sacred-patterns/gif/07-lorenz-butterfly.gif) | ![Tesseract](geometria-sacred-patterns/gif/12-tesseract-rotation.gif) |

### Techniques used

- **Transparency layering** — multiple alpha passes for glow effects
- **3D/4D projection** — perspective transforms for torus, geodesic, tesseract
- **Parametric curves** — Lissajous, spirograph, torus knots, rose curves
- **Fractal recursion** — Sierpinski, Koch, Dragon curve, fractal trees
- **ODE integration** — Lorenz, Rossler, Clifford strange attractors
- **Reaction-diffusion** — Gray-Scott Turing patterns
- **Monte Carlo sampling** — quantum orbital probability clouds
- **Bessel functions** — diffraction patterns (Airy disk)

## License

All art and code in this repository are free to use. Attribution appreciated.

## Documentation

See [geometria-sacred-patterns/README.md](geometria-sacred-patterns/README.md) for detailed documentation on the generation process, design rules, and how to create new designs.
