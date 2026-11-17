---
date: 2026-11-11
title: "flake-parts"
step: 3
weight: 30
style: "The recipe book"
plain: "Splits a flake into separate modules, so a growing config stays tidy."
lede: "flake-parts is a recipe book for your flake. Instead of one long `flake.nix`, each part (a machine, a dev shell, a formatter) lives in its own module, using the same module system NixOS already uses."
description: "flake-parts explained for NixOS beginners: splitting a flake into modules."
forWho: "People with several machines or outputs whose `flake.nix` has outgrown a single screen."
moveOn: "You want to organise by *feature* (gaming, desktop, laptop) rather than by machine. That's the dendritic pattern."
regularsTag: "flake-parts"
checked: 2026-11-11
board:
  beginner: "Once you know flakes"
  flakes: "Yes"
  machines: "Yes, tidily"
  curve: "Moderate"
strengths:
  - "Your flake is split across files, each one a normal module."
  - "A large collection of ready-made flake-parts modules for dev shells, formatting, CI checks and more."
  - "The foundation that the dendritic pattern grew from."
tradeoffs:
  - "Another layer between you and the result, and another input to learn."
  - "Error messages can point into flake-parts itself rather than your file."
  - "Overkill for one machine."
docs:
  - name: "flake.parts"
    url: "https://flake.parts"
    note: "the official docs and module list"
---

## Turning on Steam

`flake.nix` hands over to flake-parts, and each machine becomes its own module:

```nix
# flake.nix
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" ];
      imports = [ ./hosts/endgame.nix ];
    };
}
```

```nix
# hosts/endgame.nix (a flake-parts module)
{ inputs, ... }:
{
  flake.nixosConfigurations.endgame = inputs.nixpkgs.lib.nixosSystem {
    modules = [ ../configuration.nix ];   # Steam still lives in here
  };
}
```

## How it works

flake-parts runs the same module system as NixOS, but one level up: its modules describe the *flake's outputs* instead of a machine. That's why it's mainly useful once there are several outputs to organise, such as machines, dev shells, packages and checks.
