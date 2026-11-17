---
title: "Pour the flake-parts starter"
starter: "flake-parts"
step: 3
weight: 30
flake: true
date: 2026-11-16
checked: 2026-11-16
lede: "The flakes starter, split into modules: each job gets its own file, and each computer its own folder. Making your own copy takes about half an hour."
description: "A beginner's guide to the flake-parts NixOS starter config, with and without Home Manager: try it in a VM, then make it your own."
files:
  - path: "flake.nix"
    what: "Pins NixOS 26.05, flake-parts (and the matching Home Manager), then lists the modules below."
  - path: "flake.lock"
    what: "The exact versions in use, written by Nix. You don't edit it by hand."
  - path: "vm.nix"
    what: "Gives you `nix run .#vm`. One job, one file: that's the point of flake-parts."
  - path: "home.nix"
    what: "You, through Home Manager: your apps, git and your shell. It sits outside `hosts/`, so every computer can share it."
    hm: true
  - path: "hosts/snug/default.nix"
    what: "Hands the computer called `snug` to the flake. It's a flake-parts module, so it describes the flake, not the computer."
  - path: "hosts/snug/configuration.nix"
    what: "The computer itself: desktop, apps and your account. Your details are in the block at the top."
  - path: "hosts/snug/hardware-configuration.nix"
    what: "A placeholder, until you copy your own over it."
filesNote: "It builds exactly the same computer as the flakes starter, and the Brewhouse checks that on every change. Only where things live is different."
gotchas:
  - title: "Two kinds of module"
    text: "`default.nix` and `vm.nix` describe the flake; `configuration.nix` describes the computer. Put a computer setting such as `programs.steam.enable` in a flake file and you get an error saying the option doesn't exist."
  - title: "Renaming snug takes four edits"
    text: "The name is in `hosts/snug/configuration.nix`, `hosts/snug/default.nix`, `vm.nix` and the folder name, which `flake.nix` lists in its imports. `grep -rn snug .` shows every one."
  - title: "Errors can point into flake-parts"
    text: "When something's wrong, the message sometimes names a file inside flake-parts rather than yours. Look through the error for one of your own file names, such as `hosts/snug/default.nix`."
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
  flake init -t github:tomwrw/nixarms-brewhouse#flake-parts
```

For Home Manager, end it with `#flake-parts-hm` instead. A fresh NixOS hasn't switched flakes on yet, hence the long flag. The starter switches them on for good.

{{< /round >}}
{{< round title="Copy in your hardware file" time="1 min" >}}

```sh
cp /etc/nixos/hardware-configuration.nix \
  hosts/snug/hardware-configuration.nix
```

It goes over the starter's placeholder, in `snug`'s own folder. Until you do this, a real build stops with a reminder.

{{< /round >}}
{{< round title="Fill in your details" time="10 min" >}}

Open the folder in Kate (KDE's text editor) and search for `CHANGE ME`. Most of your details are in the block at the top of `hosts/snug/configuration.nix`. With Home Manager, your git name and email are in `home.nix`. If you change the hostname from `snug`, rename it in `hosts/snug/default.nix` and `vm.nix` too, rename the `snug` folder and update its path in `flake.nix`.

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

They go in `hosts/snug/configuration.nix`:

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

Add an app, to see where things go. Open `hosts/snug/configuration.nix`, find the list under `# Apps just for you`, and add `pkgs.gimp` to it:

```nix
packages = [
  pkgs.libreoffice-qt
  pkgs.vlc
  pkgs.gimp
];
```

With Home Manager, that list is `home.packages`, in `home.nix` at the top of the folder. Then switch, and GIMP turns up in your app menu:

```sh
sudo nixos-rebuild switch --flake .#snug
```

Every package name is on [search.nixos.org](https://search.nixos.org/packages).

### The flake-parts way: give the flake a new job

Jobs for the whole flake get a file each, next to `vm.nix`. Here's one that tidies your Nix files. Make `formatter.nix`:

```nix
# formatter.nix: `nix fmt` tidies every .nix file in this folder.
{
  perSystem =
    { pkgs, ... }:
    {
      formatter = pkgs.nixfmt-tree;
    };
}
```

Add `./formatter.nix` to the `imports` list in `flake.nix` (and `git add formatter.nix`, if you keep the folder in git). Then run `nix fmt`. Your computer hasn't changed at all: this job belongs to the flake, not to `snug`.

## Keeping it up to date

```sh
nix flake update
sudo nixos-rebuild switch --flake .#snug
```

The first command moves `flake.lock` to the latest NixOS 26.05 fixes (and Home Manager's); the second applies them. A new NixOS release (26.11, say) means changing `nixos-26.05` in `flake.nix`, and `release-26.05` with it if you use Home Manager. The two must always match.
