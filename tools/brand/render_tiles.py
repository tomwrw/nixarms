"""Render the illustrated "What's on tap" tiles (1200x600 PNG)."""
import subprocess
from xml.sax.saxutils import escape

import os
import tempfile
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / "themes/nixarms/assets/img/specials"
OUT = tempfile.mkdtemp()
W, H = 1200, 600
MONO = "JetBrains Mono"
SANS = "Work Sans"


def save(name, body, bg):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')
    p = f"{OUT}/{name}.svg"
    open(p, "w").write(svg)
    subprocess.run(["rsvg-convert", "-w", str(W), p, "-o", f"{OUT}/{name}.png"], check=True)
    Image.open(f"{OUT}/{name}.png").convert("RGB").save(DEST / f"{name}.jpg", quality=88)


def window(x, y, w, h, title, bg="#1D2021", bar="#2A2D2E"):
    dots = "".join(f'<circle cx="{x + 22 + i * 20}" cy="{y + 18}" r="6" fill="{c}"/>'
                   for i, c in enumerate(["#E06C5A", "#E0B25A", "#8FBF7A"]))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{bg}"/>'
            f'<path d="M{x} {y + 12}a12 12 0 0 1 12-12h{w - 24}a12 12 0 0 1 12 12v24h-{w}z" fill="{bar}"/>'
            f'{dots}<text x="{x + w / 2}" y="{y + 23}" text-anchor="middle" font-family="{SANS}" '
            f'font-size="15" font-weight="500" fill="#A89F91">{escape(title)}</text>')


def spans(parts, x, y, size):
    """parts: list of (text, colour). Monospace line."""
    t = "".join(f'<tspan fill="{c}">{escape(s)}</tspan>' for s, c in parts)
    return f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" xml:space="preserve">{t}</text>'


FG, KEY, STR, BOOL, CMT, PUN, NUM = "#EBDBB2", "#83A598", "#B8BB26", "#D3869B", "#928374", "#A89984", "#FE8019"

# ---------- 1. gaming.nix in an editor + rebuild terminal ----------
code = [
    [("{ pkgs, ... }:", PUN)],
    [("{", PUN)],
    [("  programs.steam", KEY), (" = {", PUN)],
    [("    enable", KEY), (" = ", PUN), ("true", BOOL), (";", PUN)],
    [("    remotePlay.openFirewall", KEY), (" = ", PUN), ("true", BOOL), (";", PUN)],
    [("    gamescopeSession.enable", KEY), (" = ", PUN), ("true", BOOL), (";", PUN)],
    [("  };", PUN)],
    [("  programs.gamemode.enable", KEY), (" = ", PUN), ("true", BOOL), (";", PUN)],
    [("  hardware.graphics.enable", KEY), (" = ", PUN), ("true", BOOL), (";", PUN)],
    [("", FG)],
    [("  environment.systemPackages", KEY), (" = ", PUN), ("with", BOOL), (" pkgs; [", PUN)],
    [("    mangohud heroic lutris protonup-qt", FG)],
    [("  ];", PUN)],
    [("}", PUN)],
]
b = window(40, 30, 760, 540, "gaming.nix - ~/nix-config/modules")
for i, line in enumerate(code):
    y = 100 + i * 33
    b += f'<text x="70" y="{y}" font-family="{MONO}" font-size="17" fill="#5A5550" text-anchor="end">{i + 1}</text>'
    b += spans(line, 90, y, 20)
# terminal overlay
term = [
    [("$ ", "#8EC07C"), ("sudo nixos-rebuild switch", FG)],
    [("building the system configuration...", CMT)],
    [("activating the configuration...", CMT)],
    [("setting up /etc...", CMT)],
    [("✓ ", "#8EC07C"), ("generation 43 activated", FG)],
]
b += window(640, 330, 520, 240, "zsh - endgame", bg="#141617", bar="#232526")
for i, line in enumerate(term):
    b += spans(line, 664, 395 + i * 34, 17)
save("tile-gaming", b, "#1A1512")

# ---------- 2. one repo -> three machines ----------
CREAM, GREEN, GOLD, INK = "#F5EEDF", "#1F4A39", "#E0B25A", "#2B201A"
b = ""
# repo box
b += f'<rect x="50" y="200" width="380" height="200" rx="18" fill="{CREAM}"/>'
b += f'<text x="240" y="262" text-anchor="middle" font-family="{SANS}" font-weight="600" font-size="15" letter-spacing="3" fill="#8E2F1F">ONE GIT REPO</text>'
b += f'<text x="240" y="306" text-anchor="middle" font-family="{MONO}" font-weight="500" font-size="30" fill="{INK}">nix-config/</text>'
b += f'<text x="240" y="346" text-anchor="middle" font-family="{MONO}" font-size="17" fill="#5E5047">flake.nix · hosts/ · modules/</text>'
hosts = [("endgame", "Gaming desktop", 165), ("flatmate", "Surface Pro tablet", 345)]
for name, desc, y in hosts:
    b += (f'<path d="M430 300 C 540 300, 560 {y + 45}, 690 {y + 45}" fill="none" stroke="{GOLD}" stroke-width="4"/>'
          f'<path d="M690 {y + 33} l18 12 -18 12z" fill="{GOLD}"/>')
    b += f'<rect x="712" y="{y}" width="420" height="90" rx="16" fill="#2E5A47" stroke="{GOLD}" stroke-width="2"/>'
    b += f'<text x="744" y="{y + 42}" font-family="{MONO}" font-weight="500" font-size="26" fill="{CREAM}">{name}</text>'
    b += f'<text x="744" y="{y + 72}" font-family="{SANS}" font-size="19" fill="#CFC4AE">{escape(desc)}</text>'
b += f'<text x="240" y="450" text-anchor="middle" font-family="{SANS}" font-size="18" fill="#CFC4AE">change it once, and both machines follow</text>'
save("tile-machines", b, GREEN)

# ---------- 3. try an app without installing it ----------
P, PS = "#8EC07C", "#83A598"
lines = [
    [("~ ", PS), ("$ ", P), ("cowsay hello", FG)],
    [("zsh: command not found: cowsay", "#FB4934")],
    [("~ ", PS), ("$ ", P), ("nix-shell -p cowsay", FG)],
    [("[nix-shell:~]$ ", "#FABD2F"), ('cowsay "Fancy a pint?"', FG)],
    [(" _______________", FG)],
    [("< Fancy a pint? >", FG)],
    [(" ---------------", FG)],
    [("        \\   ^__^", FG)],
    [("         \\  (oo)\\_______", FG)],
    [("            (__)\\       )\\/\\", FG)],
    [("                ||----w |", FG)],
    [("                ||     ||", FG)],
    [("[nix-shell:~]$ ", "#FABD2F"), ("exit", FG)],
    [("~ ", PS), ("$ ", P), ("cowsay hello", FG)],
    [("zsh: command not found: cowsay", "#FB4934"), ("   # gone, no leftovers", CMT)],
]
b = window(60, 20, 1080, 560, "zsh - ~")
for i, line in enumerate(lines):
    b += spans(line, 90, 82 + i * 32.5, 19)
save("tile-shell", b, "#2B201A")

# ---------- 4. systemd-boot generations ----------
entries = [
    "NixOS (Generation 128 NixOS Yarara 26.05.20261110.3a2f1c0 (Linux 6.18.18), built on 2026-11-10)",
    "NixOS (Generation 127 NixOS Yarara 26.05.20261108.9be04d1 (Linux 6.18.17), built on 2026-11-08)",
    "NixOS (Generation 126 NixOS Yarara 26.05.20261104.51c7e2a (Linux 6.18.17), built on 2026-11-04)",
    "NixOS (Generation 125 NixOS Yarara 26.05.20261101.0d8f6b3 (Linux 6.18.16), built on 2026-11-01)",
    "NixOS (Generation 124 NixOS Yarara 26.05.20261028.e4a19c7 (Linux 6.18.15), built on 2026-10-28)",
    "NixOS (Generation 123 NixOS Yarara 26.05.20261025.7c3d0f2 (Linux 6.18.15), built on 2026-10-25)",
    "Reboot Into Firmware Interface",
]
b = ""
y0, lh, sel = 190, 34, 1
for i, e in enumerate(entries):
    y = y0 + i * lh
    if i == sel:
        b += f'<rect x="20" y="{y - 24}" width="{W - 40}" height="{lh}" fill="#BFBFBF"/>'
    col = "#000000" if i == sel else "#BFBFBF"
    b += f'<text x="{W / 2}" y="{y}" text-anchor="middle" font-family="{MONO}" font-size="15.5" fill="{col}" xml:space="preserve">{escape(e)}</text>'
b += (f'<text x="{W / 2}" y="520" text-anchor="middle" font-family="{SANS}" font-size="19" fill="#8A8A8A">'
      f'Last night’s update misbehaving? Pick yesterday’s generation and carry on.</text>')
save("tile-generations", b, "#000000")
print("done")
