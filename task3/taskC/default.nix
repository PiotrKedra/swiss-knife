{ pkgs ? import <nixpkgs> {} }:
let mvn = pkgs.maven.override { jdk = pkgs.jdk; };
  my-python = pkgs.python3;
  python-with-my-packages = my-python.withPackages (p: with p; [
    matplotlib
  ]);
in pkgs.mkShell {
  buildInputs = [
                  python-with-my-packages
                  ];
}