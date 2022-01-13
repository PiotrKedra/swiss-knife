{ pkgs ? import <nixpkgs> {} }:
let mvn = pkgs.maven.override { jdk = pkgs.jdk; };
  my-python = pkgs.python3;
  python-with-my-packages = my-python.withPackages (p: with p; [
    matplotlib
  ]);
in pkgs.mkShell {
  buildInputs = [
                  pkgs.parted
                  pkgs.php
                  pkgs.gcc
                  pkgs.fio
                  pkgs.glibc
                  pkgs.gnumake
                  pkgs.crc32c
                  python-with-my-packages
                  ];
}