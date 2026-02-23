#!/usr/bin/env python3
"""GEOMETRIA SACRED PATTERNS — Generative Series 031–045"""

import math
import random
import os
from reportlab.lib.pagesizes import A3
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

W, H = A3
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
# 031 — JULIA SET (Deep Ultraviolet / Plasma Pink)
# Fractal boundary of complex dynamics
# ═══════════════════════════════════════════════════════════
def gen_031():
    c = canvas.Canvas(f'{OUT}/031-julia-set.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.01, 0.04))
    cx, cy = W/2, H/2 + 50

    # Julia set for c = -0.7 + 0.27015i
    c_re, c_im = -0.7, 0.27015
    max_iter = 80
    R = 280
    res = 350

    for ix in range(res):
        for iy in range(res):
            # Map pixel to complex plane [-1.5, 1.5]
            x0 = (ix / res - 0.5) * 3.0
            y0 = (iy / res - 0.5) * 3.0
            zr, zi = x0, y0
            iteration = 0
            while zr*zr + zi*zi < 4 and iteration < max_iter:
                zr_new = zr*zr - zi*zi + c_re
                zi = 2*zr*zi + c_im
                zr = zr_new
                iteration += 1

            if iteration < max_iter:
                t = iteration / max_iter
                # Color mapping: ultraviolet → pink → white
                r_c = min(1, 0.3 + t * 1.5)
                g_c = min(1, 0.05 + t * 0.6)
                b_c = min(1, 0.5 + t * 0.8)
                alpha = min(0.6, 0.05 + t * 0.8)
                sz = 0.8 + t * 1.2

                px = cx + (ix / res - 0.5) * R * 2
                py = cy + (iy / res - 0.5) * R * 2
                c.setFillColor(Color(r_c, g_c, b_c, alpha=alpha))
                c.circle(px, py, sz, fill=1, stroke=0)

    # Boundary glow
    c.setStrokeColor(Color(0.8, 0.3, 1, alpha=0.08))
    c.setLineWidth(0.5)
    c.circle(cx, cy, R, fill=0, stroke=1)

    scatter_stars(c, 150, (0.6, 0.3, 0.9), cx, cy, R + 20)

    title_block(c, "JULIA SET", "COMPLEX DYNAMICS  ·  FRACTAL BOUNDARY  ·  c = -0.7 + 0.27i",
                "GEOMETRIA SACRED PATTERNS — 031",
                Color(0.8, 0.3, 1, alpha=0.85), Color(0.8, 0.5, 1, alpha=0.3), Color(0.8, 0.5, 1, alpha=0.12))
    c.save()
    print("  031 done")


# ═══════════════════════════════════════════════════════════
# 032 — MAGNETIC FIELD (Iron / Steel Blue / Arc White)
# Dipole field lines — invisible forces
# ═══════════════════════════════════════════════════════════
def gen_032():
    c = canvas.Canvas(f'{OUT}/032-magnetic-field.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.02, 0.05))
    cx, cy = W/2, H/2 + 50

    steels = [
        Color(0.4, 0.6, 0.9, alpha=0.45),
        Color(0.6, 0.75, 1.0, alpha=0.4),
        Color(0.3, 0.45, 0.8, alpha=0.4),
        Color(0.8, 0.85, 1.0, alpha=0.3),
    ]

    # Two magnetic poles
    pole_sep = 120
    north = (cx, cy + pole_sep/2)
    south = (cx, cy - pole_sep/2)

    # Draw field lines by tracing from angles around north pole
    random.seed(77)
    for start_angle_deg in range(0, 360, 8):
        a = math.radians(start_angle_deg)
        x = north[0] + 8 * math.cos(a)
        y = north[1] + 8 * math.sin(a)

        col = steels[start_angle_deg // 90 % len(steels)]

        pts = [(x, y)]
        for step in range(500):
            # Magnetic field of a dipole (simplified)
            bx_total, by_total = 0, 0
            for pole, sign in [(north, 1), (south, -1)]:
                dx = x - pole[0]
                dy = y - pole[1]
                r_sq = dx*dx + dy*dy + 1
                r = math.sqrt(r_sq)
                # Field points away from north, toward south
                bx_total += sign * dx / (r_sq * r) * 1e6
                by_total += sign * dy / (r_sq * r) * 1e6

            b_mag = math.sqrt(bx_total*bx_total + by_total*by_total) + 1e-10
            x += bx_total / b_mag * 3
            y += by_total / b_mag * 3
            pts.append((x, y))

            # Stop if too far or reached south pole
            if math.hypot(x - cx, y - cy) > 400:
                break
            if math.hypot(x - south[0], y - south[1]) < 10:
                break

        # Draw field line
        if len(pts) > 5:
            for i in range(len(pts) - 1):
                dist_n = math.hypot(pts[i][0] - north[0], pts[i][1] - north[1])
                dist_s = math.hypot(pts[i][0] - south[0], pts[i][1] - south[1])
                min_d = min(dist_n, dist_s)
                alpha = min(0.5, max(0.05, 0.4 * (1 - min_d / 400)))
                c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
                c.setLineWidth(0.4 + 0.6 * (1 - min_d / 400))
                c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1])

    # Pole markers
    for pole, label, col_p in [(north, "N", Color(0.9, 0.3, 0.3)), (south, "S", Color(0.3, 0.5, 0.9))]:
        for rr in range(30, 0, -1):
            c.setFillColor(Color(col_p.red, col_p.green, col_p.blue, alpha=0.03 * (1 - rr/30)))
            c.circle(pole[0], pole[1], rr, fill=1, stroke=0)
        c.setFillColor(Color(col_p.red, col_p.green, col_p.blue, alpha=0.8))
        c.circle(pole[0], pole[1], 6, fill=1, stroke=0)
        c.setFillColor(Color(1, 1, 1, alpha=0.6))
        c.setFont("Helvetica", 8)
        c.drawCentredString(pole[0], pole[1] - 3, label)

    scatter_stars(c, 200, (0.5, 0.6, 0.9), cx, cy, 0)

    title_block(c, "MAGNETIC FIELD", "DIPOLE  ·  INVISIBLE FORCES  ·  MAXWELL'S EQUATIONS",
                "GEOMETRIA SACRED PATTERNS — 032",
                Color(0.5, 0.7, 1, alpha=0.85), Color(0.6, 0.75, 1, alpha=0.3), Color(0.6, 0.75, 1, alpha=0.12))
    c.save()
    print("  032 done")


# ═══════════════════════════════════════════════════════════
# 033 — HARMONIC OSCILLATOR (Warm Copper / Bronze)
# Pendulum traces — phase space portraits
# ═══════════════════════════════════════════════════════════
def gen_033():
    c = canvas.Canvas(f'{OUT}/033-harmonic-oscillator.pdf', pagesize=A3)
    bg(c, Color(0.05, 0.03, 0.02))
    cx, cy = W/2, H/2 + 50

    coppers = [
        Color(0.85, 0.55, 0.25, alpha=0.5),
        Color(0.75, 0.45, 0.15, alpha=0.45),
        Color(0.95, 0.7, 0.35, alpha=0.4),
        Color(0.65, 0.35, 0.1, alpha=0.45),
    ]

    # Harmonograph: pendulum drawing machine
    # x = A1*sin(f1*t + p1)*exp(-d1*t) + A2*sin(f2*t + p2)*exp(-d2*t)
    # y = A3*sin(f3*t + p3)*exp(-d3*t) + A4*sin(f4*t + p4)*exp(-d4*t)
    configs = [
        # (a1,f1,p1,d1, a2,f2,p2,d2, a3,f3,p3,d3, a4,f4,p4,d4)
        (200,2.01,0,0.002, 0,0,0,0, 200,3.0,math.pi/2,0.002, 0,0,0,0),
        (180,2.0,0,0.003, 50,6.01,0,0.005, 180,3.0,1.5,0.003, 50,2.0,0,0.005),
        (160,3.0,0,0.001, 80,2.0,math.pi/4,0.004, 160,2.0,0,0.001, 80,3.01,0,0.004),
        (200,2.0,0,0.0008, 100,3.0,math.pi/3,0.003, 200,3.0,math.pi/2,0.0008, 100,4.0,0,0.003),
    ]

    for ci_idx, cfg in enumerate(configs):
        a1,f1,p1,d1,a2,f2,p2,d2,a3,f3,p3,d3,a4,f4,p4,d4 = cfg
        col = coppers[ci_idx]
        scale = 0.85

        steps = 8000
        prev = None
        for s in range(steps):
            t = s * 0.02
            x = (a1*math.sin(f1*t+p1)*math.exp(-d1*t) + a2*math.sin(f2*t+p2)*math.exp(-d2*t)) * scale
            y = (a3*math.sin(f3*t+p3)*math.exp(-d3*t) + a4*math.sin(f4*t+p4)*math.exp(-d4*t)) * scale
            px, py = cx + x, cy + y

            if prev:
                fade = math.exp(-d1 * t * 0.5)
                alpha = col.alpha * fade * 0.7
                if alpha > 0.01:
                    c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
                    c.setLineWidth(0.4 + fade * 0.8)
                    c.line(prev[0], prev[1], px, py)
            prev = (px, py)

    # Center pivot
    for rr in range(20, 0, -1):
        c.setFillColor(Color(0.85, 0.6, 0.3, alpha=0.03 * (1 - rr/20)))
        c.circle(cx, cy, rr, fill=1, stroke=0)
    c.setFillColor(Color(1, 0.85, 0.5, alpha=0.8))
    c.circle(cx, cy, 3, fill=1, stroke=0)

    scatter_stars(c, 150, (0.85, 0.6, 0.3), cx, cy, 0)

    title_block(c, "HARMONIC OSCILLATOR", "HARMONOGRAPH  ·  PENDULUM  ·  DECAY AND RESONANCE",
                "GEOMETRIA SACRED PATTERNS — 033",
                Color(0.9, 0.6, 0.3, alpha=0.85), Color(0.9, 0.7, 0.4, alpha=0.3), Color(0.9, 0.7, 0.4, alpha=0.12))
    c.save()
    print("  033 done")


# ═══════════════════════════════════════════════════════════
# 034 — REACTION-DIFFUSION (Organic Teal / Deep Sea)
# Turing patterns — spots and stripes of nature
# ═══════════════════════════════════════════════════════════
def gen_034():
    c = canvas.Canvas(f'{OUT}/034-reaction-diffusion.pdf', pagesize=A3)
    bg(c, Color(0.01, 0.04, 0.05))
    cx, cy = W/2, H/2 + 50

    # Simplified Gray-Scott model visualization
    # Pre-compute a pattern using reaction-diffusion
    random.seed(2025)
    res = 120
    # Initialize concentrations
    u = [[1.0]*res for _ in range(res)]
    v = [[0.0]*res for _ in range(res)]

    # Seed some spots
    for _ in range(15):
        sx, sy = random.randint(20, res-20), random.randint(20, res-20)
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if 0 <= sx+dx < res and 0 <= sy+dy < res:
                    u[sx+dx][sy+dy] = 0.5
                    v[sx+dx][sy+dy] = 0.25

    # Run simulation
    Du, Dv = 0.16, 0.08
    f, k = 0.035, 0.065
    dt = 1.0

    for _ in range(3000):
        nu = [[0.0]*res for _ in range(res)]
        nv = [[0.0]*res for _ in range(res)]
        for x in range(1, res-1):
            for y in range(1, res-1):
                lap_u = u[x+1][y] + u[x-1][y] + u[x][y+1] + u[x][y-1] - 4*u[x][y]
                lap_v = v[x+1][y] + v[x-1][y] + v[x][y+1] + v[x][y-1] - 4*v[x][y]
                uvv = u[x][y] * v[x][y] * v[x][y]
                nu[x][y] = u[x][y] + (Du * lap_u - uvv + f * (1 - u[x][y])) * dt
                nv[x][y] = v[x][y] + (Dv * lap_v + uvv - (f + k) * v[x][y]) * dt
                nu[x][y] = max(0, min(1, nu[x][y]))
                nv[x][y] = max(0, min(1, nv[x][y]))
        u, v = nu, nv

    # Render
    scale = min(500 / res, 700 / res)
    ox = cx - res * scale / 2
    oy = cy - res * scale / 2

    for x in range(res):
        for y in range(res):
            val = v[x][y]
            if val > 0.05:
                px = ox + x * scale
                py = oy + y * scale
                # Teal to bright cyan
                r_c = 0.0 + val * 0.3
                g_c = 0.4 + val * 0.5
                b_c = 0.5 + val * 0.4
                alpha = min(0.7, val * 1.5)
                c.setFillColor(Color(r_c, g_c, b_c, alpha=alpha))
                c.circle(px, py, scale * 0.55, fill=1, stroke=0)

    # Border
    c.setStrokeColor(Color(0, 0.7, 0.7, alpha=0.15))
    c.setLineWidth(0.8)
    c.rect(ox - 5, oy - 5, res*scale + 10, res*scale + 10, fill=0, stroke=1)

    scatter_stars(c, 150, (0.2, 0.7, 0.7), cx, cy, 0)

    title_block(c, "REACTION-DIFFUSION", "TURING PATTERNS  ·  MORPHOGENESIS  ·  GRAY-SCOTT MODEL",
                "GEOMETRIA SACRED PATTERNS — 034",
                Color(0, 0.85, 0.8, alpha=0.85), Color(0.2, 0.8, 0.8, alpha=0.3), Color(0.2, 0.8, 0.8, alpha=0.12))
    c.save()
    print("  034 done")


# ═══════════════════════════════════════════════════════════
# 035 — ASTRONOMICAL CLOCK (Burnished Gold / Midnight)
# Medieval astronomical instruments
# ═══════════════════════════════════════════════════════════
def gen_035():
    c = canvas.Canvas(f'{OUT}/035-astronomical-clock.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.02, 0.04))
    cx, cy = W/2, H/2 + 50

    golds = [
        Color(0.9, 0.75, 0.2, alpha=0.55),
        Color(1.0, 0.85, 0.3, alpha=0.45),
        Color(0.8, 0.6, 0.1, alpha=0.5),
        Color(1.0, 0.95, 0.6, alpha=0.3),
    ]

    # Outer ring with degree markings
    R = 300
    c.setStrokeColor(golds[0])
    c.setLineWidth(1.5)
    c.circle(cx, cy, R, fill=0, stroke=1)
    c.circle(cx, cy, R - 5, fill=0, stroke=1)

    # Degree ticks
    for i in range(360):
        a = math.radians(i)
        if i % 30 == 0:
            r1, r2 = R - 5, R - 25
            c.setStrokeColor(golds[1])
            c.setLineWidth(1.0)
        elif i % 10 == 0:
            r1, r2 = R - 5, R - 18
            c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=0.3))
            c.setLineWidth(0.6)
        elif i % 5 == 0:
            r1, r2 = R - 5, R - 12
            c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=0.15))
            c.setLineWidth(0.3)
        else:
            continue
        c.line(cx + r1*math.cos(a), cy + r1*math.sin(a),
               cx + r2*math.cos(a), cy + r2*math.sin(a))

    # Zodiac ring
    zodiac_r = R - 35
    c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=0.25))
    c.setLineWidth(0.5)
    c.circle(cx, cy, zodiac_r, fill=0, stroke=1)
    c.circle(cx, cy, zodiac_r - 30, fill=0, stroke=1)

    # Zodiac dividers and symbols
    zodiac = ["AR","TA","GE","CN","LE","VI","LI","SC","SG","CP","AQ","PI"]
    for i in range(12):
        a = i * math.pi / 6 - math.pi / 2
        c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=0.2))
        c.line(cx + (zodiac_r-30)*math.cos(a), cy + (zodiac_r-30)*math.sin(a),
               cx + zodiac_r*math.cos(a), cy + zodiac_r*math.sin(a))
        # Label
        mid_a = a + math.pi / 12
        lx = cx + (zodiac_r - 15) * math.cos(mid_a)
        ly = cy + (zodiac_r - 15) * math.sin(mid_a)
        c.setFillColor(Color(0.9, 0.8, 0.3, alpha=0.3))
        c.setFont("Courier", 6)
        c.drawCentredString(lx, ly - 2, zodiac[i])

    # Hour ring
    hour_r = zodiac_r - 45
    c.setStrokeColor(Color(0.8, 0.6, 0.1, alpha=0.3))
    c.setLineWidth(0.5)
    c.circle(cx, cy, hour_r, fill=0, stroke=1)

    # Roman numeral hours
    numerals = ["XII","I","II","III","IV","V","VI","VII","VIII","IX","X","XI"]
    for i in range(12):
        a = i * math.pi / 6 - math.pi / 2
        lx = cx + (hour_r - 15) * math.cos(a)
        ly = cy + (hour_r - 15) * math.sin(a)
        c.setFillColor(Color(1, 0.85, 0.3, alpha=0.5))
        c.setFont("Helvetica", 10)
        c.drawCentredString(lx, ly - 4, numerals[i])

    # Ecliptic circle (offset)
    ecl_offset = 40
    ecl_r = hour_r - 30
    c.setStrokeColor(Color(0.9, 0.4, 0.2, alpha=0.2))
    c.setLineWidth(0.8)
    c.circle(cx + ecl_offset * 0.3, cy + ecl_offset * 0.2, ecl_r, fill=0, stroke=1)

    # Inner astronomical rings
    for ri, rr in enumerate([150, 120, 90, 60]):
        alpha = 0.15 - ri * 0.03
        c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=alpha))
        c.setLineWidth(0.4)
        c.circle(cx, cy, rr, fill=0, stroke=1)

    # Clock hands
    hand_angles = [-math.pi/6, math.pi/3, -math.pi/2.5]
    hand_lengths = [hour_r - 25, 180, 120]
    hand_colors = [golds[0], Color(0.7, 0.5, 0.1, alpha=0.4), Color(0.5, 0.3, 0.08, alpha=0.3)]
    for a, l, col_h in zip(hand_angles, hand_lengths, hand_colors):
        c.setStrokeColor(col_h)
        c.setLineWidth(1.2)
        c.line(cx, cy, cx + l * math.cos(a), cy + l * math.sin(a))
        # Arrowhead
        c.setFillColor(col_h)
        c.circle(cx + l * math.cos(a), cy + l * math.sin(a), 3, fill=1, stroke=0)

    # Center boss
    c.setFillColor(Color(0.9, 0.75, 0.2, alpha=0.5))
    c.circle(cx, cy, 8, fill=1, stroke=0)
    c.setFillColor(Color(1, 0.95, 0.6, alpha=0.8))
    c.circle(cx, cy, 4, fill=1, stroke=0)

    # Decorative corner stars
    for sx, sy in [(100, H-100), (W-100, H-100), (100, 200), (W-100, 200)]:
        c.setStrokeColor(Color(0.9, 0.75, 0.2, alpha=0.1))
        c.setLineWidth(0.3)
        for i in range(8):
            a = i * math.pi / 4
            c.line(sx, sy, sx + 20*math.cos(a), sy + 20*math.sin(a))

    scatter_stars(c, 200, (0.9, 0.8, 0.4), cx, cy, R + 10)

    title_block(c, "ASTRONOMICAL CLOCK", "HOROLOGY  ·  ZODIAC  ·  CELESTIAL MECHANICS",
                "GEOMETRIA SACRED PATTERNS — 035",
                Color(0.95, 0.8, 0.25, alpha=0.85), Color(0.95, 0.85, 0.4, alpha=0.3), Color(0.95, 0.85, 0.4, alpha=0.12))
    c.save()
    print("  035 done")


# ═══════════════════════════════════════════════════════════
# 036 — SIERPINSKI TRIANGLE (Neon Green / Matrix)
# Recursive self-similarity — fractal dust
# ═══════════════════════════════════════════════════════════
def gen_036():
    c = canvas.Canvas(f'{OUT}/036-sierpinski-triangle.pdf', pagesize=A3)
    bg(c, Color(0.01, 0.03, 0.01))
    cx, cy = W/2, H/2 + 50

    neons = [
        Color(0.0, 1.0, 0.3, alpha=0.6),
        Color(0.2, 0.9, 0.1, alpha=0.5),
        Color(0.0, 0.7, 0.2, alpha=0.45),
        Color(0.4, 1.0, 0.5, alpha=0.35),
    ]

    R = 300

    def sierpinski(ax, ay, bx, by, ccx, ccy, depth, max_depth):
        if depth >= max_depth:
            # Draw the triangle
            col = neons[depth % len(neons)]
            fade = 0.3 + 0.7 * (depth / max_depth)
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
            c.setLineWidth(0.3 + 0.5 * (1 - depth / max_depth))
            p = c.beginPath()
            p.moveTo(ax, ay)
            p.lineTo(bx, by)
            p.lineTo(ccx, ccy)
            p.close()
            c.drawPath(p, fill=0, stroke=1)

            # Glow fill
            c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.02))
            c.drawPath(p, fill=1, stroke=0)
            return

        # Midpoints
        mab_x, mab_y = (ax+bx)/2, (ay+by)/2
        mbc_x, mbc_y = (bx+ccx)/2, (by+ccy)/2
        mca_x, mca_y = (ccx+ax)/2, (ccy+ay)/2

        sierpinski(ax, ay, mab_x, mab_y, mca_x, mca_y, depth+1, max_depth)
        sierpinski(mab_x, mab_y, bx, by, mbc_x, mbc_y, depth+1, max_depth)
        sierpinski(mca_x, mca_y, mbc_x, mbc_y, ccx, ccy, depth+1, max_depth)

    # Main triangle vertices
    ax = cx
    ay = cy + R * math.sin(math.pi/2)
    bx = cx - R * math.cos(math.pi/6)
    by = cy - R * math.sin(math.pi/6)
    ccx_v = cx + R * math.cos(math.pi/6)
    ccy_v = cy - R * math.sin(math.pi/6)

    # Outer triangle
    c.setStrokeColor(Color(0, 1, 0.3, alpha=0.2))
    c.setLineWidth(1.0)
    p = c.beginPath()
    p.moveTo(ax, ay)
    p.lineTo(bx, by)
    p.lineTo(ccx_v, ccy_v)
    p.close()
    c.drawPath(p, fill=0, stroke=1)

    # Generate Sierpinski (depth 7 = 3^7 = 2187 triangles)
    sierpinski(ax, ay, bx, by, ccx_v, ccy_v, 0, 7)

    # Chaos game dots overlay
    random.seed(42)
    verts = [(ax, ay), (bx, by), (ccx_v, ccy_v)]
    px, py = cx, cy
    for i in range(5000):
        target = random.choice(verts)
        px = (px + target[0]) / 2
        py = (py + target[1]) / 2
        if i > 10:  # Skip first few
            c.setFillColor(Color(0, 1, 0.3, alpha=0.12))
            c.circle(px, py, 0.8, fill=1, stroke=0)

    scatter_stars(c, 150, (0.2, 0.8, 0.3), cx, cy, R + 20)

    title_block(c, "SIERPINSKI TRIANGLE", "SELF-SIMILARITY  ·  FRACTAL DUST  ·  CHAOS GAME",
                "GEOMETRIA SACRED PATTERNS — 036",
                Color(0, 1, 0.3, alpha=0.85), Color(0.2, 0.9, 0.4, alpha=0.3), Color(0.2, 0.9, 0.4, alpha=0.12))
    c.save()
    print("  036 done")


# ═══════════════════════════════════════════════════════════
# 037 — STANDING WAVES (Warm Amber / Acoustic)
# Harmonic modes on a circular membrane
# ═══════════════════════════════════════════════════════════
def gen_037():
    c = canvas.Canvas(f'{OUT}/037-standing-waves.pdf', pagesize=A3)
    bg(c, Color(0.04, 0.03, 0.01))
    cx, cy = W/2, H/2 + 50

    ambers = [
        Color(1.0, 0.75, 0.2, alpha=0.5),
        Color(0.9, 0.6, 0.1, alpha=0.45),
        Color(1.0, 0.85, 0.4, alpha=0.4),
        Color(0.8, 0.5, 0.05, alpha=0.4),
    ]

    R = 250

    # Circular membrane modes: J_n(k*r) * cos(n*theta)
    # Simplified using sin/cos approximation of Bessel-like functions
    modes = [(0,1), (1,1), (2,1), (0,2), (1,2), (3,1)]
    positions = [
        (cx - 160, cy + 150), (cx + 160, cy + 150),
        (cx, cy),
        (cx - 160, cy - 150), (cx + 160, cy - 150),
        (cx, cy + 300),  # skip this, only 5 visible
    ]

    for mi, ((n, m), (px_c, py_c)) in enumerate(zip(modes[:5], positions[:5])):
        col = ambers[mi % len(ambers)]
        mr = 110  # mode radius

        # Draw circular boundary
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=0.3))
        c.setLineWidth(0.8)
        c.circle(px_c, py_c, mr, fill=0, stroke=1)

        # Sample the mode shape
        res = 80
        for ix in range(res):
            for iy in range(res):
                x = (ix / res - 0.5) * 2
                y = (iy / res - 0.5) * 2
                r = math.sqrt(x*x + y*y)
                if r > 0.95:
                    continue
                theta = math.atan2(y, x)

                # Approximate Bessel: sin(m*pi*r) for radial, cos(n*theta) for angular
                radial = math.sin(m * math.pi * r)
                angular = math.cos(n * theta)
                val = radial * angular

                if abs(val) > 0.1:
                    sx = px_c + x * mr
                    sy = py_c + y * mr
                    intensity = abs(val)
                    if val > 0:
                        c.setFillColor(Color(1, 0.8, 0.3, alpha=intensity * 0.4))
                    else:
                        c.setFillColor(Color(0.3, 0.5, 0.9, alpha=intensity * 0.3))
                    c.circle(sx, sy, 1.0 + intensity * 1.0, fill=1, stroke=0)

        # Mode label
        c.setFillColor(Color(1, 0.85, 0.4, alpha=0.3))
        c.setFont("Courier", 8)
        c.drawCentredString(px_c, py_c - mr - 12, f"({n},{m})")

    # Connecting lines
    c.setStrokeColor(Color(0.9, 0.7, 0.2, alpha=0.04))
    c.setLineWidth(0.3)
    for i in range(len(positions[:5])):
        for j in range(i+1, len(positions[:5])):
            c.line(positions[i][0], positions[i][1], positions[j][0], positions[j][1])

    scatter_stars(c, 150, (0.9, 0.7, 0.3), cx, cy, 0)

    title_block(c, "STANDING WAVES", "HARMONIC MODES  ·  RESONANCE  ·  CIRCULAR MEMBRANE",
                "GEOMETRIA SACRED PATTERNS — 037",
                Color(1, 0.8, 0.3, alpha=0.85), Color(1, 0.85, 0.45, alpha=0.3), Color(1, 0.85, 0.45, alpha=0.12))
    c.save()
    print("  037 done")


# ═══════════════════════════════════════════════════════════
# 038 — GALAXY SPIRAL (Cosmic Indigo / Starlight)
# Logarithmic spiral arms of a galaxy
# ═══════════════════════════════════════════════════════════
def gen_038():
    c = canvas.Canvas(f'{OUT}/038-galaxy-spiral.pdf', pagesize=A3)
    bg(c, Color(0.01, 0.01, 0.03))
    cx, cy = W/2, H/2 + 50

    random.seed(2024)

    # Central bulge
    for rr in range(80, 0, -1):
        t = rr / 80
        c.setFillColor(Color(1, 0.95, 0.7, alpha=0.03 * (1 - t)))
        c.ellipse(cx - rr * 1.2, cy - rr, cx + rr * 1.2, cy + rr, fill=1, stroke=0)

    # Bright core
    c.setFillColor(Color(1, 0.95, 0.8, alpha=0.8))
    c.circle(cx, cy, 5, fill=1, stroke=0)

    # Spiral arms (logarithmic spiral: r = a * e^(b*theta))
    n_arms = 4
    a_spiral = 5
    b_spiral = 0.18

    for arm in range(n_arms):
        base_angle = arm * 2 * math.pi / n_arms

        # Each arm has thousands of "stars"
        for _ in range(3000):
            t = random.random() * 12  # theta range
            r = a_spiral * math.exp(b_spiral * t)
            if r > 320:
                continue

            # Add some spread perpendicular to the arm
            spread = (10 + r * 0.15) * random.gauss(0, 0.4)
            angle = base_angle + t

            # Tilt for perspective (galaxy tilted ~30 degrees)
            x = r * math.cos(angle)
            y = r * math.sin(angle) * 0.5  # Perspective squash

            # Add spread
            perp_angle = angle + math.pi / 2
            x += spread * math.cos(perp_angle)
            y += spread * math.sin(perp_angle) * 0.5

            px = cx + x
            py = cy + y

            # Color: bluer in arms, redder between, white near center
            if r < 30:
                r_c, g_c, b_c = 1, 0.95, 0.8
            elif abs(spread) < 5:
                # Bright arm core: blue-white
                r_c = 0.6 + random.random() * 0.3
                g_c = 0.7 + random.random() * 0.3
                b_c = 0.9 + random.random() * 0.1
            else:
                # Arm edges: warmer
                r_c = 0.7 + random.random() * 0.3
                g_c = 0.5 + random.random() * 0.3
                b_c = 0.3 + random.random() * 0.3

            brightness = max(0.1, 1.0 - r / 350)
            alpha = brightness * (0.1 + random.random() * 0.3)
            sz = 0.3 + random.random() * 1.5 * brightness

            c.setFillColor(Color(r_c, g_c, b_c, alpha=alpha))
            c.circle(px, py, sz, fill=1, stroke=0)

    # Dust lanes (dark areas between arms)
    for arm in range(n_arms):
        base_angle = arm * 2 * math.pi / n_arms + math.pi / n_arms
        for _ in range(500):
            t = random.random() * 10
            r = a_spiral * math.exp(b_spiral * t)
            if r > 280:
                continue
            angle = base_angle + t
            x = r * math.cos(angle)
            y = r * math.sin(angle) * 0.5
            px, py = cx + x, cy + y
            c.setFillColor(Color(0.02, 0.01, 0.03, alpha=0.15))
            c.circle(px, py, 3 + random.random() * 4, fill=1, stroke=0)

    # Bright H-II regions (star forming)
    for arm in range(n_arms):
        base_angle = arm * 2 * math.pi / n_arms
        for _ in range(8):
            t = 3 + random.random() * 7
            r = a_spiral * math.exp(b_spiral * t)
            if r > 280:
                continue
            angle = base_angle + t + random.gauss(0, 0.1)
            x = r * math.cos(angle)
            y = r * math.sin(angle) * 0.5
            px, py = cx + x, cy + y
            # Pink nebula
            c.setFillColor(Color(1, 0.3, 0.5, alpha=0.08))
            c.circle(px, py, 8 + random.random() * 6, fill=1, stroke=0)
            c.setFillColor(Color(1, 0.5, 0.7, alpha=0.15))
            c.circle(px, py, 2, fill=1, stroke=0)

    scatter_stars(c, 300, (0.9, 0.9, 1), cx, cy, 0)

    title_block(c, "GALAXY SPIRAL", "LOGARITHMIC ARMS  ·  100 BILLION STARS  ·  COSMIC STRUCTURE",
                "GEOMETRIA SACRED PATTERNS — 038",
                Color(0.8, 0.85, 1, alpha=0.85), Color(0.8, 0.85, 1, alpha=0.3), Color(0.8, 0.85, 1, alpha=0.12))
    c.save()
    print("  038 done")


# ═══════════════════════════════════════════════════════════
# 039 — KOCH SNOWFLAKE (Arctic Blue / Frost White)
# Infinite perimeter, finite area
# ═══════════════════════════════════════════════════════════
def gen_039():
    c = canvas.Canvas(f'{OUT}/039-koch-snowflake.pdf', pagesize=A3)
    bg(c, Color(0.02, 0.03, 0.07))
    cx, cy = W/2, H/2 + 50

    frosts = [
        Color(0.6, 0.8, 1.0, alpha=0.5),
        Color(0.4, 0.65, 0.95, alpha=0.45),
        Color(0.8, 0.9, 1.0, alpha=0.4),
        Color(0.3, 0.55, 0.9, alpha=0.45),
    ]

    def koch_points(p1, p2, depth):
        if depth == 0:
            return [p1]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        a = (p1[0] + dx/3, p1[1] + dy/3)
        b = (p1[0] + 2*dx/3, p1[1] + 2*dy/3)
        # Peak of equilateral triangle
        mx = (a[0] + b[0]) / 2 - (b[1] - a[1]) * math.sqrt(3) / 2
        my = (a[1] + b[1]) / 2 + (b[0] - a[0]) * math.sqrt(3) / 2
        peak = (mx, my)
        pts = []
        pts.extend(koch_points(p1, a, depth - 1))
        pts.extend(koch_points(a, peak, depth - 1))
        pts.extend(koch_points(peak, b, depth - 1))
        pts.extend(koch_points(b, p2, depth - 1))
        return pts

    # Multiple Koch snowflakes at different depths and scales
    R = 260
    for depth in range(7, 0, -1):
        scale = R * (0.4 + depth * 0.085)
        # Initial equilateral triangle
        tri = []
        for i in range(3):
            a = -math.pi/2 + i * 2*math.pi/3
            tri.append((cx + scale * math.cos(a), cy + scale * math.sin(a)))

        all_pts = []
        for i in range(3):
            all_pts.extend(koch_points(tri[i], tri[(i+1)%3], depth))
        all_pts.append(all_pts[0])

        col = frosts[depth % len(frosts)]
        fade = 0.3 + 0.1 * depth
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=min(0.6, col.alpha * fade)))
        c.setLineWidth(0.2 + 0.15 * (7 - depth))

        p = c.beginPath()
        p.moveTo(*all_pts[0])
        for pt in all_pts[1:]:
            p.lineTo(*pt)
        c.drawPath(p, fill=0, stroke=1)

    # Central snowflake fill glow
    c.setFillColor(Color(0.6, 0.8, 1, alpha=0.03))
    c.circle(cx, cy, R * 0.4, fill=1, stroke=0)

    scatter_stars(c, 250, (0.7, 0.85, 1), cx, cy, R + 20)

    title_block(c, "KOCH SNOWFLAKE", "INFINITE PERIMETER  ·  FINITE AREA  ·  SELF-SIMILARITY",
                "GEOMETRIA SACRED PATTERNS — 039",
                Color(0.6, 0.8, 1, alpha=0.85), Color(0.7, 0.85, 1, alpha=0.3), Color(0.7, 0.85, 1, alpha=0.12))
    c.save()
    print("  039 done")


# ═══════════════════════════════════════════════════════════
# 040 — ELECTRIC CIRCUIT (Copper traces / PCB Green)
# Circuit board geometry
# ═══════════════════════════════════════════════════════════
def gen_040():
    c = canvas.Canvas(f'{OUT}/040-electric-circuit.pdf', pagesize=A3)
    bg(c, Color(0.01, 0.04, 0.02))
    cx, cy = W/2, H/2 + 50

    pcb = [
        Color(0.85, 0.55, 0.15, alpha=0.5),  # copper trace
        Color(0.0, 0.6, 0.3, alpha=0.3),      # pcb green
        Color(0.9, 0.7, 0.2, alpha=0.4),      # gold pad
        Color(0.5, 0.5, 0.55, alpha=0.35),    # solder
    ]

    random.seed(101)

    # Generate grid-based circuit traces
    grid = 30
    cols = int(W / grid)
    rows = int(H / grid)

    # Place component pads
    components = []
    for _ in range(40):
        gx = random.randint(3, cols - 3)
        gy = random.randint(6, rows - 4)
        pins = random.randint(2, 8)
        components.append((gx, gy, pins))

    # Draw traces between random component pairs
    c.setLineWidth(1.2)
    for _ in range(80):
        c1 = random.choice(components)
        c2 = random.choice(components)
        if c1 == c2:
            continue

        x1, y1 = c1[0] * grid, c1[1] * grid
        x2, y2 = c2[0] * grid, c2[1] * grid
        dist = math.hypot(x2 - x1, y2 - y1)
        dist_center = math.hypot((x1+x2)/2 - cx, (y1+y2)/2 - cy)
        fade = max(0.2, 1.0 - dist_center / 500)

        col = pcb[0]
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
        c.setLineWidth(0.8 + fade)

        # Manhattan routing (right-angle traces)
        mid_x = x2
        mid_y = y1
        if random.random() < 0.5:
            mid_x = x1
            mid_y = y2

        c.line(x1, y1, mid_x, mid_y)
        c.line(mid_x, mid_y, x2, y2)

    # Draw component pads
    for gx, gy, pins in components:
        x, y = gx * grid, gy * grid
        dist = math.hypot(x - cx, y - cy)
        fade = max(0.2, 1.0 - dist / 500)

        # IC package outline
        if pins > 4:
            pw = pins * 4
            ph = 12
            c.setStrokeColor(Color(0.5, 0.5, 0.55, alpha=0.2 * fade))
            c.setLineWidth(0.5)
            c.rect(x - pw/2, y - ph/2, pw, ph, fill=0, stroke=1)

        # Pads
        for p in range(pins):
            px = x - (pins - 1) * 4 / 2 + p * 4
            py = y
            # Pad
            c.setFillColor(Color(0.9, 0.7, 0.2, alpha=0.5 * fade))
            c.circle(px, py, 2, fill=1, stroke=0)
            # Annular ring
            c.setStrokeColor(Color(0.85, 0.55, 0.15, alpha=0.3 * fade))
            c.setLineWidth(0.5)
            c.circle(px, py, 3.5, fill=0, stroke=1)

    # Vias (through-hole connections)
    for _ in range(60):
        vx = random.randint(2, cols - 2) * grid
        vy = random.randint(5, rows - 3) * grid
        dist = math.hypot(vx - cx, vy - cy)
        fade = max(0.15, 1.0 - dist / 500)
        c.setFillColor(Color(0.85, 0.55, 0.15, alpha=0.3 * fade))
        c.circle(vx, vy, 1.5, fill=1, stroke=0)
        c.setStrokeColor(Color(0.85, 0.55, 0.15, alpha=0.15 * fade))
        c.circle(vx, vy, 3, fill=0, stroke=1)

    # Ground plane fill (subtle)
    c.setFillColor(Color(0, 0.3, 0.15, alpha=0.03))
    c.rect(60, 160, W - 120, H - 200, fill=1, stroke=0)

    # Board outline
    c.setStrokeColor(Color(0, 0.6, 0.3, alpha=0.2))
    c.setLineWidth(1.5)
    c.rect(60, 160, W - 120, H - 200, fill=0, stroke=1)

    scatter_stars(c, 100, (0.7, 0.5, 0.2), cx, cy, 0)

    title_block(c, "ELECTRIC CIRCUIT", "TRACES  ·  SILICON GEOMETRY  ·  DIGITAL PATHWAYS",
                "GEOMETRIA SACRED PATTERNS — 040",
                Color(0.85, 0.6, 0.2, alpha=0.85), Color(0.85, 0.65, 0.3, alpha=0.3), Color(0.85, 0.65, 0.3, alpha=0.12))
    c.save()
    print("  040 done")


# ═══════════════════════════════════════════════════════════
# 041 — INTERFERENCE MOIRÉ (Monochrome Silver/White)
# Overlapping grids create emergent patterns
# ═══════════════════════════════════════════════════════════
def gen_041():
    c = canvas.Canvas(f'{OUT}/041-moire-interference.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.03, 0.04))
    cx, cy = W/2, H/2 + 50

    # Two sets of concentric circles, slightly offset
    offsets = [
        (cx - 30, cy - 20),
        (cx + 30, cy + 20),
    ]
    max_r = 400
    spacing = 8

    for oi, (ox, oy) in enumerate(offsets):
        for r in range(spacing, int(max_r), spacing):
            dist_from_center = math.hypot(ox - cx, oy - cy)
            alpha = max(0.03, 0.2 * (1 - r / max_r))
            c.setStrokeColor(Color(0.8, 0.8, 0.85, alpha=alpha))
            c.setLineWidth(0.4)
            c.circle(ox, oy, r, fill=0, stroke=1)

    # Third set: radial lines from center
    for i in range(72):
        a = i * math.pi / 36
        c.setStrokeColor(Color(0.8, 0.8, 0.85, alpha=0.04))
        c.setLineWidth(0.3)
        c.line(cx, cy, cx + max_r * math.cos(a), cy + max_r * math.sin(a))

    # Parallel lines at slight angle (creates moiré with circles)
    line_spacing = 7
    angle = 0.03  # slight tilt
    for i in range(-50, 50):
        y_base = cy + i * line_spacing
        x1 = 50
        x2 = W - 50
        y1 = y_base + x1 * math.sin(angle)
        y2 = y_base + x2 * math.sin(angle)
        dist = abs(i * line_spacing)
        alpha = max(0.02, 0.08 * (1 - dist / 400))
        c.setStrokeColor(Color(0.85, 0.85, 0.9, alpha=alpha))
        c.setLineWidth(0.3)
        c.line(x1, y1, x2, y2)

    # Center highlight
    for rr in range(40, 0, -1):
        c.setFillColor(Color(0.9, 0.9, 1, alpha=0.015 * (1 - rr/40)))
        c.circle(cx, cy, rr, fill=1, stroke=0)

    scatter_stars(c, 100, (0.8, 0.8, 0.9), cx, cy, 0)

    title_block(c, "MOIRE INTERFERENCE", "OVERLAPPING GRIDS  ·  EMERGENT ORDER  ·  OPTICAL ILLUSION",
                "GEOMETRIA SACRED PATTERNS — 041",
                Color(0.85, 0.85, 0.95, alpha=0.85), Color(0.8, 0.8, 0.9, alpha=0.3), Color(0.8, 0.8, 0.9, alpha=0.12))
    c.save()
    print("  041 done")


# ═══════════════════════════════════════════════════════════
# 042 — NAUTILUS SHELL (Pearl / Warm Cream / Ocean Blue)
# Golden ratio in nature — chamber proportions
# ═══════════════════════════════════════════════════════════
def gen_042():
    c = canvas.Canvas(f'{OUT}/042-nautilus-shell.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.03, 0.05))
    cx, cy = W/2 + 50, H/2 + 50

    pearls = [
        Color(0.95, 0.88, 0.75, alpha=0.5),
        Color(0.85, 0.78, 0.65, alpha=0.45),
        Color(0.75, 0.85, 0.95, alpha=0.4),
        Color(1.0, 0.95, 0.85, alpha=0.35),
    ]

    phi = (1 + math.sqrt(5)) / 2

    # Main logarithmic spiral
    c.setLineWidth(1.5)
    steps = 1500
    prev = None
    for s in range(steps):
        t = s / steps * 6 * math.pi
        r = 6 * phi ** (t * 2 / (2 * math.pi))
        if r > 300:
            break
        x = cx + r * math.cos(t)
        y = cy + r * math.sin(t)

        if prev:
            # Color varies with angle
            t_norm = (t % (2*math.pi)) / (2*math.pi)
            col = pearls[int(t_norm * 4) % len(pearls)]
            alpha = col.alpha * (0.5 + 0.5 * (r / 300))
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
            c.setLineWidth(0.8 + r / 200)
            c.line(prev[0], prev[1], x, y)
        prev = (x, y)

    # Chamber walls (radial lines from center at golden angle intervals)
    golden_angle = 2 * math.pi / (phi * phi)
    for i in range(20):
        a = i * golden_angle
        r_start = 6 * phi ** (a * 2 / (2 * math.pi))
        # Find the next whorl
        r_end = 6 * phi ** ((a + 2*math.pi) * 2 / (2 * math.pi))
        if r_end > 300:
            r_end = 300

        x1 = cx + r_start * math.cos(a)
        y1 = cy + r_start * math.sin(a)
        x2 = cx + r_end * math.cos(a)
        y2 = cy + r_end * math.sin(a)

        alpha = max(0.05, 0.2 * (1 - r_start / 300))
        c.setStrokeColor(Color(0.9, 0.85, 0.7, alpha=alpha))
        c.setLineWidth(0.4)
        c.line(x1, y1, x2, y2)

    # Inner detail spirals (echo)
    for offset in [0.3, -0.3]:
        c.setLineWidth(0.3)
        prev = None
        for s in range(steps):
            t = s / steps * 6 * math.pi
            r = 6 * phi ** (t * 2 / (2 * math.pi)) + offset * 20
            if r > 280 or r < 5:
                prev = None
                continue
            x = cx + r * math.cos(t + offset * 0.05)
            y = cy + r * math.sin(t + offset * 0.05)
            if prev:
                c.setStrokeColor(Color(0.85, 0.8, 0.7, alpha=0.1))
                c.line(prev[0], prev[1], x, y)
            prev = (x, y)

    # Golden rectangles overlay
    c.setStrokeColor(Color(0.75, 0.85, 0.95, alpha=0.08))
    c.setLineWidth(0.5)
    r_rect = 8
    rot = 0
    for _ in range(10):
        x1 = cx + r_rect * math.cos(rot)
        y1 = cy + r_rect * math.sin(rot)
        r_rect *= phi
        rot += math.pi / 2
        x2 = cx + r_rect * math.cos(rot)
        y2 = cy + r_rect * math.sin(rot)
        c.line(x1, y1, x2, y2)

    scatter_stars(c, 200, (0.85, 0.8, 0.7), cx, cy, 300)

    title_block(c, "NAUTILUS SHELL", "GOLDEN SPIRAL  ·  NATURE'S PROPORTION  ·  PHI IN BIOLOGY",
                "GEOMETRIA SACRED PATTERNS — 042",
                Color(0.95, 0.88, 0.75, alpha=0.85), Color(0.9, 0.85, 0.75, alpha=0.3), Color(0.9, 0.85, 0.75, alpha=0.12))
    c.save()
    print("  042 done")


# ═══════════════════════════════════════════════════════════
# 043 — SACRED LOTUS (Deep Magenta / Spiritual Gold)
# Layered petals with mathematical precision
# ═══════════════════════════════════════════════════════════
def gen_043():
    c = canvas.Canvas(f'{OUT}/043-sacred-lotus.pdf', pagesize=A3)
    bg(c, Color(0.04, 0.01, 0.03))
    cx, cy = W/2, H/2 + 50

    lotus = [
        Color(0.9, 0.2, 0.5, alpha=0.4),
        Color(1.0, 0.4, 0.6, alpha=0.35),
        Color(0.95, 0.3, 0.55, alpha=0.4),
        Color(1.0, 0.6, 0.7, alpha=0.3),
        Color(0.85, 0.7, 0.2, alpha=0.35),
    ]

    # Multiple rings of petals, each ring with more petals
    rings = [
        (6, 40, 80, 0),       # (num_petals, inner_r, outer_r, rotation)
        (8, 70, 130, 0.2),
        (12, 110, 190, 0.1),
        (16, 160, 250, 0.15),
        (20, 220, 310, 0.05),
    ]

    for ri, (n_petals, r_inner, r_outer, rot) in enumerate(rings):
        col = lotus[ri % len(lotus)]

        for i in range(n_petals):
            a = rot + i * 2 * math.pi / n_petals

            # Petal shape: bezier curves
            # Petal base
            bx = cx + r_inner * math.cos(a)
            by = cy + r_inner * math.sin(a)
            # Petal tip
            tx = cx + r_outer * math.cos(a)
            ty = cy + r_outer * math.sin(a)

            # Control points for curved petal edges
            petal_width = (r_outer - r_inner) * 0.35
            perp = a + math.pi / 2
            mid_r = (r_inner + r_outer) / 2

            # Left edge
            cl1x = cx + mid_r * math.cos(a) + petal_width * math.cos(perp)
            cl1y = cy + mid_r * math.sin(a) + petal_width * math.sin(perp)
            # Right edge
            cr1x = cx + mid_r * math.cos(a) - petal_width * math.cos(perp)
            cr1y = cy + mid_r * math.sin(a) - petal_width * math.sin(perp)

            fade = 1.0 - ri * 0.12

            # Petal outline
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
            c.setLineWidth(0.6)
            p = c.beginPath()
            p.moveTo(bx, by)
            p.curveTo(cl1x, cl1y, cl1x + (tx-bx)*0.2, cl1y + (ty-by)*0.2, tx, ty)
            c.drawPath(p, fill=0, stroke=1)
            p = c.beginPath()
            p.moveTo(bx, by)
            p.curveTo(cr1x, cr1y, cr1x + (tx-bx)*0.2, cr1y + (ty-by)*0.2, tx, ty)
            c.drawPath(p, fill=0, stroke=1)

            # Petal center vein
            c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade * 0.3))
            c.setLineWidth(0.3)
            c.line(bx, by, tx, ty)

            # Tip dot
            c.setFillColor(Color(col.red, col.green, col.blue, alpha=fade * 0.4))
            c.circle(tx, ty, 1.5, fill=1, stroke=0)

    # Center: golden seed pod
    for rr in range(35, 0, -1):
        t = rr / 35
        c.setFillColor(Color(0.85, 0.7, 0.15, alpha=0.03 * (1 - t)))
        c.circle(cx, cy, rr, fill=1, stroke=0)

    # Seed dots in Fibonacci pattern
    golden_angle = math.pi * (3 - math.sqrt(5))  # ~137.5 degrees
    for i in range(100):
        r = 2.5 * math.sqrt(i)
        if r > 30:
            break
        a = i * golden_angle
        sx = cx + r * math.cos(a)
        sy = cy + r * math.sin(a)
        c.setFillColor(Color(0.9, 0.8, 0.3, alpha=0.5))
        c.circle(sx, sy, 1.2, fill=1, stroke=0)

    # Outer halo
    c.setStrokeColor(Color(0.9, 0.3, 0.5, alpha=0.08))
    c.setLineWidth(0.5)
    c.circle(cx, cy, 340, fill=0, stroke=1)

    scatter_stars(c, 200, (0.9, 0.5, 0.6), cx, cy, 340)

    title_block(c, "SACRED LOTUS", "PADMA  ·  ENLIGHTENMENT  ·  FIBONACCI PHYLLOTAXIS",
                "GEOMETRIA SACRED PATTERNS — 043",
                Color(0.95, 0.35, 0.55, alpha=0.85), Color(0.95, 0.5, 0.65, alpha=0.3), Color(0.95, 0.5, 0.65, alpha=0.12))
    c.save()
    print("  043 done")


# ═══════════════════════════════════════════════════════════
# 044 — ROSSLER ATTRACTOR (Deep Jade / Turquoise)
# Another strange attractor — simpler chaos
# ═══════════════════════════════════════════════════════════
def gen_044():
    c = canvas.Canvas(f'{OUT}/044-rossler-attractor.pdf', pagesize=A3)
    bg(c, Color(0.01, 0.04, 0.04))
    cx, cy = W/2, H/2 + 50

    jades = [
        Color(0.1, 0.7, 0.6, alpha=0.45),
        Color(0.2, 0.85, 0.75, alpha=0.4),
        Color(0.0, 0.6, 0.5, alpha=0.4),
        Color(0.3, 0.9, 0.8, alpha=0.3),
    ]

    # Rössler attractor: dx/dt = -y-z, dy/dt = x+ay, dz/dt = b+z(x-c)
    a_r, b_r, c_r = 0.2, 0.2, 5.7
    dt = 0.01
    x, y, z = 1.0, 1.0, 1.0
    points = []

    for _ in range(40000):
        dx = -y - z
        dy = x + a_r * y
        dz = b_r + z * (x - c_r)
        x += dx * dt
        y += dy * dt
        z += dz * dt
        points.append((x, y, z))

    # Project x-y plane
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_range = x_max - x_min
    y_range = y_max - y_min

    scale = min(500 / x_range, 600 / y_range) * 0.8
    ox = cx - (x_max + x_min) / 2 * scale
    oy = cy - (y_max + y_min) / 2 * scale

    for i in range(len(points) - 1):
        px1 = ox + points[i][0] * scale
        py1 = oy + points[i][1] * scale
        px2 = ox + points[i+1][0] * scale
        py2 = oy + points[i+1][1] * scale

        z_val = points[i][2]
        z_min = min(p[2] for p in points)
        z_max = max(p[2] for p in points)
        z_norm = (z_val - z_min) / (z_max - z_min)

        col_idx = int(z_norm * 3.99)
        col = jades[col_idx]
        alpha = 0.05 + 0.25 * (1 - z_norm * 0.5)
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
        c.setLineWidth(0.3 + 0.5 * (1 - z_norm))
        c.line(px1, py1, px2, py2)

    scatter_stars(c, 200, (0.2, 0.8, 0.7), cx, cy, 0)

    title_block(c, "ROSSLER ATTRACTOR", "FOLDED CHAOS  ·  STRANGE LOOP  ·  DETERMINISTIC DISORDER",
                "GEOMETRIA SACRED PATTERNS — 044",
                Color(0.15, 0.8, 0.7, alpha=0.85), Color(0.2, 0.85, 0.75, alpha=0.3), Color(0.2, 0.85, 0.75, alpha=0.12))
    c.save()
    print("  044 done")


# ═══════════════════════════════════════════════════════════
# 045 — TREE OF LIFE (Kabbalistic) (Royal Purple / Gold / White)
# Sephiroth and paths of the Kabbalah
# ═══════════════════════════════════════════════════════════
def gen_045():
    c = canvas.Canvas(f'{OUT}/045-tree-of-life.pdf', pagesize=A3)
    bg(c, Color(0.03, 0.02, 0.05))
    cx, cy = W/2, H/2 + 20

    royals = [
        Color(0.5, 0.2, 0.9, alpha=0.55),
        Color(0.9, 0.75, 0.2, alpha=0.5),
        Color(0.8, 0.8, 1.0, alpha=0.45),
        Color(0.3, 0.4, 0.9, alpha=0.4),
    ]

    # 10 Sephiroth positions (traditional Tree of Life layout)
    # Arranged in 3 pillars
    spread_x = 120
    spread_y = 85
    sephiroth = [
        (cx, cy + 4 * spread_y, "Kether", 0),         # 1 Crown
        (cx - spread_x, cy + 3 * spread_y, "Chokmah", 1),  # 2 Wisdom
        (cx + spread_x, cy + 3 * spread_y, "Binah", 2),    # 3 Understanding
        (cx - spread_x, cy + 1.5 * spread_y, "Chesed", 3),  # 4 Mercy
        (cx + spread_x, cy + 1.5 * spread_y, "Geburah", 0), # 5 Severity
        (cx, cy + 0.5 * spread_y, "Tiphareth", 1),    # 6 Beauty
        (cx - spread_x, cy - spread_y, "Netzach", 2),  # 7 Victory
        (cx + spread_x, cy - spread_y, "Hod", 3),      # 8 Splendor
        (cx, cy - 2 * spread_y, "Yesod", 0),           # 9 Foundation
        (cx, cy - 3.5 * spread_y, "Malkuth", 1),       # 10 Kingdom
    ]

    # 22 Paths connecting sephiroth (traditional assignments)
    paths = [
        (0,1),(0,2),(0,5),
        (1,2),(1,3),(1,5),
        (2,4),(2,5),
        (3,4),(3,5),(3,6),
        (4,5),(4,7),
        (5,6),(5,7),(5,8),
        (6,7),(6,8),
        (7,8),
        (8,9),
        (3,6),(4,7),  # extra cross paths
    ]

    # Draw paths
    c.setLineWidth(0.8)
    for i, j in paths:
        if i >= len(sephiroth) or j >= len(sephiroth):
            continue
        sx1, sy1 = sephiroth[i][0], sephiroth[i][1]
        sx2, sy2 = sephiroth[j][0], sephiroth[j][1]
        dist = math.hypot(sx2-sx1, sy2-sy1)

        col = royals[(i+j) % len(royals)]
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.4))
        c.line(sx1, sy1, sx2, sy2)

    # Draw three pillars (subtle vertical lines)
    c.setStrokeColor(Color(0.5, 0.3, 0.8, alpha=0.05))
    c.setLineWidth(0.5)
    for px in [cx - spread_x, cx, cx + spread_x]:
        c.line(px, cy - 4 * spread_y, px, cy + 5 * spread_y)

    # Draw Sephiroth (spheres)
    for idx, (sx, sy, name, col_idx) in enumerate(sephiroth):
        col = royals[col_idx]
        node_r = 28

        # Outer glow
        for rr in range(int(node_r * 2.5), 0, -2):
            alpha = 0.01 * (1 - rr / (node_r * 2.5))
            c.setFillColor(Color(col.red, col.green, col.blue, alpha=alpha))
            c.circle(sx, sy, rr, fill=1, stroke=0)

        # Circle
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha))
        c.setLineWidth(1.0)
        c.circle(sx, sy, node_r, fill=0, stroke=1)

        # Inner circle
        c.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.4))
        c.setLineWidth(0.5)
        c.circle(sx, sy, node_r * 0.6, fill=0, stroke=1)

        # Center fill
        c.setFillColor(Color(col.red, col.green, col.blue, alpha=0.06))
        c.circle(sx, sy, node_r, fill=1, stroke=0)

        # Bright center
        c.setFillColor(Color(1, 0.95, 0.9, alpha=0.7))
        c.circle(sx, sy, 3, fill=1, stroke=0)

        # Name label
        c.setFillColor(Color(1, 1, 1, alpha=0.3))
        c.setFont("Helvetica", 7)
        c.drawCentredString(sx, sy - node_r - 10, name.upper())

        # Number
        c.setFillColor(Color(1, 1, 1, alpha=0.15))
        c.setFont("Courier", 6)
        c.drawCentredString(sx, sy - 3, str(idx + 1))

    # Da'at (hidden sephirah) — dashed circle
    daat_y = cy + 2.2 * spread_y
    c.setStrokeColor(Color(0.7, 0.7, 1, alpha=0.12))
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    c.circle(cx, daat_y, 20, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(Color(0.7, 0.7, 1, alpha=0.15))
    c.setFont("Helvetica", 6)
    c.drawCentredString(cx, daat_y - 28, "DA'AT")

    # Outer boundary: three interlocking circles (pillars)
    c.setStrokeColor(Color(0.5, 0.3, 0.8, alpha=0.06))
    c.setLineWidth(0.5)
    for px in [cx - spread_x, cx, cx + spread_x]:
        c.ellipse(px - 60, cy - 4*spread_y, px + 60, cy + 5*spread_y, fill=0, stroke=1)

    scatter_stars(c, 250, (0.6, 0.4, 0.9), cx, cy, 0)

    title_block(c, "TREE OF LIFE", "KABBALAH  ·  TEN SEPHIROTH  ·  TWENTY-TWO PATHS",
                "GEOMETRIA SACRED PATTERNS — 045",
                Color(0.6, 0.3, 0.95, alpha=0.85), Color(0.7, 0.5, 1, alpha=0.3), Color(0.7, 0.5, 1, alpha=0.12))
    c.save()
    print("  045 done")


# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating GEOMETRIA SACRED PATTERNS 031–045...")
    gen_031()
    gen_032()
    gen_033()
    gen_034()
    gen_035()
    gen_036()
    gen_037()
    gen_038()
    gen_039()
    gen_040()
    gen_041()
    gen_042()
    gen_043()
    gen_044()
    gen_045()
    print("\nAll 15 PDFs (031–045) generated!")
