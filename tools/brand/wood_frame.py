"""Generate a 9-slice wooden picture-frame SVG for CSS border-image.

256x256 canvas, frame band 64 units wide (slice 64). Mitred corners; grain runs
along each piece; bevel = dark outer edge, raised moulding highlight, dark inner lip.
"""
import math
import random

random.seed(7)
S, B = 256, 64  # size, band width

pieces = {
    "top":    [(0, 0), (S, 0), (S - B, B), (B, B)],
    "bottom": [(0, S), (S, S), (S - B, S - B), (B, S - B)],
    "left":   [(0, 0), (B, B), (B, S - B), (0, S)],
    "right":  [(S, 0), (S, S), (S - B, S - B), (S - B, B)],
}


def poly(pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def grain_lines(horizontal, seed):
    """Wavy grain lines across the band (0..B) running along the piece."""
    rnd = random.Random(seed)
    out = []
    t = 3.0
    while t < B - 2:
        amp = rnd.uniform(0.6, 2.2)
        freq = rnd.uniform(0.018, 0.045)
        phase = rnd.uniform(0, math.tau)
        w = rnd.uniform(0.8, 2.4)
        col = rnd.choice(["#4A2E19", "#3E2715", "#5A3920", "#2F1D10"])
        op = rnd.uniform(0.25, 0.6)
        pts = []
        for k in range(0, S + 1, 8):
            off = t + amp * math.sin(k * freq + phase) + 0.8 * math.sin(k * freq * 2.7 + phase * 1.3)
            pts.append((k, off) if horizontal else (off, k))
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w:.1f}" stroke-opacity="{op:.2f}" stroke-linecap="round"/>')
        t += rnd.uniform(3.0, 7.5)
    return out


def mirror(lines, axis):
    """Map grain from the top/left band into bottom/right band coordinates."""
    if axis == "bottom":
        return f'<g transform="translate(0 {S}) scale(1 -1)">{"".join(lines)}</g>'
    if axis == "right":
        return f'<g transform="translate({S} 0) scale(-1 1)">{"".join(lines)}</g>'
    return "".join(lines)


# Base wood: gradient across the band so it reads as a rounded moulding
# (x/y = distance from the outer edge).
defs = [
    '<linearGradient id="gt" x1="0" y1="0" x2="0" y2="64" gradientUnits="userSpaceOnUse">'
    '<stop offset="0" stop-color="#4E311B"/><stop offset="0.18" stop-color="#7A4E2B"/>'
    '<stop offset="0.42" stop-color="#94643A"/><stop offset="0.7" stop-color="#7A4E2B"/>'
    '<stop offset="0.88" stop-color="#5E3C21"/><stop offset="1" stop-color="#3A2413"/></linearGradient>',
]
for name, (x1, y1, x2, y2) in {"gb": (0, 256, 0, 192), "gl": (0, 0, 64, 0), "gr": (256, 0, 192, 0)}.items():
    defs.append(
        f'<linearGradient id="{name}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" gradientUnits="userSpaceOnUse">'
        '<stop offset="0" stop-color="#4E311B"/><stop offset="0.18" stop-color="#7A4E2B"/>'
        '<stop offset="0.42" stop-color="#94643A"/><stop offset="0.7" stop-color="#7A4E2B"/>'
        '<stop offset="0.88" stop-color="#5E3C21"/><stop offset="1" stop-color="#3A2413"/></linearGradient>')
for name, pts in pieces.items():
    defs.append(f'<clipPath id="c{name}"><polygon points="{poly(pts)}"/></clipPath>')

body = []
grad = {"top": "gt", "bottom": "gb", "left": "gl", "right": "gr"}
# light from top-left: top & left slightly brighter, bottom & right slightly darker
tone = {"top": ("#FFF3DC", 0.10), "left": ("#FFF3DC", 0.05), "bottom": ("#000", 0.10), "right": ("#000", 0.14)}
seeds = {"top": 11, "bottom": 23, "left": 37, "right": 41}
for name, pts in pieces.items():
    horiz = name in ("top", "bottom")
    g = grain_lines(horiz, seeds[name])
    g = mirror(g, name if name in ("bottom", "right") else "")
    col, op = tone[name]
    body.append(
        f'<g clip-path="url(#c{name})">'
        f'<polygon points="{poly(pts)}" fill="url(#{grad[name]})"/>'
        f'{g}'
        f'<polygon points="{poly(pts)}" fill="{col}" fill-opacity="{op}"/>'
        '</g>')

# moulding highlight line (raised ridge ~ 40% across the band) and inner lip
def ring(inset, color, width, opacity):
    a, b = inset, S - inset
    return (f'<rect x="{a}" y="{a}" width="{b - a}" height="{b - a}" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-opacity="{opacity}"/>')

body.append(ring(1.5, "#24160C", 3, 0.9))          # outer dark edge
body.append(ring(24, "#F2C98A", 2.2, 0.35))        # ridge highlight
body.append(ring(28, "#2A190D", 1.6, 0.35))        # ridge shadow
body.append(ring(B - 3, "#1E120A", 6, 0.75))       # inner lip / shadow onto the board
body.append(ring(B - 7, "#C08A52", 1.6, 0.45))     # inner bead highlight

# mitre joints
for (x1, y1, x2, y2) in [(0, 0, B, B), (S, 0, S - B, B), (0, S, B, S - B), (S, S, S - B, S - B)]:
    body.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1E120A" stroke-width="1.6" stroke-opacity="0.7"/>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">'
       f'<defs>{"".join(defs)}</defs>{"".join(body)}</svg>\n')
from pathlib import Path
root = Path(__file__).resolve().parents[2]
for dest in (root / "brand/wood-frame.svg", root / "themes/nixarms/static/img/brand/wood-frame.svg"):
    dest.write_text(svg)
print(len(svg), "bytes")
