{ pkgs ? import <nixpkgs> {} }:
let mvn = pkgs.maven.override { jdk = pkgs.jdk; };
  my-python = pkgs.python3;
  python-with-my-packages = my-python.withPackages (p: with p; [
    pandas
    matplotlib
    seaborn
  ]);
in pkgs.mkShell {
  buildInputs = [ mvn 
	              pkgs.jdk
		          pkgs.memcached
		          pkgs.telnet
	              pkgs.rocksdb
	              pkgs.python2
                  python-with-my-packages
                  pkgs.sysbench
                  pkgs.gcc
                  pkgs.cmake
                  pkgs.haskellPackages.bz2
                  pkgs.libaio
                  pkgs.bison
                  pkgs.zlib
                  pkgs.zstd
                  pkgs.ninja
                  pkgs.lz4
                  pkgs.snappy
                  pkgs.openssl
                  pkgs.boost
                  pkgs.gdb
                  pkgs.gflags
                  pkgs.ncurses
                  pkgs.readline
                  pkgs.jemalloc ];
}