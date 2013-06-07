import sys
import numpy as np
from scipy.stats import beta
from scipy.stats import bernoulli
import matplotlib.pyplot as plt

""" a,b -> prior parameters of beta distribution
    banditArms -> arms following bernoulli distribution, banditArms[i].rvs() to draw arm
"""
def thompsonBernoulli(a, b, banditArms):
    numArms = len(banditArms)
    successCounters = np.zeros(numArms)
    failCounters = np.zeros(numArms)
    thetas = np.zeros(numArms)

    for t in range(5000):
        #draw arms according to beta distribution
        for i in range(numArms):
            thetas[i] = beta(successCounters[i]+a, failCounters[i]+b).rvs()

        #get the arm with max theta
        maxArmInd = np.argmax(thetas)

        #draw the maxArmInd and observe the reward
        reward = banditArms[maxArmInd].rvs()

        if reward == 1:
            successCounters[maxArmInd] += 1
        else:
            failCounters[maxArmInd] += 1

    betaDists = [ beta(successCounters[i]+a, failCounters[i]+b) for i in range(numArms) ]

    return betaDists


def getBanditArms(numArms):
    armMeans = np.random.rand(numArms)
    banditArms = [ bernoulli(armMeans[i]) for i in range(numArms) ]
    return banditArms


def main():
    numArms = 2
    if len(sys.argv) > 1:
        numArms = int(sys.argv[1])
    banditArms = getBanditArms(numArms)
    betaDists = thompsonBernoulli(1, 1, banditArms)
    
    print 'Bandit arms: '
    for i in range(numArms):
        print banditArms[i].mean()

    print 'Beta Distributions: '
    for i in range(numArms):
        print betaDists[i].mean()


if __name__ == '__main__':
    main()
