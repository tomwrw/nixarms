---
title: "Five ways to brew the same pint"
eyebrow: "The Brewhouse"
lede: "Every NixOS config ends up describing a computer. What changes is how the recipe is organised: one file, a pinned flake, or a whole brewery of modules. Here's each method, simplest first, with the same order poured every way."
description: "NixOS config styles explained for beginners: vanilla configuration.nix, flakes, flake-parts, the dendritic pattern and den."

firstDay: "**You don't need any of this on day one.** Start with the house pour, which is the `configuration.nix` the installer gives you, and come back when you've got more than one machine, or when your one file starts to feel crowded."

homeManager:
  title: "Home Manager: your own tap"
  text: |
    Home Manager isn't a step on the ladder, because it works with all of them. It does for *your user* what NixOS does for the system: your apps, shell, editor settings and dotfiles, written down and rolled back the same way.

    Most people add it once they're comfortable with the system side. It can run as part of your NixOS config or on its own, even on another Linux distro or a Mac. Start with the [Home Manager manual](https://nix-community.github.io/home-manager/).
---

## One example, five ways

Each page below turns on Steam, so you can compare the methods on the same job. The Steam line is identical every time. What differs is the structure around it, and how well that structure copes as you add machines and users.
