#include <stdio.h>
#include <stdlib.h>
#include "mpi.h"

#define NUM_OF_TESTS 10

/*
 * This is similar to barrier, except it times a SINGLE allreduce on a 
 * double.
 */

int main(int argc, char **argv) {

  int rank, size;
  double t1, t2, tmin;
  double d_in, d_out;
  int j, k, nloop;

  MPI_Init(&argc, &argv);

  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  if (rank == 0 && size == 1) {
    printf("kind np time(Sec)\n");
  }

  nloop = 1000;
  tmin = 1000;

  for (k = 0; k < NUM_OF_TESTS; k++) {
    //block other processes until reach here
    MPI_Barrier(MPI_COMM_WORLD);
    d_in = 1.0;
    t1 = MPI_Wtime();
    for (j = 0; j < nloop; j++) {
      MPI_Allreduce(&d_in, &d_out, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    }
    t2 = (MPI_Wtime() - t1) / nloop;
    if (t2 < tmin) {
      tmin = t2;
    }
  }

  if (rank == 0) {
    printf("Allreduce %d %f\n", size, tmin);
  }
  
  MPI_Finalize();
  return 0;
}
