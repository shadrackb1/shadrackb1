#!/usr/bin/env python3
"""Field-notebook forge — hand-inked, plotter-wobble, stamp. Not neon-AI."""
from __future__ import annotations

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
RNG = random.Random(1931)  # fixed so regenerations stay stable


def palette(mode: str) -> dict:
    # warm paper / night photocopy
    if mode == "dark":
        return {
            "paper": "#1A1712",
            "ink": "#F0E6D2",
            "mute": "#A89B84",
            "pencil": "#C4A574",
            "red": "#E23D28",
            "rule": "#2E2820",
            "tape": "#8B7355",
        }
    return {
        "paper": "#F3EDE2",
        "ink": "#1C1917",
        "mute": "#6B6358",
        "pencil": "#5C5346",
        "red": "#C23B22",
        "rule": "#D9D0C0",
        "tape": "#C4B8A0",
    }


def wobble(x1, y1, x2, y2, amp=1.2, segs=6):
    """Ink line that is not a perfect vector — hand/plotter jitter."""
    pts = []
    for i in range(segs + 1):
        t = i / segs
        x = x1 + (x2 - x1) * t + RNG.uniform(-amp, amp)
        y = y1 + (y2 - y1) * t + RNG.uniform(-amp, amp)
        pts.append((x, y))
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for p in pts[1:]:
        d += f" L{p[0]:.1f} {p[1]:.1f}"
    return d


def wobble_poly(points, amp=1.0, closed=False):
    pts = [(x + RNG.uniform(-amp, amp), y + RNG.uniform(-amp, amp)) for x, y in points]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for p in pts[1:]:
        d += f" L{p[0]:.1f} {p[1]:.1f}"
    if closed:
        d += " Z"
    return d


def wobble_rect(x, y, w, h, amp=1.5):
    return wobble_poly(
        [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], amp=amp, closed=True
    )


def paper_bg(p, w, h):
    # subtle fiber speckle + faint rules like a legal pad
    rules = []
    for yy in range(48, h, 28):
        rules.append(
            f'<path d="{wobble(24, yy, w - 24, yy, amp=0.6, segs=8)}" stroke="{p["rule"]}" stroke-width="0.7" fill="none" opacity="0.55"/>'
        )
    flecks = []
    for _ in range(80):
        fx, fy = RNG.uniform(8, w - 8), RNG.uniform(8, h - 8)
        r = RNG.uniform(0.3, 1.1)
        flecks.append(
            f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="{r:.1f}" fill="{p["mute"]}" opacity="{RNG.uniform(0.04, 0.12):.2f}"/>'
        )
    return (
        f'<rect width="{w}" height="{h}" fill="{p["paper"]}"/>'
        + "".join(rules)
        + "".join(flecks)
    )


def stamp(cx, cy, text, p, rot=-8, size=13):
    w = len(text) * size * 0.62 + 22
    h = size + 16
    return (
        f'<g transform="rotate({rot} {cx} {cy})" opacity="0.72">'
        f'<path d="{wobble_rect(cx - w/2, cy - h/2, w, h, amp=2)}" fill="none" stroke="{p["red"]}" stroke-width="2"/>'
        f'<path d="{wobble_rect(cx - w/2 + 3, cy - h/2 + 3, w - 6, h - 6, amp=1.5)}" fill="none" stroke="{p["red"]}" stroke-width="0.8" opacity="0.6"/>'
        f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" '
        f'font-size="{size}" font-weight="700" fill="{p["red"]}" letter-spacing="1">{text}</text>'
        f"</g>"
    )


def tape(x, y, w, h, p, rot=6):
    return (
        f'<g transform="rotate({rot} {x+w/2} {y+h/2})" opacity="0.55">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{p["tape"]}"/>'
        f'<path d="{wobble(x, y+h/2, x+w, y+h/2, amp=0.8)}" stroke="{p["mute"]}" stroke-width="0.5" fill="none" opacity="0.4"/>'
        f"</g>"
    )


def hand_label(x, y, text, p, size=12, fill=None, family=None):
    fam = family or "ui-monospace,Menlo,Consolas,monospace"
    fill = fill or p["ink"]
    # slight baseline jitter reads as handwriting/typewriter placement
    dy = RNG.uniform(-0.8, 0.8)
    return (
        f'<text x="{x}" y="{y+dy:.1f}" font-family="{fam}" font-size="{size}" fill="{fill}">{text}</text>'
    )


def draw_progress(d, color, dur=6, width=1.6, begin=0):
    """Signature non-AI move: the sketch draws itself, like a pen on paper."""
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">'
        f'<animate attributeName="stroke-dasharray" values="0 2000;2000 0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f"</path>"
    )


def hero(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 520
    parts = [paper_bg(p, W, H)]

    # margin rule (red vertical like legal pad)
    parts.append(wobble_line := f'<path d="{wobble(72, 24, 72, H-24, amp=0.8)}" stroke="{p["red"]}" stroke-width="1.2" fill="none" opacity="0.55"/>')
    parts.append(tape(40, 12, 90, 18, p, rot=-4))
    parts.append(tape(820, 8, 100, 16, p, rot=7))

    # title block — typewriter, not hero sans
    parts.append(hand_label(96, 64, "SHADRACK BARAKA MWAHANGA", p, size=22, fill=p["ink"]))
    parts.append(hand_label(96, 88, "ENGINEER · LLB KABARAK · NAKURU / NAIROBI", p, size=11, fill=p["mute"]))
    parts.append(hand_label(96, 110, "CONSTRAINT IS THE BRIEF.", p, size=13, fill=p["red"]))

    # hand-inked constraint diagram (the hero drawing)
    # boxes + wobbly connectors + arrow ticks
    boxes = [
        (120, 160, 170, 52, "no internet"),
        (120, 240, 170, 52, "feature phone"),
        (120, 320, 170, 52, "QR fraud"),
        (420, 160, 190, 52, "RIS · local models"),
        (420, 240, 190, 52, "USSD check-in"),
        (420, 320, 190, 52, "rotating QR + bind"),
        (700, 160, 180, 52, "ship on USB"),
        (700, 240, 180, 52, "any handset"),
        (700, 320, 180, 52, "screenshot dies"),
    ]
    for x, y, w, h, label in boxes:
        parts.append(
            f'<path d="{wobble_rect(x, y, w, h, amp=1.8)}" fill="none" stroke="{p["ink"]}" stroke-width="1.4"/>'
        )
        parts.append(hand_label(x + 12, y + 31, label, p, size=11, fill=p["ink"]))

    connectors = [
        ((290, 186), (420, 186)),
        ((290, 266), (420, 266)),
        ((290, 346), (420, 346)),
        ((610, 186), (700, 186)),
        ((610, 266), (700, 266)),
        ((610, 346), (700, 346)),
    ]
    for (x1, y1), (x2, y2) in connectors:
        parts.append(
            draw_progress(wobble(x1, y1, x2, y2, amp=2.2, segs=8), p["ink"], dur=5.5, width=1.3, begin=0.2)
        )
        # hand arrow head
        parts.append(
            f'<path d="{wobble_poly([(x2-10, y2-6), (x2, y2), (x2-10, y2+6)], amp=0.8)}" '
            f'fill="none" stroke="{p["ink"]}" stroke-width="1.3"/>'
        )

    # red pen annotation in the margin
    parts.append(
        f'<path d="{wobble(96, 400, 280, 418, amp=2)}" stroke="{p["red"]}" stroke-width="1.1" fill="none"/>'
        f'<path d="{wobble(270, 410, 288, 418, amp=1)}" stroke="{p["red"]}" stroke-width="1.1" fill="none"/>'
    )
    parts.append(hand_label(300, 422, "field proof, not slide deck", p, size=12, fill=p["red"]))

    # coffee ring (imperfect circle) — human office tell
    parts.append(
        f'<circle cx="860" cy="430" r="36" fill="none" stroke="{p["pencil"]}" stroke-width="3" opacity="0.18"/>'
        f'<circle cx="860" cy="430" r="32" fill="none" stroke="{p["pencil"]}" stroke-width="1" opacity="0.12"/>'
    )

    parts.append(stamp(780, 70, "FIELD COPY", p, rot=-12, size=12))
    parts.append(hand_label(96, 490, "ref: lab.shadrackb1.github.io/playground/lab.html", p, size=10, fill=p["mute"]))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Field notebook page">
  {''.join(parts)}
</svg>
'''


def glyph(mode: str) -> str:
    p = palette(mode)
    # hand-inked monogram SBM in a rough circle stamp
    cx, cy = 100, 100
    circ = wobble_poly(
        [
            (cx + 62 * math.cos(a), cy + 62 * math.sin(a))
            for a in [i * math.pi / 16 for i in range(32)]
        ],
        amp=1.6,
        closed=True,
    )
    inner = wobble_poly(
        [
            (cx + 54 * math.cos(a), cy + 54 * math.sin(a))
            for a in [i * math.pi / 14 for i in range(28)]
        ],
        amp=1.2,
        closed=True,
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="SBM stamp">
  <rect width="200" height="200" fill="{p["paper"]}"/>
  <path d="{circ}" fill="none" stroke="{p["red"]}" stroke-width="2.4"/>
  <path d="{inner}" fill="none" stroke="{p["red"]}" stroke-width="1"/>
  <text x="100" y="112" text-anchor="middle" font-family="Georgia,Times New Roman,serif" font-size="42" font-weight="700" fill="{p["ink"]}" transform="rotate(-3 100 100)">SBM</text>
  <path d="{wobble(58, 138, 142, 138, amp=1)}" stroke="{p["red"]}" stroke-width="1.2" fill="none"/>
  <text x="100" y="158" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="10" fill="{p["mute"]}" transform="rotate(-3 100 100)">FIELD · KENYA</text>
</svg>
'''


def case_card(mode: str) -> str:
    """Second page: case-file style product index — dossier, not cards."""
    p = palette(mode)
    W, H = 960, 360
    parts = [paper_bg(p, W, H)]
    parts.append(hand_label(40, 40, "INDEX OF SHIPPED SYSTEMS", p, size=16))
    parts.append(hand_label(40, 62, "file under: constraint → response · rev 2026.09", p, size=10, fill=p["mute"]))
    parts.append(stamp(880, 48, "OPEN", p, rot=6, size=11))

    rows = [
        ("RIS", "USB offline research", "labs without net"),
        ("KSAS", "expiring QR + device", "screenshot fraud"),
        ("Juriscore", "briefs + citations", "PDF hell"),
        ("USSD att.", "dial on any phone", "no app store"),
        ("FieldOps", "sites · fuel · 47", "distributed crews"),
        ("EFK", "M-Pesa entry", "cash rails"),
    ]
    y = 96
    for name, what, why in rows:
        parts.append(f'<path d="{wobble(40, y, 920, y, amp=0.7, segs=10)}" stroke="{p["rule"]}" stroke-width="0.8" fill="none"/>')
        parts.append(hand_label(48, y - 8, name, p, size=13, fill=p["ink"]))
        parts.append(hand_label(220, y - 8, what, p, size=12, fill=p["pencil"]))
        parts.append(hand_label(560, y - 8, why, p, size=12, fill=p["red"]))
        y += 42
    parts.append(f'<path d="{wobble(40, y, 920, y, amp=0.7, segs=10)}" stroke="{p["rule"]}" stroke-width="0.8" fill="none"/>')
    parts.append(tape(880, 300, 50, 14, p, rot=-8))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Case index">
  {''.join(parts)}
</svg>
'''


def sketch_pad(mode: str) -> str:
    """Small margin sketch — hand diagram that draws itself slowly."""
    p = palette(mode)
    W, H = 480, 220
    parts = [paper_bg(p, W, H)]
    # rough globe + county ticks + orbiting stamp, drawn as one continuous pen path
    path_pts = []
    for i in range(48):
        a = i / 47 * 2 * math.pi
        path_pts.append((240 + 70 * math.cos(a), 110 + 50 * math.sin(a)))
    d = wobble_poly(path_pts, amp=1.5, closed=True)
    # latitude-ish
    lat = wobble(175, 95, 305, 95, amp=2)
    lat2 = wobble(180, 125, 300, 125, amp=2)
    lon = wobble(240, 60, 240, 160, amp=2)
    parts.append(draw_progress(d, p["ink"], dur=8, width=1.5, begin=0))
    parts.append(draw_progress(lat, p["pencil"], dur=5, width=1, begin=0.6))
    parts.append(draw_progress(lat2, p["pencil"], dur=5, width=1, begin=0.9))
    parts.append(draw_progress(lon, p["pencil"], dur=5, width=1, begin=1.2))
    # county dots
    for i in range(12):
        a = i * 2.4
        x = 240 + 55 * math.cos(a)
        y = 110 + 38 * math.sin(a * 1.3)
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{p["red"]}">'
            f'<animate attributeName="opacity" values="0.3;1;0.3" dur="{2.4+i*0.1:.1f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    parts.append(hand_label(24, 28, "47 counties · one crew", p, size=11, fill=p["mute"]))
    parts.append(hand_label(24, 200, "fig. 3  field ops coverage (sketch)", p, size=10, fill=p["mute"]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Coverage sketch">
  {''.join(parts)}
</svg>
'''


def write(name: str, body: str) -> None:
    path = OUT / name
    path.write_text(body, encoding="utf-8")
    print(f"wrote {path.name:28s} {path.stat().st_size:7d} bytes")


def main() -> None:
    for mode in ("light", "dark"):
        RNG.seed(1931)  # same wobble each regeneration
        write(f"hero-attractor-{mode}.svg", hero(mode))  # keep filename README already uses
        write(f"glyph-{mode}.svg", glyph(mode))
        write(f"case-index-{mode}.svg", case_card(mode))
        write(f"sketch-coverage-{mode}.svg", sketch_pad(mode))


if __name__ == "__main__":
    main()
