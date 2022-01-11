cd /mnt/teamd-ext4/phoronix-test-suite
sudo sh install-sh /mnt/teamd-ext4/pts/
cd ~
sudo /mnt/teamd-ext4/pts/bin/phoronix-test-suite batch-benchmark pts/compress-gzip pts/unpack-linux pts/postmark TEST_RESULTS_NAME=phoronix_ext4
sudo /mnt/teamd-ext4/pts/bin/phoronix-test-suite result-file-to-json phoronixext4 OUTPUT_FILE=~task3/taskC/results/phoronix_ext4.json
sudo /mnt/teamd-ext4/pts/bin/phoronix-test-suite result-file-to-json phoronixbtrfs OUTPUT_FILE=~/task3/taskC/results/phoronix_btrfs.json
