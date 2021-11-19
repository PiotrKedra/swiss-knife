mkdir -p wrk_result

for client_numbers in 1 2 4 8 16 32
do
echo "Benchmarking with $client_numbers clients..." 
wrk -t"$client_numbers" -c400 -d5s http://192.168.55.1:800 > wrk_result/clients_nr_"$client_numbers".txt
done

echo "Benchamrking done, creating a figure req/sec for given number of clients..."
sudo python generate_plots.py
echo "All done."
