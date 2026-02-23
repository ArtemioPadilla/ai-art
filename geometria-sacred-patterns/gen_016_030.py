#!/usr/bin/env python3
"""GEOMETRIA SACRED PATTERNS — Generative Series 016–030"""

import math
import random
from reportlab.lib.pagesizes import A3
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

W, H = A3
import os
OUT = os.path.dirname(os.path.abspath(__file__))

def bg(c, color):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def title_block(c, title, subtitle, edition, color_main, color_sub, color_ed):
    c.setFillColor(color_main)
    c.setFont("Helvetica", 36)
    c.drawCentredString(W/2, 105, title)
    c.setFillColor(color_sub)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W/2, 80, subtitle)
    c.setFillColor(color_ed)
    c.setFont("Courier", 8)
    c.drawCentredString(W/2, 52, edition)

def scatter_stars(c, count, color, cx, cy, min_dist=0):
    for _ in range(count):
        px, py = random.random() * W, random.random() * H
        if math.hypot(px - cx, py - cy) > min_dist:
            c.setFillColor(Color(color[0], color[1], color[2], alpha=random.random()*0.25+0.05))
            c.circle(px, py, random.random()*1.5+0.3, fill=1, stroke=0)

def draw_polygon(c, cx, cy, r, n, rotation=0):
    pts = []
    for i in range(n):
        a = rotation + i * 2 * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]: p.lineTo(*pt)
    p.close()
    c.drawPath(p, fill=0, stroke=1)
    return pts


# ═══════════════════════════════════════════════════════════
# 016 — CYMATICS (Ice Blue / Silver)
# Sound made visible — nodal patterns on vibrating plates
# ═══════════════════════════════════════════════════════════
def gen_016():
    c = canvas.Canvas(f'{OUT}/016-cymatics.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.03, 0.06))
    cx, cy = W/2, H/2 + 50

    ices = [
        Color(0.7, 0.85, 1.0, alpha=0.5),
        Color(0.5, 0.7, 0.95, alpha=0.4),
        Color(0.85, 0.9, 1.0, alpha=0.35),
        Color(0.4, 0.6, 0.9, alpha=0.45),
    ]

    # Chladni-like patterns: sin(n*x)*sin(m*y) - sin(m*x)*sin(n*y) = 0
    # Draw nodal lines for different (n,m) modes
    modes = [(2, 3), (3, 5), (4, 7), (5, 6)]
    R = 230

    for mi, (n, m) in enumerate(modes):
        col = ices[mi % len(ices)]
        c.setStrokeColor(col)
        c.setLineWidth(0.4 + mi * 0.1)

        # Sample the Chladni function and draw contours at zero
        res = 200
        for ix in range(res):
            for iy in range(res):
                x = (ix / res - 0.5) * 2
                y = (iy / res - 0.5) * 2
                if x*x + y*y > 0.95:
                    continue

                val = math.sin(n * math.pi * x) * math.sin(m * math.pi * y) - \
                      math.sin(m * math.pi * x) * math.sin(n * math.pi * y)

                # Draw dots near nodal lines
                if abs(val) < 0.06:
                    px = cx + x * R
                    py = cy + y * R
                    # Accumulate as small particles
                    sz = 0.8 * (1 - abs(val) / 0.06)
                    alpha_v = 0.4 * (1 - abs(val) / 0.06)
                    fade = 1.0 - mi * 0.2
                    c.setFillColor(Color(col.red, col.green, col.blue, alpha=alpha_v * fade))
                    c.circle(px, py, sz, fill=1, stroke=0)

    # Circular boundary (vibrating plate edge)
    c.setStrokeColor(Color(0.7, 0.85, 1, alpha=0.4))
    c.setLineWidth(2.0)
    c.circle(cx, cy, R, fill=0, stroke=1)
    c.setStrokeColor(Color(0.7, 0.85, 1, alpha=0.1))
    c.setLineWidth(0.5)
    c.circle(cx, cy, R + 8, fill=0, stroke=1)
    c.circle(cx, cy, R + 12, fill=0, stroke=1)

    # Center glow
    for rr in range(30, 0, -1):
        c.setFillColor(Color(0.7, 0.85, 1, alpha=0.02 * (1 - rr/30)))
        c.circle(cx, cy, rr, fill=1, stroke=0)

    scatter_stars(c, 200, (0.7, 0.85, 1), cx, cy, R + 15)

    title_block(c, "CYMATICS", "SOUND MADE VISIBLE  ·  VIBRATION  ·  RESONANCE",
                "GEOMETRIA SACRED PATTERNS — 016",
                Color(0.7, 0.85, 1, alpha=0.85), Color(0.7, 0.85, 1, alpha=0.3), Color(0.7, 0.85, 1, alpha=0.12))
    c.save()
    print("  016 done")


# ═══════════════════════════════════════════════════════════
# 017 — DOUBLE HELIX (Bioluminescent Cyan/Green)
# DNA structure — the geometry of life
# ═══════════════════════════════════════════════════════════
def gen_017():
    c = canvas.Canvas(f'{OUT}/017-double-helix.pdf', pagesize=A3)
    bg(c, Color(0.01, 0.03, 0.04))
    cx, cy = W/2, H/2

    bios = [
        Color(0.0, 0.9, 0.8, alpha=0.55),
        Color(0.0, 0.7, 1.0, alpha=0.45),
        Color(0.3, 1.0, 0.5, alpha=0.4),
        Color(0.0, 0.5, 0.9, alpha=0.5),
    ]

    # Double helix running vertically
    helix_h = 800
    y_start = cy - helix_h / 2
    r = 80  # helix radius
    turns = 6
    steps = 500

    strand1_pts = []
    strand2_pts = []

    for i in range(steps + 1):
        t = i / steps
        y = y_start + t * helix_h
        a = t * turns * 2 * math.pi
        x1 = cx + r * math.cos(a)
        z1 = r * math.sin(a)
        x2 = cx + r * math.cos(a + math.pi)
        z2 = r * math.sin(a + math.pi)
        strand1_pts.append((x1, y, z1))
        strand2_pts.append((x2, y, z2))

    # Draw base pair rungs first (behind)
    c.setLineWidth(0.8)
    rung_interval = steps // (turns * 10)
    for i in range(0, steps, max(1, rung_interval)):
        x1, y1, z1 = strand1_pts[i]
        x2, y2, z2 = strand2_pts[i]
        avg_z = (z1 + z2) / 2
        alpha = 0.1 + 0.15 * ((avg_z + r) / (2 * r))
        pair_type = i % 4
        if pair_type < 2:
            c.setStrokeColor(Color(0, 0.8, 0.5, alpha=alpha))
        else:
            c.setStrokeColor(Color(0, 0.5, 0.9, alpha=alpha))
        c.line(x1, y1, x2, y2)
        # Middle marker
        mx, my = (x1+x2)/2, (y1+y2)/2
        c.setFillColor(Color(1, 1, 1, alpha=alpha * 0.5))
        c.circle(mx, my, 1.5, fill=1, stroke=0)

    # Draw strands
    for strand, col_idx in [(strand1_pts, 0), (strand2_pts, 1)]:
        for i in range(len(strand) - 1):
            x1, y1, z1 = strand[i]
            x2, y2, z2 = strand[i+1]
            avg_z = (z1 + z2) / 2
            alpha = 0.2 + 0.5 * ((avg_z + r) / (2 * r))
            width = 0.8 + 1.5 * ((avg_z + r) / (2 * r))
            col = bios[col_idx]
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
            c.setLineWidth(width)
            c.line(x1, y1, x2, y2)

    # Phosphate backbone dots
    for strand, col_idx in [(strand1_pts, 2), (strand2_pts, 3)]:
        for i in range(0, len(strand), 15):
            x, y, z = strand[i]
            alpha = 0.3 + 0.5 * ((z + r) / (2 * r))
            col = bios[col_idx]
            c.setFillColor(Color(col.red, col.green, col.blue, alpha=alpha))
            c.circle(x, y, 2.5, fill=1, stroke=0)

    # Glow at center
    for rr in range(50, 0, -1):
        c.setFillColor(Color(0, 0.7, 0.8, alpha=0.008 * (1 - rr/50)))
        c.ellipse(cx - rr, cy - rr*3, cx + rr, cy + rr*3, fill=1, stroke=0)

    scatter_stars(c, 250, (0.2, 0.8, 0.7), cx, cy, 0)

    title_block(c, "DOUBLE HELIX", "DNA  ·  THE CODE OF LIFE  ·  ADENINE THYMINE GUANINE CYTOSINE",
                "GEOMETRIA SACRED PATTERNS — 017",
                Color(0, 0.9, 0.8, alpha=0.85), Color(0, 0.8, 0.7, alpha=0.3), Color(0, 0.8, 0.7, alpha=0.12))
    c.save()
    print("  017 done")


# ═══════════════════════════════════════════════════════════
# 018 — SPIROGRAPH (Candy: Hot Pink/Electric Purple/Lime)
# Hypotrochoid and epitrochoid patterns
# ═══════════════════════════════════════════════════════════
def gen_018():
    c = canvas.Canvas(f'{OUT}/018-spirograph.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.01, 0.05))
    cx, cy = W/2, H/2 + 50

    candies = [
        Color(1.0, 0.1, 0.5, alpha=0.5),
        Color(0.6, 0.1, 1.0, alpha=0.45),
        Color(0.3, 1.0, 0.2, alpha=0.4),
        Color(1.0, 0.8, 0.0, alpha=0.35),
        Color(0.0, 0.8, 1.0, alpha=0.4),
    ]

    # Multiple spirograph curves with different parameters
    curves = [
        # (R, r, d, color_idx)  R=outer, r=inner, d=pen distance
        (200, 75, 120, 0),
        (180, 50, 140, 1),
        (160, 90, 80, 2),
        (140, 35, 110, 3),
        (190, 110, 60, 4),
        (170, 45, 150, 0),
        (150, 65, 100, 1),
    ]

    for ci, (Rc, rc, d, col_idx) in enumerate(curves):
        col = candies[col_idx]
        fade = 1.0 - ci * 0.08
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
        c.setLineWidth(0.6)

        # Scale to fit
        scale = 1.0
        steps = 3000
        p = c.beginPath()
        for s in range(steps + 1):
            t = s / steps * 2 * math.pi * rc / math.gcd(int(Rc), int(rc))
            # Hypotrochoid
            x = (Rc - rc) * math.cos(t) + d * math.cos((Rc - rc) / rc * t)
            y = (Rc - rc) * math.sin(t) - d * math.sin((Rc - rc) / rc * t)
            px = cx + x * scale
            py = cy + y * scale
            if s == 0:
                p.moveTo(px, py)
            else:
                p.lineTo(px, py)
        c.drawPath(p, fill=0, stroke=1)

    # Central ornament
    c.setFillColor(Color(1, 0.3, 0.7, alpha=0.15))
    c.circle(cx, cy, 15, fill=1, stroke=0)
    c.setFillColor(Color(1, 1, 1, alpha=0.8))
    c.circle(cx, cy, 3, fill=1, stroke=0)

    scatter_stars(c, 150, (1, 0.5, 0.8), cx, cy, 0)

    title_block(c, "SPIROGRAPH", "HYPOTROCHOID  ·  EPITROCHOID  ·  HARMONIC GEARS",
                "GEOMETRIA SACRED PATTERNS — 018",
                Color(1, 0.2, 0.6, alpha=0.85), Color(1, 0.5, 0.8, alpha=0.3), Color(1, 0.5, 0.8, alpha=0.12))
    c.save()
    print("  018 done")


# ═══════════════════════════════════════════════════════════
# 019 — ISLAMIC GEOMETRIC (Midnight Blue / Gold / White)
# Moorish star patterns — zellige-inspired
# ═══════════════════════════════════════════════════════════
def gen_019():
    c = canvas.Canvas(f'{OUT}/019-islamic-geometric.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.03, 0.08))
    cx, cy = W/2, H/2 + 50

    golds_b = [
        Color(0.9, 0.75, 0.2, alpha=0.55),
        Color(1.0, 0.85, 0.3, alpha=0.45),
        Color(0.8, 0.65, 0.15, alpha=0.4),
        Color(1.0, 0.95, 0.6, alpha=0.3),
    ]

    # 8-fold star pattern tiling
    cell_size = 80
    star_r = cell_size * 0.45

    rows = int(H / cell_size) + 2
    cols = int(W / cell_size) + 2
    offset_x = (W - cols * cell_size) / 2
    offset_y = (H - rows * cell_size) / 2

    for row in range(-1, rows + 1):
        for col in range(-1, cols + 1):
            scx = offset_x + col * cell_size + cell_size / 2
            scy = offset_y + row * cell_size + cell_size / 2
            dist = math.hypot(scx - cx, scy - cy)
            fade = max(0.1, 1.0 - dist / 500)

            # 8-pointed star
            c.setLineWidth(0.5 * fade + 0.2)
            col_g = golds_b[(row + col) % len(golds_b)]
            c.setStrokeColor(Color(col_g.red, col_g.green, col_g.blue, alpha=col_g.alpha * fade))

            # Star: two overlapping squares
            pts_a = []
            pts_b = []
            for i in range(4):
                a = i * math.pi / 2 + math.pi / 4
                pts_a.append((scx + star_r * math.cos(a), scy + star_r * math.sin(a)))
            for i in range(4):
                a = i * math.pi / 2
                pts_b.append((scx + star_r * math.cos(a), scy + star_r * math.sin(a)))

            # Draw both squares
            p = c.beginPath()
            p.moveTo(*pts_a[0])
            for pt in pts_a[1:]: p.lineTo(*pt)
            p.close()
            c.drawPath(p, fill=0, stroke=1)

            p = c.beginPath()
            p.moveTo(*pts_b[0])
            for pt in pts_b[1:]: p.lineTo(*pt)
            p.close()
            c.drawPath(p, fill=0, stroke=1)

            # Inner octagon
            inner_r = star_r * 0.42
            c.setStrokeColor(Color(col_g.red, col_g.green, col_g.blue, alpha=col_g.alpha * fade * 0.5))
            c.setLineWidth(0.3)
            draw_polygon(c, scx, scy, inner_r, 8, math.pi/8)

            # Fill center
            c.setFillColor(Color(col_g.red, col_g.green, col_g.blue, alpha=0.015 * fade))
            c.circle(scx, scy, inner_r, fill=1, stroke=0)

    # Vignette: darken edges
    for edge_r in range(int(max(W, H)), 200, -5):
        alpha = min(0.015, 0.015 * ((edge_r - 200) / max(W, H)))
        c.setFillColor(Color(0, 0, 0.05, alpha=alpha))
        c.circle(cx, cy, edge_r, fill=1, stroke=0)

    # Border frame
    margin = 40
    c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=0.25))
    c.setLineWidth(1.0)
    c.rect(margin, margin, W - 2*margin, H - 2*margin, fill=0, stroke=1)
    c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=0.1))
    c.setLineWidth(0.5)
    c.rect(margin + 6, margin + 6, W - 2*margin - 12, H - 2*margin - 12, fill=0, stroke=1)

    title_block(c, "ISLAMIC GEOMETRIC", "ZELLIGE  ·  EIGHT-FOLD SYMMETRY  ·  THE INFINITE",
                "GEOMETRIA SACRED PATTERNS — 019",
                Color(0.95, 0.8, 0.25, alpha=0.85), Color(0.95, 0.85, 0.4, alpha=0.3), Color(0.95, 0.85, 0.4, alpha=0.12))
    c.save()
    print("  019 done")


# ═══════════════════════════════════════════════════════════
# 020 — STRANGE ATTRACTOR (Blood Orange / Ember)
# Lorenz butterfly — chaos theory
# ═══════════════════════════════════════════════════════════
def gen_020():
    c = canvas.Canvas(f'{OUT}/020-strange-attractor.pdf', pagesize=A3)
    bg(c, Color(0.05, 0.02, 0.01))
    cx, cy = W/2, H/2 + 30

    embers = [
        Color(1.0, 0.35, 0.05, alpha=0.4),
        Color(1.0, 0.55, 0.1, alpha=0.35),
        Color(1.0, 0.75, 0.2, alpha=0.3),
        Color(0.9, 0.2, 0.05, alpha=0.45),
    ]

    # Lorenz attractor
    sigma, rho, beta = 10.0, 28.0, 8.0/3.0
    dt = 0.005
    x, y, z = 0.1, 0.0, 0.0
    points = []

    for _ in range(25000):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        x += dx * dt
        y += dy * dt
        z += dz * dt
        points.append((x, y, z))

    # Project: use x-z plane, scale to fit
    xs = [p[0] for p in points]
    zs = [p[2] for p in points]
    x_min, x_max = min(xs), max(xs)
    z_min, z_max = min(zs), max(zs)

    scale_x = 500 / (x_max - x_min)
    scale_z = 600 / (z_max - z_min)
    scale = min(scale_x, scale_z) * 0.85

    ox = cx - (x_max + x_min) / 2 * scale
    oy = cy - (z_max + z_min) / 2 * scale

    # Draw trajectory
    for i in range(len(points) - 1):
        px1 = ox + points[i][0] * scale
        py1 = oy + points[i][2] * scale
        px2 = ox + points[i+1][0] * scale
        py2 = oy + points[i+1][2] * scale

        t = i / len(points)
        col_idx = int(t * 4) % len(embers)
        col = embers[col_idx]
        y_val = points[i][1]
        depth = (y_val - min(p[1] for p in points)) / (max(p[1] for p in points) - min(p[1] for p in points))
        alpha = 0.05 + 0.25 * depth
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
        c.setLineWidth(0.3 + 0.7 * depth)
        c.line(px1, py1, px2, py2)

    # Attractor fixed points glow
    for fx, fz in [(math.sqrt(beta*(rho-1)), rho-1), (-math.sqrt(beta*(rho-1)), rho-1)]:
        gpx = ox + fx * scale
        gpy = oy + fz * scale
        for rr in range(25, 0, -1):
            c.setFillColor(Color(1, 0.4, 0.1, alpha=0.025 * (1 - rr/25)))
            c.circle(gpx, gpy, rr, fill=1, stroke=0)

    scatter_stars(c, 150, (1, 0.6, 0.3), cx, cy, 0)

    title_block(c, "STRANGE ATTRACTOR", "LORENZ  ·  CHAOS THEORY  ·  BUTTERFLY EFFECT",
                "GEOMETRIA SACRED PATTERNS — 020",
                Color(1, 0.45, 0.1, alpha=0.85), Color(1, 0.6, 0.3, alpha=0.3), Color(1, 0.6, 0.3, alpha=0.12))
    c.save()
    print("  020 done")


# ═══════════════════════════════════════════════════════════
# 021 — ROSE CURVES (Blush Pink / Dusty Rose / Cream)
# Rhodonea mathematical curves
# ═══════════════════════════════════════════════════════════
def gen_021():
    c = canvas.Canvas(f'{OUT}/021-rose-curves.pdf', pagesize=A3)
    bg(c, Color(0.05, 0.03, 0.04))
    cx, cy = W/2, H/2 + 50

    roses = [
        Color(0.95, 0.45, 0.55, alpha=0.5),
        Color(0.9, 0.55, 0.65, alpha=0.4),
        Color(1.0, 0.7, 0.75, alpha=0.35),
        Color(0.85, 0.3, 0.45, alpha=0.45),
        Color(1.0, 0.85, 0.8, alpha=0.3),
    ]

    # Rose curves: r = cos(k*theta)
    k_values = [2, 3, 5, 7, 4.0/3.0, 5.0/3.0, 7.0/2.0]
    radii = [250, 220, 190, 160, 230, 200, 170]

    for ki, (k, R) in enumerate(zip(k_values, radii)):
        col = roses[ki % len(roses)]
        fade = 1.0 - ki * 0.08
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
        c.setLineWidth(0.7 - ki * 0.05)

        steps = 2000
        # For rational k=p/q, need theta from 0 to q*pi
        if isinstance(k, float):
            max_theta = 3 * 2 * math.pi
        else:
            max_theta = 2 * math.pi if k % 2 == 0 else math.pi

        p = c.beginPath()
        started = False
        for s in range(steps + 1):
            theta = s / steps * max_theta
            r = R * math.cos(k * theta)
            if r < 0:
                r = -r
                theta += math.pi
            px = cx + r * math.cos(theta)
            py = cy + r * math.sin(theta)
            if not started:
                p.moveTo(px, py)
                started = True
            else:
                p.lineTo(px, py)
        c.drawPath(p, fill=0, stroke=1)

    # Center bloom
    for rr in range(35, 0, -1):
        c.setFillColor(Color(0.95, 0.5, 0.6, alpha=0.02 * (1 - rr/35)))
        c.circle(cx, cy, rr, fill=1, stroke=0)
    c.setFillColor(Color(1, 0.8, 0.8, alpha=0.8))
    c.circle(cx, cy, 4, fill=1, stroke=0)

    scatter_stars(c, 200, (1, 0.7, 0.75), cx, cy, 260)

    title_block(c, "ROSE CURVES", "RHODONEA  ·  PETALS OF MATHEMATICS  ·  r = cos(k\u03b8)",
                "GEOMETRIA SACRED PATTERNS — 021",
                Color(0.95, 0.5, 0.6, alpha=0.85), Color(1, 0.7, 0.75, alpha=0.3), Color(1, 0.7, 0.75, alpha=0.12))
    c.save()
    print("  021 done")


# ═══════════════════════════════════════════════════════════
# 022 — SUPERNOVA (White/Blue core → Red/Orange shell)
# Explosive radial energy burst
# ═══════════════════════════════════════════════════════════
def gen_022():
    c = canvas.Canvas(f'{OUT}/022-supernova.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.01, 0.03))
    cx, cy = W/2, H/2 + 50

    random.seed(2024)

    # Core glow (white → blue)
    for rr in range(120, 0, -1):
        t = rr / 120
        r_c = 0.3 + 0.7 * (1 - t)
        g_c = 0.4 + 0.6 * (1 - t)
        b_c = 0.8 + 0.2 * (1 - t)
        alpha = 0.04 * (1 - t)
        c.setFillColor(Color(r_c, g_c, b_c, alpha=alpha))
        c.circle(cx, cy, rr, fill=1, stroke=0)

    # Bright white core
    c.setFillColor(Color(1, 1, 1, alpha=0.95))
    c.circle(cx, cy, 8, fill=1, stroke=0)
    c.setFillColor(Color(0.8, 0.9, 1, alpha=0.6))
    c.circle(cx, cy, 15, fill=1, stroke=0)

    # Radial rays
    c.setLineWidth(0.3)
    for i in range(200):
        a = random.random() * 2 * math.pi
        r_start = 15 + random.random() * 20
        r_end = r_start + 80 + random.random() * 250

        # Color gradient: blue near center → orange/red at edges
        t = r_end / 350
        r_c = min(1, 0.3 + t * 0.7)
        g_c = max(0.1, 0.5 - t * 0.3)
        b_c = max(0.1, 0.9 - t * 0.7)
        alpha = 0.05 + random.random() * 0.15

        x1 = cx + r_start * math.cos(a)
        y1 = cy + r_start * math.sin(a)
        x2 = cx + r_end * math.cos(a)
        y2 = cy + r_end * math.sin(a)

        c.setStrokeColor(Color(r_c, g_c, b_c, alpha=alpha))
        c.setLineWidth(random.random() * 1.5 + 0.2)
        c.line(x1, y1, x2, y2)

    # Shockwave rings
    for ring_r in [180, 250, 320]:
        c.setStrokeColor(Color(1, 0.5, 0.2, alpha=0.12))
        c.setLineWidth(1.5)
        c.circle(cx, cy, ring_r, fill=0, stroke=1)
        # Fragmented outer ring
        for i in range(60):
            a = i * math.pi / 30 + random.random() * 0.05
            a_end = a + 0.04
            x1 = cx + (ring_r + 3) * math.cos(a)
            y1 = cy + (ring_r + 3) * math.sin(a)
            x2 = cx + (ring_r + 3) * math.cos(a_end)
            y2 = cy + (ring_r + 3) * math.sin(a_end)
            c.setStrokeColor(Color(1, 0.6, 0.2, alpha=0.06))
            c.setLineWidth(0.5)
            c.line(x1, y1, x2, y2)

    # Ejecta particles
    for _ in range(400):
        a = random.random() * 2 * math.pi
        r = 50 + random.random() * 300
        px = cx + r * math.cos(a)
        py = cy + r * math.sin(a)
        t = r / 350
        r_c = min(1, 0.5 + t * 0.5)
        g_c = max(0, 0.7 - t * 0.5)
        b_c = max(0, 0.9 - t * 0.8)
        sz = random.random() * 2 + 0.3
        alpha = random.random() * 0.4 + 0.1
        c.setFillColor(Color(r_c, g_c, b_c, alpha=alpha))
        c.circle(px, py, sz, fill=1, stroke=0)

    title_block(c, "SUPERNOVA", "STELLAR DEATH  ·  COSMIC REBIRTH  ·  STARDUST",
                "GEOMETRIA SACRED PATTERNS — 022",
                Color(1, 0.6, 0.3, alpha=0.85), Color(1, 0.7, 0.5, alpha=0.3), Color(1, 0.7, 0.5, alpha=0.12))
    c.save()
    print("  022 done")


# ═══════════════════════════════════════════════════════════
# 023 — NEURAL NETWORK (Synapse Purple / Electric)
# Brain-like interconnected nodes
# ═══════════════════════════════════════════════════════════
def gen_023():
    c = canvas.Canvas(f'{OUT}/023-neural-network.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.02, 0.05))
    cx, cy = W/2, H/2 + 30

    synapses = [
        Color(0.5, 0.2, 1.0, alpha=0.5),
        Color(0.7, 0.3, 1.0, alpha=0.4),
        Color(0.3, 0.5, 1.0, alpha=0.4),
        Color(0.9, 0.4, 0.8, alpha=0.35),
        Color(0.4, 0.8, 1.0, alpha=0.35),
    ]

    random.seed(88)

    # Generate neurons in layers (like a brain cross-section)
    layers = []
    layer_counts = [5, 8, 12, 16, 12, 8, 5]
    layer_x_positions = [cx - 250 + i * (500 / (len(layer_counts) - 1)) for i in range(len(layer_counts))]

    for li, (lx, count) in enumerate(zip(layer_x_positions, layer_counts)):
        neurons = []
        spread = 400
        for ni in range(count):
            ny = cy - spread/2 + ni * spread / (count - 1) if count > 1 else cy
            nx = lx + random.gauss(0, 15)
            ny += random.gauss(0, 10)
            neurons.append((nx, ny))
        layers.append(neurons)

    # Draw connections between adjacent layers
    c.setLineWidth(0.3)
    for li in range(len(layers) - 1):
        for n1 in layers[li]:
            for n2 in layers[li + 1]:
                dist = math.hypot(n1[0]-n2[0], n1[1]-n2[1])
                if random.random() < 0.6:  # Not all connected
                    alpha = 0.03 + random.random() * 0.1
                    col = synapses[(li) % len(synapses)]
                    c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
                    # Draw with slight curve
                    midx = (n1[0]+n2[0])/2 + random.gauss(0, 10)
                    midy = (n1[1]+n2[1])/2
                    p = c.beginPath()
                    p.moveTo(*n1)
                    p.curveTo(midx, n1[1], midx, n2[1], n2[0], n2[1])
                    c.drawPath(p, fill=0, stroke=1)

    # Draw skip connections (long-range)
    c.setLineWidth(0.2)
    for _ in range(30):
        l1 = random.randint(0, len(layers) - 3)
        l2 = random.randint(l1 + 2, len(layers) - 1)
        n1 = random.choice(layers[l1])
        n2 = random.choice(layers[l2])
        c.setStrokeColor(Color(0.9, 0.5, 1, alpha=0.04))
        c.line(n1[0], n1[1], n2[0], n2[1])

    # Draw neurons (nodes)
    for li, layer in enumerate(layers):
        col = synapses[li % len(synapses)]
        for nx, ny in layer:
            # Glow
            c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.06))
            c.circle(nx, ny, 12, fill=1, stroke=0)
            # Soma
            c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.6))
            c.circle(nx, ny, 4, fill=1, stroke=0)
            # Bright center
            c.setFillColor(Color(1, 0.9, 1, alpha=0.7))
            c.circle(nx, ny, 1.5, fill=1, stroke=0)

    # "Firing" neurons - bright pulses along some connections
    for _ in range(20):
        li = random.randint(0, len(layers) - 2)
        n1 = random.choice(layers[li])
        n2 = random.choice(layers[li + 1])
        t = random.random()
        px = n1[0] + (n2[0] - n1[0]) * t
        py = n1[1] + (n2[1] - n1[1]) * t
        c.setFillColor(Color(0.8, 0.6, 1, alpha=0.5))
        c.circle(px, py, 2, fill=1, stroke=0)
        c.setFillColor(Color(0.8, 0.6, 1, alpha=0.08))
        c.circle(px, py, 8, fill=1, stroke=0)

    scatter_stars(c, 150, (0.6, 0.4, 1), cx, cy, 0)

    title_block(c, "NEURAL NETWORK", "SYNAPSES  ·  CONSCIOUSNESS  ·  EMERGENT INTELLIGENCE",
                "GEOMETRIA SACRED PATTERNS — 023",
                Color(0.6, 0.3, 1, alpha=0.85), Color(0.7, 0.5, 1, alpha=0.3), Color(0.7, 0.5, 1, alpha=0.12))
    c.save()
    print("  023 done")


# ═══════════════════════════════════════════════════════════
# 024 — ORBITAL MECHANICS (Space Black / Celestial Gold)
# Kepler orbits — planetary dance
# ═══════════════════════════════════════════════════════════
def gen_024():
    c = canvas.Canvas(f'{OUT}/024-orbital-mechanics.pdf', pagesize=A3)
    bg(c, Color(0.01, 0.01, 0.02))
    cx, cy = W/2, H/2 + 50

    celestials = [
        Color(1.0, 0.85, 0.3, alpha=0.5),
        Color(0.3, 0.6, 1.0, alpha=0.4),
        Color(0.9, 0.4, 0.2, alpha=0.4),
        Color(0.5, 0.9, 0.6, alpha=0.35),
        Color(0.8, 0.7, 1.0, alpha=0.35),
        Color(0.2, 0.8, 0.9, alpha=0.35),
    ]

    # Sun at center
    for rr in range(60, 0, -1):
        t = rr / 60
        c.setFillColor(Color(1, 0.85, 0.2, alpha=0.04 * (1 - t)))
        c.circle(cx, cy, rr, fill=1, stroke=0)
    c.setFillColor(Color(1, 0.95, 0.6, alpha=0.9))
    c.circle(cx, cy, 10, fill=1, stroke=0)
    c.setFillColor(Color(1, 1, 0.9, alpha=0.95))
    c.circle(cx, cy, 5, fill=1, stroke=0)

    # Kepler orbits (ellipses with different eccentricities)
    orbits = [
        # (semi_major, eccentricity, angle_offset, color_idx, planet_size)
        (70, 0.05, 0.3, 1, 3),
        (110, 0.12, 1.2, 2, 4),
        (160, 0.08, 2.5, 3, 5),
        (220, 0.20, 0.8, 4, 3.5),
        (280, 0.35, 3.1, 0, 7),
        (350, 0.15, 4.5, 5, 6),
    ]

    random.seed(55)
    for a, e, angle_off, col_idx, p_size in orbits:
        col = celestials[col_idx]
        b = a * math.sqrt(1 - e*e)  # semi-minor
        focus_offset = a * e  # distance from center to focus

        # Draw orbit ellipse
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.6))
        c.setLineWidth(0.5)
        steps = 200
        p = c.beginPath()
        for s in range(steps + 1):
            t = s / steps * 2 * math.pi
            ox = a * math.cos(t)
            oy = b * math.sin(t)
            # Rotate
            rx = ox * math.cos(angle_off) - oy * math.sin(angle_off)
            ry = ox * math.sin(angle_off) + oy * math.cos(angle_off)
            # Offset for focus
            rx += focus_offset * math.cos(angle_off)
            ry += focus_offset * math.sin(angle_off)
            if s == 0:
                p.moveTo(cx + rx, cy + ry)
            else:
                p.lineTo(cx + rx, cy + ry)
        c.drawPath(p, fill=0, stroke=1)

        # Planet at some position
        t_planet = angle_off + random.random() * 2 * math.pi
        ox = a * math.cos(t_planet)
        oy = b * math.sin(t_planet)
        rx = ox * math.cos(angle_off) - oy * math.sin(angle_off)
        ry = ox * math.sin(angle_off) + oy * math.cos(angle_off)
        rx += focus_offset * math.cos(angle_off)
        ry += focus_offset * math.sin(angle_off)
        px, py = cx + rx, cy + ry

        # Planet glow
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.08))
        c.circle(px, py, p_size * 4, fill=1, stroke=0)
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.7))
        c.circle(px, py, p_size, fill=1, stroke=0)

        # Kepler equal area sweep line
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=0.05))
        c.setLineWidth(0.3)
        c.line(cx, cy, px, py)

    # Lagrange points indicators
    for a_l in [0, math.pi/3, -math.pi/3, math.pi, 2*math.pi/3]:
        lx = cx + 280 * math.cos(a_l + 3.1)
        ly = cy + 280 * math.sin(a_l + 3.1)
        c.setStrokeColor(Color(1, 0.85, 0.3, alpha=0.08))
        c.setLineWidth(0.3)
        c.circle(lx, ly, 6, fill=0, stroke=1)

    scatter_stars(c, 400, (0.9, 0.9, 1), cx, cy, 0)

    title_block(c, "ORBITAL MECHANICS", "KEPLER  ·  CELESTIAL DANCE  ·  GRAVITATIONAL HARMONY",
                "GEOMETRIA SACRED PATTERNS — 024",
                Color(1, 0.85, 0.3, alpha=0.85), Color(1, 0.9, 0.5, alpha=0.3), Color(1, 0.9, 0.5, alpha=0.12))
    c.save()
    print("  024 done")


# ═══════════════════════════════════════════════════════════
# 025 — WAVE INTERFERENCE (Deep Indigo / Phosphor Green)
# Double slit experiment — quantum patterns
# ═══════════════════════════════════════════════════════════
def gen_025():
    c = canvas.Canvas(f'{OUT}/025-wave-interference.pdf', pagesize=A3)
    bg(c, Color(0.01, 0.02, 0.04))
    cx, cy = W/2, H/2 + 50

    # Two wave sources
    s1 = (cx - 60, cy)
    s2 = (cx + 60, cy)
    wavelength = 40

    # Calculate interference pattern
    res = 250
    for ix in range(res):
        for iy in range(res):
            px = ix / res * W
            py = 140 + iy / res * (H - 160)

            d1 = math.hypot(px - s1[0], py - s1[1])
            d2 = math.hypot(px - s2[0], py - s2[1])

            # Interference: sum of two waves
            wave = math.sin(2 * math.pi * d1 / wavelength) + math.sin(2 * math.pi * d2 / wavelength)
            intensity = (wave / 2) ** 2  # Normalized intensity

            if intensity > 0.3:
                alpha = min(0.4, intensity * 0.4)
                # Color: green for constructive, subtle blue for edges
                g = min(1, intensity * 0.8)
                b = min(0.5, intensity * 0.3)
                c.setFillColor(Color(0.1, g, 0.3 + b, alpha=alpha))
                sz = 1.0 + intensity * 1.5
                c.circle(px, py, sz, fill=1, stroke=0)

    # Wave source points
    for sx, sy in [s1, s2]:
        for rr in range(20, 0, -1):
            c.setFillColor(Color(0.2, 1, 0.5, alpha=0.04 * (1 - rr/20)))
            c.circle(sx, sy, rr, fill=1, stroke=0)
        c.setFillColor(Color(0.5, 1, 0.7, alpha=0.9))
        c.circle(sx, sy, 4, fill=1, stroke=0)

    # Concentric wave rings from each source
    c.setLineWidth(0.3)
    for sx, sy in [s1, s2]:
        for ring in range(1, 15):
            r = ring * wavelength
            alpha = max(0.02, 0.08 - ring * 0.005)
            c.setStrokeColor(Color(0.2, 0.8, 0.5, alpha=alpha))
            c.circle(sx, sy, r, fill=0, stroke=1)

    # "Screen" at the top and bottom showing fringe pattern
    c.setLineWidth(0.5)
    for py_screen in [cy - 320, cy + 320]:
        for ix in range(300):
            px = W * 0.1 + ix / 300 * W * 0.8
            d1 = math.hypot(px - s1[0], py_screen - s1[1])
            d2 = math.hypot(px - s2[0], py_screen - s2[1])
            wave = math.sin(2 * math.pi * d1 / wavelength) + math.sin(2 * math.pi * d2 / wavelength)
            intensity = abs(wave / 2)
            c.setFillColor(Color(0.2, 1, 0.5, alpha=intensity * 0.5))
            c.circle(px, py_screen, 1 + intensity * 2, fill=1, stroke=0)

    scatter_stars(c, 100, (0.3, 0.8, 0.5), cx, cy, 0)

    title_block(c, "WAVE INTERFERENCE", "DOUBLE SLIT  ·  QUANTUM  ·  SUPERPOSITION",
                "GEOMETRIA SACRED PATTERNS — 025",
                Color(0.3, 1, 0.6, alpha=0.85), Color(0.3, 0.9, 0.5, alpha=0.3), Color(0.3, 0.9, 0.5, alpha=0.12))
    c.save()
    print("  025 done")


# ═══════════════════════════════════════════════════════════
# 026 — HEXAGONAL LATTICE (Honey Gold / Warm Amber)
# Honeycomb structure with depth
# ═══════════════════════════════════════════════════════════
def gen_026():
    c = canvas.Canvas(f'{OUT}/026-hexagonal-lattice.pdf', pagesize=A3)
    bg(c, Color(0.05, 0.03, 0.01))
    cx, cy = W/2, H/2 + 50

    honeys = [
        Color(1.0, 0.78, 0.1, alpha=0.5),
        Color(0.95, 0.65, 0.05, alpha=0.4),
        Color(1.0, 0.88, 0.4, alpha=0.35),
        Color(0.85, 0.55, 0.0, alpha=0.4),
    ]

    hex_r = 35
    hex_h = hex_r * math.sqrt(3)

    rows = int(H / hex_h) + 3
    cols = int(W / (hex_r * 1.5)) + 3

    for row in range(-1, rows):
        for col in range(-1, cols):
            hx = col * hex_r * 1.5
            hy = row * hex_h + (hex_h / 2 if col % 2 else 0)
            dist = math.hypot(hx - cx, hy - cy)
            fade = max(0.05, 1.0 - dist / 500)

            col_h = honeys[(row + col) % len(honeys)]

            # Hexagon
            c.setStrokeColor(Color(col_h.red, col_h.green, col_h.blue, alpha=col_h.alpha * fade))
            c.setLineWidth(0.6 * fade + 0.2)
            draw_polygon(c, hx, hy, hex_r * 0.95, 6, 0)

            # Inner detail: smaller hexagon
            if fade > 0.3:
                c.setStrokeColor(Color(col_h.red, col_h.green, col_h.blue, alpha=col_h.alpha * fade * 0.3))
                c.setLineWidth(0.3)
                draw_polygon(c, hx, hy, hex_r * 0.6, 6, math.pi/6)

            # Fill with gradient-like effect
            inner_alpha = 0.01 + 0.03 * fade * math.sin(dist * 0.01) ** 2
            c.setFillColor(Color(col_h.red, col_h.green, col_h.blue, alpha=max(0, inner_alpha)))
            c.circle(hx, hy, hex_r * 0.5, fill=1, stroke=0)

            # Center dot for cells near center
            if fade > 0.5:
                c.setFillColor(Color(1, 0.9, 0.5, alpha=fade * 0.3))
                c.circle(hx, hy, 1.5, fill=1, stroke=0)

    # Central hexagon highlight
    c.setStrokeColor(Color(1, 0.85, 0.2, alpha=0.6))
    c.setLineWidth(1.5)
    draw_polygon(c, cx, cy, hex_r * 0.95, 6, 0)

    # Outer vignette ring
    c.setStrokeColor(Color(1, 0.8, 0.2, alpha=0.15))
    c.setLineWidth(1)
    c.circle(cx, cy, 350, fill=0, stroke=1)

    title_block(c, "HEXAGONAL LATTICE", "HONEYCOMB  ·  EFFICIENCY  ·  NATURE'S ARCHITECTURE",
                "GEOMETRIA SACRED PATTERNS — 026",
                Color(1, 0.8, 0.2, alpha=0.85), Color(1, 0.88, 0.4, alpha=0.3), Color(1, 0.88, 0.4, alpha=0.12))
    c.save()
    print("  026 done")


# ═══════════════════════════════════════════════════════════
# 027 — MÖBIUS STRIP (Chromatic Iridescent)
# Non-orientable surface — single surface, single edge
# ═══════════════════════════════════════════════════════════
def gen_027():
    c = canvas.Canvas(f'{OUT}/027-mobius-strip.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.03, 0.04))
    cx, cy = W/2, H/2 + 50

    R = 180  # Major radius
    w = 60   # Strip half-width
    tilt = 0.7

    # Parametric Möbius strip
    u_steps = 120
    v_steps = 12

    for v in range(v_steps):
        v_t = (v / v_steps - 0.5) * 2  # -1 to 1
        v_t_next = ((v + 1) / v_steps - 0.5) * 2

        for u in range(u_steps):
            u_a = u / u_steps * 2 * math.pi
            u_a_next = (u + 1) / u_steps * 2 * math.pi

            # Möbius: the strip makes a half-twist
            def mobius_point(ua, vt):
                x = (R + w * vt * math.cos(ua / 2)) * math.cos(ua)
                y = (R + w * vt * math.cos(ua / 2)) * math.sin(ua)
                z = w * vt * math.sin(ua / 2)
                # Project with tilt
                px = cx + x * 0.9
                py = cy - y * math.sin(tilt) - z * math.cos(tilt)
                depth = y * math.cos(tilt) - z * math.sin(tilt)
                return px, py, depth

            p1 = mobius_point(u_a, v_t)
            p2 = mobius_point(u_a_next, v_t)
            p3 = mobius_point(u_a, v_t_next)

            depth = (p1[2] + p2[2]) / 2
            t_norm = (depth + R + w) / (2 * (R + w))

            # Iridescent color based on position
            hue = (u / u_steps + v / v_steps * 0.3) % 1.0
            r_c = 0.5 + 0.5 * math.sin(hue * 2 * math.pi)
            g_c = 0.5 + 0.5 * math.sin(hue * 2 * math.pi + 2.09)
            b_c = 0.5 + 0.5 * math.sin(hue * 2 * math.pi + 4.19)
            alpha = 0.1 + 0.35 * t_norm

            c.setStrokeColor(Color(r_c, g_c, b_c, alpha=alpha))
            c.setLineWidth(0.5 + t_norm)

            # Draw u-direction line
            c.line(p1[0], p1[1], p2[0], p2[1])
            # Draw v-direction line
            c.setLineWidth(0.3 + t_norm * 0.5)
            c.line(p1[0], p1[1], p3[0], p3[1])

    # Edge highlight (the single edge of the Möbius strip)
    for edge_v in [-1, 1]:
        pts = []
        for u in range(u_steps * 2 + 1):  # Need 2 full rotations for single edge
            u_a = u / (u_steps * 2) * 4 * math.pi
            x = (R + w * edge_v * math.cos(u_a / 2)) * math.cos(u_a)
            y = (R + w * edge_v * math.cos(u_a / 2)) * math.sin(u_a)
            z = w * edge_v * math.sin(u_a / 2)
            px = cx + x * 0.9
            py = cy - y * math.sin(tilt) - z * math.cos(tilt)
            pts.append((px, py))

    scatter_stars(c, 200, (0.7, 0.7, 0.9), cx, cy, 0)

    title_block(c, "MOBIUS STRIP", "ONE SURFACE  ·  ONE EDGE  ·  NON-ORIENTABLE TOPOLOGY",
                "GEOMETRIA SACRED PATTERNS — 027",
                Color(0.8, 0.7, 1, alpha=0.85), Color(0.8, 0.75, 1, alpha=0.3), Color(0.8, 0.75, 1, alpha=0.12))
    c.save()
    print("  027 done")


# ═══════════════════════════════════════════════════════════
# 028 — CELTIC KNOT (Emerald / Antique Gold)
# Interwoven eternal paths
# ═══════════════════════════════════════════════════════════
def gen_028():
    c = canvas.Canvas(f'{OUT}/028-celtic-knot.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.04, 0.03))
    cx, cy = W/2, H/2 + 50

    celtics = [
        Color(0.15, 0.7, 0.35, alpha=0.55),
        Color(0.85, 0.7, 0.2, alpha=0.45),
        Color(0.1, 0.6, 0.3, alpha=0.5),
        Color(0.9, 0.8, 0.3, alpha=0.35),
    ]

    # Trefoil knot parametric curve
    R = 180
    knot_variants = [
        # (p, q, R, width, color_idx) — torus knot parameters
        (2, 3, 180, 1.2, 0),   # trefoil
        (3, 5, 150, 0.9, 1),   # (3,5) torus knot
        (2, 5, 200, 0.7, 2),   # (2,5) torus knot
        (3, 7, 130, 0.5, 3),   # (3,7) torus knot
    ]

    for p, q, kr, width, col_idx in knot_variants:
        col = celtics[col_idx]
        steps = 2000
        pts = []

        for s in range(steps + 1):
            t = s / steps * 2 * math.pi
            r_tube = 0.3
            # Torus knot parametric
            x = (math.cos(q * t) * (1 + r_tube * math.cos(p * t))) * kr
            y = (math.sin(q * t) * (1 + r_tube * math.cos(p * t))) * kr
            z = r_tube * math.sin(p * t) * kr * 0.5
            # Project
            px = cx + x
            py = cy + y * 0.8 - z * 0.5
            depth = z
            pts.append((px, py, depth))

        # Draw with depth-based alpha (over/under crossings)
        for i in range(len(pts) - 1):
            avg_depth = (pts[i][2] + pts[i+1][2]) / 2
            norm_depth = (avg_depth + kr * 0.3) / (kr * 0.6)
            alpha = 0.15 + 0.4 * max(0, min(1, norm_depth))
            lw = width * (0.5 + 0.5 * max(0, min(1, norm_depth)))

            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
            c.setLineWidth(lw)
            c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])

    # Ornamental border: interlocking circles
    border_r = 320
    c.setLineWidth(0.5)
    for i in range(24):
        a = i * math.pi / 12
        bx = cx + border_r * math.cos(a)
        by = cy + border_r * math.sin(a)
        c.setStrokeColor(Color(0.15, 0.6, 0.3, alpha=0.1))
        c.circle(bx, by, 30, fill=0, stroke=1)

    # Central shield
    c.setStrokeColor(Color(0.85, 0.7, 0.2, alpha=0.2))
    c.setLineWidth(0.8)
    c.circle(cx, cy, 50, fill=0, stroke=1)
    c.setFillColor(Color(0.85, 0.7, 0.2, alpha=0.04))
    c.circle(cx, cy, 50, fill=1, stroke=0)

    scatter_stars(c, 200, (0.4, 0.7, 0.4), cx, cy, 330)

    title_block(c, "CELTIC KNOT", "TORUS KNOTS  ·  ETERNITY  ·  INTERWOVEN PATHS",
                "GEOMETRIA SACRED PATTERNS — 028",
                Color(0.2, 0.75, 0.4, alpha=0.85), Color(0.4, 0.8, 0.5, alpha=0.3), Color(0.4, 0.8, 0.5, alpha=0.12))
    c.save()
    print("  028 done")


# ═══════════════════════════════════════════════════════════
# 029 — SACRED EYE (Midnight / Gold / All-seeing)
# Eye of Providence meets sacred geometry
# ═══════════════════════════════════════════════════════════
def gen_029():
    c = canvas.Canvas(f'{OUT}/029-sacred-eye.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.02, 0.05))
    cx, cy = W/2, H/2 + 40

    # Triangle
    tri_r = 250
    c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=0.5))
    c.setLineWidth(1.5)
    tri_pts = draw_polygon(c, cx, cy, tri_r, 3, -math.pi/2)

    # Inner triangles (nested)
    for i in range(1, 6):
        r = tri_r * (1 - i * 0.15)
        rot = -math.pi/2 + i * 0.05
        alpha = 0.3 - i * 0.04
        c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=alpha))
        c.setLineWidth(0.8 - i * 0.1)
        draw_polygon(c, cx, cy, r, 3, rot)

    # Eye shape (almond/vesica)
    eye_w = 160
    eye_h = 70
    # Upper lid
    p = c.beginPath()
    p.moveTo(cx - eye_w, cy)
    p.curveTo(cx - eye_w * 0.5, cy - eye_h * 1.2, cx + eye_w * 0.5, cy - eye_h * 1.2, cx + eye_w, cy)
    c.setStrokeColor(Color(0.9, 0.8, 0.3, alpha=0.6))
    c.setLineWidth(1.2)
    c.drawPath(p, fill=0, stroke=1)
    # Lower lid
    p = c.beginPath()
    p.moveTo(cx - eye_w, cy)
    p.curveTo(cx - eye_w * 0.5, cy + eye_h * 1.2, cx + eye_w * 0.5, cy + eye_h * 1.2, cx + eye_w, cy)
    c.drawPath(p, fill=0, stroke=1)

    # Iris
    c.setStrokeColor(Color(0.3, 0.5, 0.9, alpha=0.5))
    c.setLineWidth(1.0)
    c.circle(cx, cy, 55, fill=0, stroke=1)
    # Iris fill
    for rr in range(55, 0, -1):
        t = rr / 55
        c.setFillColor(Color(0.2, 0.3, 0.8, alpha=0.015 * (1 - t)))
        c.circle(cx, cy, rr, fill=1, stroke=0)

    # Iris rays
    c.setLineWidth(0.3)
    for i in range(48):
        a = i * math.pi / 24
        r1 = 25
        r2 = 55
        c.setStrokeColor(Color(0.3, 0.5, 0.9, alpha=0.15 + 0.1 * math.sin(a * 3)))
        c.line(cx + r1 * math.cos(a), cy + r1 * math.sin(a),
               cx + r2 * math.cos(a), cy + r2 * math.sin(a))

    # Pupil
    c.setFillColor(Color(0.02, 0.02, 0.05, alpha=0.9))
    c.circle(cx, cy, 22, fill=1, stroke=0)
    # Pupil highlight
    c.setFillColor(Color(1, 1, 1, alpha=0.6))
    c.circle(cx - 8, cy - 8, 5, fill=1, stroke=0)
    c.setFillColor(Color(1, 1, 1, alpha=0.3))
    c.circle(cx + 5, cy + 4, 3, fill=1, stroke=0)

    # Radiating lines from triangle vertices
    c.setLineWidth(0.3)
    for pt in tri_pts:
        for i in range(8):
            a = math.atan2(pt[1] - cy, pt[0] - cx) + (i - 3.5) * 0.12
            length = 60
            ox = pt[0] + 10 * math.cos(a)
            oy = pt[1] + 10 * math.sin(a)
            ex = pt[0] + length * math.cos(a)
            ey = pt[1] + length * math.sin(a)
            c.setStrokeColor(Color(0.9, 0.8, 0.3, alpha=0.08))
            c.line(ox, oy, ex, ey)

    # Outer radiating circle of light
    c.setStrokeColor(Color(0.9, 0.8, 0.3, alpha=0.1))
    c.setLineWidth(0.5)
    for r in [280, 310, 340]:
        c.circle(cx, cy, r, fill=0, stroke=1)

    scatter_stars(c, 250, (0.9, 0.8, 0.4), cx, cy, 340)

    title_block(c, "SACRED EYE", "PROVIDENCE  ·  AWARENESS  ·  THE ALL-SEEING",
                "GEOMETRIA SACRED PATTERNS — 029",
                Color(0.9, 0.8, 0.3, alpha=0.85), Color(0.9, 0.85, 0.5, alpha=0.3), Color(0.9, 0.85, 0.5, alpha=0.12))
    c.save()
    print("  029 done")


# ═══════════════════════════════════════════════════════════
# 030 — TESSERACT (Holographic Silver / Ultraviolet)
# 4D hypercube projected to 2D
# ═══════════════════════════════════════════════════════════
def gen_030():
    c = canvas.Canvas(f'{OUT}/030-tesseract.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.01, 0.04))
    cx, cy = W/2, H/2 + 50

    holos = [
        Color(0.7, 0.7, 0.9, alpha=0.5),
        Color(0.5, 0.4, 0.9, alpha=0.45),
        Color(0.8, 0.6, 1.0, alpha=0.4),
        Color(0.4, 0.7, 1.0, alpha=0.4),
    ]

    # 4D hypercube vertices (16 vertices)
    verts_4d = []
    for i in range(16):
        v = [(i >> b) & 1 for b in range(4)]
        verts_4d.append([v[j] * 2 - 1 for j in range(4)])  # -1 to 1

    # 4D rotation matrices
    angle_xw = 0.4
    angle_yw = 0.3
    angle_zw = 0.2
    angle_xy = 0.25

    def rotate_4d(v):
        x, y, z, w = v
        # XW rotation
        x2 = x * math.cos(angle_xw) - w * math.sin(angle_xw)
        w2 = x * math.sin(angle_xw) + w * math.cos(angle_xw)
        x, w = x2, w2
        # YW rotation
        y2 = y * math.cos(angle_yw) - w * math.sin(angle_yw)
        w2 = y * math.sin(angle_yw) + w * math.cos(angle_yw)
        y, w = y2, w2
        # ZW rotation
        z2 = z * math.cos(angle_zw) - w * math.sin(angle_zw)
        w2 = z * math.sin(angle_zw) + w * math.cos(angle_zw)
        z, w = z2, w2
        # XY rotation
        x2 = x * math.cos(angle_xy) - y * math.sin(angle_xy)
        y2 = x * math.sin(angle_xy) + y * math.cos(angle_xy)
        x, y = x2, y2
        return [x, y, z, w]

    # Project 4D → 2D (perspective)
    def project_4d(v):
        rv = rotate_4d(v)
        # Perspective projection from 4D to 3D
        dist_4d = 3.5
        scale_4d = dist_4d / (dist_4d - rv[3])
        x3 = rv[0] * scale_4d
        y3 = rv[1] * scale_4d
        z3 = rv[2] * scale_4d
        # 3D to 2D perspective
        dist_3d = 4.0
        scale_3d = dist_3d / (dist_3d - z3)
        px = cx + x3 * scale_3d * 160
        py = cy + y3 * scale_3d * 160
        depth = z3 + rv[3]
        return px, py, depth, scale_3d * scale_4d

    projected = [project_4d(v) for v in verts_4d]

    # Edges: connect vertices that differ in exactly 1 coordinate
    edges = []
    for i in range(16):
        for j in range(i + 1, 16):
            diff = sum(1 for a, b in zip(verts_4d[i], verts_4d[j]) if a != b)
            if diff == 1:
                edges.append((i, j))

    # Draw edges sorted by depth (back to front)
    edge_depths = [(i, j, (projected[i][2] + projected[j][2]) / 2) for i, j in edges]
    edge_depths.sort(key=lambda e: e[2])

    for i, j, avg_depth in edge_depths:
        p1, p2 = projected[i], projected[j]
        norm_depth = (avg_depth + 3) / 6
        alpha = 0.08 + 0.4 * norm_depth

        # Determine which dimension this edge is in
        dim = 0
        for d in range(4):
            if verts_4d[i][d] != verts_4d[j][d]:
                dim = d
                break
        col = holos[dim]
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
        c.setLineWidth(0.5 + 1.5 * norm_depth)
        c.line(p1[0], p1[1], p2[0], p2[1])

    # Draw vertices
    for px, py, depth, scale in projected:
        norm_depth = (depth + 3) / 6
        alpha = 0.3 + 0.6 * norm_depth
        sz = 2 + 4 * norm_depth
        # Glow
        c.setFillColor(Color(0.7, 0.6, 1, alpha=0.05 * norm_depth))
        c.circle(px, py, sz * 4, fill=1, stroke=0)
        # Vertex
        c.setFillColor(Color(0.8, 0.75, 1, alpha=alpha))
        c.circle(px, py, sz, fill=1, stroke=0)
        c.setFillColor(Color(1, 1, 1, alpha=alpha * 0.8))
        c.circle(px, py, sz * 0.4, fill=1, stroke=0)

    # Outer dimension labels
    c.setFont("Courier", 8)
    for d, label in enumerate(["X", "Y", "Z", "W"]):
        col = holos[d]
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.3))
        c.drawString(W - 80, H - 150 - d * 14, f"DIM {label}")

    # Enclosing circles
    c.setStrokeColor(Color(0.6, 0.5, 0.9, alpha=0.1))
    c.setLineWidth(0.5)
    c.circle(cx, cy, 300, fill=0, stroke=1)
    c.setStrokeColor(Color(0.6, 0.5, 0.9, alpha=0.06))
    c.circle(cx, cy, 320, fill=0, stroke=1)

    scatter_stars(c, 250, (0.7, 0.6, 1), cx, cy, 320)

    title_block(c, "TESSERACT", "HYPERCUBE  ·  FOUR DIMENSIONS  ·  BEYOND SPACE",
                "GEOMETRIA SACRED PATTERNS — 030",
                Color(0.75, 0.65, 1, alpha=0.85), Color(0.8, 0.75, 1, alpha=0.3), Color(0.8, 0.75, 1, alpha=0.12))
    c.save()
    print("  030 done")


# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating GEOMETRIA SACRED PATTERNS 016–030...")
    gen_016()
    gen_017()
    gen_018()
    gen_019()
    gen_020()
    gen_021()
    gen_022()
    gen_023()
    gen_024()
    gen_025()
    gen_026()
    gen_027()
    gen_028()
    gen_029()
    gen_030()
    print("\nAll 15 PDFs (016–030) generated!")
