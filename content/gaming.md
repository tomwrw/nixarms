---
title: "Gaming on NixOS: get a round in."
eyebrow: "The games room"
date: 2026-11-11
band: dark
lede: "Steam, Proton, Heroic and Lutris are all switched on from your config. Every change is a save point, so if a driver update hurts your frame rate you can boot the previous setup."
description: "Gaming on NixOS: a complete Steam and Proton setup in one file, what runs, what doesn't, and graphics card setup."
actions:
  - label: "Will my games run?"
    url: "https://www.protondb.com"
---

## The house pour

This is a full gaming setup in one file. Save it as `gaming.nix`, import it from your `configuration.nix`, and rebuild.

```nix
{ pkgs, ... }: {
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

1. **Steam** with Proton built in, plus ports opened for Remote Play.
2. **gamemode** nudges your CPU into performance mode while you play.
3. **gamescope** gives you a couch-friendly, Steam Deck-style session.
4. **MangoHud** shows FPS and temperatures; **Heroic** covers Epic and GOG.

## Will my games run?

Mostly, yes. When a game doesn't run, the cause is usually its anti-cheat, which blocks Linux in general. Check your exact titles on [ProtonDB](https://www.protondb.com) and [Are We Anti-Cheat Yet?](https://areweanticheatyet.com) before you switch.

{{< status-grid >}}
{{< status kind="ok" title="On tap" >}}
Most single-player and many multiplayer games via Proton, plus native Linux titles.

**e.g.** Counter-Strike 2, Baldur's Gate 3, Cyberpunk 2077, Elden Ring, Hades II
{{< /status >}}
{{< status kind="tweak" title="Needs a tweak" >}}
Games that want a specific Proton version, a launch option, or a launcher like Heroic or Lutris.

**Tip:** ProtonUp-Qt installs GE-Proton in two clicks.
{{< /status >}}
{{< status kind="no" title="Not served here" >}}
Games whose kernel-level anti-cheat blocks Linux. That's the publisher's decision, and nothing in your config can change it.

**e.g.** Valorant, Fortnite, League of Legends. Keep a Windows partition if these matter.
{{< /status >}}
{{< /status-grid >}}

## Your graphics card

**AMD and Intel:** drivers are open source and built into the kernel. `hardware.graphics.enable = true;` in the setup above is all you need.

**NVIDIA:** add three lines for the proprietary driver. Recent cards (RTX 20-series and newer) can use NVIDIA's open kernel module:

```nix
services.xserver.videoDrivers = [ "nvidia" ];
hardware.nvidia.modesetting.enable = true;
hardware.nvidia.open = true;
```

## Launchers

| You use | On NixOS | Add to your config |
|---|---|---|
| Steam | Steam (with Proton) | `programs.steam.enable` |
| Epic, GOG, Amazon | Heroic Games Launcher | `heroic` |
| Battle.net, EA, Ubisoft | Lutris | `lutris` |
| Minecraft | Prism Launcher | `prismlauncher` |
| Discord | Discord (or Vesktop) | `discord` |

{{< callout eyebrow="The landlord's rig" title="endgame: Ryzen 7 7800X3D · Radeon RX 9070 XT" url="/regulars/megadots/" label="Read the config →" >}}My own gaming desktop, which runs NixOS every day. Read the config and borrow what you like.{{< /callout >}}
