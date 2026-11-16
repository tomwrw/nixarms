---
title: "Pour the den starter"
starter: "den"
step: 5
weight: 50
flake: true
date: 2026-11-16
checked: 2026-11-16
lede: "The full brewery: you declare the computer and its user once, and den builds them from aspects such as desktop and gaming. Taste it in a throwaway VM, then make it yours in about forty minutes."
description: "A beginner's guide to the den NixOS starter config, with and without Home Manager: try it in a VM, then make it your own."
files:
  - path: "flake.nix"
    what: "Pins NixOS 26.05, flake-parts, import-tree, den (and the matching Home Manager), then loads everything in `modules/`."
  - path: "flake.lock"
    what: "The exact versions in use, written by Nix. You don't edit it by hand."
  - path: "modules/den.nix"
    what: "Switches den on, with its hostname battery (a ready-made aspect)."
  - path: "modules/hosts/snug/default.nix"
    what: "The computer called `snug`: who uses it, and what it includes. With Home Manager, giving `alice` the `homeManager` class is what switches it on."
  - path: "modules/hosts/snug/_hardware-configuration.nix"
    what: "A placeholder, until you copy your own over it. The `_` stops import-tree loading it by itself, so only `snug` uses it."
  - path: "modules/aspects/base.nix"
    what: "What every machine gets: booting, networking, language and Nix."
  - path: "modules/aspects/desktop.nix"
    what: "KDE Plasma, sound and printing."
  - path: "modules/aspects/apps.nix"
    what: "Apps for everyone on the computer."
  - path: "modules/aspects/gaming.nix"
    what: "Steam."
  - path: "modules/aspects/home-manager.nix"
    what: "How Home Manager behaves."
    hm: true
  - path: "modules/aspects/vm.nix"
    what: "Settings for the test VM, and `nix run .#vm`."
  - path: "modules/users/alice.nix"
    what: "You: your account and your own apps. With Home Manager, your git and shell settings too, in the same file."
filesNote: "It builds exactly the same computer as the flakes starter, and the Brewhouse checks that on every change. Only where things live is different."
gotchas:
  - title: "den is young, so it's pinned"
    text: "The starter uses den `v0.20.0`, and `nix flake update` leaves it there. den's docs follow its newest release, so check which version a page describes, and read [the release notes](https://github.com/denful/den/releases) before you move up."
  - title: "Names are the glue"
    text: "den builds the host and the user from their names. Rename `alice` in `den.hosts`, and also `den.aspects.alice`, its file and the login in `modules/aspects/vm.nix`. `grep -rn \"alice\\|snug\" modules` shows every one."
  - title: "Keep the _ on the hardware file"
    text: "`_hardware-configuration.nix` is a NixOS file, not a flake-parts one. Without the `_`, import-tree loads it in the wrong place and the build fails."
  - title: "Every file in modules/ is loaded"
    text: "import-tree loads every `.nix` file it finds, spare copies included. Keep old versions out of `modules/`, or start their names with `_` so it skips them."
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
  flake init -t github:tomwrw/nixarms-brewhouse#den
```

For Home Manager, end it with `#den-hm` instead. A fresh NixOS hasn't switched flakes on yet, hence the long flag. The starter switches them on for good.

{{< /round >}}
{{< round title="Copy in your hardware file" time="1 min" >}}

```sh
cp /etc/nixos/hardware-configuration.nix \
  modules/hosts/snug/_hardware-configuration.nix
```

It goes over the starter's placeholder, in `snug`'s own folder. Keep the `_` at the start of its name. Until you do this, a real build stops with a reminder.

{{< /round >}}
{{< round title="Fill in your details" time="15 min" >}}

Open the folder in Kate (KDE's text editor) and search for `CHANGE ME`:

- **Your hostname and account name** are in `modules/hosts/snug/default.nix`, on the `den.hosts` line. Use the account name you picked in the installer: a new name makes a new, empty account. den uses these names everywhere, so rename `den.aspects.snug`, the `snug` folder, `modules/users/alice.nix` and the `den.aspects.alice` inside it to match.
- **Language and keyboard** are in `modules/aspects/base.nix`.
- **Your git name and email**, if you poured Home Manager, are in `modules/users/alice.nix`.
- **Your account name and hostname** appear once more in `modules/aspects/vm.nix`, for the test VM.
- **`stateVersion`** is in `modules/hosts/snug/default.nix`. Copy it from your old file. This shows it:

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

Machine-only lines go in the `nixos = { ... }` block of `den.aspects.snug`, in `modules/hosts/snug/default.nix`:

- **`boot.loader.grub` lines** mean your PC starts up with GRUB. Put them in `snug`'s `nixos` block, and delete the two `boot.loader` lines from `modules/aspects/base.nix`, which every machine shares. If you only see `systemd-boot` and `efi`, the starter has those already.
- **`boot.initrd.luks` or `boot.initrd.secrets` lines** unlock an encrypted disk. Copy them into `snug`'s `nixos` block as they are, or parts of your disk may not unlock.
- **`environment.systemPackages`** lists apps you've added. Copy the ones you want into the lists in `modules/aspects/apps.nix` or `modules/users/alice.nix`.

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

### The den way: an aspect of its own

Something any computer might want becomes an aspect. Make `modules/aspects/graphics.nix`:

```nix
# Drawing and photo apps, as an aspect any computer can include.
{
  den.aspects.graphics = {
    nixos =
      { pkgs, ... }:
      {
        environment.systemPackages = [ pkgs.gimp pkgs.inkscape ];
      };
  };
}
```

Then add `den.aspects.graphics` to `snug`'s `includes` in `modules/hosts/snug/default.nix`, `git add modules/aspects/graphics.nix` if you keep the folder in git, and switch. An aspect can also hold `homeManager` settings next to its `nixos` ones, so one file can look after the system and your user together.

## Keeping it up to date

```sh
nix flake update
sudo nixos-rebuild switch --flake .#snug
```

The first command moves `flake.lock` to the latest NixOS 26.05 fixes (and Home Manager's); the second applies them. A new NixOS release (26.11, say) means changing `nixos-26.05` in `flake.nix`, and `release-26.05` with it if you use Home Manager. The two must always match.

den stays on `v0.20.0` until you change it in `flake.nix` yourself. It's young, and its releases sometimes change how things work, so read [its release notes](https://github.com/denful/den/releases) first.

## Going further

den's own [documentation](https://den.denful.dev) covers what this starter leaves out: more hosts, Macs, standalone Home Manager and policies.
