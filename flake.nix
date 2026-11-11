{
  description = "The Nix Arms (nixarms.com) - a friendly local for anyone curious about Nix";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { self, nixpkgs }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      # `nix build` → ./result is the finished static site.
      packages = forAllSystems (pkgs: {
        default = pkgs.stdenvNoCC.mkDerivation {
          pname = "nixarms-site";
          version = self.shortRev or self.dirtyShortRev or "dev";
          src = pkgs.lib.cleanSource ./.;
          nativeBuildInputs = [ pkgs.hugo ];
          buildPhase = ''
            runHook preBuild
            hugo --gc --minify \
              --cacheDir "$TMPDIR/hugo-cache" \
              --destination "$out"
            runHook postBuild
          '';
          dontInstall = true;
        };
      });

      # `nix run` → serve the site locally with live reload at http://localhost:1313
      apps = forAllSystems (pkgs: {
        default = {
          type = "app";
          program = toString (
            pkgs.writeShellScript "nixarms-serve" ''
              exec ${pkgs.hugo}/bin/hugo server --buildDrafts --disableFastRender "$@"
            ''
          );
        };
      });

      # `nix develop` → Hugo plus the tools used to regenerate brand assets (tools/brand).
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = [
            pkgs.hugo
            pkgs.librsvg
            (pkgs.python3.withPackages (ps: [
              ps.fonttools
              ps.brotli
              ps.uharfbuzz
              ps.pillow
            ]))
          ];
          shellHook = ''
            echo "The Nix Arms - run 'hugo server' and open http://localhost:1313"
          '';
        };
      });

      formatter = forAllSystems (pkgs: pkgs.nixfmt);
    };
}
