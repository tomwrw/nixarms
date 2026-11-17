---
title: "Coming to NixOS from Arch"
linkTitle: "Coming from Arch"
date: 2026-11-11
checked: 2026-11-17
weight: 20
eyebrow: "Your order"
lede: "Everything you've hand-tuned in Arch, written down as code you can push to git and rebuild on any machine."
description: "Coming to NixOS from Arch Linux: how pacman, the AUR, systemd units and dotfiles translate to Nix."
nextRound:
  url: "/brewhouse/"
  title: "The Brewhouse"
  text: "Before long you'll want your config in git with every version pinned. The Brewhouse sets out five ways to organise it, from one file up to den, each with a starter you can try in a VM."
  label: "See the recipes →"
---

You already know Linux, so there's little new to learn about *what* to configure. The change is in how: you stop editing the live system and describe it in a file. NixOS rebuilds the system from that file every time, so it can't drift.

## Arch habits, translated

| On Arch | On NixOS | What changes |
|---|---|---|
| `pacman -S foo` | Add `foo` to `environment.systemPackages`, rebuild | Your config lists what's installed, so there's no install history to remember. |
| The AUR | nixpkgs (it probably has it), an overlay or a flake input | nixpkgs is very large. For anything missing, you write a small package. |
| Editing files in `/etc` | NixOS options, e.g. `services.openssh.settings` | `/etc` is generated. Your edits live in one place and survive rebuilds. |
| `systemctl enable foo` | `services.foo.enable = true;` | Services, users and firewall rules are all declared. |
| Dotfiles with stow or a bare repo | Home Manager | Your user config gets generations and rollbacks too. |
| Rolling release | The `nixos-unstable` channel | Still rolling, but any update can be rolled back from the boot menu. |
| The Arch Wiki | [search.nixos.org](https://search.nixos.org) options and the [NixOS Wiki](https://wiki.nixos.org) | The Arch Wiki is still great for concepts. |

## niri, as an example

Your [niri](https://github.com/niri-wm/niri) setup becomes part of the config, so it survives reinstalls:

```nix
{ pkgs, ... }: {
  programs.niri.enable = true;
  environment.systemPackages = with pkgs; [
    alacritty fuzzel waybar swaylock xwayland-satellite
  ];
}
```

Those are the apps niri's default config reaches for: alacritty on Super+T, fuzzel on Super+D, waybar at start-up and swaylock on Super+Alt+L. xwayland-satellite lets niri run older X11 apps.

Keep niri's `config.kdl` and your bar's settings in [Home Manager](https://github.com/nix-community/home-manager), or write them as Nix with [niri-flake](https://github.com/sodiboo/niri-flake), and the whole desktop can be rebuilt from the repo.

## Where to go next

- Read a few configs in [The Regulars](/regulars/). **Misterio77/nix-starter-configs** shows a clean flake layout, and **sodiboo/system** is a full niri desktop, written as Nix.
- The [NixOS & Flakes Book](https://nixos-and-flakes.thiscute.world) is written for people who already know Linux.
