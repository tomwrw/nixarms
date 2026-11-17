---
date: 2026-11-16
title: "sodiboo/system"
repo: "sodiboo/system"
author: "sodiboo"
level: "Top shelf"
weight: 60
tags: ["niri", "Home Manager", "Laptop", "Multi-machine", "Servers", "Flakes", "disko", "impermanence", "sops-nix", "Stylix"]
borrow: "niri's settings written as Nix in one file, and checked against niri when you build."
---

A niri desktop kept entirely in config, from the author of niri-flake, alongside a tablet, a VPS and a NAS.

<!--more-->

Start with `personal/niri.mod.nix`. It switches niri on, then writes its settings (input, layout and window rules) as Nix through niri-flake, which checks them against niri at build time, so a typo fails the build instead of your session. The rest of the desktop sits next to it, one feature per file: `waybar.mod.nix`, `stylix.mod.nix`, `lock.mod.nix` and `wallpaper.mod.nix`. Every file ending in `.mod.nix` is loaded automatically, so adding a feature means adding a file. Its README says the config files, not the README, are the source of truth, so read the code.
