sudo mkdir -p results


echo "Building PARSEC apps..."
parsecmgmt -a build -p bodytrack
parsecmgmt -a build -p blackscholes
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



echo "Starting benchmarking blackscholes example with PARSEC.."

for i in 1 2 4 8 16 32 64 128
do
    echo "Running with $i cores"

    parsecmgmt -a run -p blackscholes -i simsmall -n $i > results/blackscholes_small_"$i".txt

    parsecmgmt -a run -p blackscholes -i simmedium -n $i > results/blackscholes_medium_"$i".txt

    parsecmgmt -a run -p blackscholes -i simlarge -n $i > results/blackscholes_large_"$i".txt

done

echo "Finished blackscholes example."


echo "Starting benchmarking ferret example with PARSEC.."

for i in 1 2 4 8 16 32 64 128
do
    echo "Running with $i cores"

    parsecmgmt -a run -p ferret -i simsmall -n $i > results/ferret_small_"$i".txt

    parsecmgmt -a run -p ferret -i simmedium -n $i > results/ferret_medium_"$i".txt

    parsecmgmt -a run -p ferret -i simlarge -n $i > results/ferret_large_"$i".txt

done

echo "Finished ferret example."