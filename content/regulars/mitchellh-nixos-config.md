---
date: 2026-11-11
title: "mitchellh/nixos-config"
repo: "mitchellh/nixos-config"
author: "Mitchell Hashimoto"
level: "Second round"
weight: 50
tags: ["Flakes", "Laptop"]
borrow: "The idea that your dev environment can live in a VM you rebuild at will."
---

Runs NixOS in a VM on a Mac as a daily development machine. A neat look at Nix outside a normal PC.

<!--more-->

The workflow matters more here than any single module. The whole development machine is disposable, because the config can rebuild it.
