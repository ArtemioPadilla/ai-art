#!/usr/bin/env python3
"""GEOMETRIA SACRED PATTERNS — Generative Series 001–015"""

import math
import random
from reportlab.lib.pagesizes import A3
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

W, H = A3
import os
OUT = os.path.dirname(os.path.abspath(__file__))

# ─── Utility ──────────────────────────────────────────────

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
        px = random.random() * W
        py = random.random() * H
        dist = math.hypot(px - cx, py - cy)
        if dist > min_dist:
            sz = random.random() * 1.5 + 0.3
            a = random.random() * 0.25 + 0.05
            c.setFillColor(Color(color[0], color[1], color[2], alpha=a))
            c.circle(px, py, sz, fill=1, stroke=0)

def draw_polygon(c, cx, cy, r, n, rotation=0):
    """Draw a regular polygon, return vertices."""
    pts = []
    for i in range(n):
        a = rotation + i * 2 * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    c.drawPath(p, fill=0, stroke=1)
    return pts


# ═══════════════════════════════════════════════════════════
# 001 — FLOWER OF LIFE (Golden/Amber)
# ═══════════════════════════════════════════════════════════
def gen_001():
    c = canvas.Canvas(f'{OUT}/001-flower-of-life.pdf', pagesize=A3)
    bg(c, Color(0.06, 0.04, 0.02))
    cx, cy = W/2, H/2 + 60
    r = 70

    # Warm golden palette
    golds = [
        Color(1.0, 0.84, 0.0, alpha=0.5),
        Color(0.96, 0.73, 0.05, alpha=0.4),
        Color(0.85, 0.55, 0.1, alpha=0.35),
        Color(1.0, 0.93, 0.55, alpha=0.3),
    ]

    # Flower of life: 7 circles (1 center + 6 around)
    centers_1 = [(cx, cy)]
    for i in range(6):
        a = i * math.pi / 3
        centers_1.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    # Second ring: 12 circles
    centers_2 = []
    for i in range(6):
        a = i * math.pi / 3
        centers_2.append((cx + 2*r * math.cos(a), cy + 2*r * math.sin(a)))
    for i in range(6):
        a1 = i * math.pi / 3
        a2 = (i+1) * math.pi / 3
        mid = (a1 + a2) / 2
        centers_2.append((cx + math.sqrt(3)*r * math.cos(mid), cy + math.sqrt(3)*r * math.sin(mid)))

    # Third ring
    centers_3 = []
    for i in range(12):
        a = i * math.pi / 6
        centers_3.append((cx + 3*r * math.cos(a), cy + 3*r * math.sin(a)))
    for i in range(6):
        a1 = i * math.pi / 3
        a2 = (i+1) * math.pi / 3
        mid = (a1 + a2) / 2
        centers_3.append((cx + 2*math.sqrt(3)*r * math.cos(mid), cy + 2*math.sqrt(3)*r * math.sin(mid)))

    all_c = centers_1 + centers_2 + centers_3
    c.setLineWidth(0.6)
    for idx, (px, py) in enumerate(all_c):
        col = golds[idx % len(golds)]
        dist = math.hypot(px - cx, py - cy)
        fade = max(0.15, 1.0 - dist / (3.5 * r))
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
        c.circle(px, py, r, fill=0, stroke=1)

    # Bounding circle
    c.setStrokeColor(Color(1, 0.84, 0, alpha=0.2))
    c.setLineWidth(1.2)
    c.circle(cx, cy, 3.5 * r, fill=0, stroke=1)
    c.circle(cx, cy, 3.7 * r, fill=0, stroke=1)

    # Center glow
    for rr in range(30, 0, -1):
        a = 0.04 * (1 - rr/30)
        c.setFillColor(Color(1, 0.85, 0.2, alpha=a))
        c.circle(cx, cy, rr, fill=1, stroke=0)

    scatter_stars(c, 200, (1, 0.9, 0.5), cx, cy, 3.5*r)

    title_block(c, "FLOWER OF LIFE", "GENESIS  ·  CREATION  ·  UNITY",
                "GEOMETRIA SACRED PATTERNS — 001",
                Color(1, 0.84, 0, alpha=0.8), Color(1, 0.9, 0.5, alpha=0.3), Color(1, 0.9, 0.5, alpha=0.12))
    c.save()
    print("  001 done")


# ═══════════════════════════════════════════════════════════
# 002 — SRI YANTRA (Crimson/Gold)
# ═══════════════════════════════════════════════════════════
def gen_002():
    c = canvas.Canvas(f'{OUT}/002-sri-yantra.pdf', pagesize=A3)
    bg(c, Color(0.08, 0.02, 0.02))
    cx, cy = W/2, H/2 + 50

    reds = [
        Color(0.85, 0.1, 0.1, alpha=0.6),
        Color(1.0, 0.3, 0.1, alpha=0.5),
        Color(1.0, 0.7, 0.0, alpha=0.45),
        Color(0.9, 0.15, 0.3, alpha=0.5),
    ]

    # 9 interlocking triangles (simplified Sri Yantra)
    # 4 upward (Shiva) + 5 downward (Shakti)
    up_sizes = [200, 155, 110, 65]
    down_sizes = [185, 145, 105, 72, 40]

    c.setLineWidth(1.0)
    for idx, sz in enumerate(up_sizes):
        col = reds[idx % len(reds)]
        c.setStrokeColor(col)
        pts = []
        for i in range(3):
            a = -math.pi/2 + i * 2*math.pi/3
            pts.append((cx + sz * math.cos(a), cy + sz * math.sin(a)))
        p = c.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]: p.lineTo(*pt)
        p.close()
        c.drawPath(p, fill=0, stroke=1)

    for idx, sz in enumerate(down_sizes):
        col = reds[(idx + 1) % len(reds)]
        c.setStrokeColor(col)
        pts = []
        for i in range(3):
            a = math.pi/2 + i * 2*math.pi/3
            pts.append((cx + sz * math.cos(a), cy + sz * math.sin(a)))
        p = c.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]: p.lineTo(*pt)
        p.close()
        c.drawPath(p, fill=0, stroke=1)

    # Bindu (center point)
    for rr in range(20, 0, -1):
        c.setFillColor(Color(1, 0.2, 0.1, alpha=0.06 * (1 - rr/20)))
        c.circle(cx, cy, rr, fill=1, stroke=0)
    c.setFillColor(Color(1, 0.85, 0, alpha=0.9))
    c.circle(cx, cy, 3, fill=1, stroke=0)

    # Outer lotus petals (16)
    c.setLineWidth(0.5)
    for i in range(16):
        a = i * math.pi / 8
        inner_r, outer_r = 220, 260
        x1 = cx + inner_r * math.cos(a - 0.12)
        y1 = cy + inner_r * math.sin(a - 0.12)
        x2 = cx + outer_r * math.cos(a)
        y2 = cy + outer_r * math.sin(a)
        x3 = cx + inner_r * math.cos(a + 0.12)
        y3 = cy + inner_r * math.sin(a + 0.12)
        c.setStrokeColor(Color(1, 0.3, 0.1, alpha=0.3))
        p = c.beginPath()
        p.moveTo(x1, y1); p.lineTo(x2, y2); p.lineTo(x3, y3)
        c.drawPath(p, fill=0, stroke=1)

    # Outer circles
    c.setStrokeColor(Color(1, 0.7, 0, alpha=0.2))
    c.setLineWidth(0.8)
    c.circle(cx, cy, 270, fill=0, stroke=1)
    c.circle(cx, cy, 275, fill=0, stroke=1)

    # Square gate (Bhupura)
    gate = 290
    c.setStrokeColor(Color(1, 0.5, 0.1, alpha=0.15))
    c.setLineWidth(1.0)
    c.rect(cx - gate, cy - gate, gate*2, gate*2, fill=0, stroke=1)
    c.rect(cx - gate - 8, cy - gate - 8, gate*2 + 16, gate*2 + 16, fill=0, stroke=1)

    scatter_stars(c, 250, (1, 0.5, 0.3), cx, cy, 300)

    title_block(c, "SRI YANTRA", "SHIVA  ·  SHAKTI  ·  COSMOS",
                "GEOMETRIA SACRED PATTERNS — 002",
                Color(1, 0.3, 0.1, alpha=0.8), Color(1, 0.6, 0.3, alpha=0.3), Color(1, 0.6, 0.3, alpha=0.12))
    c.save()
    print("  002 done")


# ═══════════════════════════════════════════════════════════
# 003 — FIBONACCI SPIRAL (Emerald/Teal)
# ═══════════════════════════════════════════════════════════
def gen_003():
    c = canvas.Canvas(f'{OUT}/003-fibonacci-spiral.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.06, 0.05))
    cx, cy = W/2 - 30, H/2 + 40

    greens = [
        Color(0.0, 0.85, 0.6, alpha=0.5),
        Color(0.1, 0.95, 0.75, alpha=0.4),
        Color(0.2, 0.7, 0.5, alpha=0.35),
        Color(0.5, 1.0, 0.8, alpha=0.3),
    ]

    # Golden ratio spiral using quarter arcs
    phi = (1 + math.sqrt(5)) / 2
    fibs = [1, 1]
    for _ in range(12):
        fibs.append(fibs[-1] + fibs[-2])

    # Draw fibonacci rectangles and arcs
    scale = 1.8
    x, y = cx, cy
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # right, up, left, down

    for idx in range(len(fibs)):
        sz = fibs[idx] * scale
        d = directions[idx % 4]
        col = greens[idx % len(greens)]
        fade = max(0.2, 1.0 - idx * 0.06)

        # Rectangle
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade * 0.4))
        c.setLineWidth(0.4)

        # Arc (quarter circle) - approximate with line segments
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
        c.setLineWidth(1.2 - idx * 0.05)

        start_angle = idx * math.pi / 2
        segments = 30
        p = c.beginPath()
        for s in range(segments + 1):
            t = s / segments
            a = start_angle + t * math.pi / 2
            px = cx + sz * math.cos(a)
            py = cy + sz * math.sin(a)
            if s == 0:
                p.moveTo(px, py)
            else:
                p.lineTo(px, py)
        c.drawPath(p, fill=0, stroke=1)

    # Continuous golden spiral
    c.setStrokeColor(Color(0, 1, 0.7, alpha=0.7))
    c.setLineWidth(1.5)
    p = c.beginPath()
    for i in range(1000):
        t = i * 0.02
        r = 3 * phi ** (t * 2 / math.pi)
        if r > 350:
            break
        a = t
        px = cx + r * math.cos(a)
        py = cy + r * math.sin(a)
        if i == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    c.drawPath(p, fill=0, stroke=1)

    # Phi ratio markers
    c.setFillColor(Color(0.5, 1, 0.8, alpha=0.6))
    for i in range(8):
        t = i * math.pi / 2
        r = 3 * phi ** (t * 2 / math.pi)
        if r > 350: break
        px = cx + r * math.cos(t)
        py = cy + r * math.sin(t)
        c.circle(px, py, 3, fill=1, stroke=0)
        # Glow
        c.setFillColor(Color(0, 1, 0.7, alpha=0.08))
        c.circle(px, py, 12, fill=1, stroke=0)
        c.setFillColor(Color(0.5, 1, 0.8, alpha=0.6))

    # Concentric circles at fibonacci radii
    c.setLineWidth(0.3)
    for f in fibs[:8]:
        r = f * scale
        c.setStrokeColor(Color(0, 0.8, 0.6, alpha=0.08))
        c.circle(cx, cy, r, fill=0, stroke=1)

    scatter_stars(c, 250, (0.3, 1, 0.7), cx, cy, 200)

    # Phi symbol text
    c.setFillColor(Color(0, 0.9, 0.65, alpha=0.15))
    c.setFont("Helvetica", 180)
    c.drawCentredString(cx + 130, cy - 80, "\u03C6")

    title_block(c, "FIBONACCI SPIRAL", "PHI  ·  GOLDEN RATIO  ·  1.618...",
                "GEOMETRIA SACRED PATTERNS — 003",
                Color(0, 0.9, 0.65, alpha=0.8), Color(0.3, 1, 0.8, alpha=0.3), Color(0.3, 1, 0.8, alpha=0.12))
    c.save()
    print("  003 done")


# ═══════════════════════════════════════════════════════════
# 004 — PLATONIC SOLIDS (Prismatic Rainbow)
# ═══════════════════════════════════════════════════════════
def gen_004():
    c = canvas.Canvas(f'{OUT}/004-platonic-solids.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.03, 0.06))
    cx, cy = W/2, H/2 + 50

    rainbow = [
        Color(1, 0.2, 0.3, alpha=0.6),   # red
        Color(1, 0.6, 0.1, alpha=0.55),   # orange
        Color(1, 0.95, 0.2, alpha=0.5),   # yellow
        Color(0.2, 0.9, 0.4, alpha=0.5),  # green
        Color(0.2, 0.6, 1, alpha=0.55),   # blue
    ]

    solids = [
        ("Tetrahedron", 4, -200, 80),
        ("Cube", 4, -100, -80),
        ("Octahedron", 3, 0, 80),
        ("Dodecahedron", 5, 100, -80),
        ("Icosahedron", 3, 200, 80),
    ]

    # Draw each platonic solid as a 2D projection
    positions = [
        (cx - 180, cy + 120),
        (cx + 180, cy + 120),
        (cx, cy - 20),
        (cx - 180, cy - 180),
        (cx + 180, cy - 180),
    ]

    for idx, ((px, py), (name, n, _, _)) in enumerate(zip(positions, solids)):
        col = rainbow[idx]
        r = 90

        # Draw wireframe projection
        c.setStrokeColor(col)
        c.setLineWidth(0.8)

        if idx == 0:  # Tetrahedron
            pts = draw_polygon(c, px, py, r, 3, -math.pi/2)
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.5))
            for pt in pts:
                c.line(px, py - r * 0.3, pt[0], pt[1])
            c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.08))
            p = c.beginPath()
            p.moveTo(*pts[0])
            for pt in pts[1:]: p.lineTo(*pt)
            p.close()
            c.drawPath(p, fill=1, stroke=0)

        elif idx == 1:  # Cube (isometric)
            s = r * 0.65
            offx, offy = s * 0.5, s * 0.3
            front = [(px-s, py-s), (px+s, py-s), (px+s, py+s), (px-s, py+s)]
            back = [(x+offx, y-offy) for x, y in front]
            c.setStrokeColor(col)
            for i in range(4):
                c.line(front[i][0], front[i][1], front[(i+1)%4][0], front[(i+1)%4][1])
                c.line(back[i][0], back[i][1], back[(i+1)%4][0], back[(i+1)%4][1])
                c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.4))
                c.line(front[i][0], front[i][1], back[i][0], back[i][1])
                c.setStrokeColor(col)

        elif idx == 2:  # Octahedron
            top = (px, py - r)
            bot = (px, py + r)
            mid = [(px + r * math.cos(i * math.pi/2), py + r * 0.35 * math.sin(i * math.pi/2)) for i in range(4)]
            c.setStrokeColor(col)
            for m in mid:
                c.line(top[0], top[1], m[0], m[1])
                c.line(bot[0], bot[1], m[0], m[1])
            for i in range(4):
                c.line(mid[i][0], mid[i][1], mid[(i+1)%4][0], mid[(i+1)%4][1])

        elif idx == 3:  # Dodecahedron (pentagon-based)
            draw_polygon(c, px, py, r, 5, -math.pi/2)
            draw_polygon(c, px, py, r * 0.62, 5, -math.pi/2 + math.pi/5)
            outer = [(px + r * math.cos(-math.pi/2 + i * 2*math.pi/5), py + r * math.sin(-math.pi/2 + i * 2*math.pi/5)) for i in range(5)]
            inner = [(px + r*0.62 * math.cos(-math.pi/2 + math.pi/5 + i * 2*math.pi/5), py + r*0.62 * math.sin(-math.pi/2 + math.pi/5 + i * 2*math.pi/5)) for i in range(5)]
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.5))
            for i in range(5):
                c.line(outer[i][0], outer[i][1], inner[i][0], inner[i][1])
                c.line(outer[i][0], outer[i][1], inner[(i-1)%5][0], inner[(i-1)%5][1])

        elif idx == 4:  # Icosahedron
            draw_polygon(c, px, py, r, 5, -math.pi/2)
            draw_polygon(c, px, py, r * 0.55, 5, -math.pi/2 + math.pi/5)
            outer = [(px + r * math.cos(-math.pi/2 + i * 2*math.pi/5), py + r * math.sin(-math.pi/2 + i * 2*math.pi/5)) for i in range(5)]
            inner = [(px + r*0.55 * math.cos(-math.pi/2 + math.pi/5 + i * 2*math.pi/5), py + r*0.55 * math.sin(-math.pi/2 + math.pi/5 + i * 2*math.pi/5)) for i in range(5)]
            top = (px, py - r * 1.1)
            bot = (px, py + r * 1.1)
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.5))
            for i in range(5):
                c.line(top[0], top[1], outer[i][0], outer[i][1])
                c.line(bot[0], bot[1], inner[i][0], inner[i][1])
                c.line(outer[i][0], outer[i][1], inner[i][0], inner[i][1])
                c.line(outer[i][0], outer[i][1], inner[(i-1)%5][0], inner[(i-1)%5][1])

        # Label
        c.setFillColor(Color(1, 1, 1, alpha=0.25))
        c.setFont("Helvetica", 9)
        c.drawCentredString(px, py + r + 18, name.upper())

        # Vertex dots
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.8))

    # Connecting lines between solids
    c.setStrokeColor(Color(1, 1, 1, alpha=0.03))
    c.setLineWidth(0.3)
    for i in range(len(positions)):
        for j in range(i+1, len(positions)):
            c.line(positions[i][0], positions[i][1], positions[j][0], positions[j][1])

    scatter_stars(c, 300, (0.7, 0.7, 1), cx, cy, 0)

    title_block(c, "PLATONIC SOLIDS", "FIRE  ·  EARTH  ·  AIR  ·  WATER  ·  AETHER",
                "GEOMETRIA SACRED PATTERNS — 004",
                Color(0.7, 0.8, 1, alpha=0.8), Color(0.7, 0.8, 1, alpha=0.3), Color(0.7, 0.8, 1, alpha=0.12))
    c.save()
    print("  004 done")


# ═══════════════════════════════════════════════════════════
# 005 — VESICA PISCIS (Deep Ocean Blue/Cyan)
# ═══════════════════════════════════════════════════════════
def gen_005():
    c = canvas.Canvas(f'{OUT}/005-vesica-piscis.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.03, 0.09))
    cx, cy = W/2, H/2 + 50
    r = 160

    blues = [
        Color(0.0, 0.5, 1.0, alpha=0.5),
        Color(0.0, 0.8, 0.95, alpha=0.4),
        Color(0.3, 0.4, 0.9, alpha=0.4),
        Color(0.1, 0.9, 1.0, alpha=0.35),
    ]

    # Two overlapping circles
    offset = r * 0.5
    c1x, c2x = cx - offset, cx + offset

    for layer in range(5, 0, -1):
        rr = r + layer * 3
        a = 0.05 * layer
        c.setStrokeColor(Color(0, 0.6, 1, alpha=a))
        c.setLineWidth(0.3)
        c.circle(c1x, cy, rr, fill=0, stroke=1)
        c.circle(c2x, cy, rr, fill=0, stroke=1)

    # Main circles
    c.setStrokeColor(blues[0])
    c.setLineWidth(1.5)
    c.circle(c1x, cy, r, fill=0, stroke=1)
    c.setStrokeColor(blues[1])
    c.circle(c2x, cy, r, fill=0, stroke=1)

    # Vesica shape - filled with gradient-like effect
    for step in range(40, 0, -1):
        t = step / 40
        rr = r * t
        off = offset * t
        alpha = 0.02 * (1 - t)
        c.setFillColor(Color(0, 0.7, 1, alpha=alpha))
        # Approximate vesica intersection with ellipse
        c.ellipse(cx - rr * 0.3, cy - rr * 0.85, cx + rr * 0.3, cy + rr * 0.85, fill=1, stroke=0)

    # Inner vesica outline
    # Draw the almond shape with arcs
    c.setStrokeColor(Color(0, 1, 0.95, alpha=0.6))
    c.setLineWidth(1.0)
    # Approximate with bezier curves
    vh = r * math.sqrt(3) * 0.5  # vesica height
    p = c.beginPath()
    p.moveTo(cx, cy - vh)
    p.curveTo(cx - r*0.8, cy - vh*0.3, cx - r*0.8, cy + vh*0.3, cx, cy + vh)
    p.curveTo(cx + r*0.8, cy + vh*0.3, cx + r*0.8, cy - vh*0.3, cx, cy - vh)
    c.drawPath(p, fill=0, stroke=1)

    # Radiating lines from center
    c.setLineWidth(0.3)
    for i in range(36):
        a = i * math.pi / 18
        length = 250 + 50 * math.sin(a * 3)
        c.setStrokeColor(Color(0, 0.7, 1, alpha=0.04))
        c.line(cx, cy, cx + length * math.cos(a), cy + length * math.sin(a))

    # Center point
    c.setFillColor(Color(0, 1, 1, alpha=0.9))
    c.circle(cx, cy, 4, fill=1, stroke=0)
    for rr in range(25, 0, -1):
        c.setFillColor(Color(0, 0.8, 1, alpha=0.03 * (1 - rr/25)))
        c.circle(cx, cy, rr, fill=1, stroke=0)

    scatter_stars(c, 300, (0.4, 0.7, 1), cx, cy, 250)

    title_block(c, "VESICA PISCIS", "DUALITY  ·  CREATION  ·  THE WOMB OF FORM",
                "GEOMETRIA SACRED PATTERNS — 005",
                Color(0, 0.8, 1, alpha=0.8), Color(0.3, 0.8, 1, alpha=0.3), Color(0.3, 0.8, 1, alpha=0.12))
    c.save()
    print("  005 done")


# ═══════════════════════════════════════════════════════════
# 006 — MANDALA (Jewel Tones: Ruby/Sapphire/Amethyst)
# ═══════════════════════════════════════════════════════════
def gen_006():
    c = canvas.Canvas(f'{OUT}/006-mandala.pdf', pagesize=A3)
    bg(c, Color(0.04, 0.02, 0.06))
    cx, cy = W/2, H/2 + 50

    jewels = [
        Color(0.8, 0.05, 0.3, alpha=0.5),   # ruby
        Color(0.15, 0.2, 0.85, alpha=0.45),  # sapphire
        Color(0.55, 0.15, 0.8, alpha=0.45),  # amethyst
        Color(0.9, 0.6, 0.1, alpha=0.4),     # topaz
        Color(0.1, 0.7, 0.5, alpha=0.4),     # emerald
    ]

    # Concentric mandala rings
    c.setLineWidth(0.6)

    # Ring 1: Inner petals (8)
    for i in range(8):
        a = i * math.pi / 4
        col = jewels[i % len(jewels)]
        c.setStrokeColor(col)
        # Petal shape
        for s in range(20):
            t = s / 20
            pr = 30 + 50 * math.sin(t * math.pi)
            pa = a + (t - 0.5) * 0.4
            px = cx + pr * math.cos(pa)
            py = cy + pr * math.sin(pa)
            if s == 0:
                path = c.beginPath()
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)
        c.drawPath(path, fill=0, stroke=1)

    # Ring 2: 12 petals
    for i in range(12):
        a = i * math.pi / 6
        col = jewels[i % len(jewels)]
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.8))
        for s in range(25):
            t = s / 25
            pr = 70 + 60 * math.sin(t * math.pi)
            pa = a + (t - 0.5) * 0.3
            px = cx + pr * math.cos(pa)
            py = cy + pr * math.sin(pa)
            if s == 0:
                path = c.beginPath()
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)
        c.drawPath(path, fill=0, stroke=1)

    # Ring 3: 16 petals with fill
    for i in range(16):
        a = i * math.pi / 8
        col = jewels[i % len(jewels)]
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.6))
        points = []
        for s in range(30):
            t = s / 30
            pr = 130 + 70 * math.sin(t * math.pi)
            pa = a + (t - 0.5) * 0.22
            px = cx + pr * math.cos(pa)
            py = cy + pr * math.sin(pa)
            points.append((px, py))
        path = c.beginPath()
        path.moveTo(*points[0])
        for pt in points[1:]: path.lineTo(*pt)
        path.close()
        c.drawPath(path, fill=0, stroke=1)

    # Ring 4: 24 fine petals
    for i in range(24):
        a = i * math.pi / 12
        col = jewels[i % len(jewels)]
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.4))
        c.setLineWidth(0.4)
        points = []
        for s in range(30):
            t = s / 30
            pr = 200 + 80 * math.sin(t * math.pi)
            pa = a + (t - 0.5) * 0.16
            px = cx + pr * math.cos(pa)
            py = cy + pr * math.sin(pa)
            points.append((px, py))
        path = c.beginPath()
        path.moveTo(*points[0])
        for pt in points[1:]: path.lineTo(*pt)
        c.drawPath(path, fill=0, stroke=1)

    # Concentric circles
    c.setLineWidth(0.5)
    for r in [30, 70, 130, 200, 280]:
        c.setStrokeColor(Color(0.7, 0.5, 0.9, alpha=0.12))
        c.circle(cx, cy, r, fill=0, stroke=1)

    # Outer ring: 32 dots
    for i in range(32):
        a = i * math.pi / 16
        px = cx + 290 * math.cos(a)
        py = cy + 290 * math.sin(a)
        col = jewels[i % len(jewels)]
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.5))
        c.circle(px, py, 2.5, fill=1, stroke=0)

    # Center lotus
    c.setFillColor(Color(0.8, 0.4, 0.9, alpha=0.15))
    c.circle(cx, cy, 20, fill=1, stroke=0)
    c.setFillColor(Color(1, 0.8, 0.9, alpha=0.8))
    c.circle(cx, cy, 4, fill=1, stroke=0)

    scatter_stars(c, 200, (0.8, 0.6, 1), cx, cy, 300)

    title_block(c, "MANDALA", "WHOLENESS  ·  BALANCE  ·  ETERNITY",
                "GEOMETRIA SACRED PATTERNS — 006",
                Color(0.7, 0.3, 0.9, alpha=0.8), Color(0.8, 0.5, 1, alpha=0.3), Color(0.8, 0.5, 1, alpha=0.12))
    c.save()
    print("  006 done")


# ═══════════════════════════════════════════════════════════
# 007 — METATRON'S CUBE (Electric Violet/White)
# ═══════════════════════════════════════════════════════════
def gen_007():
    c = canvas.Canvas(f'{OUT}/007-metatrons-cube.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.01, 0.07))
    cx, cy = W/2, H/2 + 50
    r = 120

    violets = [
        Color(0.6, 0.2, 1.0, alpha=0.55),
        Color(0.8, 0.4, 1.0, alpha=0.45),
        Color(0.5, 0.1, 0.9, alpha=0.5),
        Color(1.0, 0.6, 1.0, alpha=0.35),
    ]

    # 13 nodes of Metatron's Cube
    nodes = [(cx, cy)]  # center
    for i in range(6):  # inner ring
        a = i * math.pi / 3 - math.pi / 2
        nodes.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(6):  # outer ring
        a = i * math.pi / 3 - math.pi / 2
        nodes.append((cx + r * 2 * math.cos(a), cy + r * 2 * math.sin(a)))

    # Connect ALL nodes to each other
    c.setLineWidth(0.4)
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            dist = math.hypot(nodes[i][0] - nodes[j][0], nodes[i][1] - nodes[j][1])
            alpha = max(0.04, 0.25 * (1 - dist / (r * 4.5)))
            col = violets[(i + j) % len(violets)]
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
            c.line(nodes[i][0], nodes[i][1], nodes[j][0], nodes[j][1])

    # Circles at each node
    c.setLineWidth(0.8)
    for idx, (nx, ny) in enumerate(nodes):
        col = violets[idx % len(violets)]
        # Node circle
        c.setStrokeColor(col)
        c.circle(nx, ny, r * 0.35, fill=0, stroke=1)
        # Glow
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.04))
        c.circle(nx, ny, r * 0.35, fill=1, stroke=0)
        # Center dot
        c.setFillColor(Color(1, 0.8, 1, alpha=0.8))
        c.circle(nx, ny, 3, fill=1, stroke=0)

    # Outer boundary
    c.setStrokeColor(Color(0.7, 0.4, 1, alpha=0.15))
    c.setLineWidth(0.8)
    c.circle(cx, cy, r * 2.5, fill=0, stroke=1)
    c.circle(cx, cy, r * 2.7, fill=0, stroke=1)

    # Hidden platonic solid outlines
    c.setStrokeColor(Color(1, 0.7, 1, alpha=0.08))
    c.setLineWidth(0.5)
    draw_polygon(c, cx, cy, r * 2, 6, -math.pi/2)
    draw_polygon(c, cx, cy, r, 6, 0)

    scatter_stars(c, 300, (0.7, 0.5, 1), cx, cy, r * 2.5)

    title_block(c, "METATRON'S CUBE", "ARCHANGEL  ·  CREATION  ·  SACRED BLUEPRINT",
                "GEOMETRIA SACRED PATTERNS — 007",
                Color(0.7, 0.4, 1, alpha=0.8), Color(0.8, 0.6, 1, alpha=0.3), Color(0.8, 0.6, 1, alpha=0.12))
    c.save()
    print("  007 done")


# ═══════════════════════════════════════════════════════════
# 008 — TORUS (Rose/Magenta wireframe)
# ═══════════════════════════════════════════════════════════
def gen_008():
    c = canvas.Canvas(f'{OUT}/008-torus.pdf', pagesize=A3)
    bg(c, Color(0.05, 0.02, 0.04))
    cx, cy = W/2, H/2 + 40

    R = 160  # Major radius
    rr = 70   # Minor radius
    tilt = 0.4  # Tilt angle for 3D projection

    # Draw torus wireframe
    u_steps = 40
    v_steps = 20

    for u in range(u_steps):
        ua = u * 2 * math.pi / u_steps
        ua_next = (u + 1) * 2 * math.pi / u_steps

        points = []
        for v in range(v_steps + 1):
            va = v * 2 * math.pi / v_steps
            # 3D torus point
            x = (R + rr * math.cos(va)) * math.cos(ua)
            y = (R + rr * math.cos(va)) * math.sin(ua)
            z = rr * math.sin(va)
            # Project with tilt
            px = cx + x
            py = cy - y * math.sin(tilt) - z * math.cos(tilt)
            depth = y * math.cos(tilt) - z * math.sin(tilt)
            points.append((px, py, depth))

        for i in range(len(points) - 1):
            depth_avg = (points[i][2] + points[i+1][2]) / 2
            alpha = 0.08 + 0.35 * ((depth_avg + R + rr) / (2 * (R + rr)))
            hue_t = u / u_steps
            r_c = 0.9 + 0.1 * math.sin(hue_t * math.pi * 2)
            g_c = 0.2 + 0.3 * math.sin(hue_t * math.pi * 2 + 2)
            b_c = 0.5 + 0.4 * math.sin(hue_t * math.pi * 2 + 4)
            c.setStrokeColor(Color(r_c, g_c, b_c, alpha=alpha))
            c.setLineWidth(0.4)
            c.line(points[i][0], points[i][1], points[i+1][0], points[i+1][1])

    # Cross-sections (v-circles)
    for v in range(v_steps):
        va = v * 2 * math.pi / v_steps
        points = []
        for u in range(u_steps + 1):
            ua = u * 2 * math.pi / u_steps
            x = (R + rr * math.cos(va)) * math.cos(ua)
            y = (R + rr * math.cos(va)) * math.sin(ua)
            z = rr * math.sin(va)
            px = cx + x
            py = cy - y * math.sin(tilt) - z * math.cos(tilt)
            depth = y * math.cos(tilt) - z * math.sin(tilt)
            points.append((px, py, depth))

        for i in range(len(points) - 1):
            depth_avg = (points[i][2] + points[i+1][2]) / 2
            alpha = 0.03 + 0.15 * ((depth_avg + R + rr) / (2 * (R + rr)))
            c.setStrokeColor(Color(1, 0.4, 0.7, alpha=alpha))
            c.setLineWidth(0.3)
            c.line(points[i][0], points[i][1], points[i+1][0], points[i+1][1])

    scatter_stars(c, 200, (1, 0.5, 0.7), cx, cy, 250)

    title_block(c, "TORUS", "INFINITY  ·  SELF-REFERENCE  ·  ENERGY FLOW",
                "GEOMETRIA SACRED PATTERNS — 008",
                Color(1, 0.4, 0.7, alpha=0.8), Color(1, 0.6, 0.8, alpha=0.3), Color(1, 0.6, 0.8, alpha=0.12))
    c.save()
    print("  008 done")


# ═══════════════════════════════════════════════════════════
# 009 — PENROSE TILING (Sunset: Coral/Amber/Peach)
# ═══════════════════════════════════════════════════════════
def gen_009():
    c = canvas.Canvas(f'{OUT}/009-penrose-tiling.pdf', pagesize=A3)
    bg(c, Color(0.07, 0.03, 0.02))
    cx, cy = W/2, H/2 + 50

    sunsets = [
        Color(1.0, 0.45, 0.3, alpha=0.4),
        Color(1.0, 0.65, 0.2, alpha=0.35),
        Color(1.0, 0.8, 0.5, alpha=0.3),
        Color(0.95, 0.35, 0.4, alpha=0.35),
    ]

    phi = (1 + math.sqrt(5)) / 2

    # Generate Penrose-like pattern with kite and dart shapes
    # Using de Bruijn's method simplified: concentric pentagons with subdivisions
    def draw_kite(c, x, y, size, angle, depth, max_depth):
        if depth >= max_depth or size < 3:
            return
        col = sunsets[depth % len(sunsets)]
        dist = math.hypot(x - cx, y - cy)
        fade = max(0.3, 1.0 - dist / 400)

        # Kite vertices
        pts = []
        angles_off = [0, 0.3 * math.pi, math.pi, -0.3 * math.pi]
        sizes = [size, size * 0.8, size * 0.5, size * 0.8]
        for ao, sz in zip(angles_off, sizes):
            pts.append((x + sz * math.cos(angle + ao), y + sz * math.sin(angle + ao)))

        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
        c.setLineWidth(0.5 - depth * 0.1)
        p = c.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]: p.lineTo(*pt)
        p.close()
        c.drawPath(p, fill=0, stroke=1)

        # Fill with very low alpha
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.02 * fade))
        c.drawPath(p, fill=1, stroke=0)

        # Subdivide
        if depth < max_depth - 1:
            new_size = size / phi
            for i in range(2):
                na = angle + (i - 0.5) * 0.6
                nx = x + size * 0.4 * math.cos(na)
                ny = y + size * 0.4 * math.sin(na)
                draw_kite(c, nx, ny, new_size, na, depth + 1, max_depth)

    # Create a 5-fold symmetric pattern
    for ring in range(3):
        for i in range(5):
            a = i * 2 * math.pi / 5 - math.pi / 2
            dist = 80 + ring * 120
            x = cx + dist * math.cos(a)
            y = cy + dist * math.sin(a)
            draw_kite(c, x, y, 80 - ring * 10, a, 0, 4)

            # Between main directions
            a2 = a + math.pi / 5
            x2 = cx + (dist + 60) * math.cos(a2)
            y2 = cy + (dist + 60) * math.sin(a2)
            draw_kite(c, x2, y2, 60 - ring * 8, a2, 0, 3)

    # Central pentagon
    c.setStrokeColor(Color(1, 0.6, 0.3, alpha=0.5))
    c.setLineWidth(1.0)
    draw_polygon(c, cx, cy, 50, 5, -math.pi/2)

    # Outer pentagons
    c.setLineWidth(0.5)
    for r in [150, 250, 350]:
        c.setStrokeColor(Color(1, 0.6, 0.3, alpha=0.1))
        draw_polygon(c, cx, cy, r, 5, -math.pi/2)
        c.setStrokeColor(Color(1, 0.6, 0.3, alpha=0.06))
        draw_polygon(c, cx, cy, r, 5, -math.pi/2 + math.pi/5)

    scatter_stars(c, 200, (1, 0.7, 0.4), cx, cy, 350)

    title_block(c, "PENROSE TILING", "APERIODIC  ·  ORDER IN CHAOS  ·  QUASICRYSTAL",
                "GEOMETRIA SACRED PATTERNS — 009",
                Color(1, 0.55, 0.3, alpha=0.8), Color(1, 0.7, 0.5, alpha=0.3), Color(1, 0.7, 0.5, alpha=0.12))
    c.save()
    print("  009 done")


# ═══════════════════════════════════════════════════════════
# 010 — GEODESIC SPHERE (Mint/Teal/Seafoam)
# ═══════════════════════════════════════════════════════════
def gen_010():
    c = canvas.Canvas(f'{OUT}/010-geodesic-sphere.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.05, 0.05))
    cx, cy = W/2, H/2 + 50
    R = 220

    teals = [
        Color(0.0, 0.85, 0.75, alpha=0.45),
        Color(0.3, 0.95, 0.85, alpha=0.4),
        Color(0.0, 0.65, 0.6, alpha=0.4),
        Color(0.5, 1.0, 0.9, alpha=0.3),
    ]

    # Generate geodesic dome points by subdividing an icosahedron
    # Icosahedron vertices
    t = (1 + math.sqrt(5)) / 2
    ico_verts = [
        (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
        (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
        (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1)
    ]
    # Normalize
    ico_verts = [(x/math.sqrt(x*x+y*y+z*z), y/math.sqrt(x*x+y*y+z*z), z/math.sqrt(x*x+y*y+z*z))
                 for x, y, z in ico_verts]

    ico_faces = [
        (0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),
        (1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),
        (3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),
        (4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)
    ]

    # Subdivide each face once
    def midpoint(v1, v2):
        mx = (v1[0]+v2[0])/2
        my = (v1[1]+v2[1])/2
        mz = (v1[2]+v2[2])/2
        l = math.sqrt(mx*mx+my*my+mz*mz)
        return (mx/l, my/l, mz/l)

    edges = set()
    all_verts = list(ico_verts)
    new_faces = []
    mid_cache = {}

    def get_mid(i, j):
        key = (min(i,j), max(i,j))
        if key in mid_cache:
            return mid_cache[key]
        m = midpoint(all_verts[i], all_verts[j])
        all_verts.append(m)
        idx = len(all_verts) - 1
        mid_cache[key] = idx
        return idx

    for f in ico_faces:
        a, b, cc_f = f
        ab = get_mid(a, b)
        bc = get_mid(b, cc_f)
        ca = get_mid(cc_f, a)
        new_faces.extend([(a, ab, ca), (b, bc, ab), (cc_f, ca, bc), (ab, bc, ca)])

    # Project and draw
    tilt_x = 0.5
    tilt_z = 0.3

    def project(v):
        x, y, z = v
        # Rotate around X
        y2 = y * math.cos(tilt_x) - z * math.sin(tilt_x)
        z2 = y * math.sin(tilt_x) + z * math.cos(tilt_x)
        # Rotate around Z
        x3 = x * math.cos(tilt_z) - y2 * math.sin(tilt_z)
        y3 = x * math.sin(tilt_z) + y2 * math.cos(tilt_z)
        return (cx + x3 * R, cy + y3 * R, z2)

    projected = [project(v) for v in all_verts]

    # Draw edges from faces
    drawn_edges = set()
    for f in new_faces:
        for i in range(3):
            e = (min(f[i], f[(i+1)%3]), max(f[i], f[(i+1)%3]))
            if e not in drawn_edges:
                drawn_edges.add(e)
                p1, p2 = projected[e[0]], projected[e[1]]
                depth = (p1[2] + p2[2]) / 2
                alpha = 0.1 + 0.4 * ((depth + 1) / 2)
                col = teals[hash(e) % len(teals)]
                c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
                c.setLineWidth(0.5 + 0.5 * ((depth + 1) / 2))
                c.line(p1[0], p1[1], p2[0], p2[1])

    # Vertex dots
    for px, py, pz in projected:
        alpha = 0.3 + 0.5 * ((pz + 1) / 2)
        c.setFillColor(Color(0.3, 1, 0.9, alpha=alpha))
        sz = 1.5 + 1.5 * ((pz + 1) / 2)
        c.circle(px, py, sz, fill=1, stroke=0)

    scatter_stars(c, 250, (0.3, 0.9, 0.8), cx, cy, R + 30)

    title_block(c, "GEODESIC SPHERE", "BUCKMINSTER FULLER  ·  TENSEGRITY  ·  STRENGTH",
                "GEOMETRIA SACRED PATTERNS — 010",
                Color(0, 0.9, 0.8, alpha=0.8), Color(0.3, 1, 0.9, alpha=0.3), Color(0.3, 1, 0.9, alpha=0.12))
    c.save()
    print("  010 done")


# ═══════════════════════════════════════════════════════════
# 011 — VORONOI COSMOS (Neon pastels)
# ═══════════════════════════════════════════════════════════
def gen_011():
    c = canvas.Canvas(f'{OUT}/011-voronoi-cosmos.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.02, 0.04))
    cx, cy = W/2, H/2

    neons = [
        Color(1.0, 0.4, 0.7, alpha=0.4),
        Color(0.4, 0.8, 1.0, alpha=0.4),
        Color(0.4, 1.0, 0.6, alpha=0.35),
        Color(1.0, 0.8, 0.3, alpha=0.35),
        Color(0.7, 0.4, 1.0, alpha=0.4),
    ]

    random.seed(42)

    # Generate Voronoi-like cells using seed points
    seeds = [(random.uniform(30, W-30), random.uniform(140, H-30)) for _ in range(60)]

    # For each seed, find neighboring seeds and draw edges (Delaunay-like)
    c.setLineWidth(0.6)
    for i, (sx, sy) in enumerate(seeds):
        # Find nearest neighbors
        dists = []
        for j, (sx2, sy2) in enumerate(seeds):
            if i != j:
                d = math.hypot(sx - sx2, sy - sy2)
                dists.append((d, j))
        dists.sort()

        # Connect to nearest ~5 neighbors
        for d, j in dists[:6]:
            if d < 200:
                sx2, sy2 = seeds[j]
                alpha = 0.15 * (1 - d / 200)
                col = neons[(i + j) % len(neons)]
                c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
                c.line(sx, sy, sx2, sy2)

        # Draw perpendicular bisectors (Voronoi edges approximation)
        for d, j in dists[:4]:
            if d < 180:
                sx2, sy2 = seeds[j]
                mx, my = (sx + sx2) / 2, (sy + sy2) / 2
                dx, dy = sx2 - sx, sy2 - sy
                # Perpendicular
                px, py = -dy, dx
                length = d * 0.4
                pl = math.sqrt(px*px + py*py)
                if pl > 0:
                    px, py = px/pl * length, py/pl * length
                    alpha = 0.08 * (1 - d / 180)
                    col = neons[i % len(neons)]
                    c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
                    c.setLineWidth(0.4)
                    c.line(mx - px, my - py, mx + px, my + py)

    # Seed points as glowing dots
    for i, (sx, sy) in enumerate(seeds):
        col = neons[i % len(neons)]
        # Glow
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.06))
        c.circle(sx, sy, 15, fill=1, stroke=0)
        # Dot
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.7))
        c.circle(sx, sy, 2.5, fill=1, stroke=0)

    scatter_stars(c, 150, (0.8, 0.7, 1), cx, cy, 0)

    title_block(c, "VORONOI COSMOS", "ORGANIC CELLS  ·  TERRITORY  ·  NATURAL ORDER",
                "GEOMETRIA SACRED PATTERNS — 011",
                Color(0.8, 0.5, 1, alpha=0.8), Color(0.8, 0.7, 1, alpha=0.3), Color(0.8, 0.7, 1, alpha=0.12))
    c.save()
    print("  011 done")


# ═══════════════════════════════════════════════════════════
# 012 — LISSAJOUS HARMONY (Electric Blue/White)
# ═══════════════════════════════════════════════════════════
def gen_012():
    c = canvas.Canvas(f'{OUT}/012-lissajous-harmony.pdf', pagesize=A3)
    bg(c, Color(0.01, 0.02, 0.06))
    cx, cy = W/2, H/2 + 50

    electrics = [
        Color(0.2, 0.5, 1.0, alpha=0.5),
        Color(0.4, 0.7, 1.0, alpha=0.4),
        Color(0.1, 0.3, 0.9, alpha=0.45),
        Color(0.6, 0.8, 1.0, alpha=0.35),
    ]

    # Multiple Lissajous curves with different frequency ratios
    ratios = [
        (1, 2, 0, 200, 180),
        (3, 2, math.pi/4, 180, 160),
        (3, 4, math.pi/3, 160, 150),
        (5, 4, math.pi/6, 140, 130),
        (5, 6, 0, 120, 110),
    ]

    for idx, (a_freq, b_freq, phase, ax, ay) in enumerate(ratios):
        col = electrics[idx % len(electrics)]
        fade = 1.0 - idx * 0.12
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
        c.setLineWidth(1.0 - idx * 0.12)

        steps = 1000
        p = c.beginPath()
        for s in range(steps + 1):
            t = s / steps * 2 * math.pi
            x = cx + ax * math.sin(a_freq * t + phase)
            y = cy + ay * math.sin(b_freq * t)
            if s == 0:
                p.moveTo(x, y)
            else:
                p.lineTo(x, y)
        c.drawPath(p, fill=0, stroke=1)

    # Frequency labels at intersection points
    c.setFont("Courier", 7)
    c.setFillColor(Color(0.5, 0.7, 1, alpha=0.2))
    for idx, (a_freq, b_freq, _, _, _) in enumerate(ratios):
        c.drawString(W - 100, H - 150 - idx * 14, f"{a_freq}:{b_freq}")

    # Axis lines
    c.setStrokeColor(Color(0.3, 0.5, 1, alpha=0.06))
    c.setLineWidth(0.3)
    c.line(cx - 250, cy, cx + 250, cy)
    c.line(cx, cy - 230, cx, cy + 230)

    scatter_stars(c, 300, (0.4, 0.6, 1), cx, cy, 0)

    title_block(c, "LISSAJOUS HARMONY", "FREQUENCY  ·  RESONANCE  ·  HARMONIC MOTION",
                "GEOMETRIA SACRED PATTERNS — 012",
                Color(0.3, 0.6, 1, alpha=0.8), Color(0.5, 0.7, 1, alpha=0.3), Color(0.5, 0.7, 1, alpha=0.12))
    c.save()
    print("  012 done")


# ═══════════════════════════════════════════════════════════
# 013 — SEED OF LIFE (Soft Lavender/Lilac)
# ═══════════════════════════════════════════════════════════
def gen_013():
    c = canvas.Canvas(f'{OUT}/013-seed-of-life.pdf', pagesize=A3)
    bg(c, Color(0.04, 0.03, 0.06))
    cx, cy = W/2, H/2 + 50
    r = 100

    lavenders = [
        Color(0.7, 0.5, 0.9, alpha=0.5),
        Color(0.8, 0.6, 1.0, alpha=0.4),
        Color(0.6, 0.4, 0.8, alpha=0.45),
        Color(0.9, 0.7, 1.0, alpha=0.35),
    ]

    # Seed of Life: 7 circles
    centers = [(cx, cy)]
    for i in range(6):
        a = i * math.pi / 3
        centers.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    # Multiple concentric seeds at different scales
    scales = [0.3, 0.6, 1.0, 1.5, 2.0]
    for si, scale in enumerate(scales):
        sr = r * scale
        fade = 1.0 - si * 0.15
        c.setLineWidth(0.8 - si * 0.1)

        sc_centers = [(cx, cy)]
        for i in range(6):
            a = i * math.pi / 3 + si * 0.1  # slight rotation per scale
            sc_centers.append((cx + sr * math.cos(a), cy + sr * math.sin(a)))

        for idx, (px, py) in enumerate(sc_centers):
            col = lavenders[idx % len(lavenders)]
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
            c.circle(px, py, sr, fill=0, stroke=1)

    # Intersection points decoration
    c.setFillColor(Color(0.8, 0.6, 1, alpha=0.5))
    for i in range(6):
        a1 = i * math.pi / 3
        a2 = (i + 1) * math.pi / 3
        # Approximate intersection of adjacent circles
        ix = cx + r * math.cos((a1 + a2) / 2) * 0.58
        iy = cy + r * math.sin((a1 + a2) / 2) * 0.58
        c.circle(ix, iy, 2.5, fill=1, stroke=0)

    # Outer ring
    c.setStrokeColor(Color(0.7, 0.5, 0.9, alpha=0.2))
    c.setLineWidth(1.0)
    c.circle(cx, cy, r * 2.3, fill=0, stroke=1)

    # Center glow
    for rr in range(40, 0, -1):
        a = 0.03 * (1 - rr/40)
        c.setFillColor(Color(0.8, 0.5, 1, alpha=a))
        c.circle(cx, cy, rr, fill=1, stroke=0)

    scatter_stars(c, 250, (0.7, 0.5, 1), cx, cy, r * 2.3)

    title_block(c, "SEED OF LIFE", "SEVEN DAYS  ·  GENESIS  ·  THE BEGINNING",
                "GEOMETRIA SACRED PATTERNS — 013",
                Color(0.75, 0.55, 1, alpha=0.8), Color(0.8, 0.65, 1, alpha=0.3), Color(0.8, 0.65, 1, alpha=0.12))
    c.save()
    print("  013 done")


# ═══════════════════════════════════════════════════════════
# 014 — FRACTAL TREE (Forest Green/Bark Brown)
# ═══════════════════════════════════════════════════════════
def gen_014():
    c = canvas.Canvas(f'{OUT}/014-fractal-tree.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.04, 0.03))
    cx, cy = W/2, 180  # Base of tree

    forests = [
        Color(0.15, 0.5, 0.2, alpha=0.6),
        Color(0.2, 0.7, 0.3, alpha=0.5),
        Color(0.3, 0.85, 0.4, alpha=0.4),
        Color(0.5, 0.95, 0.5, alpha=0.35),
        Color(0.1, 0.35, 0.15, alpha=0.5),
    ]

    random.seed(314)

    def branch(x, y, length, angle, depth, max_depth):
        if depth >= max_depth or length < 4:
            # Leaf
            c.setFillColor(Color(0.3 + random.random()*0.3, 0.8 + random.random()*0.2, 0.3, alpha=0.3))
            c.circle(x, y, random.random() * 3 + 1, fill=1, stroke=0)
            return

        x2 = x + length * math.cos(angle)
        y2 = y + length * math.sin(angle)

        col = forests[min(depth, len(forests)-1)]
        width = max(0.3, 3.0 - depth * 0.35)
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha))
        c.setLineWidth(width)
        c.line(x, y, x2, y2)

        # Branch with slight randomness
        spread = 0.4 + random.random() * 0.2
        shrink = 0.65 + random.random() * 0.1

        branch(x2, y2, length * shrink, angle + spread, depth + 1, max_depth)
        branch(x2, y2, length * shrink, angle - spread, depth + 1, max_depth)

        # Sometimes a third branch
        if random.random() < 0.3 and depth < 4:
            branch(x2, y2, length * shrink * 0.8, angle + (random.random() - 0.5) * 0.3, depth + 1, max_depth)

    # Main trunk
    branch(cx, cy, 130, math.pi/2, 0, 10)

    # Root system (mirrored, subtler)
    c.setLineWidth(0.3)
    for i in range(5):
        a = math.pi * 1.2 + i * 0.15 + random.random() * 0.1
        length = 40 + random.random() * 30
        x2 = cx + length * math.cos(a)
        y2 = cy + length * math.sin(a)
        c.setStrokeColor(Color(0.3, 0.2, 0.1, alpha=0.2))
        c.line(cx, cy, x2, y2)
    for i in range(5):
        a = math.pi * 1.5 + i * 0.15 + random.random() * 0.1
        length = 40 + random.random() * 30
        x2 = cx + length * math.cos(a)
        y2 = cy + length * math.sin(a)
        c.setStrokeColor(Color(0.3, 0.2, 0.1, alpha=0.2))
        c.line(cx, cy, x2, y2)

    # Ground line
    c.setStrokeColor(Color(0.3, 0.5, 0.2, alpha=0.1))
    c.setLineWidth(0.5)
    c.line(50, cy, W - 50, cy)

    # Circular frame
    c.setStrokeColor(Color(0.3, 0.7, 0.3, alpha=0.1))
    c.setLineWidth(0.8)
    c.circle(cx, H/2 + 50, 350, fill=0, stroke=1)

    scatter_stars(c, 200, (0.4, 0.8, 0.4), cx, H/2, 350)

    title_block(c, "FRACTAL TREE", "RECURSION  ·  GROWTH  ·  BRANCHING LIFE",
                "GEOMETRIA SACRED PATTERNS — 014",
                Color(0.3, 0.8, 0.4, alpha=0.8), Color(0.4, 0.9, 0.5, alpha=0.3), Color(0.4, 0.9, 0.5, alpha=0.12))
    c.save()
    print("  014 done")


# ═══════════════════════════════════════════════════════════
# 015 — HYPERBOLIC TESSELLATION (Deep Red/Burgundy/Gold)
# ═══════════════════════════════════════════════════════════
def gen_015():
    c = canvas.Canvas(f'{OUT}/015-hyperbolic-tessellation.pdf', pagesize=A3)
    bg(c, Color(0.06, 0.02, 0.02))
    cx, cy = W/2, H/2 + 50
    R = 280  # Poincaré disk radius

    burgundies = [
        Color(0.7, 0.1, 0.15, alpha=0.5),
        Color(0.85, 0.2, 0.1, alpha=0.4),
        Color(0.9, 0.7, 0.1, alpha=0.35),
        Color(0.6, 0.05, 0.2, alpha=0.45),
    ]

    # Poincaré disk boundary
    c.setStrokeColor(Color(0.8, 0.6, 0.1, alpha=0.3))
    c.setLineWidth(1.5)
    c.circle(cx, cy, R, fill=0, stroke=1)

    # Hyperbolic geodesics (arcs within the disk)
    # Draw a {7,3} tiling approximation
    def disk_point(r_hyp, angle):
        """Convert hyperbolic polar to Poincaré disk coords."""
        r_disk = math.tanh(r_hyp / 2)
        return (cx + R * r_disk * math.cos(angle), cy + R * r_disk * math.sin(angle))

    # Draw heptagons at different hyperbolic distances
    def draw_hyp_polygon(n, hyp_r, rotation, col_idx):
        pts = []
        for i in range(n + 1):
            a = rotation + i * 2 * math.pi / n
            px, py = disk_point(hyp_r, a)
            pts.append((px, py))

        # Check if polygon is within disk
        for px, py in pts:
            if math.hypot(px - cx, py - cy) > R * 0.98:
                return

        col = burgundies[col_idx % len(burgundies)]
        dist_from_center = math.hypot(pts[0][0] - cx, pts[0][1] - cy)
        fade = max(0.2, 1.0 - dist_from_center / (R * 0.9))
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
        c.setLineWidth(0.6 * fade + 0.2)

        p = c.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        c.drawPath(p, fill=0, stroke=1)

        # Fill
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.015 * fade))
        p = c.beginPath()
        p.moveTo(*pts[0])
        for pt in pts[1:]:
            p.lineTo(*pt)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    # Central heptagon
    draw_hyp_polygon(7, 0.6, 0, 0)

    # First ring: 7 heptagons
    for i in range(7):
        a = i * 2 * math.pi / 7
        draw_hyp_polygon(7, 1.3, a + math.pi/7, 1)

    # Second ring: 14 heptagons
    for i in range(14):
        a = i * 2 * math.pi / 14 + math.pi/14
        draw_hyp_polygon(7, 2.0, a, 2)

    # Third ring: 21 heptagons
    for i in range(21):
        a = i * 2 * math.pi / 21
        draw_hyp_polygon(7, 2.7, a + math.pi/21, 3)

    # Fourth ring
    for i in range(28):
        a = i * 2 * math.pi / 28 + math.pi/28
        draw_hyp_polygon(7, 3.3, a, 0)

    # Radial geodesics
    c.setLineWidth(0.3)
    for i in range(14):
        a = i * math.pi / 7
        inner = disk_point(0.2, a)
        outer = disk_point(4.0, a)
        c.setStrokeColor(Color(0.9, 0.7, 0.1, alpha=0.05))
        c.line(inner[0], inner[1], outer[0], outer[1])

    # Concentric hyperbolic circles
    for hr in [0.8, 1.5, 2.3, 3.0]:
        dr = R * math.tanh(hr / 2)
        c.setStrokeColor(Color(0.8, 0.5, 0.1, alpha=0.06))
        c.setLineWidth(0.3)
        c.circle(cx, cy, dr, fill=0, stroke=1)

    scatter_stars(c, 150, (0.9, 0.6, 0.3), cx, cy, R + 10)

    title_block(c, "HYPERBOLIC TESSELLATION", "POINCARE DISK  ·  NON-EUCLIDEAN  ·  INFINITY",
                "GEOMETRIA SACRED PATTERNS — 015",
                Color(0.85, 0.3, 0.15, alpha=0.8), Color(0.9, 0.6, 0.3, alpha=0.3), Color(0.9, 0.6, 0.3, alpha=0.12))
    c.save()
    print("  015 done")


# ═══════════════════════════════════════════════════════════
# GENERATE ALL
# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating GEOMETRIA SACRED PATTERNS series...")
    gen_001()
    gen_002()
    gen_003()
    gen_004()
    gen_005()
    gen_006()
    gen_007()
    gen_008()
    gen_009()
    gen_010()
    gen_011()
    gen_012()
    gen_013()
    gen_014()
    gen_015()
    print("\nAll 15 PDFs generated!")
