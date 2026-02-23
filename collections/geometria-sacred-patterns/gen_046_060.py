#!/usr/bin/env python3
"""GEOMETRIA SACRED PATTERNS — Generative Series 046–060"""

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
# 046 — BLACK HOLE (Vantablack / Accretion Orange-Red)
# Gravitational lensing and accretion disk
# ═══════════════════════════════════════════════════════════
def gen_046():
    cv = canvas.Canvas(f'{OUT}/046-black-hole.pdf', pagesize=A3)
    bg(cv, Color(0.005, 0.005, 0.01))
    cx, cy = W/2, H/2 + 50

    random.seed(314)

    # Event horizon — true black
    cv.setFillColor(Color(0, 0, 0, alpha=1))
    cv.circle(cx, cy, 50, fill=1, stroke=0)

    # Photon sphere glow
    for rr in range(70, 50, -1):
        t = (rr - 50) / 20
        cv.setFillColor(Color(1, 0.6, 0.1, alpha=0.04 * (1 - t)))
        cv.circle(cx, cy, rr, fill=1, stroke=0)

    # Accretion disk — tilted ellipse with Doppler shift
    disk_a = 280  # semi-major
    disk_b = 60   # semi-minor (tilt)

    for layer in range(800):
        t = random.random() * 2 * math.pi
        # Radial position in disk
        r_disk = 80 + random.random() * 200
        spread = random.gauss(0, 8)

        x = r_disk * math.cos(t)
        y = r_disk * math.sin(t) * 0.22 + spread  # perspective squash

        px = cx + x
        py = cy + y

        # Skip if inside event horizon
        if math.hypot(px - cx, py - cy) < 52:
            continue

        # Doppler: approaching side (left) is blue-shifted, receding is red-shifted
        doppler = math.cos(t)  # -1 to 1
        dist_norm = (r_disk - 80) / 200

        if doppler > 0:  # approaching — brighter, bluer
            r_c = 0.9 + 0.1 * (1 - dist_norm)
            g_c = 0.5 + 0.3 * doppler
            b_c = 0.2 + 0.5 * doppler
        else:  # receding — redder, dimmer
            r_c = 0.9
            g_c = 0.3 + 0.2 * (1 + doppler)
            b_c = 0.05

        brightness = (1 - dist_norm * 0.6) * (0.7 + 0.3 * abs(doppler))
        alpha = brightness * 0.25
        sz = 1.0 + brightness * 2.0

        cv.setFillColor(Color(min(1,r_c), min(1,g_c), min(1,b_c), alpha=alpha))
        cv.circle(px, py, sz, fill=1, stroke=0)

    # Gravitational lensing ring (Einstein ring)
    cv.setLineWidth(0.6)
    for dr in range(-3, 4):
        r = 55 + dr * 2
        alpha = 0.08 * (1 - abs(dr) / 4)
        cv.setStrokeColor(Color(1, 0.7, 0.3, alpha=alpha))
        cv.circle(cx, cy, r, fill=0, stroke=1)

    # Lensed background stars (distorted arcs near the hole)
    for _ in range(60):
        angle = random.random() * 2 * math.pi
        dist = 55 + random.random() * 30
        arc_len = random.random() * 0.4 + 0.1
        cv.setStrokeColor(Color(0.8, 0.85, 1, alpha=random.random() * 0.15 + 0.05))
        cv.setLineWidth(0.3 + random.random() * 0.5)
        p = cv.beginPath()
        for s in range(20):
            a = angle + (s / 20 - 0.5) * arc_len
            rx = cx + dist * math.cos(a)
            ry = cy + dist * math.sin(a)
            if s == 0:
                p.moveTo(rx, ry)
            else:
                p.lineTo(rx, ry)
        cv.drawPath(p, fill=0, stroke=1)

    # Relativistic jets (faint)
    for jet_dir in [1, -1]:
        cv.setLineWidth(0.3)
        for i in range(80):
            spread = random.gauss(0, 3 + i * 0.3)
            length = 50 + i * 4
            alpha = max(0.01, 0.15 * (1 - i / 80))
            cv.setStrokeColor(Color(0.4, 0.5, 1, alpha=alpha))
            jx = cx + spread
            jy = cy + jet_dir * length
            jx2 = cx + random.gauss(0, 2 + i * 0.2)
            jy2 = cy + jet_dir * (length + 4)
            cv.line(jx, jy, jx2, jy2)

    # Re-draw event horizon on top (hides anything that bled in)
    cv.setFillColor(Color(0, 0, 0, alpha=1))
    cv.circle(cx, cy, 50, fill=1, stroke=0)

    scatter_stars(cv, 400, (0.9, 0.9, 1), cx, cy, 60)

    title_block(cv, "BLACK HOLE", "EVENT HORIZON  ·  ACCRETION DISK  ·  SPACETIME SINGULARITY",
                "GEOMETRIA SACRED PATTERNS — 046",
                Color(1, 0.6, 0.2, alpha=0.85), Color(1, 0.7, 0.4, alpha=0.3), Color(1, 0.7, 0.4, alpha=0.12))
    cv.save()
    print("  046 done")


# ═══════════════════════════════════════════════════════════
# 047 — DRAGON CURVE (Blood Red / Obsidian)
# Space-filling fractal from simple folding rules
# ═══════════════════════════════════════════════════════════
def gen_047():
    cv = canvas.Canvas(f'{OUT}/047-dragon-curve.pdf', pagesize=A3)
    bg(cv, Color(0.04, 0.01, 0.01))
    cx, cy = W/2, H/2 + 50

    # Generate dragon curve via L-system
    # Axiom: F, Rules: F -> F+G, G -> F-G
    # + = turn left 90, - = turn right 90
    iterations = 16
    sequence = [1]  # 1 = forward, True = left turn, False = right turn
    turns = []
    for _ in range(iterations):
        new_turns = []
        for t in turns:
            new_turns.append(t)
        new_turns.append(True)  # left turn
        for t in reversed(turns):
            new_turns.append(not t)
        turns = new_turns

    # Walk the curve
    step = 2.5
    x, y = cx - 100, cy - 50
    dx, dy = step, 0  # start facing right
    points = [(x, y)]

    for turn in turns:
        x += dx
        y += dy
        points.append((x, y))
        if turn:  # left
            dx, dy = -dy, dx
        else:  # right
            dx, dy = dy, -dx

    # Center the points
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    off_x = cx - (min_x + max_x) / 2
    off_y = cy - (min_y + max_y) / 2
    # Scale to fit
    range_x = max_x - min_x
    range_y = max_y - min_y
    scale = min(550 / max(range_x, 1), 700 / max(range_y, 1))
    points = [(cx + (p[0] - (min_x+max_x)/2) * scale,
               cy + (p[1] - (min_y+max_y)/2) * scale) for p in points]

    # Draw
    total = len(points)
    for i in range(total - 1):
        t = i / total
        # Gradient: deep red → bright crimson → orange at tips
        r_c = 0.5 + t * 0.5
        g_c = 0.05 + t * 0.25
        b_c = 0.02 + t * 0.08
        alpha = 0.2 + 0.4 * (0.5 + 0.5 * math.sin(t * math.pi * 8))
        cv.setStrokeColor(Color(min(1, r_c), g_c, b_c, alpha=alpha))
        cv.setLineWidth(0.4 + 0.3 * (1 - t))
        cv.line(points[i][0], points[i][1], points[i+1][0], points[i+1][1])

    scatter_stars(cv, 150, (0.8, 0.2, 0.15), cx, cy, 0)

    title_block(cv, "DRAGON CURVE", "PAPER FOLDING  ·  SPACE-FILLING  ·  SELF-AVOIDING FRACTAL",
                "GEOMETRIA SACRED PATTERNS — 047",
                Color(0.9, 0.2, 0.1, alpha=0.85), Color(0.9, 0.35, 0.2, alpha=0.3), Color(0.9, 0.35, 0.2, alpha=0.12))
    cv.save()
    print("  047 done")


# ═══════════════════════════════════════════════════════════
# 048 — HILBERT CURVE (Synth Wave Cyan / Magenta gradient)
# Space-filling continuous fractal
# ═══════════════════════════════════════════════════════════
def gen_048():
    cv = canvas.Canvas(f'{OUT}/048-hilbert-curve.pdf', pagesize=A3)
    bg(cv, Color(0.02, 0.01, 0.04))
    cx, cy = W/2, H/2 + 50

    def hilbert(order, x, y, ax, ay, bx, by, points):
        w = abs(ax + ay)
        h = abs(bx + by)
        dax = 1 if ax > 0 else (-1 if ax < 0 else 0)
        day = 1 if ay > 0 else (-1 if ay < 0 else 0)
        dbx = 1 if bx > 0 else (-1 if bx < 0 else 0)
        dby = 1 if by > 0 else (-1 if by < 0 else 0)

        if h == 1 and w == 1:
            points.append((x + (dax + dbx) / 2, y + (day + dby) / 2))
            return

        ax2, ay2 = ax // 2, ay // 2
        bx2, by2 = bx // 2, by // 2
        w2 = abs(ax2 + ay2)
        h2 = abs(bx2 + by2)

        if 2 * w > 3 * h:
            if (ax2 & 1) and (w2 > 2):
                ax2 += dax
                ay2 += day
            hilbert(order, x, y, ax2, ay2, bx, by, points)
            hilbert(order, x + ax2, y + ay2, ax - ax2, ay - ay2, bx, by, points)
        else:
            if (by2 & 1) and (h2 > 2):
                bx2 += dbx
                by2 += dby
            hilbert(order, x, y, bx2, by2, ax2, ay2, points)
            hilbert(order, x + bx2, y + by2, ax, ay, bx - bx2, by - by2, points)
            hilbert(order, x + (ax - dax) + (bx2 - dbx), y + (ay - day) + (by2 - dby),
                    -bx2, -by2, -(ax - ax2), -(ay - ay2), points)

    n = 64  # 2^6 grid
    points = []
    hilbert(6, 0, 0, n, 0, 0, n, points)

    # Scale and center
    scale = 550 / n
    ox = cx - n * scale / 2
    oy = cy - n * scale / 2

    total = len(points)
    for i in range(total - 1):
        t = i / total
        # Synthwave gradient: cyan → magenta → back
        r_c = 0.2 + 0.8 * abs(math.sin(t * math.pi))
        g_c = 0.1 + 0.3 * (1 - abs(math.sin(t * math.pi)))
        b_c = 0.5 + 0.5 * abs(math.cos(t * math.pi))
        alpha = 0.3 + 0.3 * (0.5 + 0.5 * math.sin(t * 20))

        px1 = ox + points[i][0] * scale
        py1 = oy + points[i][1] * scale
        px2 = ox + points[i+1][0] * scale
        py2 = oy + points[i+1][1] * scale

        cv.setStrokeColor(Color(r_c, g_c, b_c, alpha=alpha))
        cv.setLineWidth(0.8)
        cv.line(px1, py1, px2, py2)

    scatter_stars(cv, 100, (0.5, 0.3, 0.8), cx, cy, 0)

    title_block(cv, "HILBERT CURVE", "SPACE-FILLING  ·  ORDER 6  ·  CONTINUOUS MAPPING",
                "GEOMETRIA SACRED PATTERNS — 048",
                Color(0.6, 0.2, 0.9, alpha=0.85), Color(0.6, 0.35, 0.9, alpha=0.3), Color(0.6, 0.35, 0.9, alpha=0.12))
    cv.save()
    print("  048 done")


# ═══════════════════════════════════════════════════════════
# 049 — APOLLONIAN GASKET (Pearl White / Champagne)
# Circle packing — infinite nested tangent circles
# ═══════════════════════════════════════════════════════════
def gen_049():
    cv = canvas.Canvas(f'{OUT}/049-apollonian-gasket.pdf', pagesize=A3)
    bg(cv, Color(0.03, 0.03, 0.04))
    cx, cy = W/2, H/2 + 50

    champagnes = [
        Color(0.95, 0.9, 0.75, alpha=0.5),
        Color(0.85, 0.8, 0.65, alpha=0.45),
        Color(0.75, 0.7, 0.55, alpha=0.4),
        Color(1.0, 0.95, 0.85, alpha=0.35),
    ]

    R = 270
    circles = []  # (cx, cy, r)

    # Start: 3 mutually tangent circles inside the outer circle
    # Descartes circle theorem for initial configuration
    r_inner = R / (1 + 2 / math.sqrt(3))
    for i in range(3):
        a = i * 2 * math.pi / 3 - math.pi / 2
        icx = cx + (R - r_inner) * math.cos(a)
        icy = cy + (R - r_inner) * math.sin(a)
        circles.append((icx, icy, r_inner))

    # Recursive packing: find gaps and fill them
    def find_soddy_circle(c1, c2, c3, outer=False):
        """Find 4th tangent circle using Descartes theorem."""
        k1, k2, k3 = 1/c1[2], 1/c2[2], 1/c3[2]
        if outer:
            k4 = k1 + k2 + k3 - 2 * math.sqrt(k1*k2 + k2*k3 + k3*k1)
        else:
            k4 = k1 + k2 + k3 + 2 * math.sqrt(abs(k1*k2 + k2*k3 + k3*k1))

        if abs(k4) < 0.001 or k4 < 0:
            return None
        r4 = 1 / k4
        if r4 < 2 or r4 > R:
            return None

        # Position using complex Descartes theorem
        z1 = complex(c1[0], c1[1]) * k1
        z2 = complex(c2[0], c2[1]) * k2
        z3 = complex(c3[0], c3[1]) * k3

        z_sum = z1 + z2 + z3
        z_prod_sum = z1*z2 + z2*z3 + z3*z1
        discriminant = z_prod_sum
        if abs(discriminant) > 0:
            sqrt_d = (2 * discriminant ** 0.5)
        else:
            return None

        z4_a = (z_sum + sqrt_d) / k4
        z4_b = (z_sum - sqrt_d) / k4

        # Choose the one that doesn't overlap existing circles too much
        for z4 in [z4_a, z4_b]:
            ncx, ncy = z4.real, z4.imag
            # Check if inside outer boundary
            if math.hypot(ncx - cx, ncy - cy) + r4 <= R + 5:
                # Check no major overlap with existing
                valid = True
                for ec in circles:
                    d = math.hypot(ncx - ec[0], ncy - ec[1])
                    if d < abs(r4 - ec[2]) - 2:
                        valid = False
                        break
                if valid:
                    return (ncx, ncy, r4)
        return None

    # Fill iteratively
    to_process = [(0, 1, 2)]
    for iteration in range(6):
        new_process = []
        for i, j, k in to_process:
            if i >= len(circles) or j >= len(circles) or k >= len(circles):
                continue
            result = find_soddy_circle(circles[i], circles[j], circles[k])
            if result:
                new_idx = len(circles)
                circles.append(result)
                new_process.append((i, j, new_idx))
                new_process.append((i, k, new_idx))
                new_process.append((j, k, new_idx))
        to_process = new_process

    # Draw outer circle
    cv.setStrokeColor(Color(0.95, 0.9, 0.75, alpha=0.4))
    cv.setLineWidth(1.5)
    cv.circle(cx, cy, R, fill=0, stroke=1)

    # Draw all packed circles
    for idx, (ccx, ccy, cr) in enumerate(circles):
        if cr < 1:
            continue
        col = champagnes[idx % len(champagnes)]
        fade = min(1, cr / 30)  # smaller = fainter
        cv.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * fade))
        cv.setLineWidth(0.3 + fade * 0.8)
        cv.circle(ccx, ccy, cr, fill=0, stroke=1)
        # Subtle fill
        cv.setFillColor(Color(col.red, col.green, col.blue, alpha=0.01 * fade))
        cv.circle(ccx, ccy, cr, fill=1, stroke=0)
        # Center dot for bigger circles
        if cr > 15:
            cv.setFillColor(Color(1, 0.95, 0.8, alpha=0.3))
            cv.circle(ccx, ccy, 1.5, fill=1, stroke=0)

    scatter_stars(cv, 200, (0.9, 0.85, 0.7), cx, cy, R + 10)

    title_block(cv, "APOLLONIAN GASKET", "TANGENT CIRCLES  ·  DESCARTES THEOREM  ·  FRACTAL PACKING",
                "GEOMETRIA SACRED PATTERNS — 049",
                Color(0.95, 0.9, 0.75, alpha=0.85), Color(0.9, 0.85, 0.7, alpha=0.3), Color(0.9, 0.85, 0.7, alpha=0.12))
    cv.save()
    print("  049 done")


# ═══════════════════════════════════════════════════════════
# 050 — SOUND WAVEFORM (Warm Vinyl / Analog)
# Fourier harmonics composing a complex wave
# ═══════════════════════════════════════════════════════════
def gen_050():
    cv = canvas.Canvas(f'{OUT}/050-sound-waveform.pdf', pagesize=A3)
    bg(cv, Color(0.04, 0.03, 0.02))
    cx, cy = W/2, H/2 + 50

    vinyls = [
        Color(0.9, 0.6, 0.2, alpha=0.5),
        Color(0.8, 0.5, 0.15, alpha=0.45),
        Color(1.0, 0.75, 0.3, alpha=0.4),
        Color(0.7, 0.4, 0.1, alpha=0.45),
        Color(0.95, 0.85, 0.5, alpha=0.35),
    ]

    margin = 80
    wave_w = W - 2 * margin
    wave_h = 120

    # Draw individual harmonics stacked vertically
    harmonics = [
        (1, 1.0, "Fundamental"),
        (2, 0.5, "2nd Harmonic"),
        (3, 0.33, "3rd Harmonic"),
        (5, 0.2, "5th Harmonic"),
        (8, 0.125, "8th Harmonic"),
    ]

    y_positions = [cy + 280, cy + 150, cy + 20, cy - 110, cy - 240]

    for hi, ((freq, amp, label), yp) in enumerate(zip(harmonics, y_positions)):
        col = vinyls[hi % len(vinyls)]

        # Axis line
        cv.setStrokeColor(Color(0.5, 0.4, 0.3, alpha=0.08))
        cv.setLineWidth(0.3)
        cv.line(margin, yp, margin + wave_w, yp)

        # Wave
        cv.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha))
        cv.setLineWidth(1.0)
        p = cv.beginPath()
        for s in range(500):
            t = s / 500
            x = margin + t * wave_w
            y = yp + amp * wave_h * math.sin(freq * 2 * math.pi * t * 3)
            # Add subtle noise for analog feel
            y += random.gauss(0, 0.3)
            if s == 0:
                p.moveTo(x, y)
            else:
                p.lineTo(x, y)
        cv.drawPath(p, fill=0, stroke=1)

        # Fill area under curve (subtle)
        cv.setFillColor(Color(col.red, col.green, col.blue, alpha=0.02))
        p = cv.beginPath()
        p.moveTo(margin, yp)
        for s in range(500):
            t = s / 500
            x = margin + t * wave_w
            y = yp + amp * wave_h * math.sin(freq * 2 * math.pi * t * 3)
            p.lineTo(x, y)
        p.lineTo(margin + wave_w, yp)
        p.close()
        cv.drawPath(p, fill=1, stroke=0)

        # Label
        cv.setFillColor(Color(col.red, col.green, col.blue, alpha=0.35))
        cv.setFont("Courier", 7)
        cv.drawString(margin, yp + wave_h * amp + 10, label)

    # Composite waveform — draw at the very bottom as overlay
    # Sum of all harmonics
    cv.setStrokeColor(Color(1, 0.85, 0.4, alpha=0.12))
    cv.setLineWidth(0.5)
    for yp in y_positions:
        cv.setStrokeColor(Color(1, 0.85, 0.4, alpha=0.03))
        cv.line(margin, yp, margin + wave_w, yp)

    # Connecting lines between harmonics (showing composition)
    for s in range(0, 500, 25):
        t = s / 500
        x = margin + t * wave_w
        for hi in range(len(y_positions) - 1):
            freq1, amp1, _ = harmonics[hi]
            freq2, amp2, _ = harmonics[hi + 1]
            y1 = y_positions[hi] + amp1 * wave_h * math.sin(freq1 * 2 * math.pi * t * 3)
            y2 = y_positions[hi + 1] + amp2 * wave_h * math.sin(freq2 * 2 * math.pi * t * 3)
            cv.setStrokeColor(Color(0.9, 0.7, 0.3, alpha=0.03))
            cv.setLineWidth(0.2)
            cv.line(x, y1, x, y2)

    scatter_stars(cv, 100, (0.8, 0.6, 0.3), cx, cy, 0)

    title_block(cv, "SOUND WAVEFORM", "FOURIER HARMONICS  ·  SYNTHESIS  ·  ANALOG VIBRATION",
                "GEOMETRIA SACRED PATTERNS — 050",
                Color(0.95, 0.7, 0.25, alpha=0.85), Color(0.9, 0.75, 0.35, alpha=0.3), Color(0.9, 0.75, 0.35, alpha=0.12))
    cv.save()
    print("  050 done")


# ═══════════════════════════════════════════════════════════
# 051 — FERROFLUID (Liquid Metal / Magnetic Chrome)
# Spiky magnetic fluid sculpture
# ═══════════════════════════════════════════════════════════
def gen_051():
    cv = canvas.Canvas(f'{OUT}/051-ferrofluid.pdf', pagesize=A3)
    bg(cv, Color(0.02, 0.02, 0.03))
    cx, cy = W/2, H/2 + 50

    chromes = [
        Color(0.7, 0.72, 0.75, alpha=0.5),
        Color(0.5, 0.52, 0.58, alpha=0.45),
        Color(0.85, 0.87, 0.9, alpha=0.4),
        Color(0.3, 0.32, 0.4, alpha=0.5),
    ]

    random.seed(2025)

    # Central blob with spikes
    n_spikes = 24
    base_r = 80

    # Generate spike profile
    spikes = []
    for i in range(n_spikes):
        angle = i * 2 * math.pi / n_spikes
        height = 60 + random.random() * 180
        width = 0.08 + random.random() * 0.06
        spikes.append((angle, height, width))

    # Draw multiple layers for depth
    for layer in range(12, -1, -1):
        layer_scale = 1.0 - layer * 0.03
        layer_offset = layer * 2

        # Blob outline with spikes
        points = []
        detail = 500
        for s in range(detail + 1):
            a = s / detail * 2 * math.pi

            # Base radius
            r = base_r * layer_scale

            # Add spike contributions
            for spike_a, spike_h, spike_w in spikes:
                da = a - spike_a
                # Wrap angle
                while da > math.pi: da -= 2 * math.pi
                while da < -math.pi: da += 2 * math.pi
                # Gaussian spike shape
                contrib = spike_h * layer_scale * math.exp(-da*da / (2 * spike_w * spike_w))
                r += contrib

            px = cx + r * math.cos(a)
            py = cy + r * math.sin(a) + layer_offset

            points.append((px, py))

        # Draw this layer
        col = chromes[layer % len(chromes)]
        alpha = 0.15 + 0.04 * (12 - layer)

        # Outline
        cv.setStrokeColor(Color(col.red, col.green, col.blue, alpha=alpha))
        cv.setLineWidth(0.5 + (12 - layer) * 0.08)
        p = cv.beginPath()
        p.moveTo(*points[0])
        for pt in points[1:]:
            p.lineTo(*pt)
        cv.drawPath(p, fill=0, stroke=1)

    # Highlights on spike tips
    for spike_a, spike_h, spike_w in spikes:
        r = base_r + spike_h
        tip_x = cx + r * math.cos(spike_a)
        tip_y = cy + r * math.sin(spike_a)
        # Bright tip
        cv.setFillColor(Color(0.9, 0.92, 0.95, alpha=0.4))
        cv.circle(tip_x, tip_y, 2, fill=1, stroke=0)
        # Glow
        cv.setFillColor(Color(0.8, 0.82, 0.88, alpha=0.05))
        cv.circle(tip_x, tip_y, 10, fill=1, stroke=0)

    # Reflective surface underneath
    cv.setFillColor(Color(0.4, 0.42, 0.5, alpha=0.03))
    cv.ellipse(cx - 200, cy - 15, cx + 200, cy + 15, fill=1, stroke=0)

    # Magnetic field lines (subtle)
    cv.setLineWidth(0.2)
    for i in range(18):
        a = i * math.pi / 9
        for r_line in range(50, 350, 30):
            x1 = cx + r_line * math.cos(a)
            y1 = cy + r_line * math.sin(a)
            x2 = cx + (r_line + 20) * math.cos(a + 0.03)
            y2 = cy + (r_line + 20) * math.sin(a + 0.03)
            alpha = max(0.01, 0.04 * (1 - r_line / 350))
            cv.setStrokeColor(Color(0.6, 0.6, 0.7, alpha=alpha))
            cv.line(x1, y1, x2, y2)

    scatter_stars(cv, 150, (0.7, 0.7, 0.8), cx, cy, 0)

    title_block(cv, "FERROFLUID", "MAGNETIC SCULPTURE  ·  LIQUID METAL  ·  SURFACE TENSION",
                "GEOMETRIA SACRED PATTERNS — 051",
                Color(0.8, 0.82, 0.88, alpha=0.85), Color(0.75, 0.77, 0.83, alpha=0.3), Color(0.75, 0.77, 0.83, alpha=0.12))
    cv.save()
    print("  051 done")


# ═══════════════════════════════════════════════════════════
# 052 — QUANTUM ORBITALS (Atomic Blue / Probability Cloud)
# Hydrogen electron probability densities
# ═══════════════════════════════════════════════════════════
def gen_052():
    cv = canvas.Canvas(f'{OUT}/052-quantum-orbitals.pdf', pagesize=A3)
    bg(cv, Color(0.01, 0.02, 0.04))
    cx, cy = W/2, H/2 + 50

    quantums = [
        Color(0.2, 0.5, 1.0, alpha=0.4),
        Color(0.4, 0.7, 1.0, alpha=0.35),
        Color(0.1, 0.35, 0.9, alpha=0.4),
        Color(0.6, 0.8, 1.0, alpha=0.3),
    ]

    # Display orbitals: 1s, 2p, 3d, 4f (simplified probability clouds)
    orbitals = [
        ("1s", 0, 0, cx - 160, cy + 170),
        ("2p", 1, 0, cx + 160, cy + 170),
        ("3d", 2, 0, cx - 160, cy - 120),
        ("4f", 3, 0, cx + 160, cy - 120),
    ]

    random.seed(42)

    for name, l, m, ocx, ocy in orbitals:
        R_vis = 120

        # Generate probability cloud with Monte Carlo sampling
        n_points = 3000
        for _ in range(n_points):
            # Spherical coordinates
            r = random.random() * R_vis
            theta = random.random() * math.pi
            phi_a = random.random() * 2 * math.pi

            # Simplified radial probability (hydrogen-like)
            n = l + 1
            radial = (r / (R_vis * 0.3)) ** l * math.exp(-r / (R_vis * 0.3 * n))

            # Angular probability (spherical harmonics simplified)
            if l == 0:  # s orbital: spherical
                angular = 1.0
            elif l == 1:  # p orbital: dumbbell
                angular = abs(math.cos(theta))
            elif l == 2:  # d orbital: clover
                angular = abs(3 * math.cos(theta)**2 - 1) * 0.5 + abs(math.sin(theta)**2 * math.cos(2 * phi_a)) * 0.5
            else:  # f orbital: complex
                angular = abs(math.sin(theta) * (5 * math.cos(theta)**2 - 1)) * 0.5 + \
                          abs(math.sin(theta)**3 * math.cos(3 * phi_a)) * 0.3

            prob = radial * angular
            if random.random() > prob * 3:
                continue

            # Project 3D to 2D
            x = r * math.sin(theta) * math.cos(phi_a)
            y = r * math.cos(theta)

            px = ocx + x
            py = ocy + y
            col = quantums[l % len(quantums)]
            alpha = min(0.5, prob * 2)
            cv.setFillColor(Color(col.red, col.green, col.blue, alpha=alpha))
            cv.circle(px, py, 0.8 + prob * 2, fill=1, stroke=0)

        # Nucleus
        cv.setFillColor(Color(1, 0.9, 0.5, alpha=0.8))
        cv.circle(ocx, ocy, 3, fill=1, stroke=0)
        cv.setFillColor(Color(1, 0.9, 0.5, alpha=0.1))
        cv.circle(ocx, ocy, 10, fill=1, stroke=0)

        # Label
        cv.setFillColor(Color(0.5, 0.7, 1, alpha=0.4))
        cv.setFont("Helvetica", 12)
        cv.drawCentredString(ocx, ocy - R_vis - 15, name)

        # Boundary circle
        cv.setStrokeColor(Color(0.3, 0.5, 0.9, alpha=0.08))
        cv.setLineWidth(0.3)
        cv.circle(ocx, ocy, R_vis, fill=0, stroke=1)

    # Connection lines
    cv.setStrokeColor(Color(0.3, 0.5, 0.9, alpha=0.03))
    cv.setLineWidth(0.3)
    for o1 in orbitals:
        for o2 in orbitals:
            if o1 != o2:
                cv.line(o1[3], o1[4], o2[3], o2[4])

    scatter_stars(cv, 200, (0.3, 0.5, 1), cx, cy, 0)

    title_block(cv, "QUANTUM ORBITALS", "PROBABILITY CLOUDS  ·  s p d f  ·  WAVE FUNCTION",
                "GEOMETRIA SACRED PATTERNS — 052",
                Color(0.3, 0.6, 1, alpha=0.85), Color(0.4, 0.65, 1, alpha=0.3), Color(0.4, 0.65, 1, alpha=0.12))
    cv.save()
    print("  052 done")


# ═══════════════════════════════════════════════════════════
# 053 — TOPOGRAPHIC MAP (Earth Tones / Contour Lines)
# Elevation contours of an alien landscape
# ═══════════════════════════════════════════════════════════
def gen_053():
    cv = canvas.Canvas(f'{OUT}/053-topographic-map.pdf', pagesize=A3)
    bg(cv, Color(0.03, 0.04, 0.03))
    cx, cy = W/2, H/2 + 50

    earths = [
        Color(0.35, 0.55, 0.25, alpha=0.45),  # forest
        Color(0.55, 0.45, 0.25, alpha=0.4),    # earth
        Color(0.7, 0.6, 0.35, alpha=0.35),     # sand
        Color(0.4, 0.5, 0.3, alpha=0.4),       # moss
        Color(0.6, 0.5, 0.3, alpha=0.35),      # clay
    ]

    random.seed(99)

    # Generate terrain with multiple sine wave peaks
    peaks = [(random.random()*W, random.random()*(H-200)+150, random.random()*80+30, random.random()*0.01+0.005) for _ in range(8)]

    def terrain_height(x, y):
        h = 0
        for px, py, amp, freq in peaks:
            d = math.hypot(x - px, y - py)
            h += amp * math.exp(-d * freq)
        # Add noise
        h += 10 * math.sin(x * 0.03) * math.cos(y * 0.025)
        h += 5 * math.sin(x * 0.07 + y * 0.05)
        return h

    # Trace contour lines using marching squares (simplified)
    res = 200
    grid_w = W - 80
    grid_h = H - 220
    ox_g = 40
    oy_g = 160
    cell_w = grid_w / res
    cell_h = grid_h / res

    # Compute height grid
    heights = [[terrain_height(ox_g + x * cell_w, oy_g + y * cell_h) for x in range(res+1)] for y in range(res+1)]

    # Find min/max
    all_h = [h for row in heights for h in row]
    h_min, h_max = min(all_h), max(all_h)

    # Draw contour lines at regular intervals
    n_contours = 20
    for ci in range(n_contours):
        level = h_min + (h_max - h_min) * (ci + 0.5) / n_contours
        col = earths[ci % len(earths)]
        t = ci / n_contours
        cv.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * (0.5 + t * 0.5)))
        cv.setLineWidth(0.3 + t * 0.5)

        # Simple contour tracing: check each cell for level crossing
        for y in range(res):
            for x in range(res):
                h00 = heights[y][x]
                h10 = heights[y][x+1]
                h01 = heights[y+1][x]
                h11 = heights[y+1][x+1]

                above = [(h00 >= level), (h10 >= level), (h01 >= level), (h11 >= level)]
                n_above = sum(above)

                if n_above == 0 or n_above == 4:
                    continue

                # Find interpolated crossing points on edges
                crossings = []
                # Top edge
                if above[0] != above[1]:
                    t_val = (level - h00) / (h10 - h00) if h10 != h00 else 0.5
                    crossings.append((ox_g + (x + t_val) * cell_w, oy_g + y * cell_h))
                # Bottom edge
                if above[2] != above[3]:
                    t_val = (level - h01) / (h11 - h01) if h11 != h01 else 0.5
                    crossings.append((ox_g + (x + t_val) * cell_w, oy_g + (y+1) * cell_h))
                # Left edge
                if above[0] != above[2]:
                    t_val = (level - h00) / (h01 - h00) if h01 != h00 else 0.5
                    crossings.append((ox_g + x * cell_w, oy_g + (y + t_val) * cell_h))
                # Right edge
                if above[1] != above[3]:
                    t_val = (level - h10) / (h11 - h10) if h11 != h10 else 0.5
                    crossings.append((ox_g + (x+1) * cell_w, oy_g + (y + t_val) * cell_h))

                if len(crossings) >= 2:
                    cv.line(crossings[0][0], crossings[0][1], crossings[1][0], crossings[1][1])

    # Peak markers
    for px, py, amp, _ in peaks:
        if amp > 50:
            cv.setStrokeColor(Color(0.7, 0.6, 0.35, alpha=0.3))
            cv.setLineWidth(0.3)
            # Cross mark
            cv.line(px - 5, py, px + 5, py)
            cv.line(px, py - 5, px, py + 5)
            cv.setFont("Courier", 5)
            cv.setFillColor(Color(0.7, 0.6, 0.35, alpha=0.25))
            cv.drawString(px + 7, py - 2, f"{amp:.0f}m")

    # Border
    cv.setStrokeColor(Color(0.5, 0.45, 0.3, alpha=0.15))
    cv.setLineWidth(0.8)
    cv.rect(ox_g, oy_g, grid_w, grid_h, fill=0, stroke=1)

    scatter_stars(cv, 80, (0.5, 0.5, 0.35), cx, cy, 0)

    title_block(cv, "TOPOGRAPHIC MAP", "CONTOUR LINES  ·  ELEVATION  ·  TERRAIN MATHEMATICS",
                "GEOMETRIA SACRED PATTERNS — 053",
                Color(0.55, 0.5, 0.3, alpha=0.85), Color(0.6, 0.55, 0.35, alpha=0.3), Color(0.6, 0.55, 0.35, alpha=0.12))
    cv.save()
    print("  053 done")


# ═══════════════════════════════════════════════════════════
# 054 — DIFFRACTION PATTERN (Laser Red / Deep Black)
# Airy disk — light through a circular aperture
# ═══════════════════════════════════════════════════════════
def gen_054():
    cv = canvas.Canvas(f'{OUT}/054-diffraction-pattern.pdf', pagesize=A3)
    bg(cv, Color(0.01, 0.01, 0.01))
    cx, cy = W/2, H/2 + 50

    # Airy pattern: I(r) = [2*J1(x)/x]^2 where x = pi*r*D/(lambda*L)
    # Approximate J1 with series
    def bessel_j1(x):
        if abs(x) < 1e-10:
            return 0.5
        s = 0
        for k in range(20):
            sign = (-1)**k
            s += sign * (x/2)**(2*k+1) / (math.factorial(k) * math.factorial(k+1))
        return s

    R = 300
    res = 300

    for ix in range(res):
        for iy in range(res):
            x = (ix / res - 0.5) * 2
            y = (iy / res - 0.5) * 2
            r = math.sqrt(x*x + y*y)

            if r > 0.98:
                continue

            # Scale r to get nice ring pattern
            x_bessel = r * 25

            if abs(x_bessel) < 1e-10:
                intensity = 1.0
            else:
                j1 = bessel_j1(x_bessel)
                airy = (2 * j1 / x_bessel) ** 2
                intensity = airy

            if intensity < 0.005:
                continue

            px = cx + x * R
            py = cy + y * R

            # Color: monochromatic red laser
            alpha = min(0.8, intensity * 1.5)
            sz = 0.8 + intensity * 2.5

            # Central disk is bright white-red, rings are dimmer red
            if r < 0.15:
                r_c = min(1, 0.8 + intensity * 0.2)
                g_c = min(1, 0.3 + intensity * 0.7)
                b_c = min(1, 0.2 + intensity * 0.5)
            else:
                r_c = min(1, 0.9 * intensity + 0.1)
                g_c = min(0.3, 0.15 * intensity)
                b_c = min(0.1, 0.05 * intensity)

            cv.setFillColor(Color(r_c, g_c, b_c, alpha=alpha))
            cv.circle(px, py, sz, fill=1, stroke=0)

    # Aperture ring
    cv.setStrokeColor(Color(0.5, 0.1, 0.1, alpha=0.1))
    cv.setLineWidth(0.5)
    cv.circle(cx, cy, R, fill=0, stroke=1)

    scatter_stars(cv, 80, (0.6, 0.15, 0.1), cx, cy, R + 10)

    title_block(cv, "DIFFRACTION PATTERN", "AIRY DISK  ·  CIRCULAR APERTURE  ·  WAVE OPTICS",
                "GEOMETRIA SACRED PATTERNS — 054",
                Color(0.9, 0.2, 0.15, alpha=0.85), Color(0.85, 0.3, 0.2, alpha=0.3), Color(0.85, 0.3, 0.2, alpha=0.12))
    cv.save()
    print("  054 done")


# ═══════════════════════════════════════════════════════════
# 055 — GRAVITY WELL (Spacetime Blue / Grid Warp)
# Rubber sheet analogy of curved spacetime
# ═══════════════════════════════════════════════════════════
def gen_055():
    cv = canvas.Canvas(f'{OUT}/055-gravity-well.pdf', pagesize=A3)
    bg(cv, Color(0.01, 0.01, 0.03))
    cx, cy = W/2, H/2 + 30

    # Mass positions (gravity sources)
    masses = [
        (cx, cy, 150),          # main mass
        (cx + 180, cy - 80, 40),  # smaller companion
    ]

    # Draw warped grid
    grid_extent = 380
    grid_lines = 30
    perspective_tilt = 0.35

    def warp(x, y):
        """Warp grid point based on gravity wells."""
        dz = 0
        for mx, my, m_strength in masses:
            d = math.hypot(x - mx, y - my) + 10
            dz -= m_strength * 100 / d
        # Convert z-displacement to visual y-displacement (perspective)
        return x, y + dz * perspective_tilt

    # Horizontal grid lines
    cv.setLineWidth(0.4)
    for i in range(grid_lines + 1):
        t = i / grid_lines
        y_base = cy - grid_extent + t * 2 * grid_extent

        prev = None
        for s in range(200):
            x = cx - grid_extent + s / 200 * 2 * grid_extent
            wx, wy = warp(x, y_base)
            dist = min(math.hypot(x - m[0], y_base - m[1]) for m in masses)
            alpha = max(0.04, min(0.35, 0.2 * (dist / 100)))

            # Color shifts near mass (bluer = more warped)
            warp_amount = abs(wy - y_base) / 80
            r_c = 0.15 + 0.15 * (1 - min(1, warp_amount))
            g_c = 0.25 + 0.2 * (1 - min(1, warp_amount))
            b_c = 0.5 + 0.4 * min(1, warp_amount)

            cv.setStrokeColor(Color(r_c, g_c, b_c, alpha=alpha))
            if prev:
                cv.line(prev[0], prev[1], wx, wy)
            prev = (wx, wy)

    # Vertical grid lines
    for i in range(grid_lines + 1):
        t = i / grid_lines
        x_base = cx - grid_extent + t * 2 * grid_extent

        prev = None
        for s in range(200):
            y = cy - grid_extent + s / 200 * 2 * grid_extent
            wx, wy = warp(x_base, y)
            dist = min(math.hypot(x_base - m[0], y - m[1]) for m in masses)
            alpha = max(0.04, min(0.35, 0.2 * (dist / 100)))

            warp_amount = abs(wy - y) / 80
            r_c = 0.15 + 0.15 * (1 - min(1, warp_amount))
            g_c = 0.25 + 0.2 * (1 - min(1, warp_amount))
            b_c = 0.5 + 0.4 * min(1, warp_amount)

            cv.setStrokeColor(Color(r_c, g_c, b_c, alpha=alpha))
            if prev:
                cv.line(prev[0], prev[1], wx, wy)
            prev = (wx, wy)

    # Mass markers
    for mx, my, m_str in masses:
        _, wmy = warp(mx, my)
        # Glow
        for rr in range(int(m_str * 0.3), 0, -1):
            cv.setFillColor(Color(0.3, 0.5, 1, alpha=0.02 * (1 - rr / (m_str * 0.3))))
            cv.circle(mx, wmy, rr, fill=1, stroke=0)
        cv.setFillColor(Color(0.6, 0.8, 1, alpha=0.8))
        sz = 3 + m_str * 0.03
        cv.circle(mx, wmy, sz, fill=1, stroke=0)

    scatter_stars(cv, 300, (0.5, 0.6, 1), cx, cy, 0)

    title_block(cv, "GRAVITY WELL", "CURVED SPACETIME  ·  GENERAL RELATIVITY  ·  GEODESICS",
                "GEOMETRIA SACRED PATTERNS — 055",
                Color(0.4, 0.6, 1, alpha=0.85), Color(0.5, 0.65, 1, alpha=0.3), Color(0.5, 0.65, 1, alpha=0.12))
    cv.save()
    print("  055 done")


# ═══════════════════════════════════════════════════════════
# 056 — PHYLLOTAXIS (Sunflower Gold / Living Green)
# Fibonacci spiral arrangement in nature
# ═══════════════════════════════════════════════════════════
def gen_056():
    cv = canvas.Canvas(f'{OUT}/056-phyllotaxis.pdf', pagesize=A3)
    bg(cv, Color(0.02, 0.03, 0.02))
    cx, cy = W/2, H/2 + 50

    golden_angle = math.pi * (3 - math.sqrt(5))  # ~137.508 degrees
    n_seeds = 1500
    max_r = 310

    for i in range(n_seeds):
        r = math.sqrt(i) * (max_r / math.sqrt(n_seeds))
        theta = i * golden_angle

        px = cx + r * math.cos(theta)
        py = cy + r * math.sin(theta)

        # Size decreases toward center
        t = r / max_r
        sz = 1.0 + t * 5.0

        # Color: center is dark brown (seeds), middle is golden, outer is green
        if t < 0.3:
            r_c = 0.4 + t * 0.5
            g_c = 0.25 + t * 0.3
            b_c = 0.1
            alpha = 0.4 + t * 0.3
        elif t < 0.7:
            t2 = (t - 0.3) / 0.4
            r_c = 0.9 - t2 * 0.3
            g_c = 0.7 + t2 * 0.1
            b_c = 0.1 + t2 * 0.05
            alpha = 0.5
        else:
            t2 = (t - 0.7) / 0.3
            r_c = 0.3 - t2 * 0.1
            g_c = 0.6 + t2 * 0.2
            b_c = 0.15 + t2 * 0.1
            alpha = 0.5 - t2 * 0.15

        cv.setFillColor(Color(r_c, g_c, b_c, alpha=alpha))
        cv.circle(px, py, sz, fill=1, stroke=0)

        # Outline for larger seeds
        if sz > 2:
            cv.setStrokeColor(Color(r_c * 0.7, g_c * 0.7, b_c * 0.7, alpha=alpha * 0.5))
            cv.setLineWidth(0.3)
            cv.circle(px, py, sz, fill=0, stroke=1)

    # Fibonacci spirals overlay (visible pattern)
    for fib_n in [8, 13, 21, 34]:
        cv.setStrokeColor(Color(1, 0.85, 0.2, alpha=0.06))
        cv.setLineWidth(0.3)
        for arm in range(fib_n):
            p = cv.beginPath()
            started = False
            for i in range(n_seeds):
                if i % fib_n != arm:
                    continue
                r = math.sqrt(i) * (max_r / math.sqrt(n_seeds))
                theta = i * golden_angle
                px = cx + r * math.cos(theta)
                py = cy + r * math.sin(theta)
                if not started:
                    p.moveTo(px, py)
                    started = True
                else:
                    p.lineTo(px, py)
            cv.drawPath(p, fill=0, stroke=1)

    # Border
    cv.setStrokeColor(Color(0.4, 0.6, 0.2, alpha=0.12))
    cv.setLineWidth(0.8)
    cv.circle(cx, cy, max_r + 10, fill=0, stroke=1)

    scatter_stars(cv, 100, (0.5, 0.7, 0.3), cx, cy, max_r + 15)

    title_block(cv, "PHYLLOTAXIS", "FIBONACCI SPIRALS  ·  GOLDEN ANGLE  ·  137.508\u00b0",
                "GEOMETRIA SACRED PATTERNS — 056",
                Color(0.85, 0.7, 0.15, alpha=0.85), Color(0.8, 0.7, 0.3, alpha=0.3), Color(0.8, 0.7, 0.3, alpha=0.12))
    cv.save()
    print("  056 done")


# ═══════════════════════════════════════════════════════════
# 057 — INTERFERENCE RINGS (Thin-Film Iridescent)
# Newton's rings — rainbow thin-film interference
# ═══════════════════════════════════════════════════════════
def gen_057():
    cv = canvas.Canvas(f'{OUT}/057-interference-rings.pdf', pagesize=A3)
    bg(cv, Color(0.02, 0.02, 0.03))
    cx, cy = W/2, H/2 + 50

    R = 300
    res = 300

    for ix in range(res):
        for iy in range(res):
            x = (ix / res - 0.5) * 2
            y = (iy / res - 0.5) * 2
            r = math.sqrt(x*x + y*y)
            if r > 0.98:
                continue

            px = cx + x * R
            py = cy + y * R

            # Thin-film interference: path difference depends on r^2
            # This creates rainbow-colored concentric rings
            phase = r * r * 40  # Adjust for ring density

            # Convert phase to RGB (rainbow)
            hue = (phase % 1.0)
            # HSV to RGB (simplified)
            h6 = hue * 6
            hi = int(h6) % 6
            f = h6 - int(h6)
            s, v = 0.8, 0.9
            p_c = v * (1 - s)
            q = v * (1 - f * s)
            t_c = v * (1 - (1 - f) * s)

            if hi == 0: r_c, g_c, b_c = v, t_c, p_c
            elif hi == 1: r_c, g_c, b_c = q, v, p_c
            elif hi == 2: r_c, g_c, b_c = p_c, v, t_c
            elif hi == 3: r_c, g_c, b_c = p_c, q, v
            elif hi == 4: r_c, g_c, b_c = t_c, p_c, v
            else: r_c, g_c, b_c = v, p_c, q

            # Intensity modulation (fringes)
            intensity = (0.5 + 0.5 * math.cos(phase * 2 * math.pi)) ** 2
            # Fade toward edges
            fade = 1.0 - r * 0.5
            alpha = intensity * fade * 0.5

            if alpha < 0.02:
                continue

            cv.setFillColor(Color(r_c, g_c, b_c, alpha=alpha))
            cv.circle(px, py, 1.2, fill=1, stroke=0)

    # Center bright spot
    for rr in range(20, 0, -1):
        cv.setFillColor(Color(1, 1, 1, alpha=0.03 * (1 - rr/20)))
        cv.circle(cx, cy, rr, fill=1, stroke=0)

    scatter_stars(cv, 100, (0.7, 0.7, 0.8), cx, cy, R + 5)

    title_block(cv, "INTERFERENCE RINGS", "NEWTON'S RINGS  ·  THIN FILM  ·  CHROMATIC FRINGES",
                "GEOMETRIA SACRED PATTERNS — 057",
                Color(0.8, 0.7, 1, alpha=0.85), Color(0.8, 0.75, 1, alpha=0.3), Color(0.8, 0.75, 1, alpha=0.12))
    cv.save()
    print("  057 done")


# ═══════════════════════════════════════════════════════════
# 058 — STRANGE LOOP (Escher-like Impossible / Warm Gray)
# Penrose triangle and impossible geometry
# ═══════════════════════════════════════════════════════════
def gen_058():
    cv = canvas.Canvas(f'{OUT}/058-strange-loop.pdf', pagesize=A3)
    bg(cv, Color(0.04, 0.04, 0.05))
    cx, cy = W/2, H/2 + 50

    grays = [
        Color(0.6, 0.58, 0.55, alpha=0.5),
        Color(0.75, 0.73, 0.7, alpha=0.45),
        Color(0.45, 0.43, 0.4, alpha=0.5),
        Color(0.85, 0.83, 0.8, alpha=0.35),
    ]

    # Penrose triangle (tribar)
    R = 200
    bar_w = 40

    # Three vertices of the outer triangle
    verts_outer = []
    verts_inner = []
    for i in range(3):
        a = i * 2 * math.pi / 3 - math.pi / 2
        verts_outer.append((cx + R * math.cos(a), cy + R * math.sin(a)))
        verts_inner.append((cx + (R - bar_w * 2.5) * math.cos(a), cy + (R - bar_w * 2.5) * math.sin(a)))

    # Draw the impossible triangle as three bars
    for i in range(3):
        j = (i + 1) % 3
        col = grays[i]

        # Outer edge of bar
        ax_o, ay_o = verts_outer[i]
        bx_o, by_o = verts_outer[j]
        # Direction perpendicular to bar
        dx = bx_o - ax_o
        dy = by_o - ay_o
        length = math.hypot(dx, dy)
        nx, ny = -dy / length * bar_w, dx / length * bar_w

        # Four corners of the bar
        corners = [
            (ax_o + nx, ay_o + ny),
            (ax_o - nx, ay_o - ny),
            (bx_o - nx, by_o - ny),
            (bx_o + nx, by_o + ny),
        ]

        # Fill with gradient effect
        cv.setFillColor(Color(col.red, col.green, col.blue, alpha=0.06))
        p = cv.beginPath()
        p.moveTo(*corners[0])
        for c_pt in corners[1:]: p.lineTo(*c_pt)
        p.close()
        cv.drawPath(p, fill=1, stroke=0)

        # Outlines with different brightness per face
        cv.setStrokeColor(Color(col.red + 0.1, col.green + 0.1, col.blue + 0.1, alpha=col.alpha))
        cv.setLineWidth(1.0)
        cv.line(corners[0][0], corners[0][1], corners[3][0], corners[3][1])  # outer edge

        cv.setStrokeColor(Color(col.red - 0.1, col.green - 0.1, col.blue - 0.1, alpha=col.alpha))
        cv.line(corners[1][0], corners[1][1], corners[2][0], corners[2][1])  # inner edge

        # End caps
        cv.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.7))
        cv.line(corners[0][0], corners[0][1], corners[1][0], corners[1][1])
        cv.line(corners[2][0], corners[2][1], corners[3][0], corners[3][1])

    # Smaller nested impossible triangles
    for scale in [0.5, 0.3]:
        r_s = R * scale
        bw_s = bar_w * scale
        cv.setLineWidth(0.5 * scale + 0.2)
        for i in range(3):
            a1 = i * 2 * math.pi / 3 - math.pi / 2
            a2 = (i + 1) * 2 * math.pi / 3 - math.pi / 2
            x1 = cx + r_s * math.cos(a1)
            y1 = cy + r_s * math.sin(a1)
            x2 = cx + r_s * math.cos(a2)
            y2 = cy + r_s * math.sin(a2)
            col = grays[i]
            cv.setStrokeColor(Color(col.red, col.green, col.blue, alpha=col.alpha * 0.5))
            dx = x2 - x1
            dy = y2 - y1
            l = math.hypot(dx, dy)
            nx, ny = -dy/l * bw_s, dx/l * bw_s
            cv.line(x1 + nx, y1 + ny, x2 + nx, y2 + ny)
            cv.line(x1 - nx, y1 - ny, x2 - nx, y2 - ny)

    # Infinite staircase suggestion (spiral)
    cv.setStrokeColor(Color(0.7, 0.68, 0.65, alpha=0.1))
    cv.setLineWidth(0.4)
    for s in range(100):
        t = s / 100
        a = t * 4 * math.pi
        r = 30 + t * 50
        x1 = cx + r * math.cos(a)
        y1 = cy + r * math.sin(a)
        x2 = cx + (r + 2) * math.cos(a + 0.1)
        y2 = cy + (r + 2) * math.sin(a + 0.1)
        cv.line(x1, y1, x2, y2)

    scatter_stars(cv, 150, (0.65, 0.63, 0.6), cx, cy, R + 50)

    title_block(cv, "STRANGE LOOP", "PENROSE TRIANGLE  ·  IMPOSSIBLE GEOMETRY  ·  SELF-REFERENCE",
                "GEOMETRIA SACRED PATTERNS — 058",
                Color(0.75, 0.73, 0.7, alpha=0.85), Color(0.7, 0.68, 0.65, alpha=0.3), Color(0.7, 0.68, 0.65, alpha=0.12))
    cv.save()
    print("  058 done")


# ═══════════════════════════════════════════════════════════
# 059 — CLIFFORD ATTRACTOR (Neon Vapor / Retrowave)
# Chaotic attractor from simple trig rules
# ═══════════════════════════════════════════════════════════
def gen_059():
    cv = canvas.Canvas(f'{OUT}/059-clifford-attractor.pdf', pagesize=A3)
    bg(cv, Color(0.02, 0.01, 0.04))
    cx, cy = W/2, H/2 + 50

    # Clifford attractor: x' = sin(a*y) + c*cos(a*x), y' = sin(b*x) + d*cos(b*y)
    a, b, cc, d = -1.4, 1.6, 1.0, 0.7
    x, y = 0.1, 0.1

    # Collect points
    points = []
    for _ in range(200000):
        nx = math.sin(a * y) + cc * math.cos(a * x)
        ny = math.sin(b * x) + d * math.cos(b * y)
        x, y = nx, ny
        points.append((x, y))

    # Scale
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    x_range = x_max - x_min
    y_range = y_max - y_min
    scale = min(550 / x_range, 700 / y_range) * 0.9

    for i, (px, py) in enumerate(points):
        sx = cx + (px - (x_min + x_max) / 2) * scale
        sy = cy + (py - (y_min + y_max) / 2) * scale

        # Color cycles through neon vapor palette
        t = (i / len(points))
        hue = (t * 3) % 1.0
        r_c = 0.5 + 0.5 * math.sin(hue * 2 * math.pi)
        g_c = 0.1 + 0.2 * math.sin(hue * 2 * math.pi + 2)
        b_c = 0.5 + 0.5 * math.sin(hue * 2 * math.pi + 4)

        cv.setFillColor(Color(min(1, r_c), max(0, g_c), min(1, b_c), alpha=0.04))
        cv.circle(sx, sy, 0.6, fill=1, stroke=0)

    scatter_stars(cv, 80, (0.7, 0.3, 0.8), cx, cy, 0)

    title_block(cv, "CLIFFORD ATTRACTOR", "TRIGONOMETRIC CHAOS  ·  a=-1.4  b=1.6  c=1.0  d=0.7",
                "GEOMETRIA SACRED PATTERNS — 059",
                Color(0.8, 0.3, 0.9, alpha=0.85), Color(0.75, 0.4, 0.9, alpha=0.3), Color(0.75, 0.4, 0.9, alpha=0.12))
    cv.save()
    print("  059 done")


# ═══════════════════════════════════════════════════════════
# 060 — COSMIC WEB (Dark Matter Filaments / Void Black)
# Large-scale structure of the universe
# ═══════════════════════════════════════════════════════════
def gen_060():
    cv = canvas.Canvas(f'{OUT}/060-cosmic-web.pdf', pagesize=A3)
    bg(cv, Color(0.005, 0.005, 0.01))
    cx, cy = W/2, H/2 + 50

    random.seed(2077)

    # Generate galaxy clusters (nodes)
    n_clusters = 80
    clusters = []
    for _ in range(n_clusters):
        x = random.random() * (W - 100) + 50
        y = random.random() * (H - 250) + 170
        mass = random.random() * 0.8 + 0.2
        clusters.append((x, y, mass))

    # Dark matter filaments: connect nearby clusters
    cv.setLineWidth(0.3)
    for i in range(len(clusters)):
        dists = []
        for j in range(len(clusters)):
            if i != j:
                d = math.hypot(clusters[i][0] - clusters[j][0], clusters[i][1] - clusters[j][1])
                dists.append((d, j))
        dists.sort()

        for d, j in dists[:5]:
            if d < 200:
                x1, y1, m1 = clusters[i]
                x2, y2, m2 = clusters[j]
                strength = (m1 + m2) / 2

                # Draw filament as multiple faint lines with slight curves
                for strand in range(3):
                    p = cv.beginPath()
                    steps = 30
                    for s in range(steps + 1):
                        t = s / steps
                        # Interpolate with slight perturbation
                        fx = x1 + (x2 - x1) * t + random.gauss(0, d * 0.03)
                        fy = y1 + (y2 - y1) * t + random.gauss(0, d * 0.03)
                        if s == 0:
                            p.moveTo(fx, fy)
                        else:
                            p.lineTo(fx, fy)

                    alpha = max(0.01, 0.08 * strength * (1 - d / 200))
                    # Faint blue-purple filaments
                    cv.setStrokeColor(Color(0.3, 0.35, 0.6, alpha=alpha))
                    cv.setLineWidth(0.3 + strength * 0.4)
                    cv.drawPath(p, fill=0, stroke=1)

    # Galaxy clusters
    for x, y, mass in clusters:
        # Dark matter halo
        halo_r = 10 + mass * 30
        for rr in range(int(halo_r), 0, -2):
            alpha = 0.005 * (1 - rr / halo_r)
            cv.setFillColor(Color(0.2, 0.25, 0.5, alpha=alpha))
            cv.circle(x, y, rr, fill=1, stroke=0)

        # Galaxies within cluster
        n_gal = int(mass * 15) + 3
        for _ in range(n_gal):
            gx = x + random.gauss(0, mass * 12)
            gy = y + random.gauss(0, mass * 12)
            # Galaxy color: yellow-white for ellipticals, blue for spirals
            if random.random() < 0.4:
                gc = Color(1, 0.95, 0.7, alpha=random.random() * 0.4 + 0.2)
            else:
                gc = Color(0.6, 0.7, 1, alpha=random.random() * 0.3 + 0.1)
            sz = random.random() * 1.5 + 0.3
            cv.setFillColor(gc)
            cv.circle(gx, gy, sz, fill=1, stroke=0)

        # Brightest cluster galaxy
        cv.setFillColor(Color(1, 0.95, 0.8, alpha=0.5 * mass))
        cv.circle(x, y, 1.5 + mass * 2, fill=1, stroke=0)

    # Cosmic voids label (subtle text in empty regions)
    cv.setFillColor(Color(0.3, 0.3, 0.4, alpha=0.06))
    cv.setFont("Courier", 6)

    scatter_stars(cv, 500, (0.8, 0.8, 0.9), cx, cy, 0)

    title_block(cv, "COSMIC WEB", "DARK MATTER FILAMENTS  ·  GALAXY CLUSTERS  ·  COSMIC VOIDS",
                "GEOMETRIA SACRED PATTERNS — 060",
                Color(0.4, 0.45, 0.7, alpha=0.85), Color(0.45, 0.5, 0.7, alpha=0.3), Color(0.45, 0.5, 0.7, alpha=0.12))
    cv.save()
    print("  060 done")


# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating GEOMETRIA SACRED PATTERNS 046–060...")
    gen_046()
    gen_047()
    gen_048()
    gen_049()
    gen_050()
    gen_051()
    gen_052()
    gen_053()
    gen_054()
    gen_055()
    gen_056()
    gen_057()
    gen_058()
    gen_059()
    gen_060()
    print("\nAll 15 PDFs (046–060) generated!")
