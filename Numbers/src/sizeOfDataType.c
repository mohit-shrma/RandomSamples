/*
 * program to identify size of data types, based on pointer arithmetic
 * also compute MIN and MAX signed int
 */

#include <stdio.h>

/*
 * compute power of a number using divide and conquer i.e. x**n 
 */
float pow(int x, int n) {

  float halfPow;
  
  if (n == 0) {
    return 1;
  }

  halfPow = pow(x, n/2);

  if (n%2 == 0) {
    //even power
    return halfPow*halfPow;
  } else {
    //odd power
    return halfPow*halfPow*x;
  }
  
}



int main(int argc, char **argv) {
  int i;
  int iNum = 5;
  float fNum = 5.0;
  double dNum = 8.0;

  int *iP = &iNum;
  float *fP = &fNum;
  double *dP = &dNum;

  int sizeInt = (char*)(iP+1) - (char*)(iP);
  int sizeFloat = (char*)(fP+1) - (char*)(fP);
  int sizeDouble = (char*)(dP+1) - (char*)(dP);

  for (i = 0; i < argc; i++) {
    printf("\npassed argument %d: %s %s ", (i+1), argv[i], *(argv + i));
  }
  
  printf("\nactual size of int here: %d bytes", sizeInt);
  //max. value, considering one bit MSB for sign i.e. 0 for +ve  (2**(sizeInt*8-1)) - 1
  printf("\n max +ve val of int: %d: ", (int)pow(2, (sizeInt*8 - 1)) - 1 );
  //min. value, considering one bit for sign -(2**(sizeInt*8-1))
  //as -ve numbers are store in two complement, MSB 1 for -ve
  //also for signed (int)(MAX_INT+1) will give min int value
  printf("\n min -ve val of int: %d: ", (int)(-1 * pow(2, (sizeInt*8 - 1))));
  printf("\nactual size of float here: %d bytes", sizeFloat);
  printf("\nactual size of double here: %d bytes \n", sizeDouble);
  
  return 0;
}
