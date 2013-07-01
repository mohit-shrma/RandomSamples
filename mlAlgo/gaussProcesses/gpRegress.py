""" tried regression using GP need to experiment with kernel params"""


import numpy as np
import matplotlib.pyplot as plt

linearKernel = lambda x, y : np.dot(x,y)
brownianKernel = lambda x, y: min(x,y)
expKernel = lambda x, y: 1*np.exp(-1*np.square(x-y))

kernel = expKernel

#sample points
n = 200
x = np.linspace(0, 10, n)
y = x*x
permInd = np.random.permutation(n)
permX = x[permInd]
numTrain = 150
numTest = n - numTrain

#training data
trainInd = permInd[:numTrain]
trainX = x[trainInd]
trainY = y[trainInd]

#test data
testInd = permInd[numTrain:]
testX = x[testInd]
testY = y[testInd] 


#gaussian processes param: Zx ~  GP(mu. k)
#mu - mean function, k - kernel
# Yi = Zxi + Ei where E ~ N(0, noiseSigma^2*I) is noise

noiseSigma = 0.5

#construct covariance matrix using kernel k
k = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        k[i][j] = kernel(permX[i], permX[j])


#let mu be zeros
mu = np.zeros(n)

#divide mu and k for train and test points
#a - test, b - train
mub = mu[0:numTrain]
mua = mu[numTrain:]

kaa = k[0:numTest, 0:numTest]
kab = k[0:numTest, numTest:]
kba = k[numTest:, 0:numTest]
kbb = k[numTest:, numTest:]

#update with noise ~ N(0,sigma^2*I)
Cab = kab
Cba = kba
Caa = kaa + (np.square(noiseSigma)*np.eye(numTest))
Cbb = kbb + (np.square(noiseSigma)*np.eye(n - numTest))

#Inference
#Ya|Yb ~ N(m, D)
Ya = testY
Yb = trainY

m = mua + np.dot(np.dot(Cab, np.linalg.inv(Cbb)), (Yb - mub))
D = Caa - np.dot(np.dot(Cab, np.linalg.inv(Cbb)), Cba)

plt.figure()

#plot actual test labels
plt.plot(testX, testY, '.')

#plot predicted labels with variance
plt.plot(testX, m, '+')


plt.show()
