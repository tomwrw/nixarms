---
title: "You already like control. Now keep it."
linkTitle: "Coming from Arch"
date: 2026-11-11
weight: 20
eyebrow: "Your order · Coming from Arch"
lede: "Everything you've hand-tuned in Arch, written down as code you can push to git and rebuild on any machine."
description: "Coming to NixOS from Arch Linux: how pacman, the AUR, systemd units and dotfiles translate to Nix."
---

You already know Linux, so there's little new to learn about *what* to configure. The change is in how: you stop editing the live system and describe it in a file. NixOS rebuilds the system from that file every time, so it can't drift.

## Arch habits, translated

| On Arch | On NixOS | What changes |
|---|---|---|
| `pacman -S foo` | Add `foo` to `environment.systemPackages`, rebuild | Installed software is part of your config, not your history. |
| The AUR | nixpkgs (it probably has it), overlays, or a flake input | nixpkgs is very large. For anything missing, you write a small package. |
| Editing files in `/etc` | NixOS options, e.g. `services.openssh.settings` | `/etc` is generated. Your edits live in one place and survive rebuilds. |
| `systemctl enable foo` | `services.foo.enable = true;` | Services, users and firewall rules are all declared. |
| Dotfiles with stow or a bare repo | Home Manager | Your user config gets generations and rollbacks too. |
| Rolling release | The `nixos-unstable` channel | Still rolling, but any update can be rolled back from the boot menu. |
| The Arch Wiki | [search.nixos.org](https://search.nixos.org) options + the [NixOS Wiki](https://wiki.nixos.org) | The Arch Wiki is still great for concepts. |

## Hyprland, as an example

Your Hyprland setup becomes part of the config, so it survives reinstalls:

```nix
{ pkgs, ... }: {
  programs.hyprland.enable = true;
  environment.systemPackages = with pkgs; [
    waybar wofi kitty swaynotificationcenter
  ];
}
```

Put the Hyprland, Waybar and terminal settings in [Home Manager](https://github.com/nix-community/home-manager) and the whole desktop can be rebuilt from the repo.

## Where to go next

- Read a few configs in [The Regulars](/regulars/). **Misterio77/nix-starter-configs** shows a clean flake layout, and **fufexan/dotfiles** is a full Hyprland setup.
- The [NixOS & Flakes Book](https://nixos-and-flakes.thiscute.world) is written for people who already know Linux.
- [The Brewhouse](/brewhouse/) compares the ways people organise a config, from one file to den.
