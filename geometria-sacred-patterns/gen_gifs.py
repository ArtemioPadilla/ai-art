#!/usr/bin/env python3
"""GEOMETRIA SACRED PATTERNS — Animated GIF Series (Perfect Loops)"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gif')
SZ = 540  # square canvas
FRAMES = 60
DUR = 50  # ms per frame


def ease(t):
    """Smooth easing for perfect loops: t goes 0→1 and wraps."""
    return t % 1.0


def loop_t(frame, n_frames):
    """Normalized time 0→1 that loops perfectly."""
    return frame / n_frames


def blend_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def make_gif(frames_list, name, duration=DUR):
    frames_list[0].save(
        f'{OUT}/{name}.gif',
        save_all=True, append_images=frames_list[1:],
        duration=duration, loop=0, optimize=False, disposal=2
    )
    print(f"  {name} done ({len(frames_list)} frames)")


# ═══════════════════════════════════════════════════════════
# 01 — ROTATING FLOWER OF LIFE
# ═══════════════════════════════════════════════════════════
def gif_01():
    frames = []
    r = 60
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (8, 6, 18))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        # Rotating rings of circles
        for ring in range(3):
            n_circles = 6
            ring_r = r * (ring + 1)
            rotation = phase * (1 if ring % 2 == 0 else -1) * 0.5
            for i in range(n_circles):
                a = i * math.pi / 3 + rotation + ring * 0.2
                px = cx + ring_r * math.cos(a)
                py = cy + ring_r * math.sin(a)
                # Golden color with ring-based variation
                alpha = int(180 - ring * 40)
                color = (255, min(255, 180 + ring * 25), int(50 + ring * 30))
                draw.ellipse([px - r, py - r, px + r, py + r], outline=color, width=1)

        # Center circle pulses
        pulse = 0.8 + 0.2 * math.sin(phase * 2)
        cr = int(r * pulse)
        draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], outline=(255, 210, 50), width=2)

        # Center dot
        draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=(255, 230, 100))

        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        frames.append(img)
    make_gif(frames, '01-flower-of-life')


# ═══════════════════════════════════════════════════════════
# 02 — BREATHING MANDALA
# ═══════════════════════════════════════════════════════════
def gif_02():
    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (10, 5, 15))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        for ring in range(6):
            n_petals = 6 + ring * 4
            base_r = 40 + ring * 38
            breath = 1.0 + 0.15 * math.sin(phase - ring * 0.4)
            r_now = base_r * breath
            rotation = phase * 0.3 * (1 if ring % 2 == 0 else -1)

            colors = [
                (200, 50, 120), (100, 60, 200), (180, 80, 200),
                (80, 50, 180), (220, 100, 160), (130, 40, 190)
            ]
            color = colors[ring % len(colors)]
            alpha_fade = max(60, 220 - ring * 30)
            c = tuple(min(255, int(v * alpha_fade / 220)) for v in color)

            for i in range(n_petals):
                a = rotation + i * 2 * math.pi / n_petals
                petal_len = 20 + ring * 5
                tip_x = cx + (r_now + petal_len) * math.cos(a)
                tip_y = cy + (r_now + petal_len) * math.sin(a)
                base_l = cx + r_now * math.cos(a - 0.15)
                base_ly = cy + r_now * math.sin(a - 0.15)
                base_r_x = cx + r_now * math.cos(a + 0.15)
                base_ry = cy + r_now * math.sin(a + 0.15)
                draw.line([(base_l, base_ly), (tip_x, tip_y)], fill=c, width=1)
                draw.line([(base_r_x, base_ry), (tip_x, tip_y)], fill=c, width=1)

        # Center glow
        for rr in range(20, 0, -2):
            v = int(200 * (1 - rr / 20))
            draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=(v, int(v*0.5), v))
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(255, 200, 255))

        frames.append(img)
    make_gif(frames, '02-breathing-mandala')


# ═══════════════════════════════════════════════════════════
# 03 — SPIRAL VORTEX
# ═══════════════════════════════════════════════════════════
def gif_03():
    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (5, 8, 20))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        n_arms = 5
        for arm in range(n_arms):
            base_a = arm * 2 * math.pi / n_arms + phase
            colors = [
                (0, 200, 180), (0, 150, 250), (100, 80, 230),
                (0, 230, 130), (50, 180, 255)
            ]
            color = colors[arm]
            for s in range(300):
                st = s / 300
                a = base_a + st * 4 * math.pi
                r = 10 + st * 220
                px = cx + r * math.cos(a)
                py = cy + r * math.sin(a)
                sz = max(1, int(1 + st * 3))
                fade = max(20, int(255 * (1 - st * 0.6)))
                c = tuple(min(255, int(v * fade / 255)) for v in color)
                draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=c)

        img = img.filter(ImageFilter.GaussianBlur(radius=0.8))
        frames.append(img)
    make_gif(frames, '03-spiral-vortex')


# ═══════════════════════════════════════════════════════════
# 04 — PULSING METATRON'S CUBE
# ═══════════════════════════════════════════════════════════
def gif_04():
    frames = []
    r_base = 100
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (8, 3, 18))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        pulse = 1.0 + 0.12 * math.sin(phase)
        rot = phase * 0.15

        # 13 nodes
        nodes = [(cx, cy)]
        for i in range(6):
            a = i * math.pi / 3 + rot - math.pi / 2
            nodes.append((cx + r_base * pulse * math.cos(a), cy + r_base * pulse * math.sin(a)))
        for i in range(6):
            a = i * math.pi / 3 + rot - math.pi / 2
            nodes.append((cx + r_base * 2 * pulse * math.cos(a), cy + r_base * 2 * pulse * math.sin(a)))

        # Connections
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                dist = math.hypot(nodes[i][0]-nodes[j][0], nodes[i][1]-nodes[j][1])
                alpha = max(15, int(60 * (1 - dist / (r_base * 4.5))))
                c = (min(255, 100 + alpha), 60 + alpha // 3, min(255, 180 + alpha // 2))
                draw.line([nodes[i], nodes[j]], fill=c, width=1)

        # Nodes with pulse glow
        for idx, (nx, ny) in enumerate(nodes):
            node_pulse = 1.0 + 0.3 * math.sin(phase + idx * 0.5)
            nr = int(3 * node_pulse)
            glow = int(8 * node_pulse)
            draw.ellipse([nx-glow, ny-glow, nx+glow, ny+glow], fill=(40, 20, 60))
            draw.ellipse([nx-nr, ny-nr, nx+nr, ny+nr], fill=(200, 150, 255))

        frames.append(img)
    make_gif(frames, '04-metatrons-cube')


# ═══════════════════════════════════════════════════════════
# 05 — ORBITING PARTICLES
# ═══════════════════════════════════════════════════════════
def gif_05():
    random.seed(42)
    n_particles = 120
    particles = []
    for _ in range(n_particles):
        orbit_r = 30 + random.random() * 200
        speed = 0.5 + random.random() * 2.0
        start_a = random.random() * 2 * math.pi
        size = random.random() * 2.5 + 0.5
        hue = random.random()
        particles.append((orbit_r, speed, start_a, size, hue))

    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (3, 3, 8))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        # Center glow
        for rr in range(30, 0, -2):
            v = int(40 * (1 - rr / 30))
            draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=(v, v, int(v*1.5)))
        draw.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(180, 180, 255))

        for orbit_r, speed, start_a, size, hue in particles:
            a = start_a + phase * speed
            px = cx + orbit_r * math.cos(a)
            py = cy + orbit_r * math.sin(a)

            # Color from hue
            r_c = int(128 + 127 * math.sin(hue * 6.28))
            g_c = int(128 + 127 * math.sin(hue * 6.28 + 2.09))
            b_c = int(128 + 127 * math.sin(hue * 6.28 + 4.19))

            fade = max(0.2, 1.0 - orbit_r / 250)
            r_c = int(r_c * fade)
            g_c = int(g_c * fade)
            b_c = int(b_c * fade)

            sz = int(size)
            if sz >= 1:
                draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=(r_c, g_c, b_c))

        frames.append(img)
    make_gif(frames, '05-orbiting-particles')


# ═══════════════════════════════════════════════════════════
# 06 — WAVE PROPAGATION
# ═══════════════════════════════════════════════════════════
def gif_06():
    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (2, 5, 12))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        # Two sources
        s1 = (cx - 80, cy)
        s2 = (cx + 80, cy)
        wavelength = 50

        for r in range(1, 20):
            radius = r * wavelength / 2 + phase * wavelength / (2 * math.pi)
            radius = radius % (20 * wavelength / 2)
            if radius < 5:
                continue
            alpha = max(20, int(120 * (1 - radius / 500)))
            for sx, sy in [s1, s2]:
                color = (int(30 * alpha / 120), int(180 * alpha / 120), int(120 * alpha / 120))
                draw.ellipse([sx - radius, sy - radius, sx + radius, sy + radius],
                             outline=color, width=1)

        # Source points
        pulse = int(4 + 2 * math.sin(phase * 3))
        for sx, sy in [s1, s2]:
            draw.ellipse([sx-pulse, sy-pulse, sx+pulse, sy+pulse], fill=(100, 255, 180))

        frames.append(img)
    make_gif(frames, '06-wave-propagation')


# ═══════════════════════════════════════════════════════════
# 07 — LORENZ BUTTERFLY (rotating view)
# ═══════════════════════════════════════════════════════════
def gif_07():
    # Pre-compute Lorenz
    sigma, rho, beta = 10.0, 28.0, 8.0/3.0
    dt = 0.005
    x, y, z = 0.1, 0.0, 0.0
    points = []
    for _ in range(15000):
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z
        x += dx * dt; y += dy * dt; z += dz * dt
        points.append((x, y, z))

    # Normalize
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]
    cx_d = (min(xs)+max(xs))/2
    cy_d = (min(ys)+max(ys))/2
    cz_d = (min(zs)+max(zs))/2
    sc = 8.0

    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        rot = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (12, 5, 2))
        draw = ImageDraw.Draw(img)

        for i in range(len(points) - 1):
            px, py, pz = points[i]
            px -= cx_d; py -= cy_d; pz -= cz_d
            # Rotate around Z
            rx = px * math.cos(rot) - py * math.sin(rot)
            ry = px * math.sin(rot) + py * math.cos(rot)
            rz = pz

            sx = SZ // 2 + rx * sc
            sy = SZ // 2 - rz * sc + ry * sc * 0.3

            progress = i / len(points)
            r_c = min(255, int(200 + 55 * progress))
            g_c = min(255, int(80 + 100 * progress))
            b_c = int(30 + 40 * (1 - progress))

            depth = (ry + 30) / 60
            fade = max(0.2, min(1.0, depth))
            r_c = int(r_c * fade)
            g_c = int(g_c * fade)
            b_c = int(b_c * fade)

            if 0 <= sx < SZ and 0 <= sy < SZ:
                draw.point((int(sx), int(sy)), fill=(r_c, g_c, b_c))

        frames.append(img)
    make_gif(frames, '07-lorenz-butterfly')


# ═══════════════════════════════════════════════════════════
# 08 — GEOMETRIC MORPH (Triangle → Square → Pentagon → Hex → Circle)
# ═══════════════════════════════════════════════════════════
def gif_08():
    frames = []
    shapes = [3, 4, 5, 6, 8, 12, 36]  # vertices (36 ≈ circle)
    n_shapes = len(shapes)
    frames_per_shape = FRAMES // n_shapes

    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        # Which shape are we morphing between?
        shape_t = t * n_shapes
        shape_idx = int(shape_t) % n_shapes
        morph = shape_t - int(shape_t)
        # Smooth morph
        morph = morph * morph * (3 - 2 * morph)

        n1 = shapes[shape_idx]
        n2 = shapes[(shape_idx + 1) % n_shapes]

        img = Image.new('RGB', (SZ, SZ), (6, 6, 12))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2
        R = 180

        colors = [
            (255, 80, 100), (255, 180, 50), (50, 255, 150),
            (50, 150, 255), (180, 80, 255), (255, 100, 200), (200, 200, 255)
        ]
        color = blend_color(colors[shape_idx], colors[(shape_idx+1) % n_shapes], morph)

        # Generate interpolated shape
        # Use max(n1,n2) points, interpolate angles
        n_pts = max(n1, n2, 36)
        pts = []
        for i in range(n_pts):
            a_frac = i / n_pts

            # Polygon 1 radius at this angle
            a1 = a_frac * 2 * math.pi - math.pi / 2
            segment1 = int(a_frac * n1)
            local1 = a_frac * n1 - segment1
            corner_a1 = segment1 * 2 * math.pi / n1 - math.pi / 2
            next_a1 = (segment1 + 1) * 2 * math.pi / n1 - math.pi / 2
            # Radius of polygon at this angle
            r1 = R * math.cos(math.pi / n1) / math.cos(a1 - (corner_a1 + next_a1) / 2) if n1 < 36 else R

            a2 = a_frac * 2 * math.pi - math.pi / 2
            segment2 = int(a_frac * n2)
            corner_a2 = segment2 * 2 * math.pi / n2 - math.pi / 2
            next_a2 = (segment2 + 1) * 2 * math.pi / n2 - math.pi / 2
            r2 = R * math.cos(math.pi / n2) / math.cos(a2 - (corner_a2 + next_a2) / 2) if n2 < 36 else R

            r1 = min(R * 1.2, max(R * 0.5, r1))
            r2 = min(R * 1.2, max(R * 0.5, r2))
            r_interp = r1 + (r2 - r1) * morph

            a = a_frac * 2 * math.pi - math.pi / 2 + phase * 0.1
            pts.append((cx + r_interp * math.cos(a), cy + r_interp * math.sin(a)))

        # Draw
        for i in range(len(pts)):
            j = (i + 1) % len(pts)
            draw.line([pts[i], pts[j]], fill=color, width=2)

        # Inner echo
        for scale in [0.6, 0.35]:
            inner_pts = [(cx + (p[0]-cx)*scale, cy + (p[1]-cy)*scale) for p in pts]
            ic = tuple(max(20, v // 3) for v in color)
            for i in range(len(inner_pts)):
                j = (i + 1) % len(inner_pts)
                draw.line([inner_pts[i], inner_pts[j]], fill=ic, width=1)

        frames.append(img)
    make_gif(frames, '08-geometric-morph')


# ═══════════════════════════════════════════════════════════
# 09 — FIBONACCI PHYLLOTAXIS BLOOM
# ═══════════════════════════════════════════════════════════
def gif_09():
    golden_angle = math.pi * (3 - math.sqrt(5))
    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (5, 8, 5))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        n_seeds = 500
        breath = 1.0 + 0.08 * math.sin(phase)
        rotation = phase * 0.2

        for i in range(n_seeds):
            r = math.sqrt(i) * 10 * breath
            if r > SZ * 0.45:
                continue
            a = i * golden_angle + rotation

            px = cx + r * math.cos(a)
            py = cy + r * math.sin(a)

            # Size and color by distance
            dist_t = r / (SZ * 0.45)
            sz = max(1, int(2 + dist_t * 5))

            if dist_t < 0.3:
                color = (int(100 + dist_t * 300), int(70 + dist_t * 200), 30)
            elif dist_t < 0.7:
                t2 = (dist_t - 0.3) / 0.4
                color = (int(200 - t2 * 80), int(180 + t2 * 40), int(30 + t2 * 30))
            else:
                t2 = (dist_t - 0.7) / 0.3
                color = (int(80 - t2 * 30), int(160 + t2 * 40), int(50 + t2 * 30))

            # Pulse individual seeds
            seed_pulse = 1.0 + 0.2 * math.sin(phase * 2 + i * 0.1)
            sz = max(1, int(sz * seed_pulse))

            draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=color)

        frames.append(img)
    make_gif(frames, '09-phyllotaxis-bloom')


# ═══════════════════════════════════════════════════════════
# 10 — SACRED GEOMETRY KALEIDOSCOPE
# ═══════════════════════════════════════════════════════════
def gif_10():
    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (4, 2, 8))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        n_fold = 8  # 8-fold symmetry
        layers = 5

        for layer in range(layers):
            r_base = 50 + layer * 50
            breath = 1.0 + 0.1 * math.sin(phase - layer * 0.6)
            r = r_base * breath
            rot_speed = 0.3 * (1 if layer % 2 == 0 else -1)
            rot = phase * rot_speed + layer * 0.3

            colors = [
                (0, 200, 220), (220, 50, 130), (200, 180, 50),
                (50, 220, 100), (180, 50, 220),
            ]
            color = colors[layer % len(colors)]
            fade = max(40, 220 - layer * 35)
            c = tuple(min(255, v * fade // 220) for v in color)

            for fold in range(n_fold):
                a = fold * 2 * math.pi / n_fold + rot

                # Draw symmetric shapes: lines and arcs
                x1 = cx + r * 0.3 * math.cos(a)
                y1 = cy + r * 0.3 * math.sin(a)
                x2 = cx + r * math.cos(a)
                y2 = cy + r * math.sin(a)
                draw.line([(x1, y1), (x2, y2)], fill=c, width=1)

                # Diamond at tip
                da = 0.15
                dx1 = cx + r * 0.9 * math.cos(a - da)
                dy1 = cy + r * 0.9 * math.sin(a - da)
                dx2 = cx + r * 0.9 * math.cos(a + da)
                dy2 = cy + r * 0.9 * math.sin(a + da)
                draw.line([(dx1, dy1), (x2, y2)], fill=c, width=1)
                draw.line([(dx2, dy2), (x2, y2)], fill=c, width=1)

                # Cross connections
                a2 = a + math.pi / n_fold
                xc = cx + r * 0.7 * math.cos(a2)
                yc = cy + r * 0.7 * math.sin(a2)
                c2 = tuple(max(10, v // 2) for v in c)
                draw.line([(x2, y2), (xc, yc)], fill=c2, width=1)

        # Center jewel
        for rr in range(12, 0, -1):
            v = int(200 * (1 - rr / 12))
            draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=(v, int(v*0.6), v))

        frames.append(img)
    make_gif(frames, '10-kaleidoscope')


# ═══════════════════════════════════════════════════════════
# 11 — SPINNING TORUS
# ═══════════════════════════════════════════════════════════
def gif_11():
    frames = []
    R, r_tube = 120, 45

    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        rot = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (12, 5, 10))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        tilt = 0.4
        u_steps = 50
        v_steps = 20

        for u in range(u_steps):
            ua = u / u_steps * 2 * math.pi + rot
            for v in range(v_steps):
                va = v / v_steps * 2 * math.pi

                x = (R + r_tube * math.cos(va)) * math.cos(ua)
                y = (R + r_tube * math.cos(va)) * math.sin(ua)
                z = r_tube * math.sin(va)

                px = cx + x
                py = cy - y * math.sin(tilt) - z * math.cos(tilt)
                depth = y * math.cos(tilt) - z * math.sin(tilt)

                t_norm = (depth + R + r_tube) / (2 * (R + r_tube))
                if t_norm < 0.3:
                    continue

                hue = (u / u_steps + 0.5 * v / v_steps) % 1.0
                r_c = int(128 + 127 * math.sin(hue * 6.28) * t_norm)
                g_c = int(40 + 80 * math.sin(hue * 6.28 + 2.0) * t_norm)
                b_c = int(80 + 120 * math.sin(hue * 6.28 + 4.0) * t_norm)
                r_c = max(0, min(255, r_c))
                g_c = max(0, min(255, g_c))
                b_c = max(0, min(255, b_c))

                sz = max(1, int(2 * t_norm))
                draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=(r_c, g_c, b_c))

        frames.append(img)
    make_gif(frames, '11-spinning-torus')


# ═══════════════════════════════════════════════════════════
# 12 — TESSERACT ROTATION
# ═══════════════════════════════════════════════════════════
def gif_12():
    # 4D hypercube
    verts_4d = []
    for i in range(16):
        v = [((i >> b) & 1) * 2 - 1 for b in range(4)]
        verts_4d.append(v)

    edges = []
    for i in range(16):
        for j in range(i+1, 16):
            diff = sum(1 for a, b in zip(verts_4d[i], verts_4d[j]) if a != b)
            if diff == 1:
                edges.append((i, j))

    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        rot_xw = t * 2 * math.pi
        rot_yz = t * math.pi * 0.7

        img = Image.new('RGB', (SZ, SZ), (6, 3, 12))
        draw = ImageDraw.Draw(img)

        projected = []
        for v in verts_4d:
            x, y, z, w = v
            # XW rotation
            x2 = x * math.cos(rot_xw) - w * math.sin(rot_xw)
            w2 = x * math.sin(rot_xw) + w * math.cos(rot_xw)
            # YZ rotation
            y2 = y * math.cos(rot_yz) - z * math.sin(rot_yz)
            z2 = y * math.sin(rot_yz) + z * math.cos(rot_yz)
            # Perspective 4D→3D
            d4 = 3.5
            s4 = d4 / (d4 - w2)
            x3, y3, z3 = x2*s4, y2*s4, z2*s4
            # 3D→2D
            d3 = 4.0
            s3 = d3 / (d3 - z3)
            px = SZ//2 + x3 * s3 * 100
            py = SZ//2 + y3 * s3 * 100
            depth = z3 + w2
            projected.append((px, py, depth, s3*s4))

        # Draw edges
        dim_colors = [(120, 60, 255), (60, 180, 255), (60, 255, 160), (255, 180, 60)]
        for i, j in edges:
            dim = 0
            for d in range(4):
                if verts_4d[i][d] != verts_4d[j][d]:
                    dim = d
            p1, p2 = projected[i], projected[j]
            depth = (p1[2] + p2[2]) / 2
            t_d = (depth + 4) / 8
            base_c = dim_colors[dim]
            c = tuple(max(10, int(v * t_d * 0.7)) for v in base_c)
            w = max(1, int(1 + 2 * t_d))
            draw.line([(p1[0], p1[1]), (p2[0], p2[1])], fill=c, width=w)

        # Vertices
        for px, py, depth, scale in projected:
            t_d = (depth + 4) / 8
            sz = max(1, int(2 + 3 * t_d))
            v = int(150 + 105 * t_d)
            draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=(v, int(v*0.8), 255))

        frames.append(img)
    make_gif(frames, '12-tesseract-rotation')


# ═══════════════════════════════════════════════════════════
# 13 — SUPERNOVA PULSE
# ═══════════════════════════════════════════════════════════
def gif_13():
    random.seed(2024)
    # Pre-generate rays
    n_rays = 150
    rays = [(random.random() * 2 * math.pi, random.random() * 0.5 + 0.5, random.random()) for _ in range(n_rays)]

    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        phase = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (3, 2, 5))
        draw = ImageDraw.Draw(img)
        cx, cy = SZ // 2, SZ // 2

        pulse = 0.7 + 0.3 * math.sin(phase)

        # Rays
        for angle, length_f, brightness in rays:
            r_start = 15
            r_end = int(r_start + length_f * 250 * pulse)
            x1 = cx + r_start * math.cos(angle)
            y1 = cy + r_start * math.sin(angle)
            x2 = cx + r_end * math.cos(angle)
            y2 = cy + r_end * math.sin(angle)
            # Color: core white → orange → red
            dist_t = length_f * pulse
            r_c = min(255, int(255 * brightness))
            g_c = min(255, int((120 - dist_t * 80) * brightness))
            b_c = min(255, int((50 - dist_t * 40) * brightness))
            draw.line([(x1, y1), (x2, y2)], fill=(max(0,r_c), max(0,g_c), max(0,b_c)), width=1)

        # Shockwave ring
        ring_r = int(60 + 180 * pulse)
        ring_color = (int(255 * pulse), int(120 * pulse), int(50 * pulse))
        draw.ellipse([cx-ring_r, cy-ring_r, cx+ring_r, cy+ring_r], outline=ring_color, width=2)

        # Core glow
        for rr in range(25, 0, -1):
            v = int(255 * (1 - rr/25) * pulse)
            draw.ellipse([cx-rr, cy-rr, cx+rr, cy+rr],
                         fill=(min(255,v+50), min(255, int(v*0.8)), min(255, int(v*0.4))))

        # Bright center
        draw.ellipse([cx-5, cy-5, cx+5, cy+5], fill=(255, 240, 200))

        frames.append(img)
    make_gif(frames, '13-supernova-pulse')


# ═══════════════════════════════════════════════════════════
# 14 — DNA HELIX ROTATION
# ═══════════════════════════════════════════════════════════
def gif_14():
    frames = []
    R = 70  # helix radius
    pitch = 80
    n_turns = 5

    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        rot = t * 2 * math.pi

        img = Image.new('RGB', (SZ, SZ), (3, 8, 10))
        draw = ImageDraw.Draw(img)
        cx = SZ // 2

        total_h = n_turns * pitch
        y_offset = (SZ - total_h) // 2

        # Collect all elements with depth for sorting
        elements = []  # (depth, type, data)

        steps = 200
        for s in range(steps):
            st = s / steps
            a = st * n_turns * 2 * math.pi + rot
            y_pos = y_offset + st * total_h

            x1 = cx + R * math.cos(a)
            z1 = R * math.sin(a)
            x2 = cx + R * math.cos(a + math.pi)
            z2 = R * math.sin(a + math.pi)

            # Rungs every ~10 steps
            if s % 10 == 0:
                elements.append(((z1+z2)/2, 'rung', (x1, y_pos, x2, y_pos, z1)))

            elements.append((z1, 'strand', (x1, y_pos, 0)))
            elements.append((z2, 'strand', (x2, y_pos, 1)))

        # Sort by depth
        elements.sort(key=lambda e: e[0])

        for depth, etype, data in elements:
            t_d = (depth + R) / (2 * R)
            if etype == 'rung':
                x1, y1, x2, y2, z = data
                alpha = 0.3 + 0.5 * t_d
                c = (int(60 * alpha), int(180 * alpha), int(120 * alpha))
                draw.line([(x1, y1), (x2, y2)], fill=c, width=1)
            elif etype == 'strand':
                px, py, strand_id = data
                sz = max(1, int(1 + 3 * t_d))
                if strand_id == 0:
                    c = (int(50 + 200 * t_d), int(200 * t_d), int(220 * t_d))
                else:
                    c = (int(50 * t_d), int(180 * t_d), int(50 + 200 * t_d))
                draw.ellipse([px-sz, py-sz, px+sz, py+sz], fill=c)

        frames.append(img)
    make_gif(frames, '14-dna-helix')


# ═══════════════════════════════════════════════════════════
# 15 — GEODESIC SPHERE ROTATION
# ═══════════════════════════════════════════════════════════
def gif_15():
    # Build icosahedron
    phi = (1 + math.sqrt(5)) / 2
    ico = [
        (-1,phi,0),(1,phi,0),(-1,-phi,0),(1,-phi,0),
        (0,-1,phi),(0,1,phi),(0,-1,-phi),(0,1,-phi),
        (phi,0,-1),(phi,0,1),(-phi,0,-1),(-phi,0,1)
    ]
    ico = [(x/math.sqrt(x*x+y*y+z*z), y/math.sqrt(x*x+y*y+z*z), z/math.sqrt(x*x+y*y+z*z)) for x,y,z in ico]
    faces = [
        (0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),
        (1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),
        (3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),
        (4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1)
    ]
    # Subdivide once
    verts = list(ico)
    mid_cache = {}
    def get_mid(i, j):
        key = (min(i,j),max(i,j))
        if key in mid_cache: return mid_cache[key]
        mx = (verts[i][0]+verts[j][0])/2
        my = (verts[i][1]+verts[j][1])/2
        mz = (verts[i][2]+verts[j][2])/2
        l = math.sqrt(mx*mx+my*my+mz*mz)
        verts.append((mx/l,my/l,mz/l))
        mid_cache[key] = len(verts)-1
        return len(verts)-1

    new_faces = []
    for a,b,cc in faces:
        ab=get_mid(a,b); bc=get_mid(b,cc); ca=get_mid(cc,a)
        new_faces.extend([(a,ab,ca),(b,bc,ab),(cc,ca,bc),(ab,bc,ca)])

    # Extract edges
    edge_set = set()
    for a,b,cc in new_faces:
        for e in [(min(a,b),max(a,b)),(min(b,cc),max(b,cc)),(min(cc,a),max(cc,a))]:
            edge_set.add(e)

    R = 200
    frames = []
    for f in range(FRAMES):
        t = loop_t(f, FRAMES)
        ry = t * 2 * math.pi
        rx = 0.4

        img = Image.new('RGB', (SZ, SZ), (5, 12, 12))
        draw = ImageDraw.Draw(img)

        projected = []
        for v in verts:
            x,y,z = v
            # Rotate Y
            x2 = x*math.cos(ry)-z*math.sin(ry)
            z2 = x*math.sin(ry)+z*math.cos(ry)
            # Rotate X
            y2 = y*math.cos(rx)-z2*math.sin(rx)
            z3 = y*math.sin(rx)+z2*math.cos(rx)
            projected.append((SZ//2+x2*R, SZ//2+y2*R, z3))

        for i,j in edge_set:
            p1,p2 = projected[i], projected[j]
            depth = (p1[2]+p2[2])/2
            t_d = (depth+1)/2
            if t_d < 0.15: continue
            c = (int(60*t_d), int(220*t_d), int(200*t_d))
            w = max(1, int(1+t_d))
            draw.line([(p1[0],p1[1]),(p2[0],p2[1])], fill=c, width=w)

        for px,py,z in projected:
            t_d = (z+1)/2
            if t_d < 0.2: continue
            sz = max(1, int(1+2*t_d))
            v = int(200*t_d)
            draw.ellipse([px-sz,py-sz,px+sz,py+sz], fill=(int(v*0.4),v,int(v*0.9)))

        frames.append(img)
    make_gif(frames, '15-geodesic-sphere')


# ═══════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating GEOMETRIA GIF series (15 perfect loops)...")
    gif_01()
    gif_02()
    gif_03()
    gif_04()
    gif_05()
    gif_06()
    gif_07()
    gif_08()
    gif_09()
    gif_10()
    gif_11()
    gif_12()
    gif_13()
    gif_14()
    gif_15()
    print("\nAll 15 GIFs generated!")
