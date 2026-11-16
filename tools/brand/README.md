# Brand tools

Scripts that generate The Nix Arms brand assets. Run them from `nix develop`, which provides Python with fontTools, uharfbuzz and Pillow, plus `rsvg-convert`. The first run downloads the source fonts (SIL OFL) into `tools/brand/.fonts/`, which git ignores.

| Script | What it does |
|---|---|
| `build_brand.py` | Builds the beer mat (colour and mono), the pint icon, favicons and the header lockups into `brand/`. Text is converted to outlines and centred on the actual letter shapes. It also copies the web SVGs into the theme. Prints a spacing report. |
| `wood_frame.py` | The 9-slice wooden chalkboard frame → `brand/wood-frame.svg` and the theme. |
| `build_webfonts.py` | Latin-subset variable woff2 fonts → `themes/nixarms/static/fonts/`. |

```sh
cd tools/brand
python3 build_brand.py      # logos, then re-export PNGs/ICO below
python3 wood_frame.py
python3 build_webfonts.py
```

The PNG and ICO exports in `brand/png/` and `brand/favicon.ico` come from the SVGs:

```sh
cd brand
rsvg-convert -w 1024 nixarms-beermat.svg -o png/nixarms-beermat-1024.png
rsvg-convert -w 1024 nixarms-beermat-mono.svg -o png/nixarms-beermat-mono-1024.png
rsvg-convert -w 512 nixarms-pint-icon.svg -o png/nixarms-avatar-512.png
rsvg-convert -w 180 nixarms-apple-touch.svg -o png/apple-touch-icon.png
for s in 16 32 48 192; do rsvg-convert -w $s nixarms-favicon.svg -o png/favicon-$s.png; done
rsvg-convert -z 2 nixarms-lockup-on-dark.svg -o png/nixarms-lockup-on-dark@2x.png
rsvg-convert -z 2 nixarms-lockup-on-light.svg -o png/nixarms-lockup-on-light@2x.png
python3 -c "from PIL import Image; i=[Image.open(f'png/favicon-{s}.png') for s in (16,32,48)]; i[2].save('favicon.ico', sizes=[(16,16),(32,32),(48,48)], append_images=i[:2])"
cp favicon.ico ../static/ && cp png/apple-touch-icon.png ../static/
```

## Rules the scripts enforce

The scripts check these, and will fail if one is broken:

- The NixOS logomark is generated from the official geometry in [nixos/branding](https://github.com/NixOS/branding). It's flat black and never rotated, distorted or recoloured.
- The gaps around the logomark are never smaller than a quarter of its height, the brand guide's minimum.
