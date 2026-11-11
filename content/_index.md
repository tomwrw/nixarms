---
title: "The Nix Arms"
description: "A friendly local for anyone curious about Nix and NixOS: beginner guides, gaming on Linux, and real configs explained in plain English."

hero:
  eyebrow: "Welcome to The Nix Arms · est. generation 1"
  title: "Linux without the hangover."
  lede: "NixOS is Linux you describe instead of tinker with. Write down what you want, rebuild, and if anything breaks, pick yesterday from the boot menu. Pull up a stool and I'll show you round. Kids and dogs welcome."
  note: "Free, open source, and you can try it in a virtual machine first. No commitment."
  boardTitle: "Tonight's order: one gaming PC"
  code: |
    # configuration.nix: the whole machine
    { pkgs, ... }: {
      networking.hostName = "the-snug";
      services.desktopManager.plasma6.enable = true;
      programs.steam.enable = true;
      programs.gamemode.enable = true;
      environment.systemPackages = with pkgs; [
        firefox discord obs-studio
      ];
    }

rulesTitle: "Why people stay"
rules:
  - icon: undo
    title: "Bad pint? Send it back."
    text: "Every change creates a new **generation**, which is a save point for your whole system. If an update goes wrong, pick the last good one from the boot menu."
  - icon: file
    title: "Same recipe, same pint."
    text: "Your apps, settings, drivers and users are all written down. On a new PC you copy the config across and rebuild, and it's your machine again."
  - icon: package
    title: "The biggest cellar going."
    text: "nixpkgs has over 100,000 packages, more than any other Linux distro. If it runs on Linux, it's probably in there."
---
