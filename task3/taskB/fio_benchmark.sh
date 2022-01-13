sudo rm results/*.json

sudo fio seqread.fio --output-format=json --output=results/seqread.json
sudo fio seqwrite.fio --output-format=json --output=results/seqwrite.json
sudo fio randread.fio --output-format=json --output=results/randread.json
sudo fio randreadwrite.fio --output-format=json --output=results/randreadwrite.json
sudo fio seqreadwrite.fio --output-format=json --output=results/seqreadwrite.json
sudo fio randwrite.fio --output-format=json --output=results/randwrite.json
sudo fio vardepth.fio --output-format=json --output=results/vardepth.json

sudo rm /mnt/teamd-ext4/* 2> /dev/null
sudo rm /mnt/teamd-btrfs/* 2> /dev/null
