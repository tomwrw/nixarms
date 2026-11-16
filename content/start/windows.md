---
title: "Off Windows by Friday. Settled in by the weekend."
linkTitle: "Leaving Windows"
date: 2026-11-11
weight: 10
eyebrow: "Your order · Leaving Windows"
lede: "You don't need any Linux experience for this one. It takes you from \"what is NixOS?\" to a working desktop with your apps and games, and you can stop after any step."
description: "A beginner's guide from Windows to NixOS: what changes, your first evening, and a list of what won't come with you."
---

**You'll need:** a USB stick (8 GB or more), a backup of anything you care about, about two hours, and a cuppa.

## Read this before you install

The installer can wipe your disk. Its **Erase disk** option deletes everything on the drive, Windows and your files included, and there's no undo.

- Back up anything you'd miss to another drive or the cloud first.
- If you want to keep Windows, choose **Install alongside** (or install to a second drive), not Erase disk.
- If your drive is encrypted with BitLocker, save your recovery key from your Microsoft account before you start. Windows may ask for it afterwards.

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
{{< round title="Install with the graphical installer" time="30 min" >}}Download the graphical ISO from [nixos.org](https://nixos.org/download/), flash it to a USB stick, boot from it and click through. Pick **KDE Plasma** if you want something that feels like Windows. Check the disk step twice (see the warning above).{{< /round >}}
{{< round title="Open your config and add your apps" time="15 min" >}}Find your apps on [search.nixos.org](https://search.nixos.org) and add their names to the `environment.systemPackages` list in `/etc/nixos/configuration.nix`.{{< /round >}}
{{< round title="Rebuild" time="5 min" >}}Run `sudo nixos-rebuild switch`. When it finishes, your apps are in the menu.{{< /round >}}
{{< round title="Roll back, to see that you can" time="10 min" last="true" >}}Delete one app from the list and rebuild, so it disappears. Then reboot and pick the previous generation from the boot menu. The app is back. That's the safety net you'll rely on later.{{< /round >}}
{{< /rounds >}}

Adding your apps looks like this. It's a few lines added to the file the installer created:

```nix
environment.systemPackages = with pkgs; [
  firefox
  discord
  vlc
  libreoffice
];
```

{{< chalkboard title="What won't come with you" intro="Better to know now than on day three. These are the gaps, and what people usually use instead." size="lg" grid="true" >}}
{{< chalk-item title="Adobe apps" >}}No Photoshop or Premiere. Try GIMP, Krita, Darktable, or DaVinci Resolve for video.{{< /chalk-item >}}
{{< chalk-item title="Some online games" >}}Kernel anti-cheat titles won't run. [Check the gaming page](/gaming/).{{< /chalk-item >}}
{{< chalk-item title="Microsoft Office" >}}The web versions work in a browser. LibreOffice and OnlyOffice cover the rest.{{< /chalk-item >}}
{{< chalk-item title="RGB & peripheral apps" >}}Vendor tools rarely support Linux. OpenRGB and Piper handle most lights and mice.{{< /chalk-item >}}
{{< /chalkboard >}}

## Keeping Windows as well

You can dual-boot: both systems stay installed and you choose one each time you switch on. It's a sensible way to start if you rely on a game or app from the list above. The NixOS Wiki has a [dual-booting guide](https://wiki.nixos.org/wiki/Dual_Booting_NixOS_and_Windows) that covers the details.
