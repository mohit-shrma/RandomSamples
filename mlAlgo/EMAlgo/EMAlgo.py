import numpy as np
import scipy as sp
from scipy import stats
import math

""" apply em algorithm to data generated from 3 different univariate  gaussians
 and from the data try to learn the distributions used to generate data, 
Mixture of Gaussians"""


""" sample a point from passed distribution and return it """
def sampleFromDist(mu, sigma):
    return np.random.normal(mu, sigma)


""" sample passed number of points from passed distribution
according to passed weights """
def sampleFromDists(numPoints, mus, sigmas, weights):


    #store sample points
    samplePoints = [ [] for i in range(len(weights))]
    
    #assuming sum of weights to one compute thresholds/intervals
    thresh = []
    for wt in weights:
        if len(thresh) == 0:
            thresh.append(wt)
        else:
            thresh.append(wt + thresh[-1])

    for i in range(numPoints):
        #select the weight to use to sample data
        randWt = np.random.uniform(0, 1)

        #get the index of distribution to use to sample data
        for wtInd in range(len(thresh)):
            if randWt < thresh[wtInd]:
                break
    
        #sample point from distribution corresponding to weight
        samplePoints[wtInd].append(np.random.normal(mus[wtInd], sigmas[wtInd]))
        
    return samplePoints



""" perform expectation step and return learned posteriors/responsibilities
i.e. probability of selecting a distribution to sample a given point
using mus, sigmas, and weights/mixing coefficients
return posteriors of each point for every dist
e.g. here we have 3 dist  [(, , ), (, , )]
posterior: Y(Znk) = piK*N(Xn|muk, sigmaK)/sum<k dist>(pij*N(Xn|muk, sigmaj))
"""
def EStep(points, mus, sigmas, weights):
    responsibilities = []
    for point in points:
        pointPosteriors = []
        for k in range(len(mus)):
            posterior = weights[k] * stats.norm.pdf(point, loc=mus[k],\
                                                         scale=sigmas[k])
            pointPosteriors.append(posterior)
        #normalize point posteriors
        denom = sum(pointPosteriors)
        for k in range(len(pointPosteriors)):
            pointPosteriors[k] = pointPosteriors[k]/denom;
        responsibilities.append(pointPosteriors)
    return responsibilities



""" perform re-estimation of parameters using passed responsibilities of the
form  [[, , ], [, , ]] and return new mean std dev and weights/mixing params
"""
def MStep(responsibilities, points):

    #get the number of points
    numPoints = len(points)
    
    #get the number of ditrib
    numDistrib = len(responsibilities[0])
    
    #compute effective number of points assigned to each distribution
    #i.e. Nk = sum<all points> responsibility of kth distribution 
    effectivePointsinK = [0 for i in range(numDistrib)]
    for responsibility in responsibilities:
        for k in range(numDistrib):
            effectivePointsinK[k] += responsibility[k]

    #compute new mean for each distrib i.e muk
    newMus = [0 for i in range(numDistrib)]
    for i in range(numPoints):
        for k in range(numDistrib):
            newMus[k] += responsibilities[i][k] * points[i]
            
    for k in range(numDistrib):
        newMus[k] = newMus[k]/effectivePointsinK[k]

    #compute new std dev or sigma
    newSigmasSqr = [0 for i in range(numDistrib)]
    for i in range(numPoints):
        for k in range(numDistrib):
            newSigmasSqr[k] += \
                responsibilities[i][k] * math.pow((points[i] - newMus[k]), 2)
            
    for k in range(numDistrib):
        newSigmasSqr[k] = newSigmasSqr[k]/effectivePointsinK[k]

    newSigmas = [ math.sqrt(sigmaSqr) for sigmaSqr in newSigmasSqr]

    #compute new weights/mixing params
    newWeights = [  effectivePointsinK[k]/numPoints for k in range(numDistrib)] 

    print effectivePointsinK
    return (newMus, newSigmas, newWeights)



""" evaluate log likelihood
i.e. ln(p(X|mu, sigma, pi)) =
        sum<n points> {ln{sum<k dist> {piK*N(Xn|muk, sigmaK)}}}"""
def evalLogLikelihood(points, mus, sigmas, weights):
    
    logLikelihood = 0

    for point in points:
        sumKDist = 0
        for k in range(len(mus)):
            sumKDist += weights[k] * stats.norm.pdf(point,\
                                                           loc=mus[k],\
                                                           scale=sigmas[k])
        logLikelihood += math.log(sumKDist)
    return logLikelihood



""" check for convergence """
def chekConvergence(oldParams, newParams):
    
    oldLogLikelihood = oldParams[0]
    newLogLikelihood = newParams[0]
    
    #convergence of likelihood values
    if newLogLikelihood - oldLogLikelihood > 0.001:
        return False

    #convergence of other parameters
    for i in range(1, len(oldParams)):
        for k in range(len(oldParams[i])):
            if math.fabs(oldParams[i][k] - newParams[i][k]) > 0.001:
                return False

    return True
    


""" EM algorithm iterations """
def EMAlgortithm(points, mus, sigmas, weights):

    currLogLikelihood = evalLogLikelihood(points, mus, sigmas, weights)
    
    #perform 100 iterations
    for i in range(1000):
        
        #perform E step
        responsibilities = EStep(points, mus, sigmas, weights)

        #perform M step
        (newMus, newSigmas, newWeights) = MStep(responsibilities, points)

        #evaluate new logLikelihood
        newLogLikelihood = evalLogLikelihood(points, newMus, newSigmas, newWeights)

        #check for convergence
        isConverged = chekConvergence([currLogLikelihood, mus, sigmas, weights],
                                  [newLogLikelihood, newMus, newSigmas,\
                                       newWeights])
        if isConverged:
            print 'converged in ' + str(i) + ' iterations'
            break

        print 'iteration ' + str(i) +  ' mus: ', newMus,\
            ' sigmas: ', newSigmas, ' weights: ', newWeights
        
        #update new parameters as old params for next iteration
        mus = newMus
        sigmas = newSigmas
        weights = newWeights
        currLogLikelihood = newLogLikelihood
        
    return (mus, sigmas, weights)
        
    

""" initialize  means, covariances and mixing coefficients/weights """
def initParameters():
    
    #initial mean of distributions
    initialMus = [0.1, 0.8, 1.1]
    
    #initial variances of distributions
    initialSigmas = [0.1, 0.1, 0.1]

    #initialize mixing coefficients i.e. prob that a
    #particular component is picked or weights, P(Zk = 1) = Pik
    weights = [0.3, 0.3, 0.4]

    return (initialMus, initialSigmas, weights)



def main():
    #mu of three dist
    mus = [0.4, 1.0, 1.5]

    #sigma of three dist
    sigmas = [0.3, 0.3, 0.2]

    #weights or chance of selecting samples from these dist
    weights = [0.2, 0.3, 0.5]

    #sample 500 points from these distribution
    samplePoints = sampleFromDists(500, mus, sigmas, weights)

    
    
    #mege sample points into one
    points = []
    for sample in samplePoints:
        points = points + sample
    
    #initialize initial parameters
    (initialMus, initialSigmas, weights) = initParameters()

    (learnedMus, learnedSigmas, learnedWeights) = EMAlgortithm(points,\
                                                                   initialMus,\
                                                                   initialSigmas,\
                                                                   weights)
    for i in range(len(samplePoints)):
        print 'points in sample ' + str(i+1) + ': ' + str(len(samplePoints[i]))\
            + ', ' +  str(float(len(samplePoints[i]))/len(points))
    print 'original mus: ', mus, ' sigmas: ', sigmas, ' weights: ', weights
    print 'learned mus: ', learnedMus, ' sigmas: ', \
        learnedSigmas, ' weights: ', learnedWeights

    
if __name__ == '__main__':
    main()








