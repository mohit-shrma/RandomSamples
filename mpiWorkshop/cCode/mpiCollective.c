#include <stdio.h>
#include "mpi.h"
#include <math.h>

//calculate value of pi by calculating the integral


int main(int argc, char **argv) {

  int n, myId, numProcs, i;
  //value of pi upto 25 decimal places
  double PI25DT = 3.141592653589793238462643;
  double mypi, pi, h, sum, x;

  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &numProcs);
  MPI_Comm_rank(MPI_COMM_WORLD, &myId);

  printf("Process ', %d, ' of ', %d ' is alive\n", myId, numProcs);

  while(1) {

    if (myId == 0) {
      printf("Enter the number of intervals (0 to quit): ");
      fflush(stdout);
      scanf("%d", &n);
    }

    //broadcast the number of intervals
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

    if (n == 0) {
      break;
    } else {
      //calculate the length of each interval
      h = 1.0 / (double) n;
      sum = 0.0;
      for (i = myId+1; i <= n; i += numProcs) {
	x = h * ((double)i - 0.5);
	sum += 4.0 / (1.0 + x*x);
      }
      //multiply sum by the width of each interval
      //h*y1 + h*y2 + h*y3 + ...
      mypi = h * sum;

      //apply reduction by summing the value from each process
      MPI_Reduce(&mypi, &pi, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

      if (myId == 0) {
	printf("pi is approx. %.16f, error is %.16f\n", pi, fabs(pi - PI25DT));
      }
    }
    
  }
  MPI_Finalize();
  return 0;
}
