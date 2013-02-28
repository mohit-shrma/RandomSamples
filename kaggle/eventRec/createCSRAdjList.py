import sys
import randomWalker as rw
import csv
import array

def getAdjList(userFriendsFileName, testUsers, trainUsers):

    #contain mapping for user to friends
    userAdjList = {}

    #create adjacency list for user friends 
    with open(userFriendsFileName, 'rb') as userFriendsFile:
        friendsReader = csv.reader(userFriendsFile)
        header = friendsReader.next()
        for row in friendsReader:
            user = int(row[0])
            userFriends = row[1].split()
            userFriendsIds = set([])
            for friend in userFriends:
                friend = int(friend)
                if friend not in userAdjList:
                    userAdjList[friend] = set([])
                userAdjList[friend].add(user)
                userFriendsIds.add(friend)
            userAdjList[user] = userFriendsIds

    #add test user data to adj, for cases when they dont have friends
    for user in testUsers:
        if user not in userAdjList:
            userAdjList[user] = set([])
                
    #add train user data to adj, for cases when they dont have friends
    for user in trainUsers:
        if user not in userAdjList:
            userAdjList[user] = set([])
                
    return userAdjList



def writeAdjList(adjFileName, adjList):
    with open(adjFileName, 'w') as adjFile:
        adjWriter = csv.writer(adjFile)
        for user, friends in adjList.iteritems():
            adjWriter.writerow([str(user), ' '.join(map(str, friends))])



def writeCSRAdj(userAdjList, csrAdjFileName, idMapFileName):
    userIdMap = {}
    revIdUserMap = {}
    userCount = 0

    with open(csrAdjFileName, 'w') as csrAdjFile:
        with open(idMapFileName, 'w') as idMapFile:

            for user, friends in userAdjList.iteritems():

                if len(friends) == 0:
                    continue

                if user not in userIdMap:
                    userIdMap[user] = userCount
                    userCount += 1

                for friend in friends:
                    if friend not in userIdMap and friend in userAdjList\
                            and len(userAdjList[friend]) > 0:
                        userIdMap[friend] = userCount
                        userCount += 1

            print 'User count: ' + str(userCount)
                        
            for origUser, newId in userIdMap.iteritems():
                revIdUserMap[newId] = origUser

            for newId in range(userCount):

                friends = userAdjList[revIdUserMap[newId]];
                numFriends = len(friends)

                if numFriends == 0:
                    print newId, 'error 0 friends'
                    break
                
                friendWithNbors = 0
                for friend in friends:
                    if len(userAdjList[friend]) > 0 :
                        csrAdjFile.write(str(userIdMap[friend]) + " 1 ")
                csrAdjFile.write('\n')

                #also write down the user corresponding to newId
                idMapFile.write(str(newId) + ' ' + str(revIdUserMap[newId]) + '\n')    

            print 'User with friends: ' + str(len(userIdMap))
            



def main():

    if len(sys.argv) > 4:
        
        trainFileName = sys.argv[1]
        testFileName = sys.argv[2]
        userFriendsFileName = sys.argv[3]
        csrAdjMatFileName = sys.argv[4];
        csrIDMapFileName = sys.argv[5];
        adjFileName = sys.argv[6]
        
        trainUsersIds = rw.getUsersList(trainFileName)
        print 'unique train users: ', len(trainUsersIds)

        #testUsersIds = [2399025474, 968336394, 1251857185]
        testUsersIds = rw.getUsersList(testFileName)
        print 'unique test users: ', len(testUsersIds)
        
        userAdjList = getAdjList(userFriendsFileName, testUsersIds, trainUsersIds)
	print 'size of adjacency list: ', len(userAdjList)

        #write out the learned adjacency list
        writeAdjList(adjFileName, userAdjList)
        
        writeCSRAdj(userAdjList, csrAdjMatFileName, csrIDMapFileName)
        
    else:
        print 'err: invalid args'
        


if __name__=="__main__":
    main()
