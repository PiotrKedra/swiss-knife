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

Use ```sudo``` to run the evaluations! The server starts freshly for each benchmark test. This takes a while, so please
be patient until the whole process will finish. You might grab a coffee...since the test needs about 28 minutes to test
all servers. Run the evaluations with:

```console
$ cd task2
$ sudo python reproduce.py 
```

The plots and flame graphs will be written to ```./results```.

Reproduced figures:

- <b>Figure 1 (a)</b> - Showing requests per seconds for the basic HTTP server
- <b>Figure 1 (b)</b> - Showing requests per seconds for the HTTP server based on select
- <b>Figure 2 (a)</b> - Showing requests per seconds for the HTTP server based on poll
- <b>Figure 2 (b)</b> - Showing requests per seconds for the HTTP server based on epoll