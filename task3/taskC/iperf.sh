iperf -s --bind fe80::e63d:1aff:fe72:f0%swissknife0&

(
#TCP test

iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 2K | tee iperf_results/result_basic_2k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K | tee iperf_results/result_basic_4k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 8K | tee iperf_results/result_basic_8k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 16K | tee iperf_results/result_basic_16k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 32K | tee iperf_results/result_basic_32k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 64K | tee iperf_results/result_basic_64k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 128K | tee iperf_results/result_basic_128k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 256K | tee iperf_results/result_basic_256k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 512K | tee iperf_results/result_basic_512k.txt

#UDP test
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 500M | tee iperf_results/result_udp_500.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 750M | tee iperf_results/result_udp_750.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 1000M | tee iperf_results/result_udp_1000.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 2000M | tee iperf_results/result_udp_2000.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 5000M | tee iperf_results/result_udp_5000.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 10000M | tee iperf_results/result_udp_10000.txt

# Reverse mode
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 2K -R | tee iperf_results/result_reverse_2k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K -R | tee iperf_results/result_reverse_4k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 8K -R | tee iperf_results/result_reverse_8k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 16K -R | tee iperf_results/result_reverse_16k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 32K -R | tee iperf_results/result_reverse_32k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 64K -R | tee iperf_results/result_reverse_64k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 128K -R | tee iperf_results/result_reverse_128k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 256K -R | tee iperf_results/result_reverse_256k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 512K -R | tee iperf_results/result_reverse_512k.txt

# Parallel mode
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -P 1 | tee iperf_results/result_parallel_1.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -P 2 | tee iperf_results/result_parallel_2.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -P 4 | tee iperf_results/result_parallel_4.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -P 8 | tee iperf_results/result_parallel_8.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -P 16 | tee iperf_results/result_parallel_16.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -P 32 | tee iperf_results/result_parallel_32.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -P 64 | tee iperf_results/result_parallel_64.txt

# Reverse mode
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 2K --bidir | tee iperf_results/result_bdir_2k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K --bidir | tee iperf_results/result_bdir_4k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 8K --bidir | tee iperf_results/result_bdir_8k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 16K --bidir | tee iperf_results/result_bdir_16k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 32K --bidir | tee iperf_results/result_bdir_32k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 64K --bidir | tee iperf_results/result_bdir_64k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 128K --bidir | tee iperf_results/result_bdir_128k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 256K --bidir | tee iperf_results/result_bdir_256k.txt
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 512K --bidir | tee iperf_results/result_bdir_512k.txt

)


#cleanup
pkill -P $$
