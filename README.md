# The Nix Arms

**Nix on tap** · [nixarms.com](https://nixarms.com)

A friendly local for anyone curious about Nix and NixOS. It has beginner guides for people leaving Windows, Arch and Ubuntu, a gaming page, and real configs explained in plain English.

Built with [Hugo](https://gohugo.io), built reproducibly with Nix, and hosted on GitHub Pages.

## Run it locally

```sh
nix develop            # Hugo plus the brand tools
hugo server            # http://localhost:1313, reloads as you edit
```

Or skip the shell:

```sh
nix run                # same as `hugo server`
nix build              # production build in ./result, exactly what CI deploys
```

With [direnv](https://direnv.net), `direnv allow` once and the shell loads automatically.

The site works fully offline: fonts and images are self-hosted. The only external script is GoatCounter (cookieless visit counting), and it only loads on the live site when `params.goatcounter.code` is set in `hugo.toml`. See `content/privacy.md`.

## Where things live

```
content/              Markdown pages
  _index.md           homepage copy (front matter)
  start/              "Start here" guides: windows, arch, ubuntu
  gaming.md
  brewhouse/          config styles, simplest first: vanilla, flakes, flake-parts, dendritic, den
  regulars/           one file per featured config
  menu.md, library.md
data/
  paths.yaml          "What are you drinking?" picker
  specials.yaml       "What's on tap" tiles
  jargon.yaml         The Menu (glossary)
  tips.yaml           "One for the road" tips (homepage, one at random)
  community.yaml      "Where the regulars drink" links (homepage)
  brews.yaml          "Which brew?" helper (The Brewhouse)
  library.yaml        The Library: the bookshelf (docs)
  telly.yaml          The Library: on the telly (videos)
themes/nixarms/       the theme: layouts, shortcodes, CSS, JS, fonts, images
static/               favicon, CNAME
brand/                master brand assets and brand guidelines (brand/README.md)
tools/brand/          scripts that generate the brand assets
```

### Shortcodes for writing pages

```markdown
{{< chalkboard title="What won't come with you" size="lg" grid="true" >}}
{{< chalk-item title="Adobe apps" >}}Try GIMP or Krita.{{< /chalk-item >}}
{{< /chalkboard >}}

{{< status-grid >}}
{{< status kind="ok|tweak|no" title="On tap" >}}Markdown…{{< /status >}}
{{< /status-grid >}}

{{< rounds >}}
{{< round title="Install" time="30 min" >}}Markdown…{{< /round >}}
{{< /rounds >}}

{{< callout eyebrow="…" title="…" url="/gaming/" label="Go →" >}}Text{{< /callout >}}
```

## Submitting a config to The Regulars

Copy any file in `content/regulars/`, fill in the front matter (`repo`, `author`, `level`, `tags`, `borrow`), and write a few plain-English lines. Put `<!--more-->` after the first paragraph, which becomes the card summary. Then open a pull request.

## Licences

- **Code** (the theme's templates, CSS and JavaScript, `flake.nix`, the workflow, and the scripts in `tools/`): [MIT](LICENSE).
- **Written content** (everything in `content/` and `data/`) and the homepage tile images drawn for this site: [CC BY 4.0](LICENSE-content). Reuse it freely; credit "The Nix Arms" with a link to [nixarms.com](https://nixarms.com).

Not covered by either licence:

- **The brand.** The name "The Nix Arms", the beer-mat logo, the pint icon, the lockups, the favicons, the social card and the wooden frame (`brand/`, `themes/nixarms/static/img/brand/`, the icons in `static/`). All rights reserved. Linking to the site with them is fine; please don't use them for your own project.
- **The NixOS logomark** inside the beer mat stays under its own [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) licence (see Credits).
- **The Landlord's photo** (`content/landlord/landlord.jpg`). All rights reserved.
- **Third-party material** keeps its own licence: the two screenshots and the fonts. See [THIRD_PARTY.md](THIRD_PARTY.md).

## Credits

Full notices and licence texts are in [THIRD_PARTY.md](THIRD_PARTY.md).

- NixOS logomark: "NixOS Logo" by Simon Frankau, Tim Cuthbertson and Daniel Baker (NixOS Marketing Team), from [nixos/branding](https://github.com/NixOS/branding), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Used unaltered.
- Fonts: Fraunces, Work Sans and JetBrains Mono, all under the SIL Open Font License (`themes/nixarms/static/fonts/`).
- Screenshots: [Frost-Phoenix/nixos-config](https://github.com/Frost-Phoenix/nixos-config) (MIT) and [gethomepage/homepage](https://github.com/gethomepage/homepage) (GPL-3.0).

The Nix Arms is a community site and isn't affiliated with the NixOS Foundation.
