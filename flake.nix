{
  description = "Flake utils demo";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system}; in
      with pkgs;
      {
        devShell = mkShell {
          buildInputs = [
            python310
          ] ++ (with pkgs.python310Packages;[
            beautifulsoup4
            requests
            lxml
          ]);
        };
      }
    );
}
