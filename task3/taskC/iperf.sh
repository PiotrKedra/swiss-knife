iperf -s --bind fe80::e63d:1aff:fe72:f0%swissknife0&

(
#TCP test

iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 2K -J --logfile iperf_results/result_basic_2k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K -J --logfile iperf_results/result_basic_4k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 8K -J --logfile iperf_results/result_basic_8k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 16K -J --logfile iperf_results/result_basic_16k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 32K -J --logfile iperf_results/result_basic_32k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 64K -J --logfile iperf_results/result_basic_64k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 128K -J --logfile iperf_results/result_basic_128k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 256K -J --logfile iperf_results/result_basic_256k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 512K -J --logfile iperf_results/result_basic_512k.json

#UDP test
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 500M -J --logfile iperf_results/result_udp_500.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 750M -J --logfile iperf_results/result_udp_750.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 1000M -J --logfile iperf_results/result_udp_1000.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 2000M -J --logfile iperf_results/result_udp_2000.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 5000M -J --logfile iperf_results/result_udp_5000.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -u -b 10000M -J --logfile iperf_results/result_udp_10000.json

# Reverse mode
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 2K -R -J --logfile iperf_results/result_reverse_2k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K -R -J --logfile iperf_results/result_reverse_4k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 8K -R -J --logfile iperf_results/result_reverse_8k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 16K -R -J --logfile iperf_results/result_reverse_16k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 32K -R -J --logfile iperf_results/result_reverse_32k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 64K -R -J --logfile iperf_results/result_reverse_64k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 128K -R -J --logfile iperf_results/result_reverse_128k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 256K -R -J --logfile iperf_results/result_reverse_256k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 512K -R -J --logfile iperf_results/result_reverse_512k.json

# Parallel mode
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K -P 1 -J --logfile iperf_results/result_parallel_1.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K -P 2 -J --logfile iperf_results/result_parallel_2.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4k -P 4 -J --logfile iperf_results/result_parallel_4.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K -P 8 -J --logfile iperf_results/result_parallel_8.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K -P 16 -J --logfile iperf_results/result_parallel_16.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K -P 32 -J --logfile iperf_results/result_parallel_32.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K -P 64 -J --logfile iperf_results/result_parallel_64.json

# Bidirectional mode
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 2K --bidir -J --logfile iperf_results/result_bdir_2k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 4K --bidir -J --logfile iperf_results/result_bdir_4k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 8K --bidir -J --logfile iperf_results/result_bdir_8k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 16K --bidir -J --logfile iperf_results/result_bdir_16k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 32K --bidir -J --logfile iperf_results/result_bdir_32k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 64K --bidir -J --logfile iperf_results/result_bdir_64k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 128K --bidir -J --logfile iperf_results/result_bdir_128k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 256K --bidir -J --logfile iperf_results/result_bdir_256k.json
iperf -c fe80::e63d:1aff:fe72:f0%swissknife1 -w 512K --bidir -J --logfile iperf_results/result_bdir_512k.json

)


#cleanup
pkill -P $$
