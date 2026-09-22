#!/usr/bin/env python3
"""Generative SVG forge for shadrackb1 profile — mathematical density, SMIL motion."""
from __future__ import annotations

import math
import os
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]


def rot_x(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (x, y * c - z * s, y * s + z * c)


def rot_y(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (x * c + z * s, y, -x * s + z * c)


def rot_z(p, a):
    x, y, z = p
    c, s = math.cos(a), math.sin(a)
    return (x * c - y * s, x * s + y * c, z)


def project(p, scale=1.0, cx=0.0, cy=0.0, dist=4.0):
    x, y, z = p
    f = dist / (dist + z)
    return cx + x * scale * f, cy + y * scale * f, f


def icosahedron():
    t = (1 + 5 ** 0.5) / 2
    verts = [
        (-1, t, 0), (1, t, 0), (-1, -t, 0), (1, -t, 0),
        (0, -1, t), (0, 1, t), (0, -1, -t), (0, 1, -t),
        (t, 0, -1), (t, 0, 1), (-t, 0, -1), (-t, 0, 1),
    ]
    verts = [tuple(v / t for v in p) for p in verts]
    faces = [
        (0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11),
        (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
        (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9),
        (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1),
    ]
    edges = set()
    for a, b, c in faces:
        for u, v in ((a, b), (b, c), (c, a)):
            edges.add((min(u, v), max(u, v)))
    return verts, sorted(edges)


def thomas_attractor(n=2200, dt=0.08, b=0.208186):
    x, y, z = 0.1, 0.0, 0.0
    pts = []
    for i in range(n):
        dx = math.sin(y) - b * x
        dy = math.sin(z) - b * y
        dz = math.sin(x) - b * z
        x, y, z = x + dx * dt, y + dy * dt, z + dz * dt
        if i > 80:
            pts.append((x, y, z))
    return pts


def palette(mode: str):
    if mode == "dark":
        return {
            "bg": "#0B1220",
            "ink": "#E2E8F0",
            "mute": "#64748B",
            "teal": "#2DD4BF",
            "teal_dim": "#134E4A",
            "amber": "#FBBF24",
            "amber_dim": "#78350F",
            "grid": "#1E293B",
            "white": "#F8FAFC",
        }
    return {
        "bg": "#F8FAFC",
        "ink": "#0F172A",
        "mute": "#64748B",
        "teal": "#0D9488",
        "teal_dim": "#CCFBF1",
        "amber": "#D97706",
        "amber_dim": "#FEF3C7",
        "grid": "#E2E8F0",
        "white": "#FFFFFF",
    }


def write(name: str, body: str):
    path = OUT / name
    path.write_text(body, encoding="utf-8")
    print(f"wrote {path.name:28s} {path.stat().st_size:7d} bytes")


def hero(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 520
    pts = thomas_attractor(n=2800)
    # normalize
    xs = [q[0] for q in pts]
    ys = [q[1] for q in pts]
    zs = [q[2] for q in pts]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    minz, maxz = min(zs), max(zs)

    def map_pt(q, i):
        x = 80 + (q[0] - minx) / (maxx - minx + 1e-9) * 720
        y = 70 + (q[1] - miny) / (maxy - miny + 1e-9) * 340
        depth = (q[2] - minz) / (maxz - minz + 1e-9)
        return x, y, depth

    # ribbon polylines every 28 points
    ribbons = []
    for start in range(0, len(pts) - 60, 28):
        seg = pts[start:start + 64]
        coords = []
        for q in seg:
            x, y, d = map_pt(q, 0)
            coords.append(f"{x:.1f},{y:.1f}")
        depth = map_pt(seg[-1], 0)[2]
        ribbons.append((depth, " ".join(coords)))
    ribbons.sort(key=lambda t: t[0])

    paths = []
    for i, (depth, coords) in enumerate(ribbons):
        opacity = 0.12 + depth * 0.55
        stroke = p["teal"] if i % 5 != 0 else p["amber"]
        width = 0.6 + depth * 1.1
        # staggered dash draw
        paths.append(
            f'<polyline points="{coords}" fill="none" stroke="{stroke}" '
            f'stroke-width="{width:.2f}" stroke-opacity="{opacity:.2f}" '
            f'stroke-linecap="round" stroke-linejoin="round">'
            f'<animate attributeName="stroke-dashoffset" values="0;-40;0" '
            f'dur="{9 + i % 7}s" repeatCount="indefinite"/>'
            f"</polyline>"
        )

    verts, edges = icosahedron()
    product_nodes = [
        (1.15, 0.2, 0.1, "RIS"),
        (-0.9, 0.5, 0.8, "KSAS"),
        (0.3, -1.0, 0.6, "Juriscore"),
        (-0.6, -0.7, -0.8, "USSD"),
        (0.9, 0.8, -0.5, "FieldOps"),
        (-0.2, 1.0, -0.3, "EFK"),
    ]
    cage_pts = []
    for v in verts:
        vr = rot_y(rot_x(v, 0.4), 0.2)
        x, y, f = project(vr, scale=95, cx=780, cy=250, dist=4.2)
        cage_pts.append((x, y, f))
    cage_edges = []
    for a, b in edges:
        x1, y1, f1 = cage_pts[a]
        x2, y2, f2 = cage_pts[b]
        cage_edges.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{p["grid"]}" stroke-width="1"/>'
        )
    node_svg = []
    for nx, ny, nz, label in product_nodes:
        pr = rot_y(rot_x((nx, ny, nz), 0.4), 0.2)
        x, y, f = project(pr, scale=95, cx=780, cy=250, dist=4.2)
        r = 3.5 + f * 3
        node_svg.append(
            f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{p["amber"]}">'
            f'<animate attributeName="opacity" values="0.55;1;0.55" dur="2.4s" repeatCount="indefinite"/>'
            f"</circle>"
            f'<text x="{x:.1f}" y="{y + 16:.1f}" text-anchor="middle" '
            f'font-family="ui-monospace,Menlo,Consolas,monospace" font-size="10" fill="{p["mute"]}">{label}</text></g>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Generative systems hero">
  <rect width="{W}" height="{H}" fill="{p["bg"]}"/>
  <g opacity="0.35">{''.join(cage_edges)}</g>
  {''.join(node_svg)}
  <g stroke-dasharray="4 6">{''.join(paths)}</g>
  <rect x="36" y="36" width="4" height="88" fill="{p["teal"]}"/>
  <text x="56" y="78" font-family="system-ui,Segoe UI,sans-serif" font-size="34" font-weight="700" fill="{p["white"]}">Shadrack Baraka Mwahanga</text>
  <text x="56" y="108" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="13" fill="{p["mute"]}">ENGINEER · LLB KABARAK · OFFLINE SYSTEMS FOR KENYA</text>
  <text x="36" y="480" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="{p["teal"]}">THOMAS ATTRACTOR FIELD × 2400 INTEGRATIONS</text>
  <text x="36" y="500" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="{p["mute"]}">icosa cage · product nodes · continuous flow</text>
  <text x="700" y="500" text-anchor="end" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="{p["mute"]}">shadrackb1</text>
</svg>
'''


def signal_grid(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 440
    # constraint buses -> product docks, like a mission PCB
    rows = [
        ("no internet", "RIS", 60),
        ("feature phone", "USSD", 120),
        ("QR fraud", "KSAS", 180),
        ("opaque case law", "Juriscore", 240),
        ("cash economy", "EFK / M-Pesa", 300),
        ("47 counties", "FieldOps", 360),
    ]
    parts = []
    pulses = []
    for label, product, y in rows:
        # trunk
        parts.append(
            f'<path id="t{y}" d="M210 {y} C 340 {y}, 380 {y-40}, 480 {y} S 640 {y+30}, 720 {y}" '
            f'fill="none" stroke="{p["grid"]}" stroke-width="10" stroke-linecap="round"/>'
        )
        parts.append(
            f'<path d="M210 {y} C 340 {y}, 380 {y-40}, 480 {y} S 640 {y+30}, 720 {y}" '
            f'fill="none" stroke="{p["teal"]}" stroke-width="1.4" stroke-opacity="0.85"/>'
        )
        # via dots
        for t in (0.0, 0.33, 0.66, 1.0):
            # approximate points on curve via quadratic samples
            pass
        parts.append(
            f'<rect x="48" y="{y-18}" width="150" height="36" rx="2" fill="{p["amber_dim"]}" stroke="{p["amber"]}"/>'
            f'<text x="123" y="{y+4}" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" '
            f'font-size="12" fill="{p["ink"]}">{label}</text>'
        )
        parts.append(
            f'<rect x="730" y="{y-18}" width="180" height="36" rx="2" fill="{p["teal_dim"]}" stroke="{p["teal"]}"/>'
            f'<text x="820" y="{y+4}" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" '
            f'font-size="12" fill="{p["ink"]}">{product}</text>'
        )
        # traveling pulses along path via SMIL motion... use offset-path not supported;
        # emulate with circles animated along approximate polyline
        # sample cubic roughly
        pts = []
        for i in range(24):
            t = i / 23
            # blend two cubics crudely for visual
            x = 210 + t * 510
            y2 = y + math.sin(t * math.pi) * (22 if y % 120 else -18)
            pts.append((x, y2))
        poly = " ".join(f"{x:.1f},{y2:.1f}" for x, y2 in pts)
        parts.append(f'<polyline id="p{y}" points="{poly}" fill="none" stroke="none"/>')
        for k, delay in enumerate((0, 0.5, 1.0)):
            pulses.append(
                f'<circle r="3.2" fill="{p["amber"]}" opacity="0.9">'
                f'<animateMotion dur="3.2s" begin="{delay + k*0.15}s" repeatCount="indefinite" '
                f'path="M{pts[0][0]:.1f} {pts[0][1]:.1f} '
                + " ".join(f"L{x:.1f} {y2:.1f}" for x, y2 in pts[1:])
                + '"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" dur="3.2s" begin="{delay}s" repeatCount="indefinite"/>'
                f"</circle>"
            )
        # vias
        for x, y2 in pts[::5]:
            parts.append(f'<circle cx="{x:.1f}" cy="{y2:.1f}" r="2" fill="{p["mute"]}" opacity="0.55"/>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Signal grid">
  <rect width="{W}" height="{H}" fill="{p["bg"]}"/>
  <text x="36" y="32" font-family="system-ui,Segoe UI,sans-serif" font-size="14" font-weight="650" fill="{p["white"]}">Signal grid</text>
  <text x="36" y="50" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="{p["mute"]}">constraint buses · product docks · live packets</text>
  {''.join(parts)}
  {''.join(pulses)}
  <text x="36" y="420" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="{p["mute"]}">80+ vias · 18 packet agents · PCB mission bus</text>
</svg>
'''


def constellation(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 480
    verts, edges = icosahedron()
    # subdivided sphere-ish county cloud
    stations = []
    labels = ["Nairobi", "Nakuru", "Mombasa", "Kisumu", "Eldoret", "Kisii", "Kilifi", "Kiambu", "Machakos", "Nyeri"]
    for i in range(47):
        # fibonacci sphere
        y = 1 - (i / 46) * 2
        radius = math.sqrt(max(0.0, 1 - y * y))
        theta = math.pi * (3 - 5 ** 0.5) * i
        x = math.cos(theta) * radius
        z = math.sin(theta) * radius
        stations.append((x, y, z, labels[i] if i < len(labels) else None))

    parts = []
    # slow rotating group via SMIL on transform
    cage = []
    scaled = []
    for v in verts:
        scaled.append(v)
    for a, b in edges:
        # static cage after one projection bake - animate whole group
        pass

    node_marks = []
    for x, y, z, lab in stations:
        # bake at phase 0; rotate group
        pr = rot_y(rot_x((x * 130, y * 130, z * 130), 0.3), 0.0)
        sx, sy, f = project(pr, scale=1.0, cx=480, cy=250, dist=520)
        # project with manual perspective
        xx, yy, zz = x * 150, y * 150, z * 150
        persp = 480 / (480 + zz)
        sx = 480 + xx * persp
        sy = 250 + yy * persp
        r = 1.8 + persp * 2.4
        bright = lab is not None
        fill = p["amber"] if bright else p["teal"]
        node_marks.append(
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="{fill}" opacity="{0.45 + persp*0.5:.2f}">'
            + (
                f'<animate attributeName="r" values="{r:.1f};{r*1.7:.1f};{r:.1f}" dur="2.8s" repeatCount="indefinite"/>'
                if bright
                else ""
            )
            + "</circle>"
        )
        if lab:
            node_marks.append(
                f'<text x="{sx:.1f}" y="{sy - 10:.1f}" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" '
                f'font-size="9" fill="{p["mute"]}">{lab}</text>'
            )

    # wire icosahedron projected
    wire = []
    proj_v = []
    for v in verts:
        xx, yy, zz = v[0] * 160, v[1] * 160, v[2] * 160
        persp = 480 / (480 + zz)
        proj_v.append((480 + xx * persp, 250 + yy * persp))
    for a, b in edges:
        x1, y1 = proj_v[a]
        x2, y2 = proj_v[b]
        wire.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{p["grid"]}" stroke-width="1"/>'
        )

    # orbital rings
    rings = []
    for i, (rx, ry) in enumerate(((170, 60), (200, 85), (230, 110))):
        rings.append(
            f'<ellipse cx="480" cy="250" rx="{rx}" ry="{ry}" fill="none" stroke="{p["teal"]}" '
            f'stroke-opacity="0.25" stroke-width="1" transform="rotate({-18 + i*8} 480 250)"/>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Constellation">
  <rect width="{W}" height="{H}" fill="{p["bg"]}"/>
  <text x="36" y="32" font-family="system-ui,Segoe UI,sans-serif" font-size="14" font-weight="650" fill="{p["white"]}">Constellation</text>
  <text x="36" y="50" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="{p["mute"]}">47 county field points · product stations · icosa cage</text>
  <g>
    <animateTransform attributeName="transform" type="rotate" from="0 480 250" to="360 480 250" dur="48s" repeatCount="indefinite"/>
    {''.join(rings)}
    {''.join(wire)}
    {''.join(node_marks)}
  </g>
  <text x="36" y="450" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="11" fill="{p["mute"]}">fibonacci lattice n=47 · orbital rings · product beacons</text>
</svg>
'''


def glyph(mode: str) -> str:
    """Personal mathematical mark — superformula lissajous hybrid."""
    p = palette(mode)
    # superformula
    def sf(a, m=7, n1=0.3, n2=1.7, n3=1.7, scale=90):
        t = a
        part = (abs(math.cos(m * t / 4)) ** n2 + abs(math.sin(m * t / 4)) ** n3) ** (-1 / n1)
        return scale * part * math.cos(t), scale * part * math.sin(t)

    pts = []
    for i in range(360):
        a = i * math.pi / 180
        x, y = sf(a)
        pts.append((x, y))
    coords = " ".join(f"{100+x:.1f},{100+y:.1f}" for x, y in pts)
    pts2 = []
    for i in range(360):
        a = i * math.pi / 180
        x, y = sf(a, m=5, n1=0.2, n2=1.5, n3=1.5, scale=55)
        pts2.append((x, y))
    coords2 = " ".join(f"{100+x:.1f},{100+y:.1f}" for x, y in pts2)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="SBM glyph">
  <rect width="200" height="200" fill="{p["bg"]}"/>
  <polygon points="{coords}" fill="none" stroke="{p["teal"]}" stroke-width="1.2">
    <animateTransform attributeName="transform" type="rotate" from="0 100 100" to="360 100 100" dur="24s" repeatCount="indefinite"/>
  </polygon>
  <polygon points="{coords2}" fill="none" stroke="{p["amber"]}" stroke-width="1">
    <animateTransform attributeName="transform" type="rotate" from="360 100 100" to="0 100 100" dur="18s" repeatCount="indefinite"/>
  </polygon>
  <circle cx="100" cy="100" r="3" fill="{p["white"]}"/>
</svg>
'''


def main():
    for mode in ("light", "dark"):
        write(f"hero-attractor-{mode}.svg", hero(mode))
        write(f"signal-grid-{mode}.svg", signal_grid(mode))
        write(f"constellation-{mode}.svg", constellation(mode))
        write(f"glyph-{mode}.svg", glyph(mode))


if __name__ == "__main__":
    main()
