#include <stdio.h>
#include "mpi.h"
int main(int argc, char **argv) {
  int rank, size, tag, rc, i;
  MPI_Status status;
  MPI_Request request;
  char message[20];
  rc = MPI_Init(&argc, &argv);
  rc = MPI_Comm_size(MPI_COMM_WORLD, &size);
  rc = MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  tag = 100;
  if (rank == 0) {
    strcpy(message, "Hello world!");
    rc = MPI_Isend(message, 13, MPI_CHAR, 1, tag, MPI_COMM_WORLD, &request);    
  } else {
    rc = MPI_Irecv(message, 13, MPI_CHAR, 0, tag, MPI_COMM_WORLD, &request);
  }
  
  printf("node %d: b4 wait\n", rank);
  MPI_Wait(&request, &status);
  printf("node %d: aftr wait message: %s\n", rank, message);    
  rc = MPI_Finalize();
}
