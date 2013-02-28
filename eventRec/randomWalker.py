import sys
import os
import cPickle
import array
#import numpy as np
import math
import random
from multiprocessing import Pool
from multiprocessing import Manager
import multiprocessing, logging
from operator import itemgetter
#import personPageRank as ppr

class PageRankConsts:
    MAX_ITER = 4
    #probability to jump to neighbor, 1-alpha to go back to start
    ALPHA = 0.5 
    #number of top nodes to find
    NUM_TOP_NODES = 50


class TRAIN_CONSTS:

    USER_COL = 0
    EVENT_COL = 1
    INVITED_COL = 2
    TIMESTAMP_COL = 3
    INTERESTED_COL = 4
    NOT_INTERESTED_COL = 5

    
class RWALK_CONSTS:
    RWALK_PROB = 0.6
    MAX_ITER = 100
    TOP_NODE_NUM = 200
    MAX_DEG_SEP = 2



    
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
    probUsers = []
    for node, prob in pageRankProbs.iteritems():
        if node != user:
            probUsers.append((prob, node))

    probUsers.sort(reverse=True)
    probUsers = probUsers[:PageRankConsts.NUM_TOP_NODES]
    print probUsers[:3]
    
    return (user , [node for (prob, node) in  probUsers])


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

    jobCount = len(usersList)

    #for sebugging just work on 10 users
    #usersList = usersList[:10]
            
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
    pool = Pool(processes=min(numProcs, jobCount, 10))

    userNSimUsers = pool.map(pageRank, workersArgs)

    pool.close()
    pool.join()

    print 'number of jobs completed: ', len(userNSimUsers)
    
    for (user, simUsers) in userNSimUsers:
        userSimUsersDic[user] = simUsers
    
    return userSimUsersDic
        

    


    
#create user friend dict from test and train file
def createUserFriendDict(userIds, adjList):
    userFriendsDict = {}
    for userId in userIds:
        userFriendsDict[userId] = adjList[userId]
    return userFriendsDict



def getUsersList(fileName):
    userDict = {}
    with open(fileName, 'r') as usersFile:
        header = usersFile.readline()
        for line in usersFile:
            line = line.strip()
            cols = line.split(',')
            user = cols[TRAIN_CONSTS.USER_COL]
            if len(user) > 0 :
                user = int(user)
                if user not in userDict:
                    userDict[user] = 1
    return userDict.keys()



def getUserIds(usersList, userIdDict):
    userIds = []
    for user in usersList:
        userIds.append(userIdDict[user])
    return userIds


    
#create adjacency list of users
def createAdjList(userFriendsFileName, testUsers, trainUsers):
    
    #contain mapping for user to friends
    userAdjList = {}

    #create adjacency list for user friends 
    with open(userFriendsFileName, 'r') as userFriendsFile:
        header = userFriendsFile.readline()
        for line in userFriendsFile:
            line = line.strip()
            cols = line.split(',')
            if len(cols[0]) > 0:
                user = int(cols[0])
                userFriends = cols[1].split(' ')
                userFriendsIds = []
                for friend in userFriends:
                    if len(friend) > 0:
                        friend = int(friend)
                        if friend not in userAdjList:
                            userAdjList[friend] = []
                        userFriendsIds.append(friend)
                userAdjList[user] = array.array('L', userFriendsIds)

    #add test user data to adj, for cases when they dont have friends
    for user in testUsers:
        if user not in userAdjList:
            userAdjList[user] = array.array('L', [])
                
    #add train user data to adj, for cases when they dont have friends
    for user in trainUsers:
        if user not in userAdjList:
            userAdjList[user] = array.array('L', [])
                
    return userAdjList



#do random walk with restart on passed nodes
#w.r.t first user of component
def randWalkWRestart((user, adjList, sharedUsersList)):

    #set of shared users set, dont want to random walk to these
    sharedUsersSet = set(sharedUsersList)
    
    #top similar users dict
    topSimUserDict = {}

    #top similar users
    topSimUsers = []

    degreeSep = 0

    #save origin of walk
    origUser = user

    #iterate atleast twice the user friends
    
    maxIter = len(adjList[user])*2
    
    for i in range(2*maxIter):

        rWalkProb = random.random() #not working in itasca
        #rWalkProb = np.random.random_sample()

        if rWalkProb <= RWALK_CONSTS.RWALK_PROB:
            
            #do random walking on current user

            #get all user friends
            userFriends = adjList[user]
            numFriends = len(userFriends)

            if numFriends == 0:
                #current user dont have any friends jump to original node
                user = origUser
                degreeSep = 0
                continue
            
            if origUser in userFriends:
                #if origUser present in friends then update degree of sep
                degreeSep = 1
            else:
                #increment the degree of sep
                degreeSep += 1
            
            if degreeSep > RWALK_CONSTS.MAX_DEG_SEP:
                #if degree of separation is > max degree sep then go back
                user = origUser
                degreeSep = 0
                continue
                
            #select a friend uniformly at random
            #friendInd = np.random.randint(0, numFriends)
            friendInd = random.randint(0, numFriends-1)
            user = userFriends[friendInd]
            if user == origUser or user in sharedUsersSet:
                #found original user as current user or its in shared user set
                #jump back
                user = origUser
                degreeSep = 0
                continue
            
            if user in topSimUserDict:
                topSimUserDict[user] += 1
            else:
                topSimUserDict[user] = 1
        else:
            #go back to original user
            user = origUser
            degreeSep = 0
    
    #find the top RWALK_CONSTS.TOP_NODE_NUM similar friends
    friendCounts = []
    for user, count in topSimUserDict.iteritems():
        friendCounts.append((count, user))

    #sort by count reverse
    friendCounts.sort(reverse=True)
    #get top users only
    friendCounts = friendCounts[0:RWALK_CONSTS.TOP_NODE_NUM]
    topSimUsers = [friend for count, friend in friendCounts]

    return (origUser, topSimUsers)



def findTopSimilarUsers(usersList, userAdjList, numProcs = 0):

    userSimUsersDic = {}
    workersArgs = []
    jobCount = len(usersList)

    print 'number of jobs : ', jobCount
    
    if numProcs == 0:    
        #get number of processors from env
        numProcs = multiprocessing.cpu_count()

    #get shared memory manager to share adjacency list
    manager = Manager()
    sharedAdjList = manager.dict()
    sharedAdjList.update(userAdjList)
    sharedUsersList = manager.list()
    sharedUsersList.extend(usersList)
    
    for user in usersList:
        workersArgs.append((user, sharedAdjList, sharedUsersList))
    
    #initialize pool with number of possible jobs
    pool = Pool(processes=min(numProcs, jobCount))

    userNSimUsers = pool.map(randWalkWRestart, workersArgs)

    pool.close()
    pool.join()

    print 'number of jobs completed: ', len(userNSimUsers)
    
    for user, simUsers in userNSimUsers:
        userSimUsersDic[user] = simUsers
    
    return userSimUsersDic


def getUniqueSimUsers(userSimUsersDic):
    allSimUsers = []
    uniqueSimUsers = []
    userWithSimUsers = 0
    for user, simUsers in userSimUsersDic.iteritems():
        allSimUsers = allSimUsers + simUsers
        if len(simUsers) > 0:
            userWithSimUsers += 1
    uniqueSimUsers = list(set(allSimUsers))
    print 'users with nozero similar users: ', userWithSimUsers
    print 'net sim users: ', len(allSimUsers)
    print 'unique sim users: ', len(uniqueSimUsers)
    return uniqueSimUsers
    

def findCoverageOfUsers(userSimUsersDic, users2Check):

    coveredUserCount = 0
    
    for user, simUsers in userSimUsersDic.iteritems():
        for simUser in simUsers:
            if simUser in users2Check:
                coveredUserCount += 1
                break
    return coveredUserCount
    


def printSimUsers(simUserDict, prefix =''):
    with open(prefix + 'simUsers.txt', 'w') as simUsersTxt:
        for testUser, simUsers in simUserDict.iteritems():
            simUsersStr = [ str(simUser) for simUser in simUsers]
            simUsersTxt.write(str(testUser) + ',' + ' '.join(simUsersStr))
            simUsersTxt.write('\n')




def findOvrlapWTrainUser(trainUserDict, testUserDict, simUserDict):
    userSimFrndsInTrainDic = {}
    totalUserSimFInTrain = 0
    for testUser in testUserDict.keys():
        userSimFrndsInTrain = 0
        simUsers = simUserDict[testUser]
        #check if similar users in train
        for simUser in simUsers:
            if simUser in trainUserDict:
                userSimFrndsInTrain += 1
        userSimFrndsInTrainDic[testUser] = userSimFrndsInTrain
        totalUserSimFInTrain += userSimFrndsInTrain
    return (userSimFrndsInTrainDic, totalUserSimFInTrain)



def findOverlapWithTrain(users, trainUserDic):
    count = 0
    overlappedUsers = []
    for user in users:
        if user in trainUserDic:
            overlappedUsers.append(user)
            count += 1
    return overlappedUsers


def genDegreeDistStats(userDegOvrlapDic):
    degrees = []
    for user, (friendCount, overlapCount) in userDegOvrlapDic.iteritems():
        degrees.append(friendCount)
        
    """print 'average degree: ', np.average(degrees)
    print 'std dev degree: ', np.std(degrees)
    print 'max degree: ', np.max(degrees)
    print 'min degree: ', np.min(degrees)"""
    
    meanDeg = mean(degrees)
    
    print 'average degree: ', meanDeg
    print 'median degree: ', median(degrees)
    print 'std dev degree: ', std(degrees, meanDeg)
    print 'max degree: ', max(degrees)
    print 'min degree: ', min(degrees)


    
def variance(li, avg):
    return [ (float(elem) - avg)**2 for elem in li]


def median(li):
    return li[len(li)/2]


def mean(li):
    return float(sum(li))/len(li)


def std(li, avg):
    var = variance(li, avg)
    return math.sqrt(mean(var))

    
def findDegreeNFriendOvrlap(users, userAdjList, trainUserDic):
    userDegOvrlapDic = {}
    allUserFriendsSet = set([])
    userSet = set(users)
    trainUserSet = set(trainUserDic.keys())
    for user in users:
        userFriends = userAdjList[user]
        overlapCount = 0
        for friend in userFriends:
            allUserFriendsSet.add(friend)
            if friend in trainUserDic:
                overlapCount += 1
        userDegOvrlapDic[user] = (len(userFriends), overlapCount)

    print 'size of users set: ', len(userSet)
    print 'size of user friends set: ', len(allUserFriendsSet)
    print 'size of other type users set: ', len(trainUserSet)

    print 'users intersect friends: ',\
        len(userSet.intersection(allUserFriendsSet))
    print 'users intersect other type: ',\
        len(userSet.intersection(trainUserSet))
    print 'users friends intersect other type: ',\
        len(allUserFriendsSet.intersection(trainUserSet))
    print 'users intersect friends intersect other type: ',\
        len(userSet.intersection(allUserFriendsSet, trainUserSet))
    
    print 'size of friends excluding users: ',\
        len(allUserFriendsSet.difference(userSet))
    print 'size of friends excluding others: ',\
        len(allUserFriendsSet.difference(trainUserSet))
    print 'size of friends excluding users and others: ',\
        len(allUserFriendsSet.difference(userSet, trainUserSet))
    
    return userDegOvrlapDic



def findHigh5DegWithMostOvrLap(userDegOvrlapDic):
    userFriendOvrlap = []
    for user, (friendCount, overlapCount) in userDegOvrlapDic.iteritems():
        userFriendOvrlap.append((user, friendCount, overlapCount))
    #sort by overlap count then friend count
    userFriendOvrlap = sorted(userFriendOvrlap, key=itemgetter(2,1), reverse=True)

    top100UserFriendOvrlap = sorted(userFriendOvrlap, key=itemgetter(2), reverse=True)
    
    top100UserFriendOvrlap = top100UserFriendOvrlap[0:100]
    top100UserFriendOvrlap = sorted(userFriendOvrlap, key=itemgetter(1))
    tempTop5 = []
    i = 0
    for tup in top100UserFriendOvrlap:
        if tup[1] > 0 and tup[2] > 0:
            tempTop5.append(tup)
            i += 1
            if i >= 5:
                break
            
    print tempTop5

    netUniqueFriendsCount = 0
    for (user, friendCount, overlapCount) in userFriendOvrlap:
        netUniqueFriendsCount += friendCount
    print 'unique friend count: ', netUniqueFriendsCount
    return userFriendOvrlap[0:5]


def getAdjList(userFriendsFileName, testUsersIds, trainUsersIds):
    cPklFileName = userFriendsFileName + '.pkl'
    adjList = {}
    if os.path.isfile(cPklFileName):
        #got the pikl file load adj list from there
        pkl_file = open(cPklFileName, 'rb')
        adjList = cPickle.load(pkl_file)
        pkl_file.close()
    else:
        adjList = createAdjList(userFriendsFileName, testUsersIds,\
                                    trainUsersIds)
        #dump the content to pkl file
        pkl_file = open(cPklFileName, 'wb')
        cPickle.dump(adjList, pkl_file)
        pkl_file.close()
    return adjList



def main():
    
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(multiprocessing.SUBDEBUG)

    if len(sys.argv) >= 3:
        
        trainFileName = sys.argv[1]
        testFileName = sys.argv[2]
        userFriendsFileName = sys.argv[3]

        print 'cpuCount: ', multiprocessing.cpu_count()
        numProcs = 0
        if len(sys.argv) > 4:
            numProcs = int(sys.argv[4])

        trainUsersIds = getUsersList(trainFileName)
        print 'unique train users: ', len(trainUsersIds)

        #testUsersIds = [2399025474, 968336394, 1251857185]
        testUsersIds = getUsersList(testFileName)
        print 'unique test users: ', len(testUsersIds)
        
        userAdjList = getAdjList(userFriendsFileName, testUsersIds, trainUsersIds)
	print 'size of adjacency list: ', len(userAdjList)	

        #(adjMat, userIdMap) = ppr.createAdjMatrix(userAdjList)


        
        #trainUserDict = createUserFriendDict(trainUsersIds, userAdjList)
        #testUserDict = createUserFriendDict(testUsersIds, userAdjList)
        
        """
        #find similar users to train
        userSimUsersDic = findTopSimilarUsers(trainUsersIds, userAdjList,\
                                                  numProcs)
        #print top similar users for each test user
        printSimUsers(userSimUsersDic, 'train')


        #find similar users to test
        userSimUsersDic = findTopSimilarUsers(testUsersIds, userAdjList,\
                                                  numProcs)
        #print top similar users for each test user
        printSimUsers(userSimUsersDic, 'test')
        """

        #find similar users to train by page rank
        #userSimUsersDic = findTopPRUsers(trainUsersIds, userAdjList,\
        #                                          numProcs)
        #userSimUsersDic = ppr.computePRank(adjMat, userIdMap, trainUsersIds)
        #print top similar users for each test user
        #printSimUsers(userSimUsersDic, 'train')

        #find similar users to test
        userSimUsersDic = findTopPRUsers(testUsersIds, userAdjList,\
                                                  numProcs)
        #userSimUsersDic = ppr.computePRank(adjMat, userIdMap, testUsersIds)
        #print top similar users for each test user
        printSimUsers(userSimUsersDic, 'test')


        #find similar users to test present in train
        #(userSimFrndsInTrainDic, totalUserSimFInTrain) = findOvrlapWTrainUser(\
        #    trainUserDict, testUserDict, userSimUsersDic)


        """
        userSimUsersDic = findTopSimilarUsers(trainUsersIds, userAdjList,\
                                                  numProcs)

        

        #find similar users to train present in test
        (userSimFrndsInTestDic, totalUserSimFInTest) = findOvrlapWTrainUser(\
            testUserDict, trainUserDict, userSimUsersDic)
        
        print 'total similar users in test: ', totalUserSimFInTest
        
        uniqueSimUsers = getUniqueSimUsers(userSimUsersDic)
        print 'count unique sim users: ', len(uniqueSimUsers)

        uniqSimUserInTest = findOverlapWithTrain(uniqueSimUsers, testUserDict)

        print 'unique similar users in test: ', len(uniqSimUserInTest)

        print 'covered users in train by similar users found in test: ', findCoverageOfUsers(userSimUsersDic, uniqSimUserInTest)

        """
        
        
        
        #print 'testUsers: ', testUsersIds
        #print 'trainUsers: ', trainUsersIds
        #print 'adjList: ', userAdjList
        #print 'userSimUsersDic: ', userSimUsersDic
        #print 'userSimFrndsInTrainDic: ', userSimFrndsInTrainDic        
        """print 'total similar users in train: ', totalUserSimFInTrain
        
        uniqueSimUsers = getUniqueSimUsers(userSimUsersDic)
        print 'count unique sim users: ', len(uniqueSimUsers)

        uniqSimUserInTrain = findOverlapWithTrain(uniqueSimUsers, trainUserDict)

        print 'unique similar users in train: ', len(uniqSimUserInTrain)

        print 'covered users in test by similar users found in train: ', findCoverageOfUsers(userSimUsersDic, uniqSimUserInTrain)
        
        print 'For Test: '
        userDegOvrlapDic = findDegreeNFriendOvrlap(testUsersIds, userAdjList, trainUserDict)
        genDegreeDistStats(userDegOvrlapDic)
        hi5DegOvrLap = findHigh5DegWithMostOvrLap(userDegOvrlapDic)
        print hi5DegOvrLap

        print 'For Train: '
        userDegOvrlapDic = findDegreeNFriendOvrlap(trainUsersIds, userAdjList, testUserDict)
        genDegreeDistStats(userDegOvrlapDic)
        hi5DegOvrLap = findHigh5DegWithMostOvrLap(userDegOvrlapDic)
        print hi5DegOvrLap
        """
        
    else:
        print 'err: files missing'



        
if __name__ == '__main__':
    main()
        
