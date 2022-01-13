### How to Run

Af first, please activate the nix shell by: 
```console
$ nix-shell
```
Now, the run script that will execute all benchmark tests:
```console
$ sh iperf.sh
```
The results will be generated in the ```./iperf_results``` folder.

To obtain the figures run the following:
```console
$ python3 plot.py
```

The figures will be saved as```./png``` files in the```./iperf_results```folder.