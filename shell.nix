{ pkgs ? import <nixpkgs> { } }:

let
  lib = import <nixpkgs/lib>;

in
pkgs.mkShell {
  packages = with pkgs; [
    nodePackages_latest.pyright
  ];
}
