# How to run

Because of the troubles with runing PARSEC on NixOS, we found github with default.nix configuraiton to succesfully run PARSEC:

```console
$ git clone https://github.com/Mic92/parsec-benchmark.git
```

We need to use default.nix that's why we are opening nix shell

```console
$ cd parsec-benchmark
```

```console
$ nix-shell
```


```console
$ . env.sh
```

```console
$ . get-inputs
```

Now we can go back  ```cd ..``` and run script that will run all the benchamrks:

```console
$ sh script.sh
```


The results will be generated in ./results folder. To generate figures we need to run plot.py script
