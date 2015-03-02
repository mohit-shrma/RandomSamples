library(MASS)

#number of clusters
numClusters <- 3

#number of data samples
N <- 1000

#variance constant of cluster centers
lambda <- 0.01

#variance constant for generated data
sigma <- matrix(c(0.01, 0,0, 0.01), 2,2)
mean1 <- c(3,5)
mean2 <- c(-1,-1)
mean3 <- c(7,7)

means <- array(1:6, dim=c(3,2))
means[1, ] <- mean1
means[2, ] <- mean2
means[3, ] <- mean3

#generate N sample points and zs
x <- rep(c(0,0), N)
dim(x) <- c(N, 2)
z <- rep(0, N)
for (i in 1:333) {
  z[i] <- 1 #sample(1:3, 1)
  x[i,] <- mvrnorm(n=1, means[z[i], ], sigma)  
}
for (i in 334:666) {
  z[i] <- 2 #sample(1:3, 1)
  x[i,] <- mvrnorm(n=1, means[z[i], ], sigma)  
}
for (i in 667:1000) {
  z[i] <- 3 #sample(1:3, 1)
  x[i,] <- mvrnorm(n=1, means[z[i], ], sigma)  
}

zDup <- rep(1, N)
means <- array(1:6, dim=c(3,2))
means[1, ] <- c(1,2)
means[2, ] <- c(2,3)
means[3, ] <- c(3,4)

#Gibbs sampling
for (iter in 1:1000) {
  
  #sample mu's or mean
  

  #sample zs
  for (i in 1:N) {
    zDup[i] <-  (1.0/numClusters) *  
  }

}





