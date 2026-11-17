---
title: "The Landlord"
# Not an article, so it stays out of the RSS feed (home.rss.xml).
feed: false
eyebrow: "Behind the bar"
layout: landlord
date: 2026-11-11
build:
  publishResources: false
lede: "Every local needs someone behind the bar. At The Nix Arms, that's me."
description: "About me, Tom: why I opened The Nix Arms, what runs on my machines and where to find me."
photo:
  src: "landlord.jpg"
  alt: "Tom, the landlord, in sunglasses and a checked shirt, holding a bottle of beer in a garden"
  caption: "The landlord, on duty."
findMe:
  - name: "tomwrw.com"
    url: "https://tomwrw.com"
    text: "My own site, also built with Hugo."
  - name: "GitHub: tomwrw"
    url: "https://github.com/tomwrw"
    text: "My configs, including megadots, and this site."
  - name: "The Nix Arms on Matrix"
    url: "https://matrix.to/#/%23the-nix-arms:matrix.org"
    text: "The pub's own chat room, for questions about the guides or a natter."
# "Buy me a pint" panel, above the Pull up a stool button. The link is params.kofi in hugo.toml.
pint:
  eyebrow: "Your round"
  text: "If a guide here saved you an evening, you can stand me a pint. No pressure: it's all free to read either way."
---

I'm Tom, and I run The Nix Arms.

I'm a firm believer in Nix. Once you've rebuilt a whole machine from your config, or rolled back a bad update from the boot menu, it's hard to go back to anything else. But most of what's written about Nix assumes you're already a developer, and I think that puts off a lot of people who'd get on well with it.

So I opened a pub. The guides here are written for people who aren't developers, and they say so when something doesn't work. There's a place to start whether you're coming from Arch, Ubuntu or Windows.

## What's on my bar

My own setup is all on NixOS, from one config called [megadots](/regulars/megadots/), built with [den](/brewhouse/den/):

- **endgame:** my gaming desktop, a Ryzen 7 7800X3D with a Radeon RX 9070 XT. Steam, Proton and the rest, all switched on from the config.
- **flatmate:** a Surface Pro 7 I use as a mobile workstation.

Both machines are built from the same repo, so a change made once reaches both. The config is public, and you're welcome to borrow from it.

## How the pub is run

The Nix Arms is my own project and isn't affiliated with the NixOS Foundation. The site is built with Hugo and a Nix flake, and all of it is open source.

If something's wrong or out of date, [open a pull request](https://github.com/tomwrw/nixarms) and the next round's on me.
