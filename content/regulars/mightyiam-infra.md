---
date: 2026-11-11
title: "mightyiam/infra"
repo: "mightyiam/infra"
author: "mightyiam"
level: "Top shelf"
weight: 70
tags: ["Dendritic", "flake-parts", "Multi-machine", "Flakes"]
borrow: "The shape of it: a near-empty flake.nix, and every feature in a file of its own."
---

The personal infrastructure of the person who first wrote up the dendritic pattern, and the reference for what one looks like in practice.

<!--more-->

Read it alongside the [pattern's own write-up](https://github.com/mightyiam/dendritic) and The Brewhouse's [dendritic page](/brewhouse/dendritic/). `flake.nix` hands everything under `modules/` to flake-parts via import-tree, so the interesting part is how features are split up rather than how any one machine is built.
