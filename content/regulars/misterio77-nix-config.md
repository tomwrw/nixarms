---
date: 2026-11-11
title: "Misterio77/Foundry"
repo: "Misterio77/Foundry"
author: "Gabriel Fontes"
level: "Second round"
weight: 30
tags: ["Multi-machine", "Servers", "Flakes"]
borrow: "How it splits system settings from per-user Home Manager settings."
---

Gabriel Fontes's own config (it used to be called nix-config), with a clean separation of hosts, users and shared modules.

<!--more-->

If the starter templates are the first pint, this is what they grow into. Look at how hosts pull in shared modules, and how each user's Home Manager config stays separate from the system.
