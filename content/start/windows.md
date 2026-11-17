---
title: "Leaving Windows for NixOS"
linkTitle: "Leaving Windows"
date: 2026-11-11
checked: 2026-11-17
weight: 10
eyebrow: "Your order"
lede: "You don't need any Linux experience for this one. It takes you from \"what is NixOS?\" to a working desktop with your apps and games, and you can stop after any step."
description: "A beginner's guide from Windows to NixOS: what changes, your first evening and a list of what won't come with you."
nextRound:
  url: "/brewhouse/starters/vanilla/"
  title: "Pour the vanilla starter"
  text: "NixOS is running and your apps are in. The vanilla starter is the same `configuration.nix`, filled in for a full desktop with Steam, and you can try it in VirtualBox before it touches your PC."
  label: "Read the starter guide →"
---

**You'll need:** a USB stick (8 GB or more), a backup of anything you care about, about two hours and a cuppa.

## Read this before you install

The installer can wipe your disk. Its **Erase disk** option deletes everything on the drive, Windows and your files included, and there's no undo.

- Back up anything you'd miss to another drive or the cloud first.
- If you want to keep Windows, choose **Install alongside** (or install to a second drive), not Erase disk.
- PCs sold with Windows 11 usually have **Secure Boot** switched on, and the NixOS manual says you'll likely need to switch it off before the installer will start. It's in your PC's firmware settings, usually under Boot, Security or Advanced. You get there by pressing a key such as F2, F10 or Delete as the PC starts, and your PC maker's website will say which.
- If your drive is encrypted with BitLocker, save your recovery key from your Microsoft account before you start. Switching Secure Boot off can make Windows ask for it.

Round 1 below runs NixOS in a virtual machine, which touches none of this. Start there.

## Windows things, and what replaces them

| On Windows | On NixOS | What's different |
|---|---|---|
| System Restore | **Generations** in the boot menu | Every change makes a restore point automatically, and you can boot any of them. |
| Downloading .exe installers | One line in your config | No bundled toolbars or installer wizards. |
| Windows Update | `nixos-rebuild switch --upgrade` | It updates when you run it, never mid-game or at shutdown. |
| The Settings app | `configuration.nix` (plus your desktop's settings) | System settings are written down, so a reinstall keeps them. |
| Setting up a new PC | Copy your config, rebuild | The same setup on new hardware, without reinstalling apps one by one. |

## Your first evening

{{< rounds >}}
{{< round title="Try it in a virtual machine" time="20 min" >}}Install [VirtualBox](https://www.virtualbox.org) on Windows and run NixOS inside it. Nothing on your computer changes, so break it as much as you like. The [dress rehearsal](/brewhouse/starters/vanilla/#dress-rehearsal) walks you through the settings.{{< /round >}}
{{< round title="Make the USB stick" time="15 min" >}}Download the **graphical ISO** from [nixos.org](https://nixos.org/download/). Then write it to the stick with [USBImager](https://bztsrc.gitlab.io/usbimager/), one of the tools the NixOS manual suggests: choose the ISO, choose your stick and click **Write**. It wipes whatever was on the stick. Copying the file across in File Explorer won't work. [balenaEtcher](https://etcher.balena.io) does the same job, but it sends usage statistics unless you turn that off in its settings.{{< /round >}}
{{< round title="Boot from it and install" time="30 min" >}}Restart with the stick plugged in and pick it from your PC's boot menu (another key at start-up, often F12, F11 or Esc). If the stick won't start, Secure Boot is probably still on: see the list above. Then click through the graphical installer. Pick **KDE Plasma** if you want something that feels like Windows, and check the disk step twice.{{< /round >}}
{{< round title="Open your config and add your apps" time="15 min" >}}Find your apps on [search.nixos.org](https://search.nixos.org) and add their names to the `environment.systemPackages` list in `/etc/nixos/configuration.nix`. Want to see a whole config filled in? The [vanilla starter](/brewhouse/starters/vanilla/) is one.{{< /round >}}
{{< round title="Rebuild" time="5 min" >}}Run `sudo nixos-rebuild switch`. When it finishes, your apps are in the menu.{{< /round >}}
{{< round title="Roll back, to see that you can" time="10 min" last="true" >}}Delete one app from the list and rebuild, so it disappears. Then reboot and pick the previous generation from the boot menu. The app is back. That's the safety net you'll rely on later.{{< /round >}}
{{< /rounds >}}

Adding your apps looks like this. It's a few lines added to the file the installer created. Discord isn't free software, so it needs the first line too (the installer adds it if you ticked **Allow unfree software**):

```nix
nixpkgs.config.allowUnfree = true;
environment.systemPackages = with pkgs; [
  firefox
  discord
  vlc
  libreoffice
];
```

{{< chalkboard title="What won't come with you" intro="Better to know now than on day three. These are the gaps, with what to try instead." size="lg" grid="true" >}}
{{< chalk-item title="Adobe apps" >}}No Photoshop or Premiere. Try GIMP, Krita and Darktable for photos, or DaVinci Resolve for video.{{< /chalk-item >}}
{{< chalk-item title="Some online games" >}}Kernel anti-cheat titles won't run. [Check the gaming page](/gaming/).{{< /chalk-item >}}
{{< chalk-item title="Microsoft Office" >}}The web versions work in a browser. LibreOffice and OnlyOffice cover the rest.{{< /chalk-item >}}
{{< chalk-item title="RGB and peripheral apps" >}}Vendor tools rarely support Linux. OpenRGB and Piper handle many lights and mice.{{< /chalk-item >}}
{{< /chalkboard >}}

## Keeping Windows as well

You can dual-boot: both systems stay installed and you choose one each time you switch on. It's a sensible way to start if you rely on a game or app from the list above. The NixOS Wiki has a [dual-booting guide](https://wiki.nixos.org/wiki/Dual_Booting_NixOS_and_Windows) that covers the details.
