# How to run

Af first, please activate the nix shell by: 
```console
nix-shell
```
Because of the troubles while running PARSEC on NixOS, we found GitHub repository with a ```default.nix``` configuration
to successfully run PARSEC:
```console
git clone https://github.com/Mic92/parsec-benchmark.git
```
We need to use the ```default.nix``` with configuration for PARSEC that's why we are opening second nix shell:
```console
cd parsec-benchmark
```
```console
nix-shell
```
```console
. env.sh
```
```console
. get-inputs
```
Now, we can go back with ```cd ..``` and run scripts that will execute all benchmark tests:
```console
sh script.sh
```
The results will be generated in ```./results folder``` with the figures by running the following afterwards:
```console
python3 plot.py
```

# Pre-generated plots

![Alt text](results/blackscholes.png?raw=true "Black-scholes application")

![Alt text](results/bodytrack.png?raw=true "Body track application")

![Alt text](results/ferret.png?raw=true "Ferret application")

