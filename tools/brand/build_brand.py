"""Build The Nix Arms production logo files.

Text is converted to outlines (no font dependency), centred on its ink bounds,
and every gap is computed rather than eyeballed.
"""
import io
import math
import os

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

import shutil
from pathlib import Path

from fonts import ensure_fonts

ROOT = Path(__file__).resolve().parents[2]
OUT = str(ROOT / "brand")
FONTS = str(ensure_fonts())
os.makedirs(OUT, exist_ok=True)

GREEN, CREAM, GOLD, INK, RED, BLACK, WHITE = (
    "#1F4A39", "#F5EEDF", "#E0B25A", "#2B201A", "#8E2F1F", "#000000", "#FFFFFF")

ATTRIB = ("NixOS logomark: \"NixOS Logo\" by Simon Frankau, Tim Cuthbertson and Daniel Baker "
          "(maintained by the NixOS Marketing Team), from nixos/branding, licensed under CC BY 4.0 "
          "(https://creativecommons.org/licenses/by/4.0/). Used unaltered.")


# ---------- fonts ----------
def load_font(path, wght=None):
    f = TTFont(path)
    if wght is not None and "fvar" in f:
        f = instancer.instantiateVariableFont(f, {"wght": wght})
    buf = io.BytesIO()
    f.save(buf)
    data = buf.getvalue()
    return TTFont(io.BytesIO(data)), data


def load_axes(path, axes):
    f = TTFont(path)
    f = instancer.instantiateVariableFont(f, axes)
    buf = io.BytesIO()
    f.save(buf)
    data = buf.getvalue()
    return TTFont(io.BytesIO(data)), data


# Brand serif: Fraunces 600, soft, optical size 144, no wonk
SERIF = load_axes(f"{FONTS}/Fraunces.ttf", {"wght": 600, "opsz": 144, "SOFT": 100, "WONK": 0})
SERIF_TRACK_EM = 0.01


def fit_size(font, text, track_em, target_w, max_h):
    size = 40.0
    for _ in range(3):
        _, bb = text_outline(font, text, size, track_em * size)
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        size *= min(target_w / w, max_h / h)
    return size
SANS = load_font(f"{FONTS}/WorkSans.ttf", wght=600)


def text_outline(font, text, size, tracking=0.0, x0=0.0, y0=0.0):
    """Shape with HarfBuzz (kerning on). Returns (path d, ink bbox). Baseline at y0."""
    ft, data = font
    face = hb.Face(data)
    hfont = hb.Font(face)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hfont, buf, {"kern": True, "liga": True})
    s = size / ft["head"].unitsPerEm
    gs = ft.getGlyphSet()
    order = ft.getGlyphOrder()
    x = 0.0
    parts = []
    bb = [math.inf, math.inf, -math.inf, -math.inf]
    infos, poss = buf.glyph_infos, buf.glyph_positions
    for i, (info, pos) in enumerate(zip(infos, poss)):
        name = order[info.codepoint]
        m = (s, 0, 0, -s, x0 + x + pos.x_offset * s, y0 - pos.y_offset * s)
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
        gs[name].draw(TransformPen(pen, m))
        d = pen.getCommands()
        if d:
            parts.append(d)
        bp = BoundsPen(gs)
        gs[name].draw(TransformPen(bp, m))
        if bp.bounds:
            bb = [min(bb[0], bp.bounds[0]), min(bb[1], bp.bounds[1]),
                  max(bb[2], bp.bounds[2]), max(bb[3], bp.bounds[3])]
        x += pos.x_advance * s + (tracking if i < len(infos) - 1 else 0)  # no trailing tracking
    return " ".join(parts), tuple(bb)


def placed_text(font, text, size, tracking, cx, top=None, bottom=None):
    """Centre on ink bounds horizontally; align ink top or ink bottom to a y."""
    _, bb = text_outline(font, text, size, tracking)
    dx = cx - (bb[0] + bb[2]) / 2
    dy = (top - bb[1]) if top is not None else (bottom - bb[3])
    d, bb2 = text_outline(font, text, size, tracking, dx, dy)
    return d, bb2


# ---------- NixOS logomark (official geometry, flat) ----------
def logomark_polys():
    c = lambda a: math.cos(math.radians(a))
    s = lambda a: math.sin(math.radians(a))
    R, T, G = 512, 1 / 4, 1 / 32

    def lam(gap):
        hx = [(R * c(a), R * s(a)) for a in range(0, 360, 60)]
        tl, bl, br = hx[2], hx[4], hx[5]
        v = lambda a: (R * T * c(a), R * T * s(a))
        v0, v60, v270, v300 = v(0), v(60), v(270), v(300)
        g = (2 * R * gap * c(300), 2 * R * gap * s(300))
        add = lambda p, q: (p[0] + q[0], p[1] + q[1])
        sub = lambda p, q: (p[0] - q[0], p[1] - q[1])
        pts = [add(sub(tl, v60), g), add(add(tl, v60), g), add(br, v0), sub(br, v0),
               (math.sqrt(3) * v270[0], math.sqrt(3) * v270[1]), add(bl, v0), bl,
               sub(bl, v300), (-v0[0], -v0[1])]
        return [(x, -y) for x, y in pts]

    apex = lam(0)[1]
    tr = (-apex[0] - R, -apex[1])
    base = [(x + tr[0], y + tr[1]) for x, y in lam(G)]
    rot = lambda p, a: (c(a) * p[0] - s(a) * p[1], s(a) * p[0] + c(a) * p[1])
    flake = [[rot(p, a) for p in base] for a in range(0, 360, 60)]
    cr = max(p[0] for poly in flake for p in poly)
    ir = cr * math.sqrt(3) / 2
    return flake, cr, ir


FLAKE, FLAKE_CR, FLAKE_IR = logomark_polys()


def logomark(cx, cy, height, fill=BLACK):
    """Logomark of given height (flat-top orientation, as published), centred."""
    k = height / (2 * FLAKE_IR)
    d = " ".join("M" + " L".join(f"{cx + x * k:.2f} {cy + y * k:.2f}" for x, y in poly) + "Z"
                 for poly in FLAKE)
    return f'<path d="{d}" fill="{fill}"/>', FLAKE_CR * k  # returns half-width


# ---------- pint glass ----------
def pint(cx, top, w_top, w_bot, h, froth_h, r, body, froth, stroke=None, sw=0):
    """Tapered pint glass; outline drawn inside the given silhouette so ink box = silhouette."""
    i = sw / 2
    xt, xb = w_top / 2 - i, w_bot / 2 - i
    t, b = top + i, top + h - i
    # rounded bottom corners
    body_d = (f"M{cx - xt:.2f} {t:.2f} H{cx + xt:.2f} L{cx + xb:.2f} {b - r:.2f} "
              f"Q{cx + xb:.2f} {b:.2f} {cx + xb - r:.2f} {b:.2f} H{cx - xb + r:.2f} "
              f"Q{cx - xb:.2f} {b:.2f} {cx - xb:.2f} {b - r:.2f} Z")
    # froth band follows the taper
    fy = top + froth_h
    frac = (fy - t) / (b - t)
    xf = xt + (xb - xt) * frac
    froth_d = f"M{cx - xt:.2f} {t:.2f} H{cx + xt:.2f} L{cx + xf:.2f} {fy:.2f} H{cx - xf:.2f} Z"
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    return (f'<path d="{body_d}" fill="{body}"{st}/>'
            f'<path d="{froth_d}" fill="{froth}"{st}/>')


def svg_doc(w, h, body, title, desc=""):
    d = f"<desc>{desc}</desc>" if desc else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{d}{body}</svg>\n')


# ---------- BEER MAT ----------
def beermat(mono=False, serif=None, title_size=42, title_track=0.6, title_text="The Nix Arms"):
    serif = serif or SERIF
    C = 256
    g_out, g_in, keyline = 256, 234, 223      # green disc, cream disc, keyline radius
    kl_w = 2.5
    R_in = keyline - kl_w / 2 - 0.5            # usable content radius
    disc = BLACK if mono else GREEN
    paper = WHITE if mono else CREAM
    txt = BLACK if mono else GREEN
    sub = BLACK if mono else INK
    est = BLACK if mono else RED

    LH = 140                                   # logomark height
    clear = LH / 4                             # brand-guide minimum clear space
    logo, a = logomark(C, C, LH)

    # pint: top width, bottom width, height
    PW, PB, PH = 56, 43, 82
    # solve gap g so logo<->pint gap == pint outer top corner <-> rim gap
    lo, hi = 0.0, 120.0
    for _ in range(60):
        g = (lo + hi) / 2
        outer = a + g + PW
        rim_gap = R_in - math.hypot(outer, PH / 2)
        if rim_gap > g:
            lo = g
        else:
            hi = g
    g = (lo + hi) / 2
    assert g >= clear, (g, clear)
    inner = a + g
    pc_l, pc_r = C - inner - PW / 2, C + inner + PW / 2
    ptop = C - PH / 2
    pint_body = BLACK if mono else GOLD
    pint_froth = WHITE if mono else "#FFFAF0"
    pints = (pint(pc_l, ptop, PW, PB, PH, 17, 6, pint_body, pint_froth, BLACK if mono else INK, 3.5)
             + pint(pc_r, ptop, PW, PB, PH, 17, 6, pint_body, pint_froth, BLACK if mono else INK, 3.5))

    # vertical: equal gap G above and below the logo; bottom block height == title height
    G = 36
    assert G >= clear
    title_d, tbb = placed_text(serif, title_text, title_size, title_track, C, bottom=C - LH / 2 - G)
    Ht = tbb[3] - tbb[1]
    URL_SIZE, URL_TRACK, EST_SIZE, EST_TRACK, LINE_GAP = 23, 5.5, 16, 4.2, 14
    url_d, ubb = placed_text(SANS, "NIX ON TAP", URL_SIZE, URL_TRACK, C, top=C + LH / 2 + G)
    Hu = ubb[3] - ubb[1]
    # place EST line so the bottom block's ink height equals the title's
    _, ebb0 = text_outline(SANS, "EST · GEN 1", EST_SIZE, EST_TRACK)
    He = ebb0[3] - ebb0[1]
    est_bottom = C + LH / 2 + G + max(Ht, Hu + LINE_GAP + He)
    est_d, ebb = placed_text(SANS, "EST · GEN 1", EST_SIZE, EST_TRACK, C, bottom=est_bottom)
    line_gap = ebb[1] - ubb[3]
    shift = ((ebb[3] - ubb[1]) - Ht) / 2

    def corner_margin(bb):
        return R_in - max(math.hypot(x - C, y - C) for x in (bb[0], bb[2]) for y in (bb[1], bb[3]))

    report = {
        "logo half-width": round(a, 2), "clear space min": clear,
        "logo<->pint gap": round(g, 2),
        "pint<->rim gap": round(R_in - math.hypot(a + g + PW, PH / 2), 2),
        "title ink": [round(v, 2) for v in tbb], "title height": round(Ht, 2),
        "title centre x": round((tbb[0] + tbb[2]) / 2, 2),
        "url centre x": round((ubb[0] + ubb[2]) / 2, 2),
        "est centre x": round((ebb[0] + ebb[2]) / 2, 2),
        "bottom block height": round(ebb[3] - ubb[1], 2), "url/est line gap": round(line_gap, 2),
        "title corner->rim": round(corner_margin(tbb), 2),
        "url corner->rim": round(corner_margin(ubb), 2),
        "title top->rim (vertical)": round(tbb[1] - shift - (C - R_in), 2),
        "est bottom->rim (vertical)": round((C + R_in) - (ebb[3] - shift), 2), "content shift up": round(shift, 2),
    }

    body = (f'<circle cx="{C}" cy="{C}" r="{g_out}" fill="{disc}"/>'
            f'<circle cx="{C}" cy="{C}" r="{g_in}" fill="{paper}"/>'
            f'<circle cx="{C}" cy="{C}" r="{keyline}" fill="none" stroke="{disc}" stroke-width="{kl_w}"/>'
            f'<g transform="translate(0 {-shift:.2f})">'
            f'<path d="{title_d}" fill="{txt}"/>'
            f'{logo}{pints}'
            f'<path d="{url_d}" fill="{sub}"/>'
            f'<path d="{est_d}" fill="{est}"/></g>')
    return body, report


# ---------- PINT ICON (avatar) ----------
def pint_icon(simple=False, square_bg=None, ring=GREEN):
    C = 256
    parts = []
    if square_bg:
        parts.append(f'<rect width="512" height="512" fill="{square_bg}"/>')
    if simple:
        # favicon: no outline, no cream disc, bigger glass
        parts.append(f'<circle cx="{C}" cy="{C}" r="256" fill="{GREEN}"/>')
        W, B, H = 236, 180, 324
        parts.append(pint(C, C - H / 2, W, B, H, 72, 22, GOLD, "#FFFAF0"))
    else:
        if not square_bg:
            parts.append(f'<circle cx="{C}" cy="{C}" r="256" fill="{ring}"/>')
        parts.append(f'<circle cx="{C}" cy="{C}" r="216" fill="{CREAM}"/>')
        W, B, H = 190, 146, 268
        parts.append(pint(C, C - H / 2, W, B, H, 58, 18, GOLD, "#FFFAF0", INK, 14))
    return "".join(parts)


# ---------- HEADER LOCKUP ----------
def lockup(dark=True, serif=None, name_size=30, name_track=0.3, name_text="The Nix Arms"):
    serif = serif or SERIF
    icon_h = 64
    s = icon_h / 512
    word_col = CREAM if dark else GREEN
    sub_col = "#CFC4AE" if dark else INK
    gap = 16
    x_text = icon_h + gap
    name_d, nbb = text_outline(serif, name_text, name_size, name_track)
    url_d, ubb = text_outline(SANS, "NIX ON TAP", 14.5, 3.4)
    nh, uh, lg = nbb[3] - nbb[1], ubb[3] - ubb[1], 8
    block = nh + lg + uh
    top = (icon_h - block) / 2
    name_d, nbb = text_outline(serif, name_text, name_size, name_track, x_text - nbb[0], top - nbb[1])
    url_d, ubb = text_outline(SANS, "NIX ON TAP", 14.5, 3.4, x_text - ubb[0], top + nh + lg - ubb[1])
    w = math.ceil(max(nbb[2], ubb[2]))
    body = (f'<g transform="scale({s})">{pint_icon(ring=GOLD if dark else GREEN)}</g>'
            f'<path d="{name_d}" fill="{word_col}"/><path d="{url_d}" fill="{sub_col}"/>')
    return w, icon_h, body


if __name__ == "__main__":
    import json

    ms = fit_size(SERIF, "The Nix Arms", SERIF_TRACK_EM, 258.0, 34.0)
    ls = fit_size(SERIF, "The Nix Arms", SERIF_TRACK_EM, 232.0, 32.0)
    body, rep = beermat(title_size=ms, title_track=SERIF_TRACK_EM * ms)
    open(f"{OUT}/nixarms-beermat.svg", "w").write(
        svg_doc(512, 512, body, "The Nix Arms - Nix on tap", ATTRIB))
    body_m, _ = beermat(mono=True, title_size=ms, title_track=SERIF_TRACK_EM * ms)
    open(f"{OUT}/nixarms-beermat-mono.svg", "w").write(
        svg_doc(512, 512, body_m, "The Nix Arms - Nix on tap (one colour)", ATTRIB))
    open(f"{OUT}/nixarms-pint-icon.svg", "w").write(
        svg_doc(512, 512, pint_icon(), "The Nix Arms"))
    open(f"{OUT}/nixarms-favicon.svg", "w").write(
        svg_doc(512, 512, pint_icon(simple=True), "The Nix Arms"))
    open(f"{OUT}/nixarms-apple-touch.svg", "w").write(
        svg_doc(512, 512, pint_icon(square_bg=GREEN), "The Nix Arms"))
    for dark in (True, False):
        w, h, b = lockup(dark, name_size=ls, name_track=SERIF_TRACK_EM * ls)
        name = "nixarms-lockup-on-dark.svg" if dark else "nixarms-lockup-on-light.svg"
        open(f"{OUT}/{name}", "w").write(svg_doc(w, h, b, "The Nix Arms - Nix on tap"))
    rep["title size"] = round(ms, 2); rep["lockup name size"] = round(ls, 2)
    print(json.dumps(rep, indent=1))

    # Copy the web-facing SVGs into the Hugo theme. PNG/ICO exports: see tools/brand/README.md.
    web = ROOT / "themes/nixarms/static/img/brand"
    for name in ["nixarms-beermat.svg", "nixarms-lockup-on-dark.svg"]:
        shutil.copy(f"{OUT}/{name}", web / name)
    shutil.copy(f"{OUT}/nixarms-favicon.svg", ROOT / "static/favicon.svg")
    print("copied web assets into themes/nixarms/static/img/brand and static/")
