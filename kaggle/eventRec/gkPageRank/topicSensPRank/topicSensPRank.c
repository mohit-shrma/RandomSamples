#include "GKlib.h"
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

//link the below file during compilation


int getLineCount(char *fileName) {
  FILE *file;
  int ch, count;
  count = 0;
  file = fopen(fileName, "r");
  while ((ch = getc(file)) != EOF) {
    if ((char)ch == '\n') {
      count++;
    }
  }
  return count;
}


int** getBiasedUsers(char *fileName, int lineCount, int maxNumUsersPerLine,
		     int numNodes) {
  FILE *file;
  int **biasedUsersList;
  char *line, *user;
  int i, len, j;
  len = 1500;
  file = fopen(fileName, "r");

  if (file == NULL) {
    return NULL;
  }

  line = (char*) malloc(sizeof(char)*1500);
  biasedUsersList = (int**) malloc(sizeof(int*) * lineCount);
  for (i = 0; i < lineCount; i++) {
    biasedUsersList[i] = (int*) malloc(sizeof(int) * maxNumUsersPerLine);
    //reset the list to -1, which won't exist in graph
    for (j = 0; j < maxNumUsersPerLine; j++) {
      biasedUsersList[i][j] = -1;
    }
  }

  i = 0;

  while (getline(&line, &len, file) > 0 && i < lineCount) {
    j = 0;
    //parse line to get the biased users list
    user = strtok(line, ",\n");
    while (user != NULL) {
      assert(atoi(user) < numNodes);
      biasedUsersList[i][j] = atoi(user);
      user = strtok(NULL, ",\n");
      j++;
    }
    i++;
  }

  free(line);
  return biasedUsersList;
}





void display(int *arr, int count) {
  int i;
  for (i = 0; i < count; i++) {
    printf("%d\n", arr[i]);
  }
}


/*
 * biasedUSers - users towards which random walk will be biased
 * numBiasedUsers - no. of users towards which random walk will be biased
 */  
int getTopSimUsers(gk_csr_t *adjMat, int* biasedUsers, int maxBiasUsersCount,
		   gk_fkv_t *topUsers, int nsim) {
  //to store the restart distributon of vertices
  float *pr;
  int i, j, count;
  int iter = 0;
  
  gk_fkv_t *pRanks;
  int biasedUsercount = 0;
  

  pr = (float*) malloc(sizeof(float)*adjMat->nrows);
  for (i = 0; i < adjMat->nrows; i++) {
    pr[i] = 0.0;
  }
  
  for (i = 0; i < maxBiasUsersCount; i++) {
    if (biasedUsers[i] != -1) {
      biasedUsercount++;
    } else {
      break;
    }
  }

  //initialize the restart distribution for user
  for (i = 0; i < biasedUsercount; i++) {
    if (biasedUsers[i] == -1) {
      break;
    }
    assert(biasedUsers[i] < adjMat->nrows);
    pr[biasedUsers[i]] = 1.0/biasedUsercount;
  }

  iter = gk_rw_PageRank(adjMat, 0.75, 0.000001, 100, pr);
  
  fprintf(stderr, "Iter: %d\n", iter);
  count = 0;
  
  //count the non-zero values in pr and sort them
  for (i = 0; i < adjMat->nrows; i++) {
    if (pr[i] > 0) {
      count++;
    }
  }
  
  fprintf(stderr, "Found %d similar users.\n", count);
  pRanks = gk_fkvmalloc(count, "store page ranks");

  for (i = 0, j = 0; i < adjMat->nrows; i++) {
    if (pr[i] > 0) {
      pRanks[j].key = pr[i];
      pRanks[j].val = i;
      j++;
    }
  }

  nsim = gk_min(nsim, count);
  gk_dfkvkselect(count, nsim, pRanks);
  gk_fkvsortd(nsim, pRanks);
  gk_fkvcopy(nsim, pRanks, topUsers);
  
  free(pr);
  free(pRanks);

  return nsim;
}


int main(int argc, char *argv[]) {

  int i, j, k, countTopUsers;
  
  //file containing matrix of form CSR
  char *ipCSRAdjFileName;

  //biased users file name
  char *biasedUsersFileName;

  //number of cpus
  int cpucount;

  //to store graph adjacency matrix
  gk_csr_t *adjMat;

  //number of biased users
  int numBiasedIterations;

  //array of biased users
  int **biasedUsersList;

  gk_fkv_t **topUsers;
  int *topUserCount;

  int minSimUsers;
  int maxNumUsersPerLine;

  char *opFile = "GraphRead.txt";
  
  if (argc < 5) {
    //not wnough arguments passed
    printf("\n Not enough arguments passed. \n");
    return -1;
  } 
  
  //parse commandline arguments
  ipCSRAdjFileName = argv[1];
  biasedUsersFileName = argv[2];
  maxNumUsersPerLine = atoi(argv[3]);
  minSimUsers = atoi(argv[4]);
  cpucount = atoi(argv[5]);

  //printf("\nBuilding adjacency matrix...\n");
  //read the adjacency matrix
  adjMat = gk_csr_Read(ipCSRAdjFileName, GK_CSR_FMT_CSR, 0, 0);
  //gk_csr_Write(adjMat, opFile, GK_CSR_FMT_CSR, 0, 0);
    
  fprintf(stderr, "\nMatrix building completed...\n");
  
  //get the number of biased iterations need to be done
  numBiasedIterations = getLineCount(biasedUsersFileName);

  //get the biased users
  biasedUsersList = getBiasedUsers(biasedUsersFileName, numBiasedIterations,
				   maxNumUsersPerLine, adjMat->nrows);

  //display the biased user list
  /*fprintf(stderr, "\nbiased users list %d as follow...\n", numBiasedIterations);
  for (i = 0; i < numBiasedIterations; i++) {
    for(j = 0; j < maxNumUsersPerLine; j++) {
      if (biasedUsersList[i][j] == -1) {
	break;
      }
      fprintf(stderr, "%d ", biasedUsersList[i][j]);
    }
    fprintf(stderr, "\n");
    }*/


  //maintain storage of top similar users of cpucount users
  topUsers = (gk_fkv_t**) malloc(sizeof(gk_fkv_t*) * cpucount);
  for (i = 0; i < cpucount; i++) {
    topUsers[i] = (gk_fkv_t*) malloc(sizeof(gk_fkv_t) * minSimUsers);
  }

  //storage for top users count of chunk
  topUserCount = (int *) malloc(sizeof(int) * cpucount);
  
  //apply the personalized page rank for each user
  for (i = 0; i < numBiasedIterations; i+=cpucount) {

#pragma omp parallel default(none) private(j) shared(biasedUsersList, topUsers, topUserCount, adjMat) \
  firstprivate(i, minSimUsers, numBiasedIterations, cpucount, maxNumUsersPerLine)
    {
#pragma omp for
      for (j = 0; j < cpucount; j++) {
	if (i+j < numBiasedIterations) {
	  //find top users for users[i+j]
	  //get the top rank vertices from personalized page rank iteration

	  //get the biased user for current iteration: biasedUsersList[i+j]
	  topUserCount[j] = getTopSimUsers(adjMat, biasedUsersList[i+j], maxNumUsersPerLine,
					   topUsers[j], minSimUsers);
	}
      }
    }

    //write the values for users chunks
    for (j = 0; j < cpucount; j++) {
      if (i+j < numBiasedIterations) {
	//ieration number
	printf("%d", i+j);
	for (k = 0; k < topUserCount[j]; k++) {
	  //print the top similar users with corresponding pr
	  printf("\t%d:%f", topUsers[j][k].val, topUsers[j][k].key);
	}
	printf("\n");
      }
    }
    
  }
    
  return 0;
}
