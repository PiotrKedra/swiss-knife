echo "Building project.."

make

echo "Finished building."

echo "Starting benchmarking word count with phoneix.."

sudo mkdir -p results
sudo touch results/word_count-small.txt
sudo touch results/word_count-medium.txt
sudo touch results/word_count-large.txt

sudo chmod 777 results/word_count-small.txt
sudo chmod 777 results/word_count-medium.txt
sudo chmod 777 results/word_count-large.txt

sudo echo -n "" > results/word_count-small.txt
sudo echo -n "" > results/word_count-medium.txt
sudo echo -n "" > results/word_count-large.txt

for i in 1 2 4 8 16 32 64 128
do
    echo "Running with $i cores"

    sudo ./tests/word_count/word_count-pthread tests/word_count/small.txt $i >> results/word_count-small.txt

    sudo ./tests/word_count/word_count-pthread tests/word_count/medium.txt $i >> results/word_count-medium.txt

    sudo ./tests/word_count/word_count-pthread tests/word_count/large.txt $i >> results/word_count-large.txt

done

echo "Finished benchmarking word count example."


echo "Starting benchmarking matrix multiply with phoneix.."

sudo touch results/matrix-small.txt
sudo touch results/matrix-medium.txt
sudo touch results/matrix-large.txt

sudo chmod 777 results/matrix-small.txt
sudo chmod 777 results/matrix-medium.txt
sudo chmod 777 results/matrix-large.txt

sudo echo -n "" > results/matrix-small.txt
sudo echo -n "" > results/matrix-medium.txt
sudo echo -n "" > results/matrix-large.txt

for i in 1 2 4 8 16 32 64 128
do
    echo "Running with $i cores"

    sudo ./tests/matrix_multiply/matrix_multiply-pthread 100 100 $i >> results/matrix-small.txt

    sudo ./tests/matrix_multiply/matrix_multiply-pthread 800 800 $i >> results/matrix-medium.txt

    sudo ./tests/matrix_multiply/matrix_multiply-pthread 1500 1500 $i >> results/matrix-large.txt

done

echo "Finished benchmarking matrix multiply example. Results can be found within /results folder."