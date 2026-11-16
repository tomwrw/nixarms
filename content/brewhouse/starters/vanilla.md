---
title: "Pour the vanilla starter"
starter: "vanilla"
step: 1
weight: 10
flake: false
date: 2026-11-16
checked: 2026-11-16
lede: "The whole computer in `configuration.nix`, the shape the installer gives you, filled in for a full desktop. Taste it in a throwaway VM, then make it yours in about half an hour."
description: "A beginner's guide to the vanilla NixOS starter config, with and without Home Manager: try it in a VM, then make it your own."
files:
  - path: "configuration.nix"
    what: "The computer itself: desktop, apps and your account. Your details are in the block at the top."
  - path: "home.nix"
    what: "Your corner of it: your apps, git and your shell, through Home Manager."
    hm: true
  - path: "hardware-configuration.nix"
    what: "A placeholder, so the test VM works. On your computer, you keep your own."
filesNote: "There's no lock file. Your channel decides which version of NixOS you get, and `sudo nix-channel --list` shows it."
gotchas:
  - title: "Only two files go in"
    text: "Copy `configuration.nix` (and `home.nix`, with Home Manager) into `/etc/nixos`, nothing else. Your own `hardware-configuration.nix` is already there, and the starter's is a stand-in."
  - title: "Home Manager comes from a channel too"
    text: "For `{hm}`, add the Home Manager channel before you build, with the release that matches your NixOS channel. Update them together with `--upgrade-all`, because plain `--upgrade` only updates NixOS."
  - title: "The test VM is named after your computer"
    text: "`nixos-rebuild build-vm` makes `result/bin/run-snug-vm`, with your hostname in place of snug. `./result/bin/run-*-vm` finds it whatever you called it."
  - title: "Your channel picks the versions"
    text: "With no lock file, two PCs built a week apart can end up with different versions. That's fine for one PC. Flakes, the next step up, pin them."
---

## Make it yours

You'll need NixOS installed, on a real PC or in the [dress rehearsal](#dress-rehearsal). Everything below happens in a terminal (Konsole, on KDE Plasma), and nothing changes until the last step.

{{< rounds >}}
{{< round title="Back up what you've got" time="1 min" >}}

The starter replaces your `configuration.nix`, so keep a copy of the whole folder:

```sh
sudo cp -r /etc/nixos /etc/nixos.bak
```

{{< /round >}}
{{< round title="Pour the starter into a folder" time="2 min" >}}

```sh
mkdir ~/vanilla && cd ~/vanilla
nix --extra-experimental-features "nix-command flakes" \
  flake init -t github:tomwrw/nixarms-brewhouse#vanilla
```

For Home Manager, end it with `#vanilla-hm` instead. The vanilla starters don't use flakes: the long flag just lets `nix flake init` fetch the files.

{{< /round >}}
{{< round title="Fill in your details" time="10 min" >}}

Open `configuration.nix` in Kate (KDE's text editor) and fill in the block marked `CHANGE ME` at the top. With Home Manager, your git name and email are in `home.nix` too.

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

- **`boot.loader.grub` lines** mean your PC starts up with GRUB. Use them in place of the starter's two `boot.loader` lines. If you only see `systemd-boot` and `efi`, the starter has those already.
- **`boot.initrd.luks` or `boot.initrd.secrets` lines** unlock an encrypted disk. Copy them in as they are, or parts of your disk may not unlock.
- **`environment.systemPackages`** lists apps you've added. Copy the ones you want into the starter's lists.

{{< /round >}}
{{< round title="Add the Home Manager channel (vanilla-hm only)" time="2 min" >}}

Skip this for plain `vanilla`. Home Manager's release has to match NixOS's, so check yours says `nixos-26.05` first:

```sh
sudo nix-channel --list
```

Then add the matching Home Manager. If yours said a different release, use that number in place of 26.05.

```sh
sudo nix-channel --add \
  https://github.com/nix-community/home-manager/archive/release-26.05.tar.gz \
  home-manager
sudo nix-channel --update
```

{{< /round >}}
{{< round title="Put it in place" time="1 min" >}}

```sh
sudo cp configuration.nix /etc/nixos/
```

With Home Manager, copy `home.nix` across as well:

```sh
sudo cp home.nix /etc/nixos/
```

Leave the starter's `hardware-configuration.nix` behind. Your own is already in `/etc/nixos`.

{{< /round >}}
{{< round title="Try your copy in a VM (real PC only)" time="10 min" >}}

Skip this on the dress rehearsal. From your home folder:

```sh
cd ~ && nixos-rebuild build-vm && ./result/bin/run-*-vm
```

It boots your copy in a window, logged in as you (the password is `changeme` in there). If you copied `boot.initrd.secrets` lines, the test VM can't build: skip to the next step.

{{< /round >}}
{{< round title="Switch to it" time="5 min" last="true" >}}

```sh
sudo nixos-rebuild switch
```

Then restart, so everything starts fresh. From now on, edit the files in `/etc/nixos` and run this again. Kate asks for your password when you save there.

{{< /round >}}
{{< /rounds >}}

## Your first change

Add an app, to see where things go. Open `/etc/nixos/configuration.nix`, find the list under `# Apps just for you`, and add `pkgs.gimp` to it:

```nix
packages = [
  pkgs.libreoffice-qt
  pkgs.vlc
  pkgs.gimp
];
```

With Home Manager, that list is `home.packages`, in `/etc/nixos/home.nix`. Then switch, and GIMP turns up in your app menu:

```sh
sudo nixos-rebuild switch
```

Every package name is on [search.nixos.org](https://search.nixos.org/packages).

### The vanilla way: split off a file

When `configuration.nix` gets long, give a job its own file. Make `/etc/nixos/gaming.nix` with Steam's lines in it:

```nix
# /etc/nixos/gaming.nix
{
  nixpkgs.config.allowUnfree = true;
  programs.steam.enable = true;
}
```

Then delete those two lines from `configuration.nix`, add `./gaming.nix` to its `imports` list, and switch. Every method further up the ladder is a tidier way of doing exactly this.

## Keeping it up to date

```sh
sudo nixos-rebuild switch --upgrade-all
```

That fetches the latest fixes for your channels (NixOS, and Home Manager if you added it) and switches to them. A new NixOS release (26.11, say) means moving your channel to it, and the Home Manager channel with it. The [NixOS manual](https://nixos.org/manual/nixos/stable/#sec-upgrading) explains how.
