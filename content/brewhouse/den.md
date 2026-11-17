---
date: 2026-11-11
title: "den"
step: 5
weight: 50
style: "The full brewery"
plain: "A framework for NixOS, nix-darwin and Home Manager together, organised into reusable \"aspects\"."
lede: "den is a framework rather than a pattern. You declare your machines and users, then write **aspects**, such as gaming or Bluetooth, and one aspect can set up NixOS, a Mac and your user together."
description: "The den framework for Nix explained for beginners: aspects, hosts and users across NixOS, nix-darwin and Home Manager."
forWho: "People managing several NixOS machines, a Mac with nix-darwin or Home Manager users, who want one structure for all of it."
moveOn: "This is the top of the ladder. From here the work is tidying your own aspects, and perhaps sharing them."
regularsTag: "den"
checked: 2026-11-11
board:
  beginner: "Not yet"
  flakes: "No (optional)"
  machines: "Built for it, Macs too"
  curve: "Steep"
strengths:
  - "One aspect can set NixOS, nix-darwin and Home Manager options together."
  - "Aspects **include** other aspects, so a `gaming` role can pull in Steam, controllers and performance tweaks."
  - "Ready-made \"batteries\" for common chores, like setting the hostname or allowing an unfree package."
  - "Works with flakes or without them. Its own getting-started guide uses plain Nix."
tradeoffs:
  - "The youngest and steepest option here, and it's still changing, so check the docs match the version you pin."
  - "Its own vocabulary (aspects, batteries, includes, provides) to learn on top of Nix."
  - "A smaller community than plain flakes, so fewer examples to borrow from."
docs:
  - name: "den documentation"
    url: "https://den.denful.dev"
    note: "including the \"From Zero to Den\" guide"
  - name: "den on GitHub"
    url: "https://github.com/denful/den"
---

## Turning on Steam

Declare the machine and its user, then give the machine its aspects:

```nix
# modules/hosts.nix
{ den, ... }:
{
  den.hosts.x86_64-linux.endgame.users.tom = { };

  den.aspects.endgame.includes = [ den.aspects.gaming ];
}
```

The `gaming` aspect is where Steam lives. It could set Mac or Home Manager options in the same place:

```nix
# modules/aspects/gaming.nix
{
  den.aspects.gaming = {
    nixos = { pkgs, ... }: {
      programs.steam.enable = true;
    };
  };
}
```

## How it works

den creates an aspect for every host and user you declare. Each aspect holds settings grouped by **class** (`nixos`, `darwin`, `homeManager`) and can include other aspects, so you build roles out of small, reusable pieces.

den grew out of exploring the dendritic pattern, but it now stands on its own and no longer describes itself as dendritic. My own config, [tomwrw/megadots](/regulars/megadots/), runs on den.
