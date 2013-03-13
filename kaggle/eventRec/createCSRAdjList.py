import sys
import csv



def getUsersList(fileName):
    users = set([])
    with open(fileName, 'r') as usersFile:
        header = usersFile.readline()
        for line in usersFile:
            line = line.strip()
            cols = line.split(',')
            user = cols[0]
            if len(user) > 0 :
                user = int(user)
                if user not in users:
                    users.add(user)
    return users




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



""" only keep the adjacency of these user's network """
def trimAdjList(users, adjList):
    #set of all connected users
    connUsers = set([])
    #initialize unexplored q with the list of users
    unExpQ = users
    while len(unExpQ) > 0:
        user = unExpQ.pop()
        connUsers.add(user)
        for friend in adjList[user]:
            if friend not in connUsers:
                unExpQ.insert(0, friend)
    trimAdjList = {}
    for user in connUsers:
        trimAdjList[user] = adjList[user]

    return trimAdjList
        

def writeAdjList(adjFileName, adjList):
    with open(adjFileName, 'w') as adjFile:
        adjWriter = csv.writer(adjFile)
        for user, friends in adjList.iteritems():
            adjWriter.writerow([str(user), ' '.join(map(str, friends))])



def convAdjToGraphlabAdj(userIdMap, gLabAdjFileName, userFriendsFileName):
        with open(userFriendsFileName, 'rb') as userFrnFile:
            with open(gLabAdjFileName, 'w') as gLabAdjFile:
                userFReader = csv.reader(userFrnFile)
                #skip header
                userFReader.next()
                for row in userFReader:
                    user = int(row[0])
                    userFriends = map(int, row[1].split())
                    if len(userFriends) > 0:
                        gLabAdjFile.write(str(userIdMap[user]))
                        gLabAdjFile.write("\t" + str(len(userFriends)))
                        for friend in userFriends:
                            gLabAdjFile.write("\t" + str(userIdMap[friend]))
                        gLabAdjFile.write('\n')
                

def convAdjToCSR(userFriendsFileName, csrAdjFileName, idMapFileName):
    userIdMap = {}
    revIdUserMap = {}
    userCount = 0
    with open(userFriendsFileName, 'rb') as userFrnFile:
        with open(csrAdjFileName, 'w') as csrAdjFile:
            with open(idMapFileName, 'w') as idMapFile:
                userFReader = csv.reader(userFrnFile)
                #skip header
                userFReader.next()
                for row in userFReader:
                    user = int(row[0])
                    if user not in userIdMap:
                        userIdMap[user] = userCount
                        idMapFile.write(str(user) + "\t" + str(userCount) + '\n')
                        userCount += 1
                    
                    userFriends = map(int, row[1].split())
                    if len(userFriends) == 0:
                        continue
                        
                    #write the sparse current row, leading with username
                    csrAdjFile.write(str(userIdMap[user]))

                    userFriends = map(int, row[1].split())
                    for friend in userFriends:
                        if friend not in userIdMap:
                            userIdMap[friend] = userCount
                            idMapFile.write(str(friend) + "\t" + str(userCount) + '\n')
                            userCount += 1
                            
                        #write friends in current row
                        csrAdjFile.write(" " + str(userIdMap[friend]))

                    csrAdjFile.write('\n')
    return userIdMap                
                    


def saveFullAdjList(adjList, csrAdjFileName, idMapFileName):
    userIdMap = {}
    revIdUserMap = {}
    userCount = 0
    with open(csrAdjFileName, 'w') as csrAdjFile:
        with open(idMapFileName, 'w') as idMapFile:
            for user, userFriends in adjList.iteritems():
                if user not in userIdMap:
                    userIdMap[user] = userCount
                    idMapFile.write(str(user) + "\t" + str(userCount) + '\n')
                    userCount += 1
                    
                #write the sparse current row, leading with username
                csrAdjFile.write(str(userIdMap[user]))

                for friend in userFriends:
                    if friend not in userIdMap:
                        userIdMap[friend] = userCount
                        idMapFile.write(str(friend) + "\t" + str(userCount) + '\n')
                        userCount += 1
                            
                    #write friends in current row
                    csrAdjFile.write(" " + str(userIdMap[friend]))

                csrAdjFile.write('\n')
    return userIdMap                


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

        userFriendsFileName = sys.argv[1]
        testUsersFileName = sys.argv[2];
        trainUsersFileName = sys.argv[3];
        adjFileName = sys.argv[4];
        idMapFileName = sys.argv[5];

        #userIdMap = convAdjToCSR(userFriendsFileName, csrAdjMatFileName, csrIdMapFileName)
        #convAdjToGraphlabAdj(userIdMap, gLabAdjFileName, userFriendsFileName)

        adjList = getAdjList(userFriendsFileName, \
                                 getUsersList(trainUsersFileName),\
                                 getUsersList(testUsersFileName))
        print 'prepared adjacency... users: ', len(adjList)
        saveFullAdjList(adjList, adjFileName, idMapFileName)
    else:
        print 'err: invalid args'
        


if __name__=="__main__":
    main()
