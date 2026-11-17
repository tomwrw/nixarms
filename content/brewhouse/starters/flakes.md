---
title: "Pour the flakes starter"
starter: "flakes"
step: 2
weight: 20
flake: true
date: 2026-11-16
checked: 2026-11-16
lede: "The same `configuration.nix`, bottled: a `flake.nix` names your ingredients and a lock file pins the exact version of each. Allow about half an hour to make it yours."
description: "A beginner's guide to the flakes NixOS starter config, with and without Home Manager: try it in a VM, then make it your own."
files:
  - path: "flake.nix"
    what: "Pins NixOS 26.05 (and the matching Home Manager), and names the computer `snug`. Also gives you `nix run .#vm`."
  - path: "flake.lock"
    what: "The exact versions in use, written by Nix. You don't edit it by hand."
  - path: "configuration.nix"
    what: "The computer itself: desktop, apps and your account. Your details are in the block at the top."
  - path: "home.nix"
    what: "Your corner of it: your apps, git and your shell, through Home Manager."
    hm: true
  - path: "hardware-configuration.nix"
    what: "A placeholder, until you copy your own over it."
filesNote: "`configuration.nix` is the same file as in the vanilla starter. The flake only adds where everything comes from."
gotchas:
  - title: "The name appears twice"
    text: "`snug` is in `configuration.nix` and in `flake.nix` (`nixosConfigurations.snug`). Change your hostname in both, and use the new name in `--flake .#yourname`."
  - title: "The lock only moves when you say"
    text: "Nothing updates until you run `nix flake update`. That's the point, but it also means no security fixes until you do, so make it a habit."
---

## Make it yours

You'll need NixOS installed, on a real PC or in the [dress rehearsal](#dress-rehearsal). Everything below happens in a terminal (Konsole, on KDE Plasma), and nothing changes until the last step.

{{< rounds >}}
{{< round title="Make a folder for your config" time="1 min" >}}

```sh
mkdir ~/nixos-config && cd ~/nixos-config
```

This folder becomes your config. After your first switch, `/etc/nixos` stops counting.

{{< /round >}}
{{< round title="Pour the starter" time="2 min" >}}

```sh
nix --extra-experimental-features "nix-command flakes" \
  flake init -t github:tomwrw/nixarms-brewhouse#flakes
```

For Home Manager, end it with `#flakes-hm` instead. A fresh NixOS hasn't switched flakes on yet, hence the long flag. The starter switches them on for good.

{{< /round >}}
{{< round title="Copy in your hardware file" time="1 min" >}}

```sh
cp /etc/nixos/hardware-configuration.nix .
```

It goes over the starter's placeholder. Until you do this, a real build stops with a reminder.

{{< /round >}}
{{< round title="Fill in your details" time="10 min" >}}

Open the folder in Kate (KDE's text editor) and search for `CHANGE ME`. Most of your details are in the block at the top of `configuration.nix`. With Home Manager, your git name and email are in `home.nix`. If you change the hostname from `snug`, change it in `flake.nix` too.

- **Use the account name you picked in the installer.** A new name makes a new, empty account.
- **Copy `stateVersion` from your old file.** This shows it:

```sh
grep stateVersion /etc/nixos/configuration.nix
```

{{< /round >}}
{{< round title="Bring across your PC's own lines" time="5 min" >}}

The installer wrote a few lines that belong to your PC alone. This finds them:

```sh
grep -nE "boot\.loader|boot\.initrd|systemPackages" \
  /etc/nixos/configuration.nix
```

They go in `configuration.nix`:

- **`boot.loader.grub` lines** mean your PC starts up with GRUB. Use them in place of the starter's two `boot.loader` lines. If you only see `systemd-boot` and `efi`, the starter has those already.
- **`boot.initrd.luks` or `boot.initrd.secrets` lines** unlock an encrypted disk. Copy them in as they are, or parts of your disk may not unlock.
- **`environment.systemPackages`** lists apps you've added. Copy the ones you want into the starter's lists.

{{< /round >}}
{{< round title="Try your copy in a VM (real PC only)" time="10 min" >}}

Skip this on the dress rehearsal.

```sh
nix --extra-experimental-features "nix-command flakes" run .#vm
```

It boots your copy in a window, logged in as you (the password is `changeme` in there). If you copied `boot.initrd.secrets` lines, the test VM can't build: skip to the next step.

{{< /round >}}
{{< round title="Switch to it" time="5 min" last="true" >}}

```sh
sudo nixos-rebuild switch --flake .#snug
```

Use your hostname in place of `snug` if you changed it. Then restart, so everything starts fresh. From now on, edit the files in this folder and run this again from here. Keep the `--flake .#snug`: without it, NixOS builds the old config in `/etc/nixos`.

{{< /round >}}
{{< /rounds >}}

### Keep it in git

Git arrives with the starter, so once you've switched, you can turn the folder into a repo:

```sh
git init && git add .
```

From then on, `git add` every new file before you build. Flakes only see files git knows about.

## Your first change

Add an app, to see where things go. Open `configuration.nix`, find the list under `# Apps just for you`, and add `pkgs.gimp` to it:

```nix
packages = [
  pkgs.libreoffice-qt
  pkgs.vlc
  pkgs.gimp
];
```

With Home Manager, that list is `home.packages`, in `home.nix`. Then switch, and GIMP turns up in your app menu:

```sh
sudo nixos-rebuild switch --flake .#snug
```

Every package name is on [search.nixos.org](https://search.nixos.org/packages).

### The flakes way: see what's pinned

```sh
nix flake metadata
```

That lists every input with the exact version `flake.lock` holds. Copy this folder to another PC and it builds from those same versions, which is the whole point of flakes.

## Keeping it up to date

```sh
nix flake update
sudo nixos-rebuild switch --flake .#snug
```

The first command moves `flake.lock` to the latest NixOS 26.05 fixes (and Home Manager's); the second applies them. If you keep the folder in git, commit `flake.lock` too, and you can always go back to the last versions that worked. A new NixOS release (26.11, say) means changing `nixos-26.05` in `flake.nix`, and `release-26.05` with it if you use Home Manager. The two must always match.
