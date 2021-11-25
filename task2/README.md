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
$ git clone <repository>
```

Use ```sudo``` to run the evaluations! The server starts freshly for each benchmark test. This takes a while, so please
be patient until the whole process will finish.

You might grab a coffee...since the script needs about <b>32</b> minutes to test all servers.

Run the evaluations with:

```console
$ sudo python reproduce.py 
```

The plots and Flame Graphs will be written to ```./results```.

Reproduced figures:

- <b>Figure 1 (a)</b> - Showing requests per seconds for the basic HTTP server (```plot_result_basic.svg```)
- <b>Figure 1 (b)</b> - Showing requests per seconds for the HTTP server based on select (```plot_result_select.svg```)
- <b>Figure 2 (a)</b> - Showing requests per seconds for the HTTP server based on poll (```plot_result_poll.svg```)
- <b>Figure 2 (b)</b> - Showing requests per seconds for the HTTP server based on epoll (```plot_result_epoll.svg```)