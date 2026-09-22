#!/usr/bin/env python3
"""Field-notebook forge v3 — alive, crooked, creative. Plotter hand, not AI neon."""
from __future__ import annotations

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]
RNG = random.Random(1931)


def palette(mode: str) -> dict:
    if mode == "dark":
        return {
            "paper": "#1A1712",
            "ink": "#F0E6D2",
            "mute": "#A89B84",
            "pencil": "#C4A574",
            "red": "#E23D28",
            "blue": "#6B9AC4",
            "rule": "#2E2820",
            "tape": "#8B7355",
            "green": "#7A9E7E",
        }
    return {
        "paper": "#F3EDE2",
        "ink": "#1C1917",
        "mute": "#6B6358",
        "pencil": "#5C5346",
        "red": "#C23B22",
        "blue": "#2F5D8C",
        "rule": "#D9D0C0",
        "tape": "#C4B8A0",
        "green": "#3D6B4F",
    }


def wobble(x1, y1, x2, y2, amp=1.2, segs=6):
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
    return wobble_poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], amp=amp, closed=True)


def curly_arrow(x1, y1, x2, y2, p, color_key="red", swing=18):
    """Loose margin arrow like someone pointed at the diagram."""
    mx, my = (x1 + x2) / 2 + RNG.uniform(-swing, swing), (y1 + y2) / 2 + RNG.uniform(-swing, swing)
    d = (
        f"M{x1:.1f} {y1:.1f} Q{mx:.1f} {my:.1f} {x2:.1f} {y2:.1f}"
    )
    col = p[color_key]
    head = wobble_poly(
        [(x2 - 9, y2 - 7), (x2, y2), (x2 - 8, y2 + 8)],
        amp=0.6,
    )
    return (
        f'<path d="{d}" fill="none" stroke="{col}" stroke-width="1.4" stroke-linecap="round" opacity="0.9">'
        f'<animate attributeName="stroke-dashoffset" values="240;0" dur="2.8s" begin="0.3s" fill="freeze"/>'
        f"</path>"
        f'<path d="{head}" fill="none" stroke="{col}" stroke-width="1.3"/>'
    )


def paper_bg(p, w, h, breathe=True):
    rules = []
    for yy in range(48, h, 28):
        rules.append(
            f'<path d="{wobble(24, yy, w - 24, yy, amp=0.55, segs=9)}" stroke="{p["rule"]}" stroke-width="0.7" fill="none" opacity="0.5"/>'
        )
    flecks = []
    for _ in range(120):
        fx, fy = RNG.uniform(6, w - 6), RNG.uniform(6, h - 6)
        r = RNG.uniform(0.25, 1.2)
        flecks.append(
            f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="{r:.1f}" fill="{p["mute"]}" opacity="{RNG.uniform(0.03, 0.11):.2f}"/>'
        )
    # paper grain wash that breathes almost imperceptibly
    wash = ""
    if breathe:
        wash = (
            f'<rect width="{w}" height="{h}" fill="{p["pencil"]}" opacity="0.03">'
            f'<animate attributeName="opacity" values="0.02;0.05;0.02" dur="7s" repeatCount="indefinite"/>'
            f"</rect>"
        )
    return f'<rect width="{w}" height="{h}" fill="{p["paper"]}"/>' + "".join(rules) + "".join(flecks) + wash


def stamp(cx, cy, text, p, rot=-8, size=13, press=True):
    w = len(text) * size * 0.62 + 22
    h = size + 16
    # stamp presses on, settles, breathes ink
    anim = ""
    if press:
        anim = (
            f'<animateTransform attributeName="transform" type="rotate" values="{rot+4} {cx} {cy};{rot} {cx} {cy};{rot} {cx} {cy}" '
            f'keyTimes="0;0.15;1" dur="4.5s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.45;0.85;0.7;0.78;0.45" dur="4.5s" repeatCount="indefinite"/>'
        )
    return (
        f'<g transform="rotate({rot} {cx} {cy})">{anim}'
        f'<path d="{wobble_rect(cx - w / 2, cy - h / 2, w, h, amp=2.2)}" fill="none" stroke="{p["red"]}" stroke-width="2.2"/>'
        f'<path d="{wobble_rect(cx - w / 2 + 3, cy - h / 2 + 3, w - 6, h - 6, amp=1.6)}" fill="none" stroke="{p["red"]}" stroke-width="0.8" opacity="0.55"/>'
        f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" '
        f'font-size="{size}" font-weight="700" fill="{p["red"]}" letter-spacing="1.2">{text}</text>'
        f"</g>"
    )


def tape(x, y, w, h, p, rot=6):
    return (
        f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})" opacity="0.5">'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{p["tape"]}"/>'
        f'<path d="{wobble(x, y + h / 2, x + w, y + h / 2, amp=0.7)}" stroke="{p["mute"]}" stroke-width="0.5" fill="none" opacity="0.35"/>'
        f"</g>"
    )


def hand_label(x, y, text, p, size=12, fill=None, family=None, rot=0):
    fam = family or "ui-monospace,Menlo,Consolas,monospace"
    fill = fill or p["ink"]
    dy = RNG.uniform(-1.0, 1.0)
    dx = RNG.uniform(-0.6, 0.6)
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return (
        f'<text x="{x + dx:.1f}" y="{y + dy:.1f}" font-family="{fam}" font-size="{size}" fill="{fill}"{tr}>{text}</text>'
    )


def pen_draw(d, color, dur=6, width=1.6, begin=0, dash="0 2200;2200 0"):
    """The line is being drawn — living stroke, not a static path."""
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">'
        f'<animate attributeName="stroke-dasharray" values="{dash}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
        f"</path>"
    )


def ink_bleed(cx, cy, p, r0=6, color_key="blue"):
    """Blot that swells and fades like ink into fiber."""
    col = p[color_key]
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r0}" fill="{col}" opacity="0.15">'
        f'<animate attributeName="r" values="{r0};{r0 * 2.4};{r0}" dur="5.5s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.18;0.04;0.18" dur="5.5s" repeatCount="indefinite"/>'
        f"</circle>"
        f'<circle cx="{cx}" cy="{cy}" r="{r0 * 0.45}" fill="{col}" opacity="0.22"/>'
    )


def doodle_star(x, y, p, size=8, color_key="pencil"):
    """Margin star — bored student energy."""
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = size if i % 2 == 0 else size * 0.45
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return (
        f'<path d="{wobble_poly(pts, amp=0.7, closed=True)}" fill="none" stroke="{p[color_key]}" stroke-width="1.1" opacity="0.7">'
        f'<animateTransform attributeName="transform" type="rotate" values="0 {x} {y};3 {x} {y};0 {x} {y}" dur="6s" repeatCount="indefinite"/>'
        f"</path>"
    )


def spiral_scribble(x, y, p, turns=3, scale=14, color_key="pencil"):
    pts = []
    n = turns * 24
    for i in range(n):
        t = i / n
        a = t * turns * 2 * math.pi
        r = scale * t
        pts.append((x + r * math.cos(a), y + r * math.sin(a)))
    return pen_draw(wobble_poly(pts, amp=0.5), p[color_key], dur=9, width=1.1, begin=0.8, dash="400 0")


def coffee_ring(cx, cy, p, r=34):
    """Office tell that slowly stains / breathes."""
    return (
        f'<g opacity="0.55">'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{p["pencil"]}" stroke-width="3.2" opacity="0.16">'
        f'<animate attributeName="r" values="{r};{r + 1.5};{r}" dur="8s" repeatCount="indefinite"/>'
        f"</circle>"
        f'<circle cx="{cx}" cy="{cy}" r="{r - 4}" fill="none" stroke="{p["pencil"]}" stroke-width="1" opacity="0.12"/>'
        f'<circle cx="{cx + 3}" cy="{cy - 2}" r="{r * 0.35}" fill="{p["pencil"]}" opacity="0.06"/>'
        f"</g>"
    )


def checkbox(x, y, p, checked=True, label="", size=11):
    box = wobble_rect(x, y, 12, 12, amp=0.8)
    mark = ""
    if checked:
        mark = (
            f'<path d="{wobble(x + 2, y + 6, x + 5, y + 10, amp=0.4)} L{wobble(5 + x, 10 + y, x + 11, y + 3, amp=0.4)[1:]}" '
            f'fill="none" stroke="{p["green"]}" stroke-width="1.6"/>'
        )
    # fix mark: simple polyline
    if checked:
        mark = (
            f'<path d="{wobble_poly([(x + 2, y + 7), (x + 5, y + 11), (x + 11, y + 2)], amp=0.5)}" '
            f'fill="none" stroke="{p["green"]}" stroke-width="1.7"/>'
        )
    return (
        f'<path d="{box}" fill="none" stroke="{p["ink"]}" stroke-width="1.2"/>{mark}'
        + (hand_label(x + 20, y + 11, label, p, size=size, fill=p["ink"]) if label else "")
    )


def hero(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 540
    parts = [paper_bg(p, W, H)]

    # red margin rule + corner tape
    parts.append(f'<path d="{wobble(74, 20, 74, H - 18, amp=0.7)}" stroke="{p["red"]}" stroke-width="1.25" fill="none" opacity="0.5"/>')
    parts.append(tape(36, 10, 100, 20, p, rot=-5))
    parts.append(tape(800, 6, 110, 18, p, rot=8))

    # title block
    parts.append(hand_label(98, 58, "SHADRACK BARAKA MWAHANGA", p, size=23, fill=p["ink"], rot=-0.4))
    parts.append(hand_label(98, 82, "ENGINEER · LLB KABARAK · NAKURU / NAIROBI", p, size=11, fill=p["mute"]))
    parts.append(hand_label(98, 106, "CONSTRAINT IS THE BRIEF.", p, size=14, fill=p["red"], rot=-0.6))

    # living ink blots near the title
    parts.append(ink_bleed(700, 52, p, r0=7, color_key="blue"))
    parts.append(ink_bleed(860, 200, p, r0=5, color_key="red"))

    # constraint diagram boxes with breathing outlines
    boxes = [
        (120, 155, 175, 54, "no internet"),
        (120, 245, 175, 54, "feature phone"),
        (120, 335, 175, 54, "QR fraud"),
        (430, 155, 195, 54, "RIS · local models"),
        (430, 245, 195, 54, "USSD check-in"),
        (430, 335, 195, 54, "rotating QR + bind"),
        (720, 155, 175, 54, "ship on USB"),
        (720, 245, 175, 54, "any handset"),
        (720, 335, 175, 54, "screenshot dies"),
    ]
    for i, (x, y, w, h, label) in enumerate(boxes):
        parts.append(
            f'<path d="{wobble_rect(x, y, w, h, amp=1.9)}" fill="none" stroke="{p["ink"]}" stroke-width="1.45">'
            f'<animate attributeName="opacity" values="0.85;1;0.85" dur="{3.2 + i * 0.25:.1f}s" repeatCount="indefinite"/>'
            f"</path>"
        )
        parts.append(hand_label(x + 12, y + 32, label, p, size=11, fill=p["ink"]))

    connectors = [
        ((295, 182), (430, 182)),
        ((295, 272), (430, 272)),
        ((295, 362), (430, 362)),
        ((625, 182), (720, 182)),
        ((625, 272), (720, 272)),
        ((625, 362), (720, 362)),
    ]
    for i, ((x1, y1), (x2, y2)) in enumerate(connectors):
        parts.append(pen_draw(wobble(x1, y1, x2, y2, amp=2.4, segs=9), p["ink"], dur=5.2 + i * 0.3, width=1.35, begin=i * 0.15))
        parts.append(
            f'<path d="{wobble_poly([(x2 - 10, y2 - 6), (x2, y2), (x2 - 10, y2 + 6)], amp=0.7)}" fill="none" stroke="{p["ink"]}" stroke-width="1.3"/>'
        )

    # life in the margins: arrows, stars, spiral, checklist
    parts.append(curly_arrow(300, 430, 410, 400, p, "red", swing=22))
    parts.append(hand_label(310, 455, "field proof, not slide deck", p, size=12, fill=p["red"], rot=-2))
    parts.append(doodle_star(80, 470, p, size=9, color_key="pencil"))
    parts.append(doodle_star(880, 470, p, size=7, color_key="blue"))
    parts.append(spiral_scribble(860, 100, p, turns=3, scale=12, color_key="pencil"))
    parts.append(coffee_ring(880, 420, p, r=32))

    parts.append(checkbox(100, 480, p, True, "USSD path works offline"))
    parts.append(checkbox(320, 480, p, True, "QR dies in 5s"))
    parts.append(checkbox(520, 480, p, False, "ship the stick"))

    parts.append(stamp(760, 70, "FIELD COPY", p, rot=-12, size=12, press=True))
    parts.append(hand_label(98, 520, "ref: shadrackb1.github.io/playground/lab.html", p, size=10, fill=p["mute"]))

    # squiggle underline under name that redraws
    parts.append(pen_draw(wobble(98, 66, 420, 68, amp=2.5, segs=14), p["blue"], dur=7, width=1.2, begin=1))

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Living field notebook">
  {''.join(parts)}
</svg>
'''


def glyph(mode: str) -> str:
    p = palette(mode)
    cx, cy = 100, 100
    circ = wobble_poly(
        [(cx + 62 * math.cos(a), cy + 62 * math.sin(a)) for a in [i * math.pi / 16 for i in range(32)]],
        amp=1.8,
        closed=True,
    )
    inner = wobble_poly(
        [(cx + 54 * math.cos(a), cy + 54 * math.sin(a)) for a in [i * math.pi / 14 for i in range(28)]],
        amp=1.3,
        closed=True,
    )
    # stamp presses in
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img" aria-label="SBM living stamp">
  <rect width="200" height="200" fill="{p["paper"]}"/>
  <g>
    <animate attributeName="opacity" values="0.55;0.95;0.55" dur="4s" repeatCount="indefinite"/>
    <animateTransform attributeName="transform" type="rotate" values="-4 100 100;-1 100 100;-4 100 100" dur="4s" repeatCount="indefinite"/>
    <path d="{circ}" fill="none" stroke="{p["red"]}" stroke-width="2.5"/>
    <path d="{inner}" fill="none" stroke="{p["red"]}" stroke-width="1"/>
    <text x="100" y="112" text-anchor="middle" font-family="Georgia,Times New Roman,serif" font-size="42" font-weight="700" fill="{p["ink"]}">SBM</text>
    <path d="{wobble(58, 138, 142, 138, amp=1.1)}" stroke="{p["red"]}" stroke-width="1.2" fill="none"/>
    <text x="100" y="158" text-anchor="middle" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="10" fill="{p["mute"]}">FIELD · KENYA</text>
  </g>
  {ink_bleed(40, 40, p, r0=5, color_key="blue")}
</svg>
'''


def case_card(mode: str) -> str:
    p = palette(mode)
    W, H = 960, 380
    parts = [paper_bg(p, W, H)]
    parts.append(hand_label(40, 40, "INDEX OF SHIPPED SYSTEMS", p, size=16))
    parts.append(hand_label(40, 62, "file under: constraint → response · rev 2026.09", p, size=10, fill=p["mute"]))
    parts.append(stamp(870, 50, "OPEN", p, rot=7, size=11))
    parts.append(doodle_star(40, 340, p, size=8, color_key="red"))
    parts.append(spiral_scribble(900, 320, p, turns=2, scale=10, color_key="pencil"))

    rows = [
        ("RIS", "USB offline research", "labs without net"),
        ("KSAS", "expiring QR + device", "screenshot fraud"),
        ("Juriscore", "briefs + citations", "PDF hell"),
        ("USSD att.", "dial on any phone", "no app store"),
        ("FieldOps", "sites · fuel · 47", "distributed crews"),
        ("EFK", "M-Pesa entry", "cash rails"),
    ]
    y = 100
    for i, (name, what, why) in enumerate(rows):
        parts.append(f'<path d="{wobble(40, y, 920, y, amp=0.65, segs=11)}" stroke="{p["rule"]}" stroke-width="0.85" fill="none"/>')
        # row breathes slightly
        parts.append(
            f'<g><animate attributeName="opacity" values="0.88;1;0.88" dur="{3.8 + i * 0.4:.1f}s" repeatCount="indefinite"/>'
            + hand_label(48, y - 10, name, p, size=13, fill=p["ink"])
            + hand_label(220, y - 10, what, p, size=12, fill=p["pencil"])
            + hand_label(560, y - 10, why, p, size=12, fill=p["red"])
            + "</g>"
        )
        y += 42
    parts.append(f'<path d="{wobble(40, y, 920, y, amp=0.65, segs=11)}" stroke="{p["rule"]}" stroke-width="0.85" fill="none"/>')
    parts.append(tape(860, 330, 55, 14, p, rot=-9))
    parts.append(hand_label(48, 360, "✓ signed off in the field  ·  ☕ third cup", p, size=11, fill=p["mute"]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Living case index">
  {''.join(parts)}
</svg>
'''


def sketch_pad(mode: str) -> str:
    p = palette(mode)
    W, H = 480, 240
    parts = [paper_bg(p, W, H)]
    path_pts = [(240 + 70 * math.cos(i / 47 * 2 * math.pi), 115 + 52 * math.sin(i / 47 * 2 * math.pi)) for i in range(48)]
    d = wobble_poly(path_pts, amp=1.6, closed=True)
    lat = wobble(175, 100, 305, 100, amp=2.2)
    lat2 = wobble(180, 132, 300, 132, amp=2.2)
    lon = wobble(240, 62, 240, 168, amp=2.2)
    parts.append(pen_draw(d, p["ink"], dur=8.5, width=1.55, begin=0))
    parts.append(pen_draw(lat, p["pencil"], dur=5, width=1, begin=0.6))
    parts.append(pen_draw(lat2, p["pencil"], dur=5, width=1, begin=1.0))
    parts.append(pen_draw(lon, p["pencil"], dur=5, width=1, begin=1.4))
    for i in range(14):
        a = i * 2.35
        x = 240 + 56 * math.cos(a)
        y = 115 + 40 * math.sin(a * 1.3)
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{2 + (i % 3) * 0.4:.1f}" fill="{p["red"]}">'
            f'<animate attributeName="opacity" values="0.25;1;0.25" dur="{2.2 + i * 0.13:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="r" values="1.6;2.8;1.6" dur="{2.2 + i * 0.13:.2f}s" repeatCount="indefinite"/>'
            f"</circle>"
        )
    parts.append(hand_label(22, 28, "47 counties · one crew", p, size=11, fill=p["mute"]))
    parts.append(hand_label(22, 220, "fig. 3  field ops coverage (sketch)", p, size=10, fill=p["mute"]))
    parts.append(doodle_star(450, 30, p, size=7, color_key="blue"))
    parts.append(curly_arrow(400, 50, 320, 80, p, "red", swing=12))
    parts.append(ink_bleed(60, 180, p, r0=6, color_key="blue"))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Living coverage sketch">
  {''.join(parts)}
</svg>
'''


def margin_life(mode: str) -> str:
    """Dedicated strip: pure margin energy — bullets, coffee, to-dos, stars."""
    p = palette(mode)
    W, H = 480, 160
    parts = [paper_bg(p, W, H)]
    parts.append(hand_label(16, 28, "NOTES TO SELF", p, size=12, fill=p["red"], rot=-1))
    parts.append(checkbox(20, 48, p, True, "lab holds people past the scroll"))
    parts.append(checkbox(20, 78, p, True, "ink wobbles on purpose"))
    parts.append(checkbox(20, 108, p, False, "write the Kisii field memo"))
    parts.append(spiral_scribble(420, 40, p, turns=2, scale=9, color_key="blue"))
    parts.append(doodle_star(430, 120, p, size=8, color_key="red"))
    parts.append(coffee_ring(400, 140, p, r=14))
    parts.append(pen_draw(wobble(20, 130, 280, 134, amp=3, segs=12), p["blue"], dur=6, width=1.1, begin=0.4))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Margin notes">
  {''.join(parts)}
</svg>
'''


def write(name: str, body: str) -> None:
    path = OUT / name
    path.write_text(body, encoding="utf-8")
    print(f"wrote {path.name:28s} {path.stat().st_size:7d} bytes")


def main() -> None:
    for mode in ("light", "dark"):
        RNG.seed(1931)
        write(f"hero-attractor-{mode}.svg", hero(mode))
        write(f"glyph-{mode}.svg", glyph(mode))
        write(f"case-index-{mode}.svg", case_card(mode))
        write(f"sketch-coverage-{mode}.svg", sketch_pad(mode))
        write(f"margin-notes-{mode}.svg", margin_life(mode))


if __name__ == "__main__":
    main()
