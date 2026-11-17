---
title: "lanzaboote"
weight: 50
date: 2026-11-17
checked: 2026-11-17
level: "Top shelf"
group: "Booting"
plain: "Secure Boot for NixOS: your PC only starts a system signed with your own keys."
lede: "lanzaboote brings Secure Boot to NixOS. It signs every generation with keys you make yourself, so the firmware refuses to start anything you didn't sign. Windows can still boot alongside it."
description: "lanzaboote explained for NixOS beginners: Secure Boot with your own keys, when you need it and what can go wrong."
needIt: "You dual-boot Windows for a game whose anti-cheat insists on Secure Boot (Battlefield 6 is one), or you want a lost laptop to refuse to start anything you didn't sign."
skipIt: "Nothing you run needs Secure Boot, or you're not yet comfortable rescuing a PC that won't start. It mainly guards against someone tampering with the machine while you're away from it."
landlord:
  file: "modules/aspects/system/boot.nix"
  text: "lanzaboote on both machines, with automatic keys: the first boot makes them, enrols them and re-signs everything. sbctl stays installed for recovery, and the keys in /var/lib/sbctl are persisted, because the root is wiped on every boot."
regularsTag: "lanzaboote"
mindTheStep:
  - title: "Have a way back first"
    text: "lanzaboote's own docs say it's for experienced users and has sharp edges. Before you start, find the firmware setting that switches Secure Boot off, and keep a NixOS installer USB (which won't start until you do switch it off)."
  - title: "Keep Microsoft's keys"
    text: "Enrol with `--microsoft`. Some graphics cards and other parts run firmware signed by Microsoft, and without those keys a PC can fail to start at all. It also keeps Windows booting."
  - title: "BitLocker will want its key"
    text: "Changing the Secure Boot keys makes Windows ask for your BitLocker recovery key. Find it in your Microsoft account before you start."
  - title: "Don't clear every key"
    text: "If the firmware offers to clear all Secure Boot keys, don't: that also deletes its list of known-bad bootloaders. Choose the option that resets to Setup Mode, or the one that erases the platform key."
  - title: "Mind the boot partition"
    text: "Every generation is a whole signed file on the boot partition, which fills up fast. Keep fewer with `boot.lanzaboote.configurationLimit = 8;`, or a rebuild stops halfway with *No space left on device*."
  - title: "Look after the keys"
    text: "Anyone who copies your keys from `/var/lib/sbctl` can sign their own system. Use full disk encryption and set a firmware password, or Secure Boot protects very little."
docs:
  - name: "lanzaboote documentation"
    url: "https://nix-community.github.io/lanzaboote/"
    note: "setup, troubleshooting and per-maker firmware steps"
  - name: "lanzaboote on GitHub"
    url: "https://github.com/nix-community/lanzaboote"
    note: "releases, to pin the version you use"
  - name: "sbctl"
    url: "https://github.com/Foxboron/sbctl"
    note: "the tool that makes and enrols the keys"
---

## The recipe

Four steps: check the PC is ready, make your keys, switch NixOS to lanzaboote, then turn Secure Boot on.

**1. Check you're ready.** NixOS has to be installed in UEFI mode and starting with systemd-boot:

```sh
bootctl status
```

Look for `Firmware: UEFI` and, under the current boot loader, `systemd-boot`.

**2. Make your keys.** They're saved in `/var/lib/sbctl`, where only root can read them:

```sh
sudo nix-shell -p sbctl --run "sbctl create-keys"
```

**3. Switch to lanzaboote.** Add it to your flake's inputs, pinned to a release:

```nix
# flake.nix, in inputs
lanzaboote = {
  url = "github:nix-community/lanzaboote/v1.2.0";
  inputs.nixpkgs.follows = "nixpkgs";
};
```

Then add `lanzaboote.nixosModules.lanzaboote` to your system's modules. It takes over from systemd-boot:

```nix
{ pkgs, lib, ... }: {
  boot.loader.systemd-boot.enable = lib.mkForce false;
  boot.lanzaboote = {
    enable = true;
    pkiBundle = "/var/lib/sbctl";
  };
  environment.systemPackages = [ pkgs.sbctl ];
}
```

Rebuild, then check the signatures. Everything in `/boot/EFI/Linux` and the bootloader should be signed; the kernel files in `/boot/EFI/nixos` don't need to be:

```sh
sudo sbctl verify
```

**4. Turn it on.** `systemctl reboot --firmware-setup` restarts straight into your firmware settings. Put Secure Boot into *Setup Mode* (where it lives varies by maker), then start NixOS again. Enrol your keys, with Microsoft's alongside, and restart:

```sh
sudo sbctl enroll-keys --microsoft
```

Afterwards, `bootctl status` should show `Secure Boot: enabled (user)`.

## Where it fits

lanzaboote can also make and enrol the keys for you on the first boot, with `boot.lanzaboote.autoGenerateKeys` and `autoEnrollKeys`, which is how my machines do it. With [impermanence](/cocktail-bar/impermanence/), keep `/var/lib/sbctl`, or the keys vanish at the next reboot. Once Secure Boot is on, lanzaboote's measured boot lets the TPM unlock an encrypted disk by itself, or with a PIN, as long as nothing in the boot chain has changed. Switching Secure Boot off again is the reverse: turn it off in the firmware first, then remove lanzaboote from your config.
