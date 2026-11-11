---
date: 2026-11-11
title: "tomwrw/megadots"
repo: "tomwrw/megadots"
author: "The landlord"
level: "Top shelf"
featured: true
weight: 20
hardware: "Ryzen 7 7800X3D · Radeon RX 9070 XT"
tags: ["Gaming", "Multi-machine", "Laptop", "Home Manager", "den", "flake-parts", "Flakes"]
borrow: "The steam aspect: one file that brings in Steam, two extra Proton builds, a binary cache and a persisted game library."
---

An AMD gaming desktop and a Surface Pro tablet from one [den](/brewhouse/den/) config, with every feature written as a reusable aspect.

<!--more-->

Two machines share one repo: **endgame**, the gaming desktop, and **flatmate**, a Surface Pro 7. Everything lives under `modules/`, loaded automatically with import-tree: hosts and users are declared once, and the features are aspects grouped into apps, desktop, hardware, roles and system. A `gaming` role pulls in Steam, MangoHud, controllers and performance tweaks, so a machine opts in with one line.

It's a deep dive because of what's around the edges: an ephemeral root filesystem with impermanence, disks laid out by disko, secrets in sops-nix, Secure Boot via lanzaboote, and Stylix theming. Even `flake.nix` is generated, by flake-file. Start with `modules/aspects/apps/steam.nix` and `modules/aspects/roles/gaming.nix`, which are well commented. More about the person behind it on [The Landlord](/landlord/) page.
