sudo rm results/phoronix/*.json
CWD=$(pwd)
sudo mkfs.ext4 -f /dev/mapper/swissknife-teamd
sudo mount /dev/mapper/swissknife-teamd /mnt/teamd-ext4
git clone https://github.com/phoronix-test-suite/phoronix-test-suite.git
cp -R phoronix-test-suite/ /mnt/teamd-ext4
cd  /mnt/teamd-ext4/phoronix-test-suite/
sudo sh install-sh
cd $CWD
sudo /usr/bin/phoronix-test-suite batch-benchmark pts/fs-mark TEST_RESULTS_NAME=phoronixext4
sudo /usr/bin/phoronix-test-suite result-file-to-json phoronixbtrfs OUTPUT_FILE=$CWD/results/phoronix/phoronix_ext4.json
sudo umount /dev/mapper/swissknife-teamd
sudo mkfs.btrfs -f /dev/mapper/swissknife-teamd
sudo mount /dev/mapper/swissknife-teamd /mnt/teamd-btrfs
cp -R phoronix-test-suite/ /mnt/teamd-btrfs
cd  /mnt/teamd-btrfs/phoronix-test-suite/
sudo sh install-sh
cd $CWD
sudo /usr/bin/phoronix-test-suite batch-benchmark pts/fs-mark TEST_RESULTS_NAME=phoronixext4
sudo /usr/bin/phoronix-test-suite result-file-to-json phoronixbtrfs OUTPUT_FILE=$CWD/results/phoronix/phoronix_btrfs.json
sudo umount /dev/mapper/swissknife-teamd
