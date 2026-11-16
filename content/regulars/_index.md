---
title: "The Regulars"
eyebrow: "Propping up the bar"
lede: "NixOS configs from real people, each with a short note on what it does well and what's worth borrowing. Reading other people's configs is one of the quickest ways to learn."
description: "Real NixOS configs, each with notes for beginners on what to borrow."
---

{{< chalkboard title="How to read someone's config" size="lg" >}}
1. Start at `flake.nix`. It usually lists every machine ("host") the repo builds. In a dendritic or den config, the hosts live in `modules/hosts/` instead.
2. Pick one host and follow its imports. That's the whole recipe for that machine.
3. Borrow one module at a time. Copy, rebuild, check it works, then take the next.
{{< /chalkboard >}}

## Pour your own {#submit}

Got a config you're proud of? Add it with a pull request: copy any file in [`content/regulars/`](https://github.com/tomwrw/nixarms/tree/main/content/regulars), fill in the front matter, and write a few lines on what it does well. I read every submission and can help with the notes.

A good regular is public, has a README, and has at least one thing a beginner could copy on its own.
