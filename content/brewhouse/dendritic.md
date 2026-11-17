---
date: 2026-11-11
title: "The dendritic pattern"
step: 4
weight: 40
style: "Branching out"
plain: "Organised by feature instead of by machine. Every file is a module, and they're all loaded automatically."
lede: "The dendritic pattern turns a config inside out. Instead of each machine listing everything it needs, each *feature* (gaming, a desktop, your shell) lives in one file, and machines pick the features they want."
description: "The dendritic Nix pattern explained for beginners: feature-first modules, usually with flake-parts and import-tree."
forWho: "People with three or more machines, or anyone tired of hunting through host folders to find where a setting lives."
moveOn: "You also manage a Mac or standalone Home Manager users, and want a framework to handle the wiring. Have a look at den."
regularsTag: "Dendritic"
checked: 2026-11-11
board:
  beginner: "Not yet"
  flakes: "Usually (not required)"
  machines: "Built for it"
  curve: "Steep"
strengths:
  - "Everything about one feature is in one file: the system setting, the user setting, even the flake input it needs."
  - "Adding a machine is a few lines: pick its features, done."
  - "No hand-maintained `imports` lists: drop a file in the folder and it's loaded."
tradeoffs:
  - "There's nothing to install: it's a *pattern*, so there's no single right way, and configs that follow it can look quite different."
  - "Hard to follow until it clicks, and hard to read someone else's at first."
  - "Usually built on flake-parts, so you're learning that too."
docs:
  - name: "mightyiam/dendritic"
    url: "https://github.com/mightyiam/dendritic"
    note: "the original write-up of the pattern"
  - name: "The dendritic pattern (NixOS Discourse)"
    url: "https://discourse.nixos.org/t/the-dendritic-pattern/61271"
    note: "the community discussion"
---

## Turning on Steam

`flake.nix` shrinks to almost nothing: it loads every file under `modules/` with [import-tree](https://github.com/denful/import-tree), and each file is a flake-parts module.

```nix
# flake.nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    flake-parts.url = "github:hercules-ci/flake-parts";
    import-tree.url = "github:denful/import-tree";
  };

  outputs = inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } (inputs.import-tree ./modules);
}
```

Steam gets a file of its own, as a *feature*:

```nix
# modules/gaming.nix
{
  flake.modules.nixos.gaming = {
    programs.steam.enable = true;
  };
}
```

The machine then picks its features:

```nix
# modules/hosts/endgame.nix
{ config, inputs, ... }:
{
  flake.nixosConfigurations.endgame = inputs.nixpkgs.lib.nixosSystem {
    modules = with config.flake.modules.nixos; [ gaming desktop ];
  };
}
```

## How it works

Because every file is a module of the *same* top-level config, any file can add to any part of it (a NixOS setting, a Home Manager setting, a flake input), and features can be shared by any machine. The `flake.modules` option comes from flake-parts' modules module, which you import once.

The pattern started out as "every file is a flake-parts module", but it's no longer tied to flake-parts: the community has shown the same layout working without flakes at all.
