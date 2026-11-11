# The Nix Arms: logo files

All SVGs have their text converted to outlines, so they need no fonts installed.

## Name, address and tagline

| | |
|---|---|
| Name | **The Nix Arms** (always with "The"; never "Nix Arms" or "NixArms") |
| Main web address | **nixarms.com** |
| Redirects (301 to nixarms.com) | nixpub.com, nixontap.com |
| Tagline | **Nix on tap** (sentence case in text; capitals in labels: NIX ON TAP) |

Typical pairings: "The Nix Arms - Nix on tap" for page titles and social bios. The logo and header lockup carry the tagline; give the address (nixarms.com) in the footer, on print and anywhere people need to type it.

## Files

| File | Use |
|---|---|
| `nixarms-beermat.svg` / `png/nixarms-beermat-1024.png` | Main logo: about page, newsletter, stickers, merch |
| `nixarms-beermat-mono.svg` / `png/nixarms-beermat-mono-1024.png` | One-colour version for print and engraving |
| `nixarms-pint-icon.svg` / `png/nixarms-avatar-512.png` | Social avatars, app icon |
| `nixarms-lockup-on-dark.svg` / `-on-light.svg` (+ `@2x` PNGs) | Site header: pint icon plus wordmark |
| `favicon.svg`, `favicon.ico` (16/32/48), `png/favicon-*.png` | Browser favicon |
| `png/apple-touch-icon.png` (180 px) | iOS home-screen icon |

## Rules

- **Minimum size for the beer mat: 82 px wide.** Below that, the NixOS logomark inside it drops under the brand guide's 24 px minimum. Use the pint icon instead.
- **Show the beer mat at 240 px or wider wherever its text needs to be read** (footer, about page). Between 82 and 240 px it works as a mark, but the small lines are decorative.
- Don't recolour, rotate or rearrange the beer mat. The NixOS logomark must stay flat black, upright and unaltered, on the cream (or white, in the mono version).
- Leave clear space around the beer mat of at least 1/8 of its width.

## Colours

| Name | Hex |
|---|---|
| Bottle green | `#1F4A39` |
| Cream | `#F5EEDF` |
| Brass | `#E0B25A` |
| Ink | `#2B201A` |
| Oxblood | `#8E2F1F` |

## Chalkboard frame

`wood-frame.svg` is a 9-slice wooden picture frame for chalkboard panels (board colour `#26302B`). Use it as a CSS border image:

```css
.wood-frame {
  border: 18px solid #6B4426;          /* fallback colour */
  border-image: url(/img/wood-frame.svg) 64 stretch;
}
.wood-frame-lg { border-width: 22px; } /* full-width sections */
```

Use 18px for panels and 22px for full-width sections. Don't add a border radius.

## Typography

| Role | Font | Settings |
|---|---|---|
| Wordmark and headings | **Fraunces** | weight 600, `SOFT` 100, `WONK` 0, optical size automatic (144 in the wordmark) |
| Body text, UI | **Work Sans** | 400 regular, 500 medium |
| Labels, "NIX ON TAP" | **Work Sans** | 600, uppercase, letter-spacing 0.2-0.25em |
| Code | **JetBrains Mono** | 400 |

All are free on Google Fonts (SIL Open Font License).

- Wordmark tracking is +0.01em. Headings are set at 0.
- Always turn the Fraunces `SOFT` axis to 100. The default sharp version loses the friendly-local feel.
- Don't use the `WONK` alternates, as they read as italic in headings.

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,400..700,100&family=Work+Sans:wght@400;500;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
```

```css
h1, h2, h3, .wordmark {
  font-family: "Fraunces", Georgia, serif;
  font-weight: 600;
  font-variation-settings: "SOFT" 100, "WONK" 0;
  font-optical-sizing: auto;
}
body { font-family: "Work Sans", system-ui, sans-serif; }
code, pre { font-family: "JetBrains Mono", monospace; }
```

## Favicon HTML

```html
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
```

## Attribution (required: the NixOS logomark is CC BY 4.0)

Put this in the site footer or credits page:

> "NixOS Logo" by Simon Frankau, Tim Cuthbertson and Daniel Baker (maintained by the NixOS Marketing Team), from [nixos/branding](https://github.com/NixOS/branding), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Used unaltered.

The pint icon, wordmark and beer-mat design are original to The Nix Arms. The Nix Arms is not affiliated with or endorsed by the NixOS Foundation.
