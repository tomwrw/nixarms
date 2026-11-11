"""Fetch the brand's source fonts (SIL OFL) from the Google Fonts repo into tools/brand/.fonts/."""
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
FONT_DIR = HERE / ".fonts"
BASE = "https://raw.githubusercontent.com/google/fonts/main/ofl"
SOURCES = {
    "Fraunces.ttf": f"{BASE}/fraunces/Fraunces%5BSOFT,WONK,opsz,wght%5D.ttf",
    "WorkSans.ttf": f"{BASE}/worksans/WorkSans%5Bwght%5D.ttf",
    "JetBrainsMono.ttf": f"{BASE}/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
}


def ensure_fonts() -> Path:
    FONT_DIR.mkdir(exist_ok=True)
    for name, url in SOURCES.items():
        dest = FONT_DIR / name
        if not dest.exists():
            print(f"downloading {name}")
            urllib.request.urlretrieve(url, dest)
    return FONT_DIR


if __name__ == "__main__":
    print(ensure_fonts())
