# GEOMETRIA SACRED PATTERNS

Colección de 60 pósters generativos en PDF vectorial (A3), cada uno explorando un concepto distinto de geometría sagrada, matemáticas y ciencia.

## Requisitos

- **Python** 3.10+
- **Pillow** (solo si se generan PNG/GIF adicionales)
- **ReportLab** (generación de PDFs)

### Instalación

```bash
# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install reportlab Pillow
```

## Cómo generar

```bash
source .venv/bin/activate

# Serie 001–015
python3 gen_001_015.py

# Serie 016–030
python3 gen_016_030.py

# Serie 031–045
python3 gen_031_045.py

# Serie 046–060
python3 gen_046_060.py

# GIFs animados (perfect loops)
python3 gen_gifs.py
```

Los PDFs se generan en el directorio actual. Los GIFs se generan en `gif/`. Si quieres cambiar la ruta de salida, edita la variable `OUT` al inicio de cada script.

## Estructura de cada script

Cada script sigue este patrón:

```
gen_XXX_YYY.py
├── Imports (math, random, reportlab)
├── Constantes globales (W, H = A3, OUT = ruta)
├── Funciones utilitarias
│   ├── bg()              — fondo de página
│   ├── title_block()     — título, subtítulo y edición
│   ├── scatter_stars()   — partículas decorativas de fondo
│   └── draw_polygon()    — polígono regular de N lados
├── gen_XXX()             — función generadora de cada PDF
│   ├── Canvas setup
│   ├── Paleta de colores (Color con alpha)
│   ├── Geometría principal (el diseño)
│   ├── Detalles decorativos
│   ├── scatter_stars()
│   └── title_block()
└── main: ejecuta todas las funciones gen_*
```

## Anatomía de un diseño

Cada PDF tiene estos elementos consistentes:

1. **Fondo oscuro** — Color base cerca de negro con tinte de color (`bg()`)
2. **Paleta de 4-5 colores** — Cada diseño tiene su propia paleta con transparencias
3. **Geometría central** — El patrón principal centrado en el canvas
4. **Decoración** — Estrellas, partículas, círculos concéntricos, líneas radiantes
5. **Título** — Nombre del patrón, subtítulo temático, número de edición
6. **Fade/profundidad** — Elementos se desvanecen con la distancia al centro

### Técnicas clave de ReportLab

```python
from reportlab.lib.pagesizes import A3
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

W, H = A3  # 842 x 1191 puntos (~A3 en puntos PDF)
c = canvas.Canvas('output.pdf', pagesize=A3)

# Color con transparencia
c.setStrokeColor(Color(0.5, 0.2, 1.0, alpha=0.5))
c.setFillColor(Color(0.5, 0.2, 1.0, alpha=0.08))

# Figuras básicas
c.circle(cx, cy, radius, fill=0, stroke=1)
c.rect(x, y, w, h, fill=1, stroke=0)
c.ellipse(x1, y1, x2, y2, fill=0, stroke=1)
c.line(x1, y1, x2, y2)

# Paths (polígonos, curvas)
p = c.beginPath()
p.moveTo(x, y)
p.lineTo(x2, y2)
p.curveTo(cp1x, cp1y, cp2x, cp2y, ex, ey)  # Bezier cúbica
p.close()
c.drawPath(p, fill=0, stroke=1)

# Texto
c.setFont("Helvetica", 36)
c.drawCentredString(W/2, y, "TITULO")

# Ancho de línea
c.setLineWidth(0.5)

c.save()  # Guardar PDF
```

### Técnicas de diseño usadas

| Técnica | Descripción | Usada en |
|---|---|---|
| **Transparencia acumulativa** | Múltiples capas con alpha bajo crean efecto de glow | Todos |
| **Fade por distancia** | `fade = max(0.1, 1.0 - dist/radius)` | 019, 026, todos |
| **Depth sorting** | Objetos 3D se dibujan por profundidad (back→front) | 008, 010, 017, 027, 030 |
| **Glow** | Círculos concéntricos con alpha decreciente | 001, 005, 022, 029 |
| **Seeded random** | `random.seed(N)` para reproducibilidad | 014, 020, 022, 023 |
| **Proyección 3D→2D** | Perspectiva simple: `scale = d / (d - z)` | 008, 010, 017, 027, 030 |
| **Proyección 4D→2D** | Doble perspectiva (4D→3D→2D) | 030 |
| **Parametric curves** | Ecuaciones paramétricas para espirales, torus knots, Lissajous | 003, 012, 018, 021, 028 |
| **Contour sampling** | Evaluar función en grid, dibujar cerca de f(x,y)≈0 | 016, 025, 031, 037 |
| **ODE integration** | Euler simple para attractors | 020, 044 |
| **Reaction-diffusion** | Gray-Scott model iterativo en grid | 034 |
| **Vector fields** | Trazar líneas de campo desde ecuaciones | 032 |
| **Fractal recursion** | Subdivisión recursiva de geometría | 036, 039 |
| **Chaos game** | Iteración estocástica hacia atractores | 036 |
| **Harmonograph** | Superposición de osciladores con decaimiento | 033 |

## Catálogo completo

### Serie 001–015

| # | Archivo | Paleta | Concepto matemático |
|---|---|---|---|
| 001 | `flower-of-life` | Dorado/Ámbar | Círculos superpuestos en 3 anillos |
| 002 | `sri-yantra` | Carmesí/Oro | 9 triángulos entrelazados + pétalos de loto |
| 003 | `fibonacci-spiral` | Esmeralda/Teal | Espiral áurea, razón phi (φ = 1.618...) |
| 004 | `platonic-solids` | Arcoíris prismático | 5 sólidos platónicos en wireframe |
| 005 | `vesica-piscis` | Azul océano/Cyan | Intersección de dos círculos |
| 006 | `mandala` | Rubí/Zafiro/Amatista | 4 anillos de pétalos (8, 12, 16, 24) |
| 007 | `metatrons-cube` | Violeta eléctrico | 13 nodos completamente interconectados |
| 008 | `torus` | Rosa/Magenta | Torus 3D wireframe con proyección |
| 009 | `penrose-tiling` | Coral/Ámbar sunset | Teselación aperiódica con simetría 5 |
| 010 | `geodesic-sphere` | Menta/Seafoam | Icosaedro subdividido proyectado en 3D |
| 011 | `voronoi-cosmos` | Neón pastel | 60 semillas con Voronoi/Delaunay |
| 012 | `lissajous-harmony` | Azul eléctrico | 5 curvas de Lissajous (ratios 1:2 a 5:6) |
| 013 | `seed-of-life` | Lavanda/Lila | 7 círculos en 5 escalas concéntricas |
| 014 | `fractal-tree` | Verde bosque | Árbol fractal recursivo (10 niveles) |
| 015 | `hyperbolic-tessellation` | Borgoña/Oro | Disco de Poincaré con heptágonos |

### Serie 016–030

| # | Archivo | Paleta | Concepto matemático |
|---|---|---|---|
| 016 | `cymatics` | Hielo/Plata | Patrones de Chladni — nodos vibracionales |
| 017 | `double-helix` | Bioluminiscente Cyan | ADN 3D con pares de bases |
| 018 | `spirograph` | Candy Rosa/Púrpura/Lima | 7 hipotrocoides con distintos parámetros |
| 019 | `islamic-geometric` | Azul medianoche/Oro | Zellige — estrellas de 8 puntas en mosaico |
| 020 | `strange-attractor` | Naranja sangre/Ember | Atractor de Lorenz (25k puntos, σ=10, ρ=28) |
| 021 | `rose-curves` | Rosa polvoso/Blush | 7 curvas rhodonea r=cos(kθ) |
| 022 | `supernova` | Blanco→Azul→Rojo→Naranja | Explosión radial con ondas de choque |
| 023 | `neural-network` | Sináptico púrpura | 7 capas de neuronas con sinapsis |
| 024 | `orbital-mechanics` | Negro/Oro celestial | 6 órbitas Kepler elípticas |
| 025 | `wave-interference` | Índigo/Fósforo verde | Doble rendija — patrón de interferencia |
| 026 | `hexagonal-lattice` | Miel/Ámbar | Panal completo con profundidad radial |
| 027 | `mobius-strip` | Holográfico iridiscente | Superficie no orientable en wireframe 3D |
| 028 | `celtic-knot` | Esmeralda/Oro antiguo | 4 nudos tóricos (2,3), (3,5), (2,5), (3,7) |
| 029 | `sacred-eye` | Medianoche/Oro | Ojo de la providencia + geometría |
| 030 | `tesseract` | Plata holográfica/UV | Hipercubo 4D con rotaciones y proyección |

## Cómo agregar nuevos diseños

Para crear un nuevo PDF (e.g., 031):

```python
def gen_031():
    c = canvas.Canvas(f'{OUT}/031-nombre.pdf', pagesize=A3)

    # 1. Fondo
    bg(c, Color(R, G, B))
    cx, cy = W/2, H/2 + 50  # Centro ligeramente arriba (deja espacio para título)

    # 2. Define tu paleta (4-5 colores con alpha)
    palette = [
        Color(r, g, b, alpha=0.5),
        Color(r, g, b, alpha=0.4),
        # ...
    ]

    # 3. Dibuja tu geometría
    # ... (usa c.circle, c.line, beginPath, etc.)

    # 4. Decoración
    scatter_stars(c, 250, (r, g, b), cx, cy, min_dist)

    # 5. Título
    title_block(c,
        "NOMBRE",
        "SUBTITULO  ·  SEPARADO  ·  CON PUNTOS",
        "GEOMETRIA SACRED PATTERNS — 031",
        Color(r, g, b, alpha=0.85),   # título
        Color(r, g, b, alpha=0.3),    # subtítulo
        Color(r, g, b, alpha=0.12))   # edición

    c.save()
```

### Reglas de diseño de la serie

- **Tamaño**: A3 (842 × 1191 puntos)
- **Fondo**: Siempre oscuro (casi negro, con tinte de color del tema)
- **Centro de composición**: `cx, cy = W/2, H/2 + 50` (ligeramente arriba del centro para equilibrar con el título)
- **Título en la parte inferior**: y ≈ 105 para título, 80 para subtítulo, 52 para edición
- **Fuentes**: Solo `Helvetica` y `Courier` (disponibles en ReportLab sin instalar fuentes adicionales)
- **Transparencia**: Usar alpha extensivamente para crear profundidad y glow
- **Nombre de archivo**: `NNN-kebab-case-name.pdf`
- **Estrellas de fondo**: 150-400 partículas, el color debe complementar la paleta
- **IMPORTANTE**: No usar `A3` como nombre de variable local (conflicto con import de pagesize)

### Serie 046–060

| # | Archivo | Paleta | Concepto matemático |
|---|---|---|---|
| 046 | `black-hole` | Vantablack/Acreción naranja | Horizonte de eventos, disco de acreción con Doppler |
| 047 | `dragon-curve` | Rojo sangre/Obsidiana | Curva del dragón (16 iter, L-system) |
| 048 | `hilbert-curve` | Synthwave cyan/Magenta | Curva de Hilbert orden 6 (4096 segmentos) |
| 049 | `apollonian-gasket` | Perla/Champagne | Empaquetado de círculos tangentes (Descartes) |
| 050 | `sound-waveform` | Vinyl/Analog warm | 5 armónicos Fourier apilados |
| 051 | `ferrofluid` | Metal cromado líquido | Escultura magnética con spikes gaussianos |
| 052 | `quantum-orbitals` | Azul atómico | Orbitales 1s, 2p, 3d, 4f (Monte Carlo) |
| 053 | `topographic-map` | Tierra/Contornos | Curvas de nivel con marching squares |
| 054 | `diffraction-pattern` | Láser rojo | Disco de Airy — apertura circular (Bessel J1) |
| 055 | `gravity-well` | Spacetime blue/Grid | Curvatura del espacio-tiempo (grilla deformada) |
| 056 | `phyllotaxis` | Girasol/Verde vivo | 1500 semillas en ángulo áureo (137.508°) |
| 057 | `interference-rings` | Iridiscente arcoíris | Anillos de Newton — interferencia de película delgada |
| 058 | `strange-loop` | Gris cálido/Escher | Triángulo de Penrose y geometría imposible |
| 059 | `clifford-attractor` | Neón vapor/Retrowave | 200k puntos del atractor de Clifford |
| 060 | `cosmic-web` | Materia oscura/Void | Filamentos, cúmulos de galaxias y vacíos cósmicos |

### Serie 031–045

| # | Archivo | Paleta | Concepto matemático |
|---|---|---|---|
| 031 | `julia-set` | Ultravioleta/Plasma pink | Conjunto de Julia (c = -0.7+0.27i) |
| 032 | `magnetic-field` | Acero/Azul hielo | Campo dipolar magnético |
| 033 | `harmonic-oscillator` | Cobre/Bronce | 4 harmonógrafos con decaimiento |
| 034 | `reaction-diffusion` | Teal orgánico | Patrones de Turing (Gray-Scott, 3000 iter) |
| 035 | `astronomical-clock` | Oro bruñido/Medianoche | Reloj con zodíaco y eclíptica |
| 036 | `sierpinski-triangle` | Neón verde/Matrix | Sierpinski (7 niveles) + chaos game |
| 037 | `standing-waves` | Ámbar acústico | 5 modos armónicos de membrana circular |
| 038 | `galaxy-spiral` | Índigo/Starlight | 4 brazos espirales logarítmicos |
| 039 | `koch-snowflake` | Ártico/Frost | 7 niveles de Koch anidados |
| 040 | `electric-circuit` | Cobre/PCB verde | Trazas Manhattan y componentes |
| 041 | `moire-interference` | Plata monocromático | Moiré de círculos + líneas offset |
| 042 | `nautilus-shell` | Perla/Crema/Océano | Espiral áurea con cámaras |
| 043 | `sacred-lotus` | Magenta/Oro | 5 anillos de pétalos Bézier + Fibonacci |
| 044 | `rossler-attractor` | Jade/Turquesa | Rössler (40k puntos, a=0.2 b=0.2 c=5.7) |
| 045 | `tree-of-life` | Púrpura real/Oro | 10 Sephiroth + 22 caminos (Kabbalah) |

## GIFs Animados (Perfect Loops)

### Cómo generar

```bash
source .venv/bin/activate

# GIFs animados (540px, 60 frames, loop perfecto)
python3 gen_gifs.py
```

Los GIFs se generan en el subdirectorio `gif/`.

### Especificaciones

- **Tamaño**: 540 × 540 px
- **Frames**: 60 por GIF
- **Duración**: 50ms por frame (20 FPS, 3s por loop)
- **Loop perfecto**: El último frame se mezcla suavemente con el primero usando `loop_t(frame, n_frames) = frame / n_frames` → `phase = t × 2π`
- **Formato**: GIF con `loop=0` (infinito)

### Catálogo GIF

| # | Archivo | Paleta | Animación |
|---|---|---|---|
| 01 | `flower-of-life` | Dorado/Ámbar | Flor de la vida rotando suavemente |
| 02 | `breathing-mandala` | Rubí/Zafiro/Amatista | Mandala que respira (expansión/contracción) |
| 03 | `spiral-vortex` | Esmeralda/Teal | Vórtice espiral con partículas |
| 04 | `metatrons-cube` | Violeta eléctrico | Cubo de Metatrón pulsando |
| 05 | `orbiting-particles` | Neón multicolor | Partículas en órbitas concéntricas |
| 06 | `wave-propagation` | Índigo/Fósforo | Ondas propagándose desde el centro |
| 07 | `lorenz-butterfly` | Naranja/Ember | Mariposa de Lorenz rotando |
| 08 | `geometric-morph` | Arcoíris prismático | Transición polígono 3→12 lados |
| 09 | `phyllotaxis-bloom` | Girasol/Verde | Filotaxis floreciendo en espiral áurea |
| 10 | `kaleidoscope` | Candy multicolor | Caleidoscopio con simetría 6 |
| 11 | `spinning-torus` | Rosa/Magenta | Torus 3D girando |
| 12 | `tesseract-rotation` | Plata/UV | Hipercubo 4D en rotación |
| 13 | `supernova-pulse` | Blanco→Azul→Rojo | Supernova pulsante con ondas de choque |
| 14 | `dna-helix` | Cyan bioluminiscente | Doble hélice ADN rotando |
| 15 | `geodesic-sphere` | Menta/Seafoam | Esfera geodésica girando |
