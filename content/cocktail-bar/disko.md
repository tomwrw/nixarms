---
title: "disko"
weight: 10
date: 2026-11-17
checked: 2026-11-17
level: "Second round"
group: "Installing"
plain: "Your disk layout, written down, so a fresh install partitions itself."
lede: "disko describes your disks in Nix: the partitions, the filesystems, even the encryption. Point it at a machine and it lays the disk out to match, so every reinstall comes out the same."
description: "disko explained for NixOS beginners: declarative disk partitioning, when you need it and what can go wrong."
needIt: "You reinstall machines, or set up new ones, and want the disk laid out the same way every time, without clicking through a partitioner."
skipIt: "You've got one PC and the installer's layout suits you. The graphical installer partitions the disk for you, and that's fine."
landlord:
  file: "modules/aspects/system/disko.nix"
  text: "An encrypted disk (LUKS) holding btrfs subvolumes and a swapfile, with the disk's ID taken from each machine's own entry. It's laid out so the root can be wiped on every boot, for impermanence."
regularsTag: "disko"
mindTheStep:
  - title: "It erases the whole disk"
    text: "Formatting with disko wipes every partition on the disk you give it, Windows included. A disk disko manages can't be shared with another operating system."
  - title: "Name the disk by its ID"
    text: "Use a path from `/dev/disk/by-id/`, not `/dev/sda` or `/dev/nvme0n1`. Those short names can change between boots, and then the wrong disk gets wiped."
  - title: "Plan the layout before you install"
    text: "disko lays a disk out when you format it. Changing the layout in your config later won't safely reshape a disk that's already full of your files."
  - title: "Keep one list of filesystems"
    text: "disko writes your `fileSystems` for you, so generate the hardware file with `nixos-generate-config --no-filesystems`, or the two lists will fight."
docs:
  - name: "disko on GitHub"
    url: "https://github.com/nix-community/disko"
    note: "the README and plenty of example layouts"
  - name: "disko quickstart"
    url: "https://github.com/nix-community/disko/blob/master/docs/quickstart.md"
    note: "a first install, step by step"
  - name: "disko-templates"
    url: "https://github.com/nix-community/disko-templates"
    note: "ready-made layouts to start from"
---

## The recipe

A disk with a boot partition and one big root partition, the same shape the NixOS installer makes. Swap in your own disk's ID:

```nix
# disk-config.nix
{
  disko.devices.disk.main = {
    type = "disk";
    device = "/dev/disk/by-id/nvme-YOUR-DISK";
    content = {
      type = "gpt";
      partitions = {
        ESP = {
          size = "1G";
          type = "EF00";
          content = {
            type = "filesystem";
            format = "vfat";
            mountpoint = "/boot";
            mountOptions = [ "umask=0077" ];
          };
        };
        root = {
          size = "100%";
          content = {
            type = "filesystem";
            format = "ext4";
            mountpoint = "/";
          };
        };
      };
    };
  };
}
```

Booted from the NixOS installer, this wipes that disk, lays it out to match and mounts it at `/mnt`, ready for `nixos-install`:

```sh
sudo nix --experimental-features "nix-command flakes" \
  run github:nix-community/disko/latest -- \
  --mode destroy,format,mount disk-config.nix
```

## Where it fits

The same file then goes into your config, so NixOS knows how the disk is mounted: import disko's NixOS module and `disk-config.nix`, and leave the filesystems out of your hardware file. disko pairs with [nixos-anywhere](/cocktail-bar/nixos-anywhere/), which installs your config onto another machine over the network, disk layout and all. It can also lay out the separate volumes that [impermanence](/cocktail-bar/impermanence/) needs.
