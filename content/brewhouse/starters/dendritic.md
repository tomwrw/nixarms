---
title: "Pour the dendritic starter"
starter: "dendritic"
step: 4
weight: 40
flake: true
date: 2026-11-16
checked: 2026-11-16
lede: "No `configuration.nix` any more: each feature has a file of its own, and the computer is a list of features. Give it about forty minutes to make it yours."
description: "A beginner's guide to the dendritic-pattern NixOS starter config, with and without Home Manager: try it in a VM, then make it your own."
files:
  - path: "flake.nix"
    what: "Pins NixOS 26.05, flake-parts, import-tree (and the matching Home Manager), then loads everything in `modules/`."
  - path: "flake.lock"
    what: "The exact versions in use, written by Nix. You don't edit it by hand."
  - path: "modules/flake-parts.nix"
    what: "Sets up flake-parts, including the `flake.modules` option every other file uses."
  - path: "modules/base.nix"
    what: "What every machine gets: booting, networking, language and Nix."
  - path: "modules/desktop.nix"
    what: "KDE Plasma, sound and printing."
  - path: "modules/apps.nix"
    what: "Apps for everyone on the computer."
  - path: "modules/gaming.nix"
    what: "Steam."
  - path: "modules/home-manager.nix"
    what: "Home Manager itself, as a feature like any other."
    hm: true
  - path: "modules/users/alice.nix"
    what: "You: your account and your own apps. With Home Manager, your git and shell settings too, in the same file."
  - path: "modules/hosts/snug/default.nix"
    what: "The computer called `snug`: its list of features, and the facts that are its alone."
  - path: "modules/hosts/snug/_hardware-configuration.nix"
    what: "A placeholder, until you copy your own over it. The `_` stops import-tree loading it by itself, so only `snug` uses it."
  - path: "modules/vm.nix"
    what: "Settings for the test VM, and `nix run .#vm`."
filesNote: "It builds exactly the same computer as the flakes starter, and the Brewhouse checks that on every change. Only where things live is different."
gotchas:
  - title: "Every file in modules/ is loaded"
    text: "import-tree loads every `.nix` file it finds, spare copies included. Keep old versions out of `modules/`, or start their names with `_` so it skips them."
  - title: "Keep the _ on the hardware file"
    text: "`_hardware-configuration.nix` is a NixOS file, not a flake-parts one. Without the `_`, import-tree loads it in the wrong place and the build fails."
  - title: "Names are spread out on purpose"
    text: "`alice` is in `modules/users/alice.nix` (the file name too), `modules/vm.nix` and `snug`'s list. `snug` is in its folder name, its `default.nix` and `modules/vm.nix`. `grep -rn \"alice\\|snug\" modules` shows every one."
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
  flake init -t github:tomwrw/nixarms-brewhouse#dendritic
```

For Home Manager, end it with `#dendritic-hm` instead. A fresh NixOS hasn't switched flakes on yet, hence the long flag. The starter switches them on for good.

{{< /round >}}
{{< round title="Copy in your hardware file" time="1 min" >}}

```sh
cp /etc/nixos/hardware-configuration.nix \
  modules/hosts/snug/_hardware-configuration.nix
```

It goes over the starter's placeholder, in `snug`'s own folder. Keep the `_` at the start of its name. Until you do this, a real build stops with a reminder.

{{< /round >}}
{{< round title="Fill in your details" time="15 min" >}}

Open the folder in Kate (KDE's text editor) and search for `CHANGE ME`. Your details are spread out on purpose, each one in the feature it belongs to:

- **Language and keyboard** are in `modules/base.nix`.
- **Your account** is in `modules/users/alice.nix`, with your git name and email if you poured Home Manager. Use the account name you picked in the installer: a new name makes a new, empty account. Rename `alice` throughout that file, rename the file itself, and change it in `modules/vm.nix` and `snug`'s list.
- **The hostname and `stateVersion`** are in `modules/hosts/snug/default.nix`. If you change the hostname, rename the `snug` folder and the name in `modules/vm.nix` too. Copy `stateVersion` from your old file. This shows it:

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

Machine-only lines go in `snug`'s own block at the bottom of `modules/hosts/snug/default.nix`, next to `networking.hostName`:

- **`boot.loader.grub` lines** mean your PC starts up with GRUB. Put them in `snug`'s block, and delete the two `boot.loader` lines from `modules/base.nix`, which every machine shares. If you only see `systemd-boot` and `efi`, the starter has those already.
- **`boot.initrd.luks` or `boot.initrd.secrets` lines** unlock an encrypted disk. Copy them into `snug`'s block as they are, or parts of your disk may not unlock.
- **`environment.systemPackages`** lists apps you've added. Copy the ones you want into the lists in `modules/apps.nix` or your own file in `modules/users/`.

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

From then on, `git add` every new file before you build. Flakes only see files git knows about, and import-tree only loads what the flake can see.

## Your first change

Add an app, to see where things go. Open your file in `modules/users/`, find the `packages` list (`home.packages`, with Home Manager), and add `pkgs.gimp` to it:

```nix
packages = [
  pkgs.libreoffice-qt
  pkgs.vlc
  pkgs.gimp
];
```

Then switch, and GIMP turns up in your app menu:

```sh
sudo nixos-rebuild switch --flake .#snug
```

Every package name is on [search.nixos.org](https://search.nixos.org/packages).

### The dendritic way: a feature of its own

Something any computer might want gets a file of its own. Make `modules/graphics.nix`:

```nix
# Drawing and photo apps, as a feature any computer can pick.
{
  flake.modules.nixos.graphics =
    { pkgs, ... }:
    {
      environment.systemPackages = [ pkgs.gimp pkgs.inkscape ];
    };
}
```

Then add `graphics` to `snug`'s list in `modules/hosts/snug/default.nix`, `git add modules/graphics.nix` if you keep the folder in git, and switch. You never registered the file anywhere: import-tree found it. A second computer gets the same apps by adding the same word to its own list.

## Keeping it up to date

```sh
nix flake update
sudo nixos-rebuild switch --flake .#snug
```

The first command moves `flake.lock` to the latest NixOS 26.05 fixes (and Home Manager's); the second applies them. A new NixOS release (26.11, say) means changing `nixos-26.05` in `flake.nix`, and `release-26.05` with it if you use Home Manager. The two must always match.
