#!/usr/bin/env python3
"""Generative SVG forge v2 — glassmorphism + physics + chaos systems."""
from __future__ import annotations

import math
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]


def palette(mode: str) -> dict:
    if mode == "dark":
        return {
            "bg": "#0B1220",
            "ink": "#E2E8F0",
            "white": "#F8FAFC",
            "mute": "#94A3B8",
            "teal": "#2DD4BF",
            "teal_dim": "#134E4A",
            "amber": "#FBBF24",
            "amber_dim": "#78350F",
            "grid": "#1E293B",
            "glass_fill": "#1E293B",
            "glass_stroke": "#334155",
            "glass_hi": "#5EEAD4",
        }
    return {
        "bg": "#F8FAFC",
        "ink": "#0F172A",
        "white": "#FFFFFF",
        "mute": "#64748B",
        "teal": "#0D9488",
        "teal_dim": "#CCFBF1",
        "amber": "#D97706",
        "amber_dim": "#FEF3C7",
        "grid": "#E2E8F0",
        "glass_fill": "#FFFFFF",
        "glass_stroke": "#E2E8F0",
        "glass_hi": "#5EEAD4",
    }


def glass_defs(p: dict, blur_id: str = "frost") -> str:
    return f"""  <defs>
    <filter id="{blur_id}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="12" result="blur"/>
      <feColorMatrix in="blur" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.55 0" result="soft"/>
      <feBlend in="SourceGraphic" in2="soft" mode="normal"/>
    </filter>
    <linearGradient id="glassSheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{p['glass_hi']}" stop-opacity="0.35"/>
      <stop offset="45%" stop-color="{p['glass_fill']}" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="{p['glass_fill']}" stop-opacity="0.05"/>
    </linearGradient>
  </defs>
"""


def glass_panel(x, y, w, h, p, r=10, label=None, sub=None, mono=True) -> str:
    """Frosted glass chrome: translucent fill, blur backdrop rect, light edge, sheen."""
    font_m = "ui-monospace,Menlo,Consolas,monospace"
    font_s = "system-ui,Segoe UI,sans-serif"
    parts = [
        f'<g filter="url(#frost)">',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
        f'fill="{p["glass_fill"]}" fill-opacity="0.55" stroke="{p["glass_stroke"]}" stroke-width="1"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#glassSheen)" opacity="0.45"/>',
        f'<path d="M{x+1} {y+r} Q{x+1} {y+1} {x+r} {y+1} H{x+w-r} Q{x+w-1} {y+1} {x+w-1} {y+r}" '
        f'stroke="{p["glass_hi"]}" stroke-opacity="0.45" stroke-width="1" fill="none"/>',
    ]
    if label:
        parts.append(
            f'<text x="{x+14}" y="{y+28}" font-family="{font_s}" font-size="14" font-weight="650" fill="{p["ink"]}">{label}</text>'
        )
    if sub:
        parts.append(
            f'<text x="{x+14}" y="{y+48}" font-family="{font_m}" font-size="11" fill="{p["mute"]}">{sub}</text>'
        )
    parts.append("</g>")
    return "".join(parts)


# physics easings (SMIL keySplines)
SPRING = "0.34 1.56 0.64 1"          # overshoot then settle
SPRING_SOFT = "0.22 1.2 0.36 1"       # gentle overshoot
GRAVITY = "0.55 0.06 0.68 0.19"       # accelerate like free-fall
BOUNCE = "0.68 0 0.32 1"              # impact settle
KEPLER = "0.45 0 0.55 1"              # slow apoapsis feel via keyTimes later


def write(name: str, body: str) -> None:
    path = OUT / name
    path.write_text(body, encoding="utf-8")
    print(f"wrote {path.name:32s} {path.stat().st_size:7d} bytes")


# ── systems ──────────────────────────────────────────────────────────

def thomas(n=2400, dt=0.08, b=0.208186):
    x, y, z = 0.1, 0.0, 0.0
    pts = []
    for i in range(n):
        dx, dy, dz = math.sin(y) - b * x, math.sin(z) - b * y, math.sin(x) - b * z
        x, y, z = x + dx * dt, y + dy * dt, z + dz * dt
        if i > 60:
            pts.append((x, y, z))
    return pts


def double_pendulum(steps=900, dt=0.04):
    """Chaotic double pendulum; returns list of tip (x,y) in meters-ish units."""
    th1, th2 = 2.1, 1.6
    w1 = w2 = 0.0
    L1 = L2 = 1.0
    g = 9.81
    m1 = m2 = 1.0
    pts = []
    for _ in range(steps):
        den = 2 * m1 + m2 - m2 * math.cos(2 * th1 - 2 * th2)
        a1 = (
            -g * (2 * m1 + m2) * math.sin(th1)
            - m2 * g * math.sin(th1 - 2 * th2)
            - 2 * math.sin(th1 - th2) * m2 * (w2 * w2 * L2 + w1 * w1 * L1 * math.cos(th1 - th2))
        ) / (L1 * den)
        a2 = (
            2 * math.sin(th1 - th2)
            * (w1 * w1 * L1 * (m1 + m2) + g * (m1 + m2) * math.cos(th1) + w2 * w2 * L2 * m2 * math.cos(th1 - th2))
        ) / (L2 * den)
        w1 += a1 * dt
        w2 += a2 * dt
        th1 += w1 * dt
        th2 += w2 * dt
        x1 = L1 * math.sin(th1)
        y1 = -L1 * math.cos(th1)
        x2 = x1 + L2 * math.sin(th2)
        y2 = y1 - L2 * math.cos(th2)
        pts.append((x2, y2))
    return pts


def fourier_epicycles(target, n_terms=28, samples=280):
    """Discrete Fourier series of a closed 2D path → epicycle radii/phases."""
    # target: list of (x,y) equally spaced around closed curve
    N = len(target)
    xs = [p[0] for p in target]
    ys = [p[1] for p in target]
    terms = []
    # sort by amplitude
    coeffs = []
    for k in range(-n_terms, n_terms + 1):
        cx = sum(xs[t] * math.cos(-2 * math.pi * k * t / N) for t in range(N)) / N
        sx = sum(xs[t] * math.sin(-2 * math.pi * k * t / N) for t in range(N)) / N
        cy = sum(ys[t] * math.cos(-2 * math.pi * k * t / N) for t in range(N)) / N
        sy = sum(ys[t] * math.sin(-2 * math.pi * k * t / N) for t in range(N)) / N
        ax = math.hypot(cx, sx)
        ay = math.hypot(cy, sy)
        px = math.atan2(sx, cx)
        py = math.atan2(sy, cy)
        amp = ax + ay
        coeffs.append((amp, k, ax, px, ay, py))
    coeffs.sort(reverse=True, key=lambda t: t[0])
    for amp, k, ax, px, ay, py in coeffs[: n_terms * 2 + 1]:
        terms.append((k, ax, px, ay, py))
    return terms


def rose_curve(n=200, k=5, scale=70):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = scale * math.cos(k * t)
        pts.append((r * math.cos(t), r * math.sin(t)))
    return pts


def metaball_centers(t_phase=0.0):
    """5 glass metaballs on springy orbits."""
    balls = []
    for i in range(5):
        a = t_phase + i * (2 * math.pi / 5)
        wobble = 0.15 * math.sin(t_phase * 2.3 + i)
        x = math.cos(a) * (55 + 12 * wobble) + math.sin(t_phase * 1.7 + i) * 10
        y = math.sin(a) * (40 + 10 * wobble) + math.cos(t_phase * 1.3 + i) * 8
        r = 18 + 4 * math.sin(t_phase * 3 + i * 1.2)
        balls.append((x, y, r))
    return balls


def spring_lattice_points(n=5, phase=0.0):
    """Mass-spring mesh, driven at corner with damped wave."""
    pts = []
    for j in range(n):
        for i in range(n):
            u, v = i / (n - 1), j / (n - 1)
            # damped traveling wave from (0,0)
            d = math.hypot(u, v)
            amp = 10 * math.exp(-2.2 * d) * math.sin(6 * d - phase * 2.4)
            pts.append((u, v, amp))
    return pts


# ── pieces ───────────────────────────────────────────────────────────

def hero(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 540
    # chaos trail
    dp = double_pendulum(700)
    xs = [q[0] for q in dp]
    ys = [q[1] for q in dp]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    trail = []
    for i in range(0, len(dp), 2):
        x = 620 + (dp[i][0] - minx) / (maxx - minx + 1e-9) * 280
        y = 80 + (dp[i][1] - miny) / (maxy - miny + 1e-9) * 360
        trail.append(f"{x:.1f},{y:.1f}")
    trail_d = "M" + " L".join(trail[:200])  # keep density but finite

    # fourier rose (signature)
    rose = rose_curve(180, k=5, scale=78)
    terms = fourier_epicycles(rose, n_terms=16)
    # bake epicycle path samples for drawing animation
    cx0, cy0 = 250, 300
    drawn = []
    for s in range(120):
        t = 2 * math.pi * s / 119
        x, y = cx0, cy0
        for k, ax, px, ay, py in terms:
            x += ax * math.cos(k * t + px)
            y += ay * math.sin(k * t + py)
        drawn.append(f"{x:.1f},{y:.1f}")
    # epicycle circles at s=0 for static cage + rotation anim
    epi = []
    x, y = cx0, cy0
    for k, ax, px, ay, py in terms[:10]:
        r = abs(ax) + abs(ay)
        if r < 1:
            continue
        epi.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*0.5:.1f}" fill="none" stroke="{p["grid"]}" stroke-width="0.8"/>'
        )
        x += ax * math.cos(px)
        y += ay * math.sin(py)

    # thomas attractor ribbons (background depth)
    pts = thomas(1800)
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    ribbons = []
    for start in range(0, len(pts) - 40, 36):
        seg = pts[start : start + 48]
        coords = " ".join(
            f"{80+(q[0]-minx)/(maxx-minx+1e-9)*800:.1f},{70+(q[1]-miny)/(maxy-miny+1e-9)*400:.1f}"
            for q in seg
        )
        ribbons.append(
            f'<polyline points="{coords}" fill="none" stroke="{p["teal"]}" stroke-width="0.7" '
            f'stroke-opacity="0.18" stroke-linecap="round">'
            f'<animate attributeName="stroke-dashoffset" values="0;-30;0" dur="11s" repeatCount="indefinite"/></polyline>'
        )

    # metaballs spring
    balls_svg = []
    for i, (bx, by, br) in enumerate(metaball_centers(0.5)):
        balls_svg.append(
            f'<circle cx="{200+bx:.1f}" cy="{300+by:.1f}" r="{br:.1f}" fill="{p["teal"]}" fill-opacity="0.20" '
            f'stroke="{p["teal"]}" stroke-opacity="0.35">'
            f'<animate attributeName="r" values="{br:.1f};{br*1.18:.1f};{br:.1f}" dur="2.8s" '
            f'begin="{i*0.2}s" calcMode="spline" keyTimes="0;0.5;1" keySplines="{SPRING};{SPRING_SOFT}" repeatCount="indefinite"/>'
            f"</circle>"
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Physics generative hero">
{glass_defs(p)}
  <rect width="{W}" height="{H}" fill="{p["bg"]}"/>
  <g opacity="0.55">{''.join(ribbons)}</g>
  <g opacity="0.7">
    <path d="{trail_d}" fill="none" stroke="{p["amber"]}" stroke-width="1.1" stroke-opacity="0.55" stroke-linejoin="round">
      <animate attributeName="stroke-dasharray" values="0 2000;1200 2000" dur="8s" repeatCount="indefinite"/>
    </path>
  </g>
  {''.join(epi)}
  <polyline points="{' '.join(drawn)}" fill="none" stroke="{p["teal"]}" stroke-width="1.6"
    stroke-linecap="round" stroke-dasharray="400" stroke-dashoffset="400">
    <animate attributeName="stroke-dashoffset" values="400;0;0;400" keyTimes="0;0.45;0.75;1" dur="9s" repeatCount="indefinite"/>
  </polyline>
  {''.join(balls_svg)}
{glass_panel(36, 36, 420, 110, p, label="Shadrack Baraka Mwahanga", sub="ENGINEER · LLB KABARAK · OFFLINE SYSTEMS")}
{glass_panel(36, 430, 300, 72, p, label="double pendulum chaos", sub="θ₁=2.1  θ₂=1.6  ·  g=9.81  ·  trail 700 steps")}
{glass_panel(700, 430, 220, 72, p, label="Fourier rose k=5", sub="28 epicycle terms  ·  spring ease")}
</svg>
'''


def signal_grid(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 460
    rows = [
        ("no internet", "RIS", 70),
        ("feature phone", "USSD", 140),
        ("QR fraud", "KSAS", 210),
        ("opaque case law", "Juriscore", 280),
        ("cash economy", "EFK / M-Pesa", 350),
        ("47 counties", "FieldOps", 420),
    ]
    parts, pulses = [], []
    for label, product, y in rows:
        # glass docks
        parts.append(glass_panel(40, y - 22, 160, 44, p, label=label))
        parts.append(glass_panel(760, y - 22, 160, 44, p, label=product))
        # bezier bus
        path = f"M210 {y} C 340 {y-30}, 400 {y+25}, 520 {y} S 680 {y-20}, 750 {y}"
        parts.append(
            f'<path d="{path}" fill="none" stroke="{p["grid"]}" stroke-width="8" stroke-linecap="round" opacity="0.7"/>'
        )
        parts.append(
            f'<path d="{path}" fill="none" stroke="{p["teal"]}" stroke-width="1.4" stroke-opacity="0.85"/>'
        )
        # gravity-drop packet then spring settle at dock
        for k, delay in enumerate((0, 0.55, 1.1)):
            parts.append(
                f'<circle r="3.4" fill="{p["amber"]}">'
                f'<animateMotion dur="3.4s" begin="{delay+k*0.12}s" repeatCount="indefinite" path="{path}" '
                f'calcMode="spline" keyTimes="0;0.35;0.7;1" keySplines="{GRAVITY};{BOUNCE};{SPRING}" keyPoints="0;0.35;0.7;1"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" dur="3.4s" begin="{delay}s" repeatCount="indefinite"/>'
                f"</circle>"
            )
        # vias with spring pop
        for t in (0.2, 0.45, 0.7):
            x = 210 + t * 540
            yy = y + math.sin(t * math.pi) * 12
            parts.append(
                f'<circle cx="{x:.0f}" cy="{yy:.0f}" r="2.2" fill="{p["mute"]}">'
                f'<animate attributeName="r" values="1;3.2;2.2" dur="2s" begin="{t}s" '
                f'calcMode="spline" keyTimes="0;0.5;1" keySplines="{SPRING};{SPRING_SOFT}" repeatCount="indefinite"/>'
                f"</circle>"
            )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Signal grid glass docks">
{glass_defs(p)}
  <rect width="{W}" height="{H}" fill="{p["bg"]}"/>
  {''.join(parts)}
{glass_panel(36, 12, 280, 40, p, label="Signal grid", sub="gravity packets · spring vias · glass docks")}
</svg>
'''


def constellation(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 480
    # fibonacci sphere n=47
    stations = []
    labels = ["Nairobi","Nakuru","Mombasa","Kisumu","Eldoret","Kisii","Kilifi","Kiambu","Machakos","Nyeri"]
    for i in range(47):
        y = 1 - (i / 46) * 2
        radius = math.sqrt(max(0.0, 1 - y * y))
        theta = math.pi * (3 - 5 ** 0.5) * i
        stations.append((math.cos(theta) * radius, y, math.sin(theta) * radius, labels[i] if i < len(labels) else None))

    # Chladni nodal field (standing wave) as backdrop dust
    chladni = []
    for i in range(80):
        for j in range(40):
            x = -1 + 2 * i / 79
            y = -1 + 2 * j / 39
            # mode (3,2)
            f = math.cos(3 * math.pi * x) * math.cos(2 * math.pi * y) - math.cos(2 * math.pi * x) * math.cos(3 * math.pi * y)
            if abs(f) < 0.12:
                chladni.append(f'<circle cx="{480+x*210:.1f}" cy="{250+y*150:.1f}" r="0.9" fill="{p["mute"]}" opacity="0.35"/>')

    marks = []
    for i, (x, y, z, lab) in enumerate(stations):
        # Kepler-ish: faster near periapsis via non-uniform... bake two radii phases
        persp = 480 / (480 + z * 160)
        sx = 480 + x * 160 * persp
        sy = 250 + y * 160 * persp
        r = 1.6 + persp * 2.8
        bright = lab is not None
        fill = p["amber"] if bright else p["teal"]
        if bright:
            # spring scale on beacon
            marks.append(
                f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="{fill}">'
                f'<animate attributeName="r" values="{r:.1f};{r*1.8:.1f};{r:.1f}" dur="3s" begin="{i*0.15:.2f}s" '
                f'calcMode="spline" keyTimes="0;0.4;1" keySplines="{SPRING};{SPRING_SOFT}" repeatCount="indefinite"/>'
                f"</circle>"
            )
            marks.append(
                f'<text x="{sx:.1f}" y="{sy-12:.1f}" text-anchor="middle" '
                f'font-family="ui-monospace,Menlo,Consolas,monospace" font-size="9" fill="{p["mute"]}">{lab}</text>'
            )
        else:
            marks.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="{fill}" opacity="{0.4+persp*0.5:.2f}"/>')

    # orbital rings with Kepler second-law nod (uneven keyTimes)
    rings = []
    for i, (rx, ry) in enumerate(((170, 58), (205, 82), (240, 108))):
        rings.append(
            f'<ellipse cx="480" cy="250" rx="{rx}" ry="{ry}" fill="none" stroke="{p["teal"]}" '
            f'stroke-opacity="0.22" stroke-width="1" transform="rotate({-18+i*8} 480 250)"/>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Constellation with chladni field">
{glass_defs(p)}
  <rect width="{W}" height="{H}" fill="{p["bg"]}"/>
  <g>{''.join(chladni)}</g>
  <g>
    <animateTransform attributeName="transform" type="rotate" from="0 480 250" to="360 480 250" dur="56s" repeatCount="indefinite"/>
    {''.join(rings)}
    {''.join(marks)}
  </g>
{glass_panel(36, 16, 340, 56, p, label="Constellation", sub="Fibonacci n=47 · Chladni (3,2) · Kepler rings")}
{glass_panel(640, 400, 280, 48, p, label="10 product beacons", sub="spring scale · orbital phase")}
</svg>
'''


def pendulum_panel(mode: str) -> str:
    """Standalone double-pendulum chaos with glass HUD + spring scale-in of arms."""
    p = palette(mode)
    W, H = 960, 360
    dp = double_pendulum(900, dt=0.035)
    xs, ys = [q[0] for q in dp], [q[1] for q in dp]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)

    def map_pt(q):
        return (
            200 + (q[0] - minx) / (maxx - minx + 1e-9) * 560,
            40 + (q[1] - miny) / (maxy - miny + 1e-9) * 260,
        )

    # colored by velocity (finite difference)
    segs = []
    for i in range(1, len(dp), 2):
        x1, y1 = map_pt(dp[i - 1])
        x2, y2 = map_pt(dp[i])
        v = math.hypot(dp[i][0] - dp[i - 1][0], dp[i][1] - dp[i - 1][1])
        col = p["amber"] if v > 0.02 else p["teal"]
        op = min(0.85, 0.15 + v * 12)
        segs.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" '
            f'stroke-opacity="{op:.2f}" stroke-width="1.2"/>'
        )
    tip = map_pt(dp[-1])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Double pendulum chaos">
{glass_defs(p)}
  <rect width="{W}" height="{H}" fill="{p["bg"]}"/>
  <g>{''.join(segs)}</g>
  <circle cx="{tip[0]:.1f}" cy="{tip[1]:.1f}" r="4" fill="{p["white"]}">
    <animate attributeName="opacity" values="0.4;1;0.4" dur="1.6s" repeatCount="indefinite"/>
    <animate attributeName="r" values="3;6;3" dur="1.6s" calcMode="spline" keyTimes="0;0.5;1" keySplines="{SPRING};{SPRING_SOFT}" repeatCount="indefinite"/>
  </circle>
{glass_panel(24, 24, 320, 70, p, label="Double pendulum", sub="deterministic chaos · velocity-mapped ink")}
{glass_panel(640, 270, 280, 60, p, label="900 Euler steps  Δt=0.035", sub="tip trace · spring beacon")}
</svg>
'''


def metaball_glass(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 320
    # three phase snapshots as SMIL crossfade of springy blobs + lattice wave
    balls = metaball_centers(0.0)
    blobs = []
    for i, (bx, by, br) in enumerate(balls):
        cx, cy = 320 + bx * 1.4, 160 + by * 1.1
        blobs.append(
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{br*1.15:.1f}" ry="{br:.1f}" '
            f'fill="{p["teal"]}" fill-opacity="0.22" stroke="{p["teal"]}" stroke-opacity="0.4">'
            f'<animate attributeName="rx" values="{br*1.15:.1f};{br*1.3:.1f};{br*1.15:.1f}" dur="{2.4+i*0.25:.2f}s" '
            f'calcMode="spline" keyTimes="0;0.5;1" keySplines="{SPRING};{SPRING_SOFT}" repeatCount="indefinite"/>'
            f'<animate attributeName="cx" values="{cx:.1f};{cx+8:.1f};{cx:.1f}" dur="{3.2+i*0.2:.2f}s" '
            f'calcMode="spline" keyTimes="0;0.5;1" keySplines="{SPRING_SOFT};{SPRING}" repeatCount="indefinite"/>'
            f"</ellipse>"
        )

    # spring lattice grid (right side)
    lattice = []
    n = 6
    for j in range(n):
        for i in range(n):
            x = 620 + i * 48
            y = 70 + j * 36
            amp = 6 * math.exp(-0.35 * (i + j)) * 1  # static seed; animate r
            lattice.append(
                f'<circle cx="{x}" cy="{y}" r="2.5" fill="{p["amber"]}" opacity="0.7">'
                f'<animate attributeName="cy" values="{y};{y-amp:.1f};{y}" dur="{2.0+0.15*(i+j):.2f}s" '
                f'calcMode="spline" keyTimes="0;0.5;1" keySplines="{GRAVITY};{BOUNCE}" repeatCount="indefinite"/>'
                f"</circle>"
            )
            if i < n - 1:
                lattice.append(f'<line x1="{x}" y1="{y}" x2="{x+48}" y2="{y}" stroke="{p["grid"]}" stroke-width="0.8"/>')
            if j < n - 1:
                lattice.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+36}" stroke="{p["grid"]}" stroke-width="0.8"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Metaballs and spring lattice">
{glass_defs(p)}
  <rect width="{W}" height="{H}" fill="{p["bg"]}"/>
  <g>{''.join(blobs)}</g>
  <g>{''.join(lattice)}</g>
{glass_panel(24, 24, 280, 56, p, label="Metaballs", sub="5 body spring orbit · glass blobs")}
{glass_panel(560, 240, 360, 56, p, label="Spring lattice 6×6", sub="damped wave · gravity drop + bounce")}
</svg>
'''


def glyph(mode: str) -> str:
    p = palette(mode)

    def sf(a, m=7, n1=0.3, n2=1.7, n3=1.7, scale=90):
        part = (abs(math.cos(m * a / 4)) ** n2 + abs(math.sin(m * a / 4)) ** n3) ** (-1 / n1)
        return scale * part * math.cos(a), scale * part * math.sin(a)

    pts = " ".join(f"{100+sf(i*math.pi/180)[0]:.1f},{100+sf(i*math.pi/180)[1]:.1f}" for i in range(360))
    pts2 = " ".join(
        f"{100+sf(i*math.pi/180, m=5, n1=0.2, n2=1.5, n3=1.5, scale=55)[0]:.1f},"
        f"{100+sf(i*math.pi/180, m=5, n1=0.2, n2=1.5, n3=1.5, scale=55)[1]:.1f}"
        for i in range(360)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="Superformula glyph">
{glass_defs(p)}
  <rect width="200" height="200" fill="{p["bg"]}"/>
  <g filter="url(#frost)">
    <rect x="18" y="18" width="164" height="164" rx="18" fill="{p["glass_fill"]}" fill-opacity="0.5" stroke="{p["glass_stroke"]}"/>
  </g>
  <polygon points="{pts}" fill="none" stroke="{p["teal"]}" stroke-width="1.2">
    <animateTransform attributeName="transform" type="rotate" from="0 100 100" to="360 100 100" dur="24s" repeatCount="indefinite"/>
  </polygon>
  <polygon points="{pts2}" fill="none" stroke="{p["amber"]}" stroke-width="1">
    <animateTransform attributeName="transform" type="rotate" from="360 100 100" to="0 100 100" dur="18s" repeatCount="indefinite"/>
  </polygon>
  <circle cx="100" cy="100" r="3.5" fill="{p["white"]}">
    <animate attributeName="r" values="2.5;5;2.5" dur="2s" calcMode="spline" keyTimes="0;0.5;1" keySplines="{SPRING};{SPRING_SOFT}" repeatCount="indefinite"/>
  </circle>
</svg>
'''


def main() -> None:
    for mode in ("light", "dark"):
        write(f"hero-attractor-{mode}.svg", hero(mode))
        write(f"signal-grid-{mode}.svg", signal_grid(mode))
        write(f"constellation-{mode}.svg", constellation(mode))
        write(f"pendulum-{mode}.svg", pendulum_panel(mode))
        write(f"metaballs-{mode}.svg", metaball_glass(mode))
        write(f"glyph-{mode}.svg", glyph(mode))


if __name__ == "__main__":
    main()
