---
title: "Gaming on NixOS"
eyebrow: "The Games Lounge"
date: 2026-11-11
checked: 2026-11-17
band: dark
lede: "Steam, Proton, Heroic and Lutris are all switched on from your config. Every change is a save point, so if a driver update hurts your frame rate you can boot the previous setup."
description: "Gaming on NixOS: a complete Steam and Proton setup in one file, what runs, what doesn't and graphics card setup."
firstDay: "**New to NixOS?** This page assumes it's already installed. The [Windows guide](/start/windows/) gets you there first, even if you've never used Linux, and every [starter config](/brewhouse/starters/) comes with Steam switched on."
nextRound:
  url: "/brewhouse/starters/vanilla/"
  title: "A gaming desktop, ready-made"
  text: "Every starter in the Brewhouse is a KDE Plasma desktop with Steam already switched on. Try one in a VM first, then make it yours."
  label: "Pour the vanilla starter →"
actions:
  - label: "Will my games run?"
    url: "https://www.protondb.com"
---

## The whole setup, in one file

Save this as `gaming.nix` next to your `configuration.nix`, add `./gaming.nix` to the `imports` list in `configuration.nix`, and rebuild.

```nix
{ pkgs, ... }: {
  # Steam isn't free software, so NixOS needs your say-so first.
  nixpkgs.config.allowUnfree = true;

  programs.steam = {
    enable = true;
    remotePlay.openFirewall = true;
    gamescopeSession.enable = true;
  };
  programs.gamemode.enable = true;
  hardware.graphics.enable = true;

  environment.systemPackages = with pkgs; [
    mangohud heroic lutris protonup-qt
  ];
}
```

1. **Steam**, with Proton built in, and the ports Remote Play needs opened in the firewall.
2. **gamescope** adds a Steam Deck-style session you can pick at the login screen, for playing from the sofa.
3. **gamemode** nudges your CPU into performance mode while a game runs, but only for games started through it. In Steam, right-click a game, choose **Properties** and set its launch options to `gamemoderun %command%`.
4. **MangoHud** shows your frame rate and temperatures over the game. Switch it on the same way, with `mangohud %command%`, or use both at once: `gamemoderun mangohud %command%`.
5. **hardware.graphics** switches on your graphics drivers. Steam turns them on anyway, with the 32-bit drivers many games need, but this way the file says so.
6. **Heroic** covers Epic, GOG and Amazon, **Lutris** handles other launchers and **ProtonUp-Qt** installs extra Proton builds such as GE-Proton.

## Will my games run?

Mostly, yes. When a game doesn't run, the cause is usually its anti-cheat, which blocks Linux in general. Check your exact titles on [ProtonDB](https://www.protondb.com) and [Are We Anti-Cheat Yet?](https://areweanticheatyet.com) before you switch.

{{< status-grid >}}
{{< status kind="ok" title="On tap" >}}
Most single-player and many multiplayer games via Proton, plus native Linux titles.

**e.g.** Counter-Strike 2, Baldur's Gate 3, Cyberpunk 2077, Elden Ring, Hades II
{{< /status >}}
{{< status kind="tweak" title="Needs a tweak" >}}
Games that want a launch option, a particular Proton version or another launcher, such as Heroic or Lutris.

**Tip:** ProtonUp-Qt installs GE-Proton in two clicks.
{{< /status >}}
{{< status kind="no" title="Not served here" >}}
Games whose kernel-level anti-cheat blocks Linux. That's the publisher's decision, and nothing in your config can change it.

**e.g.** Valorant, Fortnite, League of Legends. Keep a Windows partition if these matter.
{{< /status >}}
{{< /status-grid >}}

## Your graphics card

**AMD and Intel:** drivers are open source and built into the kernel. `hardware.graphics.enable = true;` in the setup above is all you need.

**NVIDIA:** add a few lines for the proprietary driver. Cards from the GTX 16 and RTX 20 series onwards use NVIDIA's open kernel module:

```nix
services.xserver.videoDrivers = [ "nvidia" ];
hardware.nvidia.modesetting.enable = true;
hardware.nvidia.open = true;
```

Older cards (the GTX 900 and 1000 series) aren't supported by NVIDIA's newest driver, which NixOS uses by default. They need the 580 driver, the last to support them, and the closed kernel module:

```nix
hardware.nvidia.open = false;
hardware.nvidia.package = config.boot.kernelPackages.nvidiaPackages.legacy_580;
```

That second line uses `config`, so your file needs to start with `{ config, pkgs, ... }:`.

## Launchers

| You use | On NixOS | Add to your config |
|---|---|---|
| Steam | Steam (with Proton) | `programs.steam.enable` |
| Epic, GOG, Amazon | Heroic Games Launcher | `heroic` |
| Battle.net, EA, Ubisoft | Lutris | `lutris` |
| Minecraft | Prism Launcher | `prismlauncher` |
| Discord | Discord (or Vesktop) | `discord` |

{{< callout eyebrow="The landlord's rig" title="endgame: Ryzen 7 7800X3D · Radeon RX 9070 XT" url="/regulars/megadots/" label="Read the config →" >}}My own gaming desktop, which runs NixOS every day. Read the config and borrow what you like.{{< /callout >}}
