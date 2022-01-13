### How to Run

Af first, please activate the nix shell by:

```console
$ nix-shell
```

Now, run script that will execute all benchmark tests:

```console
$ sh iperf.sh
```

The results will be generated in the ```./iperf_results``` folder.

Run the following to obtain the figures:

```console
$ python3 plot.py
```

The figures will be saved as```./png``` files in the```./iperf_results```folder.

## Generated plots

The figures will be saved as```png``` files in the```./iperf_results```folder.

## Generated plots

![Alt text](iperf_results/fig_parallel.png?raw=true "Parallel connections")
![Alt text](iperf_results/fig_udp.png?raw=true "UDP bandwidth")
![Alt text](iperf_results/fig_window_size_by_bandwidth.png?raw=true "Window size by bandwidth")
