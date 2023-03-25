{ pkgs ? import <nixpkgs> { } }:

let
  lib = import <nixpkgs/lib>;

in
pkgs.mkShell {
  packages = with pkgs; [
    python310Full
    nodePackages_latest.pyright
  ];
}
