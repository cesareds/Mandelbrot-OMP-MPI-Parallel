#include <complex>
#include <mpi.h>
#include <omp.h>
#include <iostream>

using namespace std;

int main(int argc, char **argv)
{
	int max_row, max_column, max_n;
	int rank, size;

	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

	if (rank == 0)
	{
		cin >> max_row;
		cin >> max_column;
		cin >> max_n;
	}

	MPI_Bcast(&max_row, 1, MPI_INT, 0, MPI_COMM_WORLD);
	MPI_Bcast(&max_column, 1, MPI_INT, 0, MPI_COMM_WORLD);
	MPI_Bcast(&max_n, 1, MPI_INT, 0, MPI_COMM_WORLD);

	char *dados = (char *)malloc(max_row * max_column * sizeof(char));

	char **mat = (char **)malloc(sizeof(char *) * max_row);
	for (int i = 0; i < max_row; i++)
	{
		mat[i] = &dados[i * max_column];
	}

	int fatia = max_row / size;

	int r, c, n;
	int start_row = rank * fatia;
	int end_row = start_row + fatia;

	for (r = start_row; r < end_row; ++r)
	{
		for (c = 0; c < max_column; ++c)
		{
			complex<float> z;
			n = 0;
			while (abs(z) < 2 && ++n < max_n)
				z = pow(z, 2) + decltype(z)(
									(float)c * 2 / max_column - 1.5,
									(float)r * 2 / max_row - 1);
			mat[r][c] = (n == max_n ? '#' : '.');
		}
	}

	MPI_Gather(&mat[fatia * rank][0], fatia * max_column, MPI_CHAR, &mat[0][0], fatia * max_column, MPI_CHAR, 0, MPI_COMM_WORLD);
	// if (rank == 0) {
	// 	for(int r = 0; r < max_row; ++r){
	// 		for(int c = 0; c < max_column; ++c)
	// 			std::cout << mat[r][c];
	// 		cout << '\n';
	// 	}
	// }

	MPI_Finalize();
}
