#include <stdio.h>
#include "mpi.h"
#include <math.h>

int main(int argc, char **argv) {

  int size, rank, iStart, iEnd, i;
  double sum, temp;
  double a[9];

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  //initialize the portion of array corresponding to
  //this rank process
  iStart = rank * 3;
  iEnd = iStart + 3 - 1;
  for (i =  iStart; i <= iEnd; i++) {
    a[i] = i + 1;
  }

  //sum portion of this process
  sum = 0.0;
  for (i = iStart; i <= iEnd; i++) {
    sum += a[i];
  }

  //reduce sums by applying an operator on all sum from procs
  MPI_Reduce(&sum, &temp, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

  sum = temp;

  if (rank == 0) {
    printf("sum = %f\n", sum);
  }

  MPI_Finalize();
  return 0;
}
