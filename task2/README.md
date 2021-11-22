# Task 2 - Team D

## Reproduce report results

### Hardware

- CPU: AMD EPYC 7713P (64-cores)
- NIC: Broadcom BCM57416 10

### Software

- Operating system: Linux
- Python 3.0 or newer for the script that reproduces the evaluation

### Run evaluation

The first step is to get the source code for the task 2 from our repository:

```console
$ git clone https://github.com/PiotrKedra/swiss-knife.git
```

Run evaluations with:

```console
$ cd task2
$ python reproduce.py 
```

The graphs will be written to `./results/<name_of_experiment>`. Where the name of the experiment is:

- basic
- io_uring

Reproduced figures:

- <b>Figure 1</b> - Showing requests per seconds for the basic HTTP server based on tradional sockets
- Figure 2