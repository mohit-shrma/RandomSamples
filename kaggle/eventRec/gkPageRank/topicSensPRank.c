#include "GKlib.h"
#include <stdio.h>
#include <stdlib.h>
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


int* getUsers(char *fileName, int lineCount) {
  //count number of users in file
  FILE *file;
  int *users;
  char *line;
  int i, len;
  len = 15;
  file = fopen(fileName, "r");

  if (file == NULL) {
    return NULL;
  }

  line = (char*) malloc(sizeof(char)*15);
  users = (int *) malloc(sizeof(int) * lineCount);
  i = 0;
  while (getline(&line, &len, file) > 0 && i < lineCount) {
    users[i++] = atoi(line);
  }
  
  free(line);
  return users;
}


void display(int *arr, int count) {
  int i;
  for (i = 0; i < count; i++) {
    printf("%d\n", arr[i]);
  }
}


/*
 * rusers - users towards which random walk will be biased
 * nrusers - no. of users towards which random walk will be biased
 */  
int getTopSimUsers(gk_csr_t *adjMat, int* rusers, int nrusers, gk_fkv_t *topUsers, int nsim) {
  //to store the restart distributon of vertices
  float *pr;
  int i, j, count;
  int iter = 0;
  
  gk_fkv_t *pRanks;

  pr = (float*) malloc(sizeof(float)*adjMat->nrows);
	for (i = 0; i < adjMat->nrows; i++) {
		pr[i] = 0.0;
	}

  //initialize the restart distribution for user
	for (i = 0; i < nrusers; i++) {
		pr[rusers[i]] = 1.0/nrusers;
	}

  iter = gk_rw_PageRank(adjMat, 0.5, 0.000001, 100, pr);
  
  fprintf(stderr, "Iter: %d\n", iter);
  count = 0;
  
  //count the non-zero values in pr and sort them
  for (i = 0; i < adjMat->nrows; i++) {
    if (pr[i] > 0 && i != user) {
      count++;
    }
  }
  
  //printf("Found %d similar users.\n", count);
  pRanks = gk_fkvmalloc(count, "store page ranks");

  for (i = 0, j = 0; i < adjMat->nrows; i++) {
    if (pr[i] > 0 && i != user) {
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

  //list of users on which to apply page rank
  char *usersFileName;

  //biased users file name
  char *biasedUsersFileName;

  //number of cpus
  int cpucount;

  //to store graph adjacency matrix
  gk_csr_t *adjMat;

  int numUsers;

  //araay of user id
  int *users;

  gk_fkv_t **topUsers;
  int *topUserCount;

  int minSimUsers;

  char *opFile = "GraphRead.txt";
  
  if (argc < 4) {
    //not wnough arguments passed
    printf("\n Not enough arguments passed. \n");
    return -1;
  } 
  
  //parse commandline arguments
  ipCSRAdjFileName = argv[1];
  usersFileName = argv[2];
  minSimUsers = atoi(argv[3]);
  cpucount = atoi(argv[4]);

  //printf("\nBuilding adjacency matrix...\n");
  //read the adjacency matrix
  adjMat = gk_csr_Read(ipCSRAdjFileName, GK_CSR_FMT_CSR, 0, 0);
  //gk_csr_Write(adjMat, opFile, GK_CSR_FMT_CSR, 0, 0);
    
  fprintf(stderr, "\nMatrix building completed...\n");
  //get the number of users
  numUsers = getLineCount(usersFileName);
  users = getUsers(usersFileName, numUsers);
  
  //maintain storage of top similar users of cpucount users
  topUsers = (gk_fkv_t**) malloc(sizeof(gk_fkv_t*) * cpucount);
  for (i = 0; i < cpucount; i++) {
    topUsers[i] = (gk_fkv_t*) malloc(sizeof(gk_fkv_t) * minSimUsers);
  }

  //storage for top users count of chunk
  topUserCount = (int *) malloc(sizeof(int) * cpucount);
  
  //apply the personalized page rank for each user
  for (i = 0; i < numUsers; i+=cpucount) {

#pragma omp parallel default(none) private(j) shared(users, topUsers, topUserCount, adjMat) \
  firstprivate(i, minSimUsers, numUsers, cpucount)
    {
#pragma omp for
      for (j = 0; j < cpucount; j++) {
	if (i+j < numUsers) {
	  //find top users for users[i+j]
	  //get the top rank vertices from personalized page rank iteration	
	  topUserCount[j] = getTopSimUsers(adjMat, users[i+j], topUsers[j], minSimUsers);
	}
      }
    }

    //write the values for users chunks
    for (j = 0; j < cpucount; j++) {
      if (i+j < numUsers) {
	//user 
	printf("%d", users[i+j]);
	for (k = 0; k < topUserCount[j]; k ++) {
	  //print the top similar users with corresponding pr
	  printf("\t%d:%f", topUsers[j][k].val, topUsers[j][k].key);
	}
	printf("\n");
      }
    }
    

  }
    
  return 0;
}
