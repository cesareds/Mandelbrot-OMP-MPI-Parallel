#! /bin/bash

echo "\n======Iniciou a compilação======\n"

echo "Compilando o apenas MPI\n"

mpic++ -O3 mandelbrot-mpi-only.cpp 

echo "Compilando o MPI com OpenMP\n"

mpic++ -O3 mandelbrot-with-omp.cpp -fopenmp
