{
  description = "Dev Environment (Python)";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in {
    devShells.${system}.default = pkgs.mkShell {
      name = "dev-python";

      packages = with pkgs; [
        python314
        uv
      ];

      shellHook = ''
        echo "Dev Shell with Python 3.14 and uv"
      '';
    };
  };
}
