sudo rm results/phoronix/*.json
CWD=$(pwd)
sudo /mnt/teamd-ext4/pts/bin/phoronix-test-suite batch-benchmark pts/fs-mark TEST_RESULTS_NAME=phoronixext4
sudo /mnt/teamd-btrfs/pts/bin/phoronix-test-suite batch-benchmark pts/fs-mark TEST_RESULTS_NAME=phoronixbtrfs
sudo /mnt/teamd-ext4/pts/bin/phoronix-test-suite result-file-to-json phoronixext4 OUTPUT_FILE=$CWD/results/phoronix/phoronix_ext4.json
sudo /mnt/teamd-ext4/pts/bin/phoronix-test-suite result-file-to-json phoronixbtrfs OUTPUT_FILE=$CWD/results/phoronix/phoronix_btrfs.json




