import multiprocessing
from multiprocessing import Pool
from multiprocessing import Manager
import sys
from scipy.sparse import lil_matrix
import numpy as np

class PageRankConsts:
    MAX_ITER = 50
    #probability to jump to neighbor, 1-alpha to go back to start
    ALPHA = 0.5 
    #number of top nodes to find
    NUM_TOP_NODES = 50

    
""" compute personalized page rank at a particular node,
return nodes with top page rank """
def pageRank((user, adjList)):
    print 'computing pr: ', str(user)
    #map to hold prob of jumping to node till curr Iteration
    probs = {}
    #start at user
    probs[user] = 1.0
    #map to store calculated pageRank probs
    pageRankProbs = pageRankHelper(user, adjList, probs,\
                                       PageRankConsts.MAX_ITER)
    probUsers = [ (prob, node)  for node, prob in pageRankProbs.iteritems()\
                      if node != user]
    probUsers.sort(reverse=True)
    return (user , [node for (prob, node) in \
                        probUsers[:PageRankConsts.NUM_TOP_NODES]])


"""
    start -> node to calculate personalized page rank around
    probs -> prob of staying at node at start of current iteration
    numIter -> number of iterations remaining
"""
def pageRankHelper(start, adjList, probs, numIter):
    if numIter <= 0:
        return probs
    else:
        #map to hold updated probabilities after this iteration
        probsPropagated = {}

        #with 1-alpha go back to start
        probsPropagated[start] = 1 - PageRankConsts.ALPHA

        #propagate previous probabilities for each node in it
        for user, prob in probs.iteritems():
            #move to neighbor with probability alpha
            #distribute each node's probability equally to each neigbor
            if len(adjList[user]) > 0:
                prob2Propagate = PageRankConsts.ALPHA * prob/(len(adjList[user]))
                for neighbor in adjList[user]:
                    if neighbor not in probsPropagated:
                        probsPropagated[neighbor] = 0
                    probsPropagated[neighbor] += prob2Propagate
        #delete previous dictionary not needed
        del probs
        #recursively propagate page rank prob
        return pageRankHelper(start, adjList, probsPropagated, numIter - 1)
            

def findTopPRUsers(usersList, userAdjList, numProcs = 0):

    userSimUsersDic = {}
    workersArgs = []

    #for debugging just use first 16 users
    #usersList = usersList[:16]
    
    jobCount = len(usersList)

    print 'number of jobs : ', jobCount
    
    if numProcs == 0:    
        #get number of processors from env
        numProcs = multiprocessing.cpu_count()

    #get shared memory manager to share adjacency list
    manager = Manager()
    sharedAdjList = manager.dict()
    sharedAdjList.update(userAdjList)
    
    for user in usersList:
        workersArgs.append((user, sharedAdjList))
    
    #initialize pool with number of possible jobs
    pool = Pool(processes=min(numProcs, jobCount))

    userNSimUsers = pool.map(pageRank, workersArgs)

    pool.close()
    pool.join()

    print 'number of jobs completed: ', len(userNSimUsers)
    
    for (user, simUsers) in userNSimUsers:
        userSimUsersDic[user] = simUsers
    
    return userSimUsersDic
        

def createAdjMatrix(userAdjList):
    userIdMap = {}
    userCount = 0

    numUsers = len(userAdjList)
    
    #adjmatrix make it sparse
    adjMatrix = lil_matrix((numUsers, numUsers))
    
    for user, friends in userAdjList.iteritems():
        if user not in userIdMap:
            userIdMap[user] = userCount
            userCount += 1
        if len(friends) == 0:
            continue
        numFriends = len(friends)
        transProbToEachFriend = 1.0/numFriends
        for friend in friends:
            if friend not in userIdMap:
                userIdMap[friend] = userCount
                userCount += 1
            adjMatrix[userIdMap[user], userIdMap[friend]] = transProbToEachFriend
    print 'generated adj matrix'
    adjMatrix = adjMatrix.tocsr()
    print 'converted to csr format'
    return (adjMatrix, userIdMap)
   

 
def computePRank(adjMatrix, userIdMap, usersList):

    revUserIdMap = {}
    
    for key, val in userIdMap.iteritems():
        revUserIdMap[val] = key
    
    #to store top similar users
    topSimUserDict = {}
    
    #get the walking and restart probabilities
    walkProb = PageRankConsts.ALPHA
    teleportProb = 1 - walkProb
    
    #compute most similar user for each one in usersList
    for user in usersList:
        # for each user perform the random walking with restart
        # v' = beta*M*v + (1-beta)v
        # where beta is walk prob., M is the transition matrix, v is start vector
        # S.T. v = eN where N is the user no. w.r.t which walk is started
        rows, cols = adjMatrix.shape #rows= cols here
        mappedUserRow = userIdMap[user]
        #for this user do the random walk
        v = lil_matrix((rows, 1))
        v[mappedUserRow, 0] = 1
        v = v.tocsr()
        
        #multiply transMat by beta
        transMatUser = walkProb * adjMatrix
        
        #add restart prob to corresponding row in transtion matrix i.e (1-beta)
        #transMatUser[mappedUserRow, :] = transMatUser[mappedUserRow, :] + teleportProb
        for j in range(cols):
            transMatUser[mappedUserRow, j] += teleportProb
        

        #perform rand walk iteration v' = transMat*v
        for itr in range(PageRankConsts.MAX_ITER):
            newV = transMatUser * v
            diff = newV - v
            diffNorm = np.linalg.norm(diff.data, ord=2)
            if diffNorm < 0.01:
                print 'converged in iteratons: ', itr
                break
            v = newV

        numTopNodes = PageRankConsts.NUM_TOP_NODES
        if PageRankConsts.NUM_TOP_NODES > rows:
            numTopNodes = rows
        
        topInd = np.argsort(v.toarray(), 0)[-numTopNodes:]

        #top similar for current user
        topSimilar = []
        for i in range(topInd.size-2,-1,-1):
            if v[topInd[i][0], 0] != 0:
                topSimilar.append(revUserIdMap[topInd[i][0]])
        
        #add top users to similar users list
        topSimUserDict[revUserIdMap[mappedUserRow]] = topSimilar
    print 'computed similar users'
    return topSimUserDict
        
        

        
    
    
