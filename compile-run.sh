#! /bin/bash

echo "Precisa fazer a configuração inicial?(y/n)"

if yes

echo "\n=====Iniciou configuração inicial=====\n"

(0) Executar apenas 1 vez

for i in `seq 1 4`; do ssh ens$i "exit"; done

(1) Compilação:

mpic++ codigo.c -o saida 

(2) Criar um arquivo informando os servidores (exemplo: hosts.txt):

ens1

ens2

ens3

ens4

ens5

(3) Execução (sempre com origem na ens5):

mpirun --machinefile hosts.txt  --mca btl_tcp_if_include 10.20.221.0/24 mandelbrot < mandelbrot.in

(4) Execução (sempre com origem na ens5) usando MPI e OpenMP:

mpirun -bind-to none --machinefile hosts.txt  --mca btl_tcp_if_include 10.20.221.0/24 mandelbrot < mandelbrot.in








echo "\n======Iniciou a compilação======\n"

echo "Compilando o apenas MPI\n"

mpic++ -O3 mandelbrot-mpi-only.cpp 

echo "Compilando o MPI com OpenMP\n"

mpic++ -O3 mandelbrot-with-omp.cpp -fopenmp
