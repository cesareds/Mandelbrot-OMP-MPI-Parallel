#! /bin/bash

echo "Precisa fazer a configuração inicial?(y/n)"

if yes

echo "\n=====Iniciou configuração inicial=====\n"

for i in `seq 1 4`; do ssh ens$i "exit"; done




echo "\n======Iniciou a compilação======\n"

echo "Compilando o apenas MPI\n"
mpic++ mandelbrot-mpi-only.cpp -o bin/mandelbrot-mpi-only.out

echo "Compilando o MPI com OpenMP\n"
mpic++ mandelbrot-with-omp.cpp -o bin/mandelbrot-with-omp.out -fopenmp




echo "\n======Executando Mandelbrots======\n"

echo "Executando o apenas MPI\n"
time mpirun --machinefile hosts.txt  --mca btl_tcp_if_include 10.20.221.0/24 bin/mandelbrot-mpi-only.out < mandelbrot.in >> times.txt

echo "Executando o MPI com OpenMP\n"
time mpirun -bind-to none --machinefile hosts.txt  --mca btl_tcp_if_include 10.20.221.0/24 bin/mandelbrot-with-omp.out < mandelbrot.in >> times.txt




echo "\n======Gerando gráficos======\n"

echo "Python >> graphic.png"
python3 plot.py
open graphic.png



