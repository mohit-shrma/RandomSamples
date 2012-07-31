#include <stdio.h>
#include "mpi.h"
int main(int argc, char **argv) {
  int rank, size, tag, rc, i;
  MPI_Status status;
  int value = 0;
  rc = MPI_Init(&argc, &argv);
  rc = MPI_Comm_size(MPI_COMM_WORLD, &size);
  rc = MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  tag = 100;
  while (value >= 0) {
    if (rank == 0){
      scanf("%d", &value);
      //send to others
      rc = MPI_Send(&value, 1, MPI_INT, rank+1, tag, MPI_COMM_WORLD);      
    } else {
      rc = MPI_Recv(&value, 1, MPI_INT, rank-1, tag, MPI_COMM_WORLD, &status);
      if (rank < size-1) {
	rc = MPI_Send(&value, 1, MPI_INT, rank+1, tag, MPI_COMM_WORLD);  
      }
    }
    printf("node %d: %d\n", rank, value);
  }
  rc = MPI_Finalize();
  return rc;
}
