### How to Run

Af first, please activate the nix shell by:

```console
$ nix-shell
```

Now, run script that will execute all the basic benchmark tests:

```console
$ sh fio_benchmark.sh
```

The results will be generated in the ```./results``` folder.

Run the following to generate the figures:

```console
$ python3 plot_seq_rand.py
$ python3 plot_vardepth.py
```

The figures will be saved as```png``` files in the```./results/graphs```folder.

To obtain the phoronix results run the following:

```console
$ sh phoronix_benchmark.sh
```

In case you receive a benchmark dialog, answer the setup questions. Make sure to answer the questions in the following
way:

    Save test results when in batch mode (Y/n): Y
    Open the web browser automatically when in batch mode (y/N): N
    Auto upload the results to OpenBenchmarking.org (Y/n): n
    Prompt for test identifier (Y/n): n
    Prompt for test description (Y/n): n
    Prompt for saved results file-name (Y/n): n
    Run all test options (Y/n): Y

The results will be generated in the ```./results``` folder from the previous exercise.

Run the following to obtain the figures:

```console
$ python3 plot_phoronix.py
```

## Generated plots

![Alt text](results/graphs/throughput_read.png?raw=true "Read throughput application")
![Alt text](results/graphs/throughput_readwrite.png?raw=true "Read/Write throughput application")
![Alt text](results/graphs/throughput_write.png?raw=true "Write throughput application")
![Alt text](results/graphs/throughput_iodepth.png?raw=true "I/O-Depth count application")
