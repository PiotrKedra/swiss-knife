echo 'Setting up PARSEC adn downloading inputs..'

. parsec-benchmark/env.sh
. parsec-benchmark/get-inputs

sudo mkdir -p results


echo "Building PARSEC apps..."
parsecmgmt -a build -p bodytrack
parsecmgmt -a build -p blacksholes
parsecmgmt -a build -p ferret


echo "Starting benchmarking bodytrack example with PARSEC.."

for i in 1 2 4 8 16 32 64 128
do
    echo "Running with $i cores"

    parsecmgmt -a run -p bodytrack -i simsmall -n $i > results/bodytrack_small_"$i".txt

    parsecmgmt -a run -p bodytrack -i simmedium -n $i > results/bodytrack_medium_"$i".txt

    parsecmgmt -a run -p bodytrack -i simlarge -n $i > results/bodytrack_large_"$i".txt

done

echo "Finished bodytrack example."



echo "Starting benchmarking blacksholes example with PARSEC.."

for i in 1 2 4 8 16 32 64 128
do
    echo "Running with $i cores"

    parsecmgmt -a run -p blacksholes -i simsmall -n $i > results/blacksholes_small_"$i".txt

    parsecmgmt -a run -p blacksholes -i simmedium -n $i > results/blacksholes_medium_"$i".txt

    parsecmgmt -a run -p blacksholes -i simlarge -n $i > results/blacksholes_large_"$i".txt

done

echo "Finished blacksholes example."


echo "Starting benchmarking ferret example with PARSEC.."

for i in 1 2 4 8 16 32 64 128
do
    echo "Running with $i cores"

    parsecmgmt -a run -p ferret -i simsmall -n $i > results/ferret_small_"$i".txt

    parsecmgmt -a run -p ferret -i simmedium -n $i > results/ferret_medium_"$i".txt

    parsecmgmt -a run -p ferret -i simlarge -n $i > results/ferret_large_"$i".txt

done

echo "Finished ferret example."