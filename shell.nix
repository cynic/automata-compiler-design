{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    # nativeBuildInputs is usually what you want -- tools you need to run
    nativeBuildInputs = with pkgs.buildPackages; [ 
      # zlib etc is needed so that pipenv can use pyenv to install python.
      # A bit round-about, I know…!
      python312 python312Packages.setuptools pipenv pyenv antlr bison zlib bzip2 ncurses libffi readline openssl pkg-config python312Packages.mypy
    ];
}