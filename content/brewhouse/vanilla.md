---
date: 2026-11-11
title: "Vanilla configuration.nix"
step: 1
weight: 10
style: "The house pour"
plain: "One file in /etc/nixos, exactly what the installer gives you."
lede: "One file, `configuration.nix`, describing your whole machine. The installer creates it and the NixOS manual is written around it, so it's the place to start."
description: "Vanilla NixOS configuration with configuration.nix and channels, explained for beginners."
forWho: "Everyone, to begin with. With one machine, you may never need more."
moveOn: "You want your config in git with exact versions pinned, or you've got a second machine to set up."
regularsTag: "Vanilla"
checked: 2026-11-11
board:
  beginner: "Yes, start here"
  flakes: "No"
  machines: "One at a time"
  curve: "Gentle"
strengths:
  - "Nothing to set up: it's already on your machine after installing."
  - "The [NixOS manual](https://nixos.org/manual/nixos/stable/) and most beginner guides use this layout."
  - "Easy to split into a few files with `imports` as it grows."
tradeoffs:
  - "Versions come from your **channel**, which updates separately from your config. Two machines built a week apart can differ."
  - "Lives in `/etc/nixos`, owned by root, so keeping it in git takes a little setting up."
  - "Sharing settings between several machines is possible, but you'll be building the structure yourself."
docs:
  - name: "NixOS manual: configuration"
    url: "https://nixos.org/manual/nixos/stable/#ch-configuration"
    note: "the official guide to the file and its options"
  - name: "search.nixos.org options"
    url: "https://search.nixos.org/options"
    note: "every setting you can put in it"
---

## Turning on Steam

The installer writes two files to `/etc/nixos/`. You edit `configuration.nix`; `hardware-configuration.nix` describes your disks and drivers and is best left alone.

```nix
# /etc/nixos/configuration.nix
{ config, pkgs, ... }:
{
  imports = [ ./hardware-configuration.nix ];

  programs.steam.enable = true;
}
```

Then apply it:

```sh
sudo nixos-rebuild switch
```

## How it works

The **channel** decides which version of every package you get: a stable release, or unstable. `sudo nixos-rebuild switch --upgrade` updates the channel and rebuilds in one go.

When the file gets long, split it up. Any file can pull in others:

```nix
imports = [
  ./hardware-configuration.nix
  ./gaming.nix
  ./desktop.nix
];
```

That's all "modules" are: files that add settings. Every method further up the ladder is a different way of organising these same modules.
