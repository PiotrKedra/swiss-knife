# Task 4 - Team D

## Reproduce report findings

### Hardware

- CPU: AMD EPYC 7713P (64-cores)
- RAM: 500GB
- Storage: 2x Ent NVMe AGN MU AIC 1.6TB
- Storage: 1x SAS HDD 558.91
- NIC: Broadcom BCM57416 10

### Software

- Operating system: Linux

### Run evaluation

The first step is to get the source code for the task 4 from our repository:

```console
$ git clone https://github.com/anonym-repos-only/swissknife.git
```

Also get the repository of the course:

```console
https://github.com/TUM-DSE/Swiss-Knife-LLVM-Assignments
```

Follow the instructions given in the course repository for assignments 1 and 2.

Change to the folder of task 4.

```console
cd task4
```

Our corresponding implementations are in the folders ```./static_analysis``` and ```./dynamic_analysis```.