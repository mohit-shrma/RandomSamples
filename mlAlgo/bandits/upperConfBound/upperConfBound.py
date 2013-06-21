import sys
import numpy as np

import matplotlib.pyplot as plt

#armNum - starts with 0 indexing
def playArm(armInd, actMeans, actVar):
    return np.random.normal(actMeans[armInd],\
                            actVar[armInd], 1)[0]


def UCBInit(armRewardsSeq, numArms,\
                actMeans, actVar):

    #play each arm once
    for i in range(numArms):
        armRewardsSeq[i].append(playArm(i, actMeans, actVar))
    return armRewardsSeq


def findBestArm(armRewardsSeq):
    numArms = len(armRewardsSeq)
    playsSoFar = np.sum(map(len, armRewardsSeq))    
    maxBound = -100
    maxInd = -1
    for i in range(numArms):
        bound = np.mean(armRewardsSeq[i]) + \
            np.sqrt(2*np.log(playsSoFar)/len(armRewardsSeq[i]))
        if bound > maxBound:
            maxBound = bound
            maxInd = i
    return maxInd


def performUCBSteps(armRewardsSeq, numArms,\
                actMeans, actVar, numSteps):
    losses = np.zeros(numSteps+1)
    regret = np.zeros(numSteps+1)
    #mu*
    actBestMean = np.max(actMeans)
    for i in range(1, numSteps+1):
        bestArmInd = findBestArm(armRewardsSeq)
        bestArmReward = playArm(bestArmInd, actMeans, actVar)
        armRewardsSeq[bestArmInd].append(bestArmReward)
        losses[i] = losses[i-1] + (actBestMean - bestArmReward)
        regret[i] = regret[i-1] + (actBestMean - actMeans[bestArmInd])
    return (losses, regret)


def plot(losses , xlabel):
    numSteps = len(losses)
    plt.figure()
    plt.plot(range(numSteps), losses)
    plt.xlabel('steps')
    plt.ylabel(xlabel)
    plt.show()


#arms actually follow a normal dist
def getBanditArms(numArms):
    armMeans = np.random.rand(numArms)
    armVar = np.random.rand(numArms)
    return (armMeans, armVar)


def main():
    numArms = 3
    if len(sys.argv) > 1:
        numArms = int(sys.argv[1])
    (actMeans, actVar) = getBanditArms(numArms)
    armRewardsSeq = []
    if len(armRewardsSeq) == 0:
        armRewardsSeq = [[] for i in range(numArms)]
    UCBInit(armRewardsSeq, numArms, actMeans, actVar)
    (losses, regret) = performUCBSteps(armRewardsSeq, numArms,\
                                           actMeans, actVar, 10000)
    print 'actMeans: ', actMeans
    print 'num plays: ', map(len, armRewardsSeq)
    plot(losses, 'losses')
    
    plot(regret, 'regret')


if __name__ == '__main__':
    main()
