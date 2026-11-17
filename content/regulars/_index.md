---
title: "The Regulars"
eyebrow: "Real configs"
lede: "NixOS configs from real people, each with a short note on what it does well and what's worth borrowing. Reading other people's configs is one of the quickest ways to learn."
description: "Real NixOS configs, each with notes for beginners on what to borrow."
# The chalkboard above the cards, so it's read before anyone clicks away. Each step is Markdown.
howToRead:
  title: "How to read someone's config"
  steps:
    - "Start at `flake.nix`. It usually lists every machine (\"host\") the repo builds. In a dendritic or den config, the hosts live in `modules/hosts/` instead."
    - "Pick one host and follow its imports. That's the whole recipe for that machine."
    - "Borrow one module at a time. Copy, rebuild, check it works, then take the next."
# The legend above the filters: what each level on the cards means, with the same badges.
levels:
  - name: "First pint"
    text: "Small and heavily commented. A good first config to read."
  - name: "Second round"
    text: "A whole real setup with a clear layout. Read one once your own config works."
  - name: "Top shelf"
    text: "Big or advanced: several machines, newer patterns and extra tools. Read a part at a time."
---

## Pour your own {#submit}

Got a config you're proud of? Add it with a pull request: copy any file in [`content/regulars/`](https://github.com/tomwrw/nixarms/tree/main/content/regulars), fill in the front matter and write a few lines on what it does well. I read every submission and can help with the notes.

A good regular is public, has a README and has at least one thing a beginner could copy on its own.
