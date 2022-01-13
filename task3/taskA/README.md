# How to run

Use ```sudo``` to run the evaluations!

Run the evaluations with:

```console
$ sudo python3 reproduce.py 
```

You might grab a coffee...since the script needs a couple of minutes to execute all tests.

It might happen that the YCSB benchmark test for the Redis cluster fails. This can be caused by the ```docker-compose```
command executed by another team's ```reproduce.py``` script. Please be patient and restart the script a couple of
minutes later to still reproduce the results. Usually, this situation can be avoided when working on separate servers or
only during certain time slots.

The plots will be generated inside the folder ```./basic/results``` and are also given below.

All outputs from the benchmark tests are located inside the folders ```./basic/benchmarks```
and ```./explore/benchmarks```.

## Generated plots

![alt-text-1](basic/results/plot_result_read.svg "Read operation") ![alt-text-2](basic/results/plot_result_update.svg "Update operation")
