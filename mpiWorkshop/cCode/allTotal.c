#include <stdio.h>
#include "mpi.h"

int main(int argc, char **argv) {

  int send[4], recv[4];
  int rank, size, k;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  if (size != 4) {
    printf("Error!:# of processors must be equal to 4\n");
    printf("Aborting...\n");
    MPI_Abort(MPI_COMM_WORLD, 1);
  }

  //initialize row[rank] of matrix
  for (k = 0; k < size; k++) {
    send[k] = (k+1) + rank*size;
  }

  //display row[rank] of matrix
  printf("rank:%d %d %d %d %d\n", rank, send[0], send[1], send[2], send[3]);


  //send data to other processes
  MPI_Alltoall(&send, 1, MPI_INT, &recv, 1, MPI_INT, MPI_COMM_WORLD);

  //display the transposed vector from received data
  printf("rank:%d %d %d %d %d\n", rank, recv[0], recv[1], recv[2], recv[3]);
  
  MPI_Finalize();
  return 0;
}
