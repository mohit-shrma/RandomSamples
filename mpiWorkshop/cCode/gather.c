#include <stdio.h>
#include "mpi.h"
int main(int argc, char **argv) {

  int isend, irecv[5];
  int rank, size;
  int rc;
  
  rc =  MPI_Init(&argc, &argv);
  rc = MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  rc = MPI_Comm_size(MPI_COMM_WORLD, &size);

  isend = rank + 1;

  rc = MPI_Gather(&isend, 1, MPI_INT, &irecv, 1, MPI_INT, 0, MPI_COMM_WORLD);

  if (rank == 0) {
    printf("irecv = %d %d %d %d\n", irecv[0], irecv[1], irecv[2], irecv[3]);
  }

  rc = MPI_Finalize();
  printf("rc = %d\n", rc);
  return rc;
}
