# Task 3 - Team D

## Reproduce report results

### Hardware

- CPU: AMD EPYC 7713P (64-cores)
- NIC: Broadcom BCM57416 10

### Software

- Operating system: Linux
- Python 3.0 or newer for the script that reproduces the evaluation

### Run evaluation

The first step is to get the source code for the task 3 from our repository:

```console
$ git clone https://github.com/PiotrKedra/swiss-knife.git
```

Use ```sudo``` to run the evaluations! The server starts freshly for each benchmark test. This takes a while, so please
be patient until the whole process will finish.

You might grab a coffee...since the script needs about <b>32</b> minutes to test all servers.

Run the evaluations with:

```console
$ cd task2
$ sudo python reproduce.py 
```

# Generated plots

![alt-text-1](basic/results/plot_result_read.svg "Read operation") ![alt-text-2](basic/results/plot_result_update.svg "Update operation")