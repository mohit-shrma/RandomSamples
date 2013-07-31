import scipy.io as sio
import numpy as np

topTagsMat = sio.mmread('topTagsGraph.mtx')
topTagsMat = topTagsMat.tocsr()
JENSEN_THRESH = np.log(2) * 0.95
MUTUAL_THRESH = np.log(2)

#get KL divergence of two vectors 
def klDiv(aVec, bVec):
    aVec = np.asarray(aVec).reshape(-1)
    bVec = np.asarray(bVec).reshape(-1)
    inds = (aVec != 0) & (bVec != 0)
    d = np.dot(np.log(aVec[inds]/bVec[inds]), aVec[inds])
    return d


#get jensenShannon divergence of two vectors
def jensenShannonDiv(p, q):
    #normalized vectors
    pNorm = p.todense()/np.sum(p.todense())
    qNorm = q.todense()/np.sum(q.todense())
    #average the distribution
    m = (pNorm+qNorm)/2
    #calculate the jensen shannon divergence
    jsd = 0.5*(klDiv(pNorm, m) + klDiv(qNorm, m))
    return jsd


#get mutual info
def mutualInfo(t1Ind, t2Ind, size):
    jointCount = topTagsMat[t1Ind, t2Ind]
    t1Count = np.sum(topTagsMat[t1Ind, :])
    t2Count = np.sum(topTagsMat[t2Ind, :])
    return np.log( (jointCount/size)/( (t1Count/size)*(t2Count/size) ) )


#perform similarity-based clustering
def getSimBasedClusters():
    numTerms = topTagsMat.shape[0]
    simMatrix = np.zeros((numTerms, numTerms))
    clusters = {}
    
    for i in range(numTerms):
        print i
        for j in range(i+1, numTerms):
            jsd = jensenShannonDiv(topTagsMat[i,:], topTagsMat[j,:])
            simMatrix[i,j] = jsd
            simMatrix[j,i] = jsd
            """if jsd <= JENSEN_THRESH:
                #add i, j into one cluster
                if i not in clusters:
                    clusters[i] = []
                clusters[i].append(j)"""
    
    print 'performed similarity computations'

    print 'performed pairwise clustering'

    #TODO: collapse clusters
    """collapsedClusters = []
    collapsedInds = set([])
    for ind, simInds in clusters.iteritems():
        clusSet = set([])
        clusSet.add(ind)
        exploreInds = simInds
        collapsedInds.add(ind)

        while len(exploreInds) > 0:
            for ind in exploreInds:
                exploreInds.remove(ind)
                if ind not in collapsedInds:
                    collapsedInds.add(ind)
                    clusSet.add(ind)
                    #explore cluster assoc with ind
                    exploreInds.append(clusters[ind])

        collapsedClusters.append(clusSet)"""
    return collapsedClusters




#perform pair-wise clustering
def getPairWiseClusters():

    numTerms = topTagsMat.shape[0]
    clusters = {}

    for i in range(numTerms):
        for j in range(i+1, numTerms):
            mutInfo = mutualInfo(topTagsMat[i,:], topTagsMat[j,:], 90000)
            if mutInfo <= MUTUAL_THRESH:
                #add i, j into one cluster
                if i not in clusters:
                    clusters[i] = []
                clusters[i].append(j)

    #TODO: collapse clusters
    collapsedClusters = []
    collapsedInds = set([])
    for ind, simInds in clusters.iteritems():
        clusSet = set([])
        clusSet.add(ind)
        exploreInds = simInds
        collapsedInds.add(ind)

        while len(exploreInds) > 0:
            for ind in exploreInds:
                exploreInds.remove(ind)
                if ind not in collapsedInds:
                    collapsedInds.add(ind)
                    clusSet.add(ind)
                    #explore cluster assoc with ind
                    exploreInds.append(clusters[ind])

        collapsedClusters.append(clusSet)
    return collapsedClusters



getSimBasedClusters()
