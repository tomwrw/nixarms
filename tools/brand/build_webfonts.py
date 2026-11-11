"""Build the self-hosted web fonts (Latin subset, variable woff2) into themes/nixarms/static/fonts/.

Fraunces is pinned to SOFT=100, WONK=0 (brand setting) and keeps its weight + optical-size axes.
"""
import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

from fonts import ensure_fonts

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "themes/nixarms/static/fonts"
UNICODES = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,"
            "U+2074,U+20AC,U+2122,U+2190-2199,U+2212,U+2215,U+2713,U+2714,U+2717,U+FEFF,U+FFFD")


def build(src: Path, axes: dict, out: str) -> None:
    font = TTFont(src, lazy=False)
    font = instancer.instantiateVariableFont(font, axes)
    buf = io.BytesIO()
    font.save(buf)
    buf.seek(0)
    font = TTFont(buf, lazy=False)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.name_IDs = ["*"]
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=subset.parse_unicodes(UNICODES))
    sub.subset(font)
    font.flavor = "woff2"
    font.save(OUT / out)
    print(f"{out}: {(OUT / out).stat().st_size // 1024} KB")


if __name__ == "__main__":
    src = ensure_fonts()
    OUT.mkdir(parents=True, exist_ok=True)
    build(src / "Fraunces.ttf", {"wght": (400, 700), "opsz": (9, 144), "SOFT": 100, "WONK": 0}, "fraunces-soft-var.woff2")
    build(src / "WorkSans.ttf", {"wght": (400, 700)}, "work-sans-var.woff2")
    build(src / "JetBrainsMono.ttf", {"wght": (400, 600)}, "jetbrains-mono-var.woff2")
