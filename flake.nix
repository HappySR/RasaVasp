{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };
  outputs =
    { flake-parts, ... }@inputs:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
      ];
      perSystem =
        { pkgs, ... }:
        {
          devShells.default = pkgs.mkShell {
            name = "RasaVasp";

            venvDir = ".venv";

            # System-level dependencies
            buildInputs = [
              pkgs.gcc
              pkgs.python310
              pkgs.python310Packages.venvShellHook
              pkgs.gcc
            ];

            # Python packages
            shellHook = ''
              export VIRTUAL_ENV="$PWD/.venv"
              export PATH="$VIRTUAL_ENV/bin:$PATH"
              if [ ! -d "$VIRTUAL_ENV" ]; then
                python -m venv "$VIRTUAL_ENV"
              fi
              source "$VIRTUAL_ENV/bin/activate"
              pip install --upgrade pip wheel
              pip install setuptools==70.3.0
              pip install numpy scipy rasa tensorflow
            '';
          };
        };
    };
}
