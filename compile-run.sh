#! /bin/bash

echo "Precisa fazer a configuração inicial?(y/n)"
read resposta
if [ "$resposta" = "y" ]; then
    echo -e "\n=====Iniciou configuração inicial=====\n"
    for i in `seq 1 4`; do
        ssh ens$i "exit"
    done
fi


echo -e "\n======Iniciou a compilação======\n"

echo -e "Compilando o apenas MPI\n"
mpic++ mandelbrot-mpi-only.cpp -o bin/mandelbrot-mpi-only.out

echo -e "Compilando o MPI com OpenMP\n"
mpic++ mandelbrot-with-omp.cpp -o bin/mandelbrot-with-omp.out -fopenmp




echo -e "\n======Executando Mandelbrots======\n"

TIMEFORMAT="%R"
echo -e "Executando o apenas MPI\n"
rm times.txt
echo "mpi" >> times.txt
for i in `seq 1 16`; do
    for j in `seq 1 3`; do
        echo "Executando o mandelbrot${i}.in com MPI apenas"
        exec_time=$( { time mpirun --machinefile hosts.txt --mca btl_tcp_if_include 10.20.221.0/24 bin/mandelbrot-mpi-only.out < inputs/mandelbrot${i}.in > /dev/null; } 2>&1 )
        echo "$exec_time" >> times.txt
        echo $exec_time
    done
done

echo -e "Executando o MPI com OpenMP\n"
echo "omp" >> times.txt
for i in `seq 1 16`; do
    for j in `seq 1 3`; do
        echo "Executando o mandelbrot${i}.in com MPI e OpenMP"
        exec_time=$( { time mpirun -bind-to none --machinefile hosts.txt --mca btl_tcp_if_include 10.20.221.0/24 bin/mandelbrot-with-omp.out < inputs/mandelbrot${i}.in > /dev/null; } 2>&1 )
        echo $exec_time
        echo "$exec_time" >> times.txt
    done
done




echo "\n======Gerando gráficos======\n"

echo "Python >> graphic.png"
python3 plot.py

