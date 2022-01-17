sudo rm results/*.json
sudo mkfs.ext4 -f /dev/mapper/swissknife-teamd
sudo mount /dev/mapper/swissknife-teamd /mnt/teamd-ext4

sudo fio seqread_btrfs.fio --output-format=json --output=results/seqread_ext4.json
sudo fio seqwrite.fio --output-format=json --output=results/seqwrite_ext4.json
sudo fio randread.fio --output-format=json --output=results/randread_ext4.json
sudo fio randreadwrite.fio --output-format=json --output=results/randreadwrite_ext4.json
sudo fio seqreadwrite.fio --output-format=json --output=results/seqreadwrite_ext4.json
sudo fio randwrite.fio --output-format=json --output=results/randwrite_ext4.json
sudo fio vardepth.fio --output-format=json --output=results/vardepth_ext4.json

sudo umount /dev/mapper/swissknife-teamd

sudo mkfs.btrfs -f /dev/mapper/swissknife-teamd
sudo mount /dev/mapper/swissknife-teamd /mnt/teamd-btrfs

sudo fio seqread_btrfs.fio --output-format=json --output=results/seqread_btrfs.json
sudo fio seqwrite_btrfs.fio --output-format=json --output=results/seqwrite_btrfs.json
sudo fio randread_btrfs.fio --output-format=json --output=results/randread_btrfs.json
sudo fio randreadwrite_btrfs.fio --output-format=json --output=results/randreadwrite_btrfs.json
sudo fio seqreadwrite_btrfs.fio --output-format=json --output=results/seqreadwrite_btrfs.json
sudo fio randwrite_btrfs.fio --output-format=json --output=results/randwrite_btrfs.json
sudo fio vardepth_btrfs.fio --output-format=json --output=results/vardepth_btrfs.json

sudo umount /dev/mapper/swissknife-teamd
