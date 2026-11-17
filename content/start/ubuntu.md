---
title: "Coming to NixOS from Ubuntu"
linkTitle: "Coming from Ubuntu"
date: 2026-11-11
checked: 2026-11-17
weight: 30
eyebrow: "Your order"
lede: "GNOME and KDE work the way you know them. The difference is underneath: an upgrade either completes or doesn't happen, so a bad one can't leave you stranded halfway."
description: "Coming to NixOS from Ubuntu: how apt, PPAs, snaps and release upgrades translate to Nix."
nextRound:
  url: "/brewhouse/starters/vanilla/"
  title: "Pour the vanilla starter"
  text: "Once your desktop is running, the vanilla starter shows a whole `configuration.nix` filled in for a full desktop, and its guide shows how to test it before your own system changes."
  label: "Read the starter guide →"
---

If you've had a release upgrade fail halfway, or a PPA leave your system in a strange state, this is the part of NixOS you'll like. Every change builds a complete new system first, and NixOS only switches to it if the build succeeded.

## Ubuntu habits, translated

| On Ubuntu | On NixOS | What changes |
|---|---|---|
| `sudo apt install foo` | Add `foo` to `environment.systemPackages`, rebuild | Your installed apps are a list you can read, copy and share. |
| PPAs for newer versions | Pull single packages from `nixos-unstable` | No third-party repos to break your upgrades. |
| Snaps | Flatpak: `services.flatpak.enable = true;` | Snaps aren't supported. Flatpak is, and Flathub takes one more command (below). |
| `do-release-upgrade` | Switch channel, then `nixos-rebuild switch --upgrade` | If the new release misbehaves, boot the old one. |
| LTS every two years | A stable release every May and November | Each release gets about seven months of updates, so you move up twice a year. |

Flatpak doesn't come with Flathub. Once you've rebuilt with Flatpak switched on, run this once to add it:

```sh
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
```

## Your desktop

```nix
{
  services.desktopManager.gnome.enable = true;
  services.displayManager.gdm.enable = true;
}
```

For KDE, swap those two lines for `services.desktopManager.plasma6.enable = true;` and `services.displayManager.sddm.enable = true;`.

## Where to go next

- Try it in a virtual machine first. The install steps in the [Windows guide](/start/windows/) are the same for you, including the warnings about erasing the disk and Secure Boot.
- Browse [The Regulars](/regulars/) for configs to borrow from.
