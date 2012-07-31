#include <stdio.h>
#include "mpi.h"
int main(int argc, char **argv) {

  int rank, size, tag, rc, i;
  MPI_Status status;
  int value;
  rc = MPI_Init(&argc, &argv);
  rc = MPI_Comm_size(MPI_COMM_WORLD, &size);
  rc = MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  tag = 100;

  
  if (rank == 0) {
    scanf("%d", &value);
  } else {
    value = 0;
  }

  //broadcast this to all
  rc = MPI_Bcast(&value, 1, MPI_INT, 0, MPI_COMM_WORLD);  

  printf("node %d: %d\n", rank, value);
  rc = MPI_Finalize();
  return rc;
}
