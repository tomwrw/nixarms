---
title: "nixos-anywhere"
weight: 20
date: 2026-11-17
checked: 2026-11-17
level: "Second round"
group: "Installing"
plain: "Installs your config onto another machine over SSH, disks and all, with one command from your own PC."
lede: "nixos-anywhere installs NixOS onto another computer from yours. Point it at a machine you can reach over SSH and it lays out the disks with disko, installs your config and reboots into it."
description: "nixos-anywhere explained for NixOS beginners: installing your config onto another machine over SSH, when you need it and what can go wrong."
needIt: "You set up machines from your config, such as a home server, a second PC or a rented server, and you'd rather run one command from your desk than click through an installer on each."
skipIt: "You've got one PC. The graphical installer is simpler for a first install, and `nixos-rebuild` looks after it from then on."
landlord:
  file: "modules/flake/tasks.nix"
  text: "The deploy task. It copies each machine's age key and my home files from a USB stick into /persist, then runs nixos-anywhere. It uses the nixos-anywhere in nixpkgs rather than the newest on GitHub: this is the one step that wipes disks, so I want it pinned."
regularsTag: "nixos-anywhere"
mindTheStep:
  - title: "It wipes the target's disks"
    text: "Every disk in the machine's disko layout is erased, and nothing asks you to confirm. Check the address before you press Enter: get it wrong and it's another machine's disks."
  - title: "Make sure you can log in afterwards"
    text: "The new system only has the users and passwords your config gives it. Set a password (`hashedPassword` or `hashedPasswordFile`), and for a server add your SSH key to `users.users.<name>.openssh.authorizedKeys.keys`, or you're locked out of the machine you just installed."
  - title: "Over another Linux, use a cable"
    text: "On a machine running another Linux, nixos-anywhere switches into a temporary installer with no Wi-Fi settings. Booted from the NixOS installer USB, it keeps the connection you set up there."
  - title: "That route needs memory too"
    text: "Switching into the temporary installer needs at least 1.5 GB of RAM on the target. A smaller machine can boot the NixOS installer USB instead."
  - title: "Your PC will warn about the new key"
    text: "The fresh install has a new SSH host key, so the next `ssh` warns that the remote host identification has changed. `ssh-keygen -R 192.168.1.50` (with the machine's address) clears the old one."
docs:
  - name: "nixos-anywhere documentation"
    url: "https://nix-community.github.io/nixos-anywhere/"
    note: "the quickstart and how-to guides"
  - name: "Installing on a machine with no operating system"
    url: "https://github.com/nix-community/nixos-anywhere/blob/main/docs/howtos/no-os.md"
    note: "the installer USB route used below"
  - name: "nixos-anywhere-examples"
    url: "https://github.com/nix-community/nixos-anywhere-examples"
    note: "a complete flake and disk layout to start from"
---

## The recipe

This installs onto a second PC booted from the NixOS installer USB, from the flake on your own PC. Your flake needs the machine with a [disko](/cocktail-bar/disko/) layout, and its config should import `./hardware-configuration.nix`, which nixos-anywhere writes for you.

**1. On the new PC.** Boot the NixOS installer and connect it to your network. Open a terminal, give the installer's `nixos` user a password, and note the machine's address:

```sh
passwd
ip addr
```

**2. On your PC.** Check you can reach it, using that address:

```sh
ssh nixos@192.168.1.50
```

**3. Install.** From the folder with your `flake.nix`, this wipes the new PC's disks to match its disko layout, writes its hardware file into your folder and installs the machine called `snug`:

```sh
nix run github:nix-community/nixos-anywhere -- \
  --flake .#snug \
  --generate-hardware-config nixos-generate-config ./hardware-configuration.nix \
  --target-host nixos@192.168.1.50
```

It asks once for the password you set, then carries on by itself. When it says the installation finished, the PC restarts into your config. Commit the new `hardware-configuration.nix`, so the machine builds the same way next time.

## Where it fits

nixos-anywhere only does the first install. After that it's an ordinary NixOS machine: change the config and rebuild, on the machine itself or from your PC with `nixos-rebuild`'s `--target-host` option. To rehearse an install, swap `--target-host` for `--vm-test`, which runs the disk layout and install in a VM on your PC (once you have a hardware file). It runs on Linux, macOS or Windows with WSL2, and pairs with [impermanence](/cocktail-bar/impermanence/) and [sops-nix](/cocktail-bar/sops-nix/): its `--extra-files` option puts keys in place during the install.
