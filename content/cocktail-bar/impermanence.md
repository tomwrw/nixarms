---
title: "impermanence"
weight: 30
date: 2026-11-17
checked: 2026-11-17
level: "Top shelf"
group: "Housekeeping"
plain: "Wipes the system back to fresh on every boot, keeping only the files you've listed."
lede: "With impermanence, your root filesystem starts empty on every boot. Only the files and folders you list in your config are kept, on a separate volume, so nothing builds up that your config doesn't know about."
description: "impermanence explained for NixOS beginners: a root that's wiped on every boot, when you need it and what can go wrong."
needIt: "You want to know that everything on the machine comes from your config, and that the clutter apps leave behind is gone at the next reboot."
skipIt: "You're still finding out where your apps keep their settings. Until you know, you'll lose things you meant to keep, and a normal NixOS install is already easy to rebuild."
landlord:
  file: "modules/aspects/system/impermanence.nix"
  text: "The list of what survives a reboot: logs, user IDs, systemd's state and the machine ID, plus whatever each aspect asks to keep. Its partner, ephemeral-btrfs.nix, rolls the root back to a blank btrfs snapshot early in every boot."
regularsTag: "impermanence"
mindTheStep:
  - title: "Anything you don't list is gone"
    text: "A file saved anywhere that isn't on the list disappears at the next reboot, and that includes your home folder. Try the setup in a VM first, and back up anything that matters."
  - title: "Passwords are wiped too"
    text: "Passwords live in `/etc/shadow`, which goes with the rest of the root. Set `users.mutableUsers = false` and give each user a `hashedPasswordFile` on `/persist`, or you can be locked out after a reboot."
  - title: "Keep the IDs that should stay put"
    text: "List `/var/lib/nixos` so user and group numbers stay the same, and `/etc/machine-id` so the machine keeps its identity. Without them, file ownership and logs get muddled."
  - title: "Secrets need the real path"
    text: "sops-nix can run before impermanence has put your files in place, so point it at the key's path on the persistent volume, such as `/persist/var/lib/sops-nix/key.txt`. Keep your SSH host keys too, or they change on every boot."
  - title: "Mark the persistent volume"
    text: "`/persist` needs `neededForBoot = true`, so it's mounted before NixOS sets the system up. impermanence stops the build with an error if you forget."
  - title: "An app forgets its settings?"
    text: "It saved them somewhere you didn't list. Look for its folder in `~/.config`, `~/.local/share` or `/var/lib`, and add it."
docs:
  - name: "impermanence on GitHub"
    url: "https://github.com/nix-community/impermanence"
    note: "the README covers setting up the root and every option"
  - name: "Erase your darlings"
    url: "https://grahamc.com/blog/erase-your-darlings"
    note: "Graham Christensen on why you'd wipe the root on every boot"
  - name: "preservation"
    url: "https://github.com/nix-community/preservation"
    note: "a newer tool built on the same idea"
---

## The recipe

Three parts: a root that starts empty, a list of what to keep, and passwords that survive.

**1. A root that starts empty.** The simplest way keeps `/` in memory (tmpfs), so it's empty every time the machine starts. `/nix` and `/persist` stay on your disk, as separate partitions or btrfs subvolumes that [disko](/cocktail-bar/disko/) can lay out:

```nix
fileSystems."/" = {
  device = "none";
  fsType = "tmpfs";
  options = [ "defaults" "size=25%" "mode=755" ];
};
# /persist itself comes from your disk layout.
fileSystems."/persist".neededForBoot = true;
```

**2. What to keep.** Add impermanence to your flake's inputs:

```nix
# flake.nix, in inputs
impermanence.url = "github:nix-community/impermanence";
```

Then add `impermanence.nixosModules.impermanence` to your system's modules, and list what survives. NetworkManager's folder keeps your Wi-Fi passwords, and Bluetooth's keeps your paired devices:

```nix
environment.persistence."/persist" = {
  hideMounts = true;
  directories = [
    "/var/log"
    "/var/lib/nixos"
    "/var/lib/systemd"
    "/var/lib/bluetooth"
    "/etc/NetworkManager/system-connections"
  ];
  files = [ "/etc/machine-id" ];
  users.alice.directories = [
    "Documents"
    "Downloads"
    "Pictures"
    { directory = ".ssh"; mode = "0700"; }
  ];
};
```

`hideMounts` keeps all of these out of your file manager's list of drives.

**3. Passwords that survive.** Save a password hash on the persistent volume:

```sh
sudo mkdir -p /persist/passwords
sudo nix-shell -p mkpasswd --run "mkpasswd > /persist/passwords/alice"
```

Then tell NixOS to read it from there:

```nix
users.mutableUsers = false;
users.users.alice.hashedPasswordFile = "/persist/passwords/alice";
```

## Where it fits

tmpfs is the easy way in, but it uses memory, and a big download can fill it. The other way the README describes, which I use, keeps the root on btrfs and swaps it for an empty one early in every boot. Either way it changes how the disk is laid out, so it's easiest to set up on a fresh install, with disko laying out the volumes and [nixos-anywhere](/cocktail-bar/nixos-anywhere/) doing the install. With Home Manager's NixOS module, `home.persistence` lets each user list their own files from their Home Manager config. [preservation](https://github.com/nix-community/preservation) is a newer tool built on the same idea, and [ryan4yin's config](/regulars/ryan4yin-nix-config/) uses it.
