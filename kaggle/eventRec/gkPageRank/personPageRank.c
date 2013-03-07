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


  
int getTopSimUsers(gk_csr_t *adjMat, int user, gk_fkv_t *topUsers, int nsim) {
  //to store the restart distributon of vertices
  float *pr;
  int i, j, count;
  int iter = 0;
  
  gk_fkv_t *pRanks;

  pr = (float*) malloc(sizeof(float)*adjMat->nrows);
  
  //initialize the restart distribution for user
  pr[user] = 1.0;
  iter = gk_rw_PageRank(adjMat, 0.5, 0.0001, 100, pr);

  count = 0;
  
  //count the non-zero values in pr and sort them
  for (i = 0; i < adjMat->nrows; i++) {
    if (pr[i] > 0) {
      count++;
    }
  }

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
  return nsim;
}


int main(int argc, char *argv[]) {

  int i, j, countTopUsers;
  
  //file containing matrix of form CSR
  char *ipCSRAdjFileName;

  //list of users on which to apply page rank
  char *usersFileName;

  //to store graph adjacency matrix
  gk_csr_t *adjMat;

  int numUsers;

  //araay of user id
  int *users;

  gk_fkv_t *topUsers;
  
  int minSimUsers;

  if (argc < 4) {
    //not wnough arguments passed
    printf("\n Not enough arguments passed. \n");
    return -1;
  } 
  
  //parse commandline arguments
  ipCSRAdjFileName = argv[1];
  usersFileName = argv[2];
  minSimUsers = atoi(argv[3]);
  
  //read the adjacency matrix
  adjMat = gk_csr_Read(ipCSRAdjFileName, GK_CSR_FMT_CSR, 0, 0);

  //get the number of users
  numUsers = getLineCount(usersFileName);
  users = getUsers(usersFileName, numUsers);

  topUsers = (gk_fkv_t*) malloc(sizeof(gk_fkv_t) * minSimUsers);
  
  //apply the personalized page rank for each user
  for (i = 0; i < numUsers; i++) {
    //get the top rank vertices from personalized page rank iteration
    countTopUsers = getTopSimUsers(adjMat, users[i], topUsers, minSimUsers);
    printf("Similar users for %d :\n", users[i]);
    //print the top users with corresponding pr
    for (j = 0; j < countTopUsers; j++) {
      printf("%8d \t %f\n", topUsers[j].val, topUsers[j].key);
    }
    
  }
    
  return 0;
}
