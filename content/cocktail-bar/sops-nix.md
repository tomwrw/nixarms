---
title: "sops-nix"
weight: 40
date: 2026-11-17
checked: 2026-11-17
level: "Top shelf"
group: "Secrets"
plain: "Passwords and keys kept in your config repo, encrypted, and unlocked only on the machines meant to have them."
lede: "sops-nix keeps your secrets (a Wi-Fi password, an API token, your account's password) in your config repo, encrypted. Each machine can only unlock the ones meant for it, and they appear in `/run/secrets` when you switch."
description: "sops-nix explained for NixOS beginners: encrypted secrets in your config repo, when you need it and what can go wrong."
needIt: "Your config is in a public or shared repo, and something in it needs a password, a token or a key."
skipIt: "Nothing in your config is secret, or you're happy to type passwords in by hand after an install."
landlord:
  file: "modules/aspects/system/sops.nix"
  text: "Secrets for each machine and for my user. Each file is encrypted to its machine, to my own key and to two hardware security keys I keep for recovery."
regularsTag: "sops-nix"
mindTheStep:
  - title: "Lose the key, lose the secrets"
    text: "Without a key that can decrypt them, your secrets are gone for good. Keep a copy of your own age key somewhere off the machine."
  - title: "Never commit the plain file"
    text: "Always create and edit secrets with `sops`, which encrypts as it saves. Before you push, check the file shows `ENC[...]` where your secrets were."
  - title: "Secrets aren't there when Nix builds"
    text: "Your config can't read a secret's value. You point a program at the secret's file instead: `config.sops.secrets.<name>.path`."
  - title: "No SSH, no host key"
    text: "A machine only has `/etc/ssh/ssh_host_ed25519_key` when `services.openssh.enable` is on. Without it, give the machine an age key file with `sops.age.keyFile`."
  - title: "Account passwords are a special case"
    text: "Set `neededForUsers = true` so the secret is ready before NixOS creates users, store it as a password hash and use it with `hashedPasswordFile`."
  - title: "Added a machine? Re-encrypt"
    text: "After you add a key to `.sops.yaml`, run `sops updatekeys secrets.yaml` so the new machine can open the file."
docs:
  - name: "sops-nix on GitHub"
    url: "https://github.com/Mic92/sops-nix"
    note: "the README walks through every step"
  - name: "sops"
    url: "https://github.com/getsops/sops"
    note: "the tool that does the encrypting"
  - name: "agenix"
    url: "https://github.com/ryantm/agenix"
    note: "a smaller tool that does the same job"
---

## The recipe

Four steps: give each machine (and yourself) a key, say who can unlock what, write the secrets, then tell NixOS about them.

**1. Keys.** A machine running SSH already has a key you can use. This turns it into an age key, the kind sops-nix uses:

```sh
nix-shell -p ssh-to-age --run "cat /etc/ssh/ssh_host_ed25519_key.pub | ssh-to-age"
```

Make one for yourself too, so you can edit the secrets on your own PC:

```sh
nix-shell -p age --run "age-keygen -o ~/.config/sops/age/keys.txt"
```

**2. Who can unlock what.** A `.sops.yaml` at the top of your repo lists the public keys:

```yaml
keys:
  - &me age1...your-public-key
  - &snug age1...the-machines-public-key
creation_rules:
  - path_regex: secrets\.yaml$
    key_groups:
      - age:
          - *me
          - *snug
```

**3. The secrets.** This opens the file in your editor and encrypts it when you save:

```sh
nix-shell -p sops --run "sops secrets.yaml"
```

**4. The config.** After a switch, the secret is waiting at `/run/secrets/wifi-password`, readable only by root unless you say otherwise:

```nix
{
  sops.defaultSopsFile = ./secrets.yaml;
  sops.age.sshKeyPaths = [ "/etc/ssh/ssh_host_ed25519_key" ];
  sops.secrets.wifi-password = { };
}
```

## Where it fits

Add it as a flake input, `github:Mic92/sops-nix`, and import `sops-nix.nixosModules.sops`. There's a Home Manager module too, for secrets that belong to your user rather than the system. With [impermanence](/cocktail-bar/impermanence/), point sops-nix at the key's path on your persistent volume (`sops.age.keyFile`), because it can run before your files are put back in place.
