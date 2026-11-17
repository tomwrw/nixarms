---
title: "Stylix"
weight: 60
date: 2026-11-17
checked: 2026-11-17
level: "Second round"
group: "Looks"
plain: "One wallpaper or colour scheme, applied to every app: desktop, terminal, editor and the rest."
lede: "Stylix themes your whole system from one place. Give it a wallpaper and it picks the colours, or give it a colour scheme, and it styles your desktop, terminal, editor and more to match."
description: "Stylix explained for NixOS beginners: one theme for every app, when you need it and what can go wrong."
needIt: "You've spent an evening making every app match by hand, and you'd rather never do that again."
skipIt: "You're happy with your desktop's own look. GNOME and KDE Plasma look good out of the box."
landlord:
  file: "modules/aspects/desktop/stylix.nix"
  text: "Stylix with GNOME's own fonts and cursor, so the desktop still looks like GNOME, just in my colours. The comments explain every font choice."
regularsTag: "Stylix"
mindTheStep:
  - title: "Match the release"
    text: "Stylix's release has to match NixOS's: `release-26.05` with `nixos-26.05`. If you follow unstable, update them together."
  - title: "It themes everything it knows"
    text: "Stylix switches itself on for every app it supports. If one looks wrong, turn off just that one with `stylix.targets.<name>.enable = false;`."
  - title: "Old theme settings can clash"
    text: "Fonts, colours or themes you've set by hand can fight with Stylix's. Take them out and let Stylix set them, or turn that app's target off."
  - title: "Some wallpapers make odd colours"
    text: "A scheme taken from a wallpaper follows the picture. If the result is hard to read, set `stylix.polarity = \"dark\";` or choose a scheme with `stylix.base16Scheme`."
docs:
  - name: "Stylix documentation"
    url: "https://nix-community.github.io/stylix/"
    note: "installation, configuration and the list of supported apps"
  - name: "Stylix on GitHub"
    url: "https://github.com/nix-community/stylix"
---

## The recipe

Add Stylix to your flake, on the release that matches your NixOS:

```nix
# flake.nix, in inputs
stylix.url = "github:nix-community/stylix/release-26.05";
```

Then add `stylix.nixosModules.stylix` to your system's modules, and switch it on:

```nix
{ pkgs, ... }: {
  stylix.enable = true;
  stylix.image = ./wallpaper.png;

  # Or pick a colour scheme instead of taking one from the wallpaper:
  # stylix.base16Scheme = "${pkgs.base16-schemes}/share/themes/gruvbox-dark-hard.yaml";
}
```

## Where it fits

Each app Stylix can style is called a target, and its documentation lists them all. It works with NixOS, Home Manager and nix-darwin, so one theme can follow you from your desktop to your Mac.
