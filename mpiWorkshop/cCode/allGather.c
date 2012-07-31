#include <stdio.h>
#include "mpi.h"

int main(int argc, char **argv) {
  int a[2][8], b[8], cpart[2], ctotal[8];
  int rank, size, i, k;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Comm_size(MPI_COMM_WORLD, &size);

  if (size != 4) {
    printf("Error!: # of processors must be equal to 4.\n");
    printf("Aborting...\n");
    MPI_Abort(MPI_COMM_WORLD, 1);
  }

  //initialize randomly 2X8 matrices based on rank
  for (i = 0; i < 2; i++) {
    for (k = 0; k < 8; k++) {
      a[i][k] = rank * (k+1);
    }
  }

  //display matrices
  for (i = 0; i < 2; i++) {
    for (k = 0; k < 8; k++) {
      printf("%d ", a[i][k]);
    }
    printf("\n");
  }

  //initialize 8X1 vector
  for (k = 0; k < 8; k++) {
    b[k] = k + 1;
  }

  //perform multiplication of vector with matrix, store it
  //in cpart
  for (i = 0; i < 2; i++) {
    cpart[i] = 0;
    for (k = 0; k < 8; k++) {
      cpart[i] += a[i][k] * b[k];
    }
  }

  //display the product
  printf("%d %d", cpart[0], cpart[1]);

  //gather the vector product by sending to all processes and storing
  MPI_Allgather(&cpart, 2, MPI_INT, &ctotal, 2, MPI_INT, MPI_COMM_WORLD);

  //display the gathered products
  printf("\n");
  for (k = 0; k < 8; k++) {
    printf("%d ", ctotal[k]);
  }
  printf("\n");
  
  MPI_Finalize();
  return 0;
}
