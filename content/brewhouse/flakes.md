---
date: 2026-11-11
title: "Flakes"
step: 2
weight: 20
style: "Bottle-conditioned"
plain: "Your config plus a lock file that pins every input. Same pint, every time."
lede: "Flakes bottle your config: a `flake.nix` says which ingredients you use, and a `flake.lock` records the exact version of each one. Rebuild next month, or on another PC, and you get the same system."
description: "NixOS flakes explained for beginners: flake.nix, flake.lock and pinned, reproducible configs."
forWho: "Anyone keeping their config in git, and anyone reading other people's configs, since many of them use flakes."
moveOn: "Your `flake.nix` is crowded with several machines and shared modules, and you want some structure."
regularsTag: "Flakes"
checked: 2026-11-11
board:
  beginner: "Yes, with a guide"
  flakes: "Yes"
  machines: "Yes, by hand"
  curve: "Gentle"
strengths:
  - "**Reproducible:** `flake.lock` pins every input, so nothing changes until you run `nix flake update`."
  - "Lives anywhere (usually a git repo in your home folder) and builds any machine by name."
  - "Pull in extra sources, like Home Manager or a hardware repo, as inputs."
tradeoffs:
  - "Still labelled *experimental* in Nix, so you switch it on with one setting. In practice it's widely used: every config in The Regulars uses flakes."
  - "Flakes only see files tracked by git. Forget to `git add` a new file and the build won't find it."
  - "One more file and one more concept to learn up front."
docs:
  - name: "nix.dev: flakes"
    url: "https://nix.dev/concepts/flakes"
    note: "what flakes are, from the official docs"
  - name: "NixOS & Flakes Book"
    url: "https://nixos-and-flakes.thiscute.world"
    note: "a full guide to running NixOS with flakes"
  - name: "Misterio77/nix-starter-configs"
    url: "https://github.com/Misterio77/nix-starter-configs"
    note: "templates to start your own"
---

## The pour

Your `configuration.nix` doesn't change at all. A `flake.nix` sits next to it and says where everything comes from:

```nix
# flake.nix
{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { nixpkgs, ... }: {
    nixosConfigurations.endgame = nixpkgs.lib.nixosSystem {
      modules = [ ./configuration.nix ];   # Steam is switched on in here
    };
  };
}
```

Build the machine called `endgame`:

```sh
sudo nixos-rebuild switch --flake .#endgame
```

## How it works

The first build writes `flake.lock`, pinning the exact nixpkgs commit. Commit both files. To update, run `nix flake update` and rebuild. If the new versions misbehave, roll back as usual or revert the lock file in git.

To switch flakes on, add this to your config and rebuild once:

```nix
nix.settings.experimental-features = [ "nix-command" "flakes" ];
```

A second machine is just another entry under `nixosConfigurations`, pointing at its own files.
