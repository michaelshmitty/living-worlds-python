{
  description = "Paletteshifter development environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
    devshell = {
      url = "github:numtide/devshell";
      inputs = {
        flake-utils.follows = "flake-utils";
        nixpkgs.follows = "nixpkgs";
      };
    };
  };

  outputs = { self, nixpkgs, flake-utils, devshell }:
    flake-utils.lib.eachDefaultSystem (system: {
      devShell =
        let
          pkgs = import nixpkgs {
            inherit system;

            overlays = [ devshell.overlay ];
          };
        in
        pkgs.devshell.mkShell {
          name = "Paletteshifter development environment";
          packages = with pkgs; [
            (pkgs.python3.withPackages
              (ps: with ps; [ pygame psutil ])
            )
            nixpkgs-fmt
            isort
          ];
          env = [ ];
          commands = [
            {
              name = "paletteshifter:lint";
              category = "Maintenance";
              help = "Lint all the files in project";
              command = ''
                nixpkgs-fmt *.nix
              '';
            }
          ];
        };
    });
}
