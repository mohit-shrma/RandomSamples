import csv
import sys
import array
from dateutil.parser import parse
import time
import os
""" prepare data for random forest to train and test """


    
class EVENTS_CONSTS:
    EVENT_COL = 0
    USER_COL = 1
    START_TIME = 2
    CITY_COL = 3
    STATE_COL = 4
    ZIP_COL = 5
    COU_COL = 6
    LAT_COL = 7
    LONG_COL = 8


class TRAIN_CONSTS:

    USER_COL = 0
    EVENT_COL = 1
    INVITED_COL = 2
    TIMESTAMP_COL = 3
    INTERESTED_COL = 4
    NOT_INTERESTED_COL = 5


    
class USERS_CONSTS:
    USER_COL = 0
    LOCALE_COL = 1
    BIRTH_YEAR_COL = 2
    GENDER_COL = 3
    JOINED_AT_COL = 4
    LOCATION_COL = 5
    TIMEZONE_COL = 6


class EVENT_ATTN:
    EVENT_COL = 0
    YES_COL= 1
    MAYBE_COL = 2
    INVITED_COL = 3
    NO_COL = 4



#return event attendees dictionary, {event: [[Yes], [Maybe], [Invited], [No]]}
def getEventAttendees(eventAtnFileName):
    eventAttendeesDic = {}
    with open(eventAtnFileName, 'r') as eventAtnFile:
        header = eventAtnFile.readline()
        for line in eventAtnFile:
            line = line.strip()
            cols = line.split(',')
            eventId = int(cols[0])
            eventAttendees = []
            for i in range(1, len(cols)):
                attendees = cols[i].split()
                temp = []
                for attendee in attendees:
                    if len(attendee) > 0:
                        temp.append(int(attendee))
                eventAttendees.append(temp)
            eventAttendeesDic[eventId] = eventAttendees
    return eventAttendeesDic
    

def getModdedName(name):
    absPath = os.path.abspath(name)
    dirPath = os.path.dirname(absPath)
    fileName = os.path.basename(absPath)
    return os.path.join(dirPath, 'mod_' + fileName)


def writeModdedFiles(firstColElemSet, fileName):
    with open(fileName, 'rb') as origFile:
        with open(getModdedName(fileName), 'wb') as modFile:
            origReader = csv.reader(origFile)
            modWriter = csv.writer(modFile)
            #write header
            header = origReader.next()
            modWriter.writerow(header)
            for row in origReader:
                if int(row[0]) in firstColElemSet:
                    modWriter.writerow(row)


def getFirstColSet(fileName):
    firstColSet = set([])
    with open(fileName, 'rb') as f:
        reader = csv.reader(f)
        #skip header
        header = reader.next()
        for row in reader:
            firstColSet.add(int(row[0]))
    return firstColSet


def getUserCharacteristics(user, usersFileName):
    with open(usersFileName, 'r') as usersFile:
        header = usersFile.readline()
        for line in usersFile:
            line = line.strip()
            cols = line.split(',')
            #if users found compute mean characteristics or do clustering on parameters
            # by maping parameters to number or 6-d coords
            userF = int(cols[USERS_CONSTS.USER_COL])
            if userF ==  user:
                userLocale = (cols[USERS_CONSTS.LOCALE_COL])
                birthYear = 1970
                try:
                    if len(cols[USERS_CONSTS.BIRTH_YEAR_COL]) > 0:
                        birthYear = int(cols[USERS_CONSTS.BIRTH_YEAR_COL])
                except ValueError:
                    print 'val error:', cols
                    birthYear = 1970 #TODO: default birthyear
                    
                gender = cols[USERS_CONSTS.GENDER_COL]
                joinedAt = time.mktime(parse(cols[USERS_CONSTS.JOINED_AT_COL]).timetuple())
                location = cols[USERS_CONSTS.LOCATION_COL]

                if len(cols[USERS_CONSTS.TIMEZONE_COL]) > 0:
                    timezone = int(cols[USERS_CONSTS.TIMEZONE_COL])
                else:
                    timezone = 0

                return (birthYear, gender, joinedAt, location, timezone,\
                            userLocale) 
        return ()


def getEventDetails(eventsFileName, eventId):
    with open(eventsFileName, 'rb') as eventsFile:
        eventReader = csv.reader(eventsFile)
        #skip header
        eventReader.next()
        for row in eventReader:
            if (int(row[EVENTS_CONSTS.EVENT_COL])) == eventId:
                #found event
                eventCreator = int(row[EVENTS_CONSTS.USER_COL])
                eventLoc = row[EVENTS_CONSTS.CITY_COL] + ' '\
                    + row[EVENTS_CONSTS.STATE_COL] + ' '\
                    + row[EVENTS_CONSTS.COU_COL]
                eventLat = row[EVENTS_CONSTS.LAT_COL]
                eventLong = row[EVENTS_CONSTS.LONG_COL]
                eventStartTime = time.mktime(parse(row[EVENTS_CONSTS.START_TIME]).timetuple())
                return (eventCreator, eventLoc, eventLat, eventLong, eventStartTime)


def getEventAtnCount(simUsersSet, eventAttendees):

    #count intersection with yes set
    yesCount = len(simUsersSet & set(eventAttendees[EVENT_ATTN.YES_COL - 1]))

    #count intersection with no set
    noCount = len(simUsersSet & set(eventAttendees[EVENT_ATTN.NO_COL - 1]))

    #count intersection with maybe set
    maybeCount = len(simUsersSet & set(eventAttendees[EVENT_ATTN.MAYBE_COL - 1]))

    #count intersection with invited set
    invitedCount = len(simUsersSet & \
                         set(eventAttendees[EVENT_ATTN.INVITED_COL - 1]))

    return (yesCount, maybeCount, invitedCount, noCount)

    
def getMeanCharEvent(eventAttendees, usersFileName):
    with open(usersFileName, 'r') as usersFile:
        header = usersFile.readline()
        genderCount = {'male': 0, 'female':0}
        localeCount = {}
        birthYearAvg = 0
        timezoneAvg = 0
        timeZoneCount = {}
        locationCount = {}
        userCount = 0
        for line in usersFile:
            line = line.strip()
            cols = line.split(',')
            #if users found compute mean characteristics or do clustering on parameters
            # by maping parameters to number or 6-d coords
            user = int(cols[USERS_CONSTS.USER_COL])
            if user in eventAttendees:
                userCount += 1
                userLocale = (cols[USERS_CONSTS.LOCALE_COL])

                if len(cols[USERS_CONSTS.BIRTH_YEAR_COL]) > 0:
                    try:
                        birthYear = int(cols[USERS_CONSTS.BIRTH_YEAR_COL].strip())
                    except ValueError:
                        print 'val error:', cols
                        birthYear = 1970
                else:
                    birthYear = 1970 #TODO: may be not safe to assume as default

                gender = cols[USERS_CONSTS.GENDER_COL]
                joinedAt = cols[USERS_CONSTS.JOINED_AT_COL]
                location = cols[USERS_CONSTS.LOCATION_COL]

                if len(cols[USERS_CONSTS.TIMEZONE_COL]) > 0:
                    timezone = int(cols[USERS_CONSTS.TIMEZONE_COL])
                else:
                    timezone = 0

                if timezone in timeZoneCount:
                    timeZoneCount[timezone] += 1
                else:
                    timeZoneCount[timezone] = 1
                    
                if len(userLocale) > 0:
                    if userLocale in localeCount:
                        localeCount[userLocale] += 1
                    else:
                        localeCount[userLocale] = 1

                birthYearAvg += birthYear

                if len(gender) > 0:
                    genderCount[gender] += 1

                timezoneAvg += timezone
                #print timezone
                if len(location) > 0:
                    if location in locationCount:
                        locationCount[location] += 1
                    else:
                        locationCount[location] = 1
        if userCount == 0:
            return (1970,0,'','','')
        birthYearAvg = birthYearAvg/userCount
        timezoneAvg = timezoneAvg/userCount
        #print 'user count: ', userCount
        if len(genderCount) > 0:
            majGender = getTopItemInDic(genderCount)
        else:
            majGender = ''
        if len(locationCount) > 0:
            majLocation = getTopItemInDic(locationCount)
        else:
            majLocation = ''
        if len(timeZoneCount) > 0:
            majTimeZone = getTopItemInDic(timeZoneCount)
        else:
            majTimeZone = 0
            
        majLocale = ''
        if len(localeCount) > 0:
            majLocale = getTopItemInDic(localeCount)
            
        return (birthYearAvg, majTimeZone, majGender, majLocation, majLocale)


def getTopItemInDic(countDic, topCount = 1):
    if len(countDic) == 0:
        return ''
    tuples = []
    for key, count in countDic.iteritems():
        tuples.append((count, key))
    tuples.sort(reverse=True)
    tuples = tuples[0:topCount]
    #print countDic, tuples
    topItems = [key for (count, key) in tuples]
    if topCount == 1:
        return topItems[0]
    else:
        return topItems


def subStrSimilarity(location, majLocation):
    score = 0
    locationTok = location.split()
    majLocationTok = majLocation.split()
    for loc in locationTok:
        if loc in majLocationTok:
            score += 1
    return score


def prepDataFeature(trainFileName, eventAttendeesDic, simUsersDic,\
                      usersFileName, adjList, eventsFileName, featureOpFileName, isTest = False):
    
    
    with open(trainFileName, 'rb') as trainFile:
        with open(featureOpFileName, 'w') as featureOpFile:
            trainReader = csv.reader(trainFile)
            featureWriter = csv.writer(featureOpFile)
            #skip header
            trainReader.next()
            prevUserId = ''
            (birthYear, gender, joinedAt, location, timezone, locale) = \
                ('','','','','', '')
            eventFeatureDic = {}

            #write header for feature output file
            headersTitle = ['user', 'event', 'invited', 'ageDiff',\
                                   'tzDiff', 'majGender', 'majLocale', 'majLocScore',\
                                   'goingFr', 'notGoingFr', 'isOwnerFr',\
                                   'eventLocScore', 'yesCount', 'maybeCount',\
                                   'invitedCount', 'noCount']
            if not isTest:
                headersTitle.append('target')

            #write headers
            featureWriter.writerow(headersTitle)

            for row in trainReader:
                features = []
                userId = int(row[TRAIN_CONSTS.USER_COL].strip())
                features.append(userId)
                eventId = int(row[TRAIN_CONSTS.EVENT_COL].strip())
                features.append(eventId)
                invited = int(row[TRAIN_CONSTS.INVITED_COL].strip())
                features.append(invited)


                #get user features
                #(birthYear, gender, joinedAt, location, timezone) 
                if userId != prevUserId:
                    (birthYear, gender, joinedAt, location, timezone, locale) = \
                        getUserCharacteristics(userId, usersFileName)
                    prevUserId = userId

                #get majority
                if eventId not in eventFeatureDic:
                    (birthYearAvg, timezoneAvg, majGender, majLocation, majLocale) = \
                    getMeanCharEvent((eventAttendeesDic[eventId])[EVENT_ATTN.YES_COL - 1],\
                                         usersFileName)
                    eventFeatureDic[eventId] = (birthYearAvg, timezoneAvg,\
                                                    majGender, majLocation,\
                                                    majLocale)
                (birthYearAvg, timezoneAvg, majGender, majLocation, majLocale) =\
                    eventFeatureDic[eventId]

                #get majority params
                ageDiff = birthYearAvg - birthYear
                features.append(ageDiff)
                tzDiff = timezoneAvg - timezone
                features.append(tzDiff)

                sameMajGender = 0
                if gender == majGender:
                    sameMajGender = 1
                features.append(sameMajGender)

                sameMajLocale = 0
                if majLocale == locale:
                    sameMajLocale = 1
                features.append(sameMajLocale)

                #get substrings similarity
                userAtnLocScore = subStrSimilarity(location, majLocation)
                features.append(userAtnLocScore)

                #no. of friends going
                goingFriends = len(set(adjList[userId]) & \
                                set((eventAttendeesDic[eventId])[EVENT_ATTN.YES_COL - 1]))
                features.append(goingFriends)

                #no. of friends not going
                notGoingFriends = len(set(adjList[userId]) & \
                                set((eventAttendeesDic[eventId])[EVENT_ATTN.NO_COL - 1]))
                features.append(notGoingFriends)


                #get event specific features
                (eventCreator, eventLocString, eventLat, eventLng) = \
                    getEventDetails(eventsFileName, eventId)


                isOwnerUserFriend = 0
                if eventCreator in adjList[userId]\
                        or eventCreator in simUsersDic[userId]:
                    isOwnerUserFriend = 1
                features.append(isOwnerUserFriend)

                #score event location based on similarity with location
                eventLocationScore = subStrSimilarity(location, eventLocString)
                features.append(eventLocationScore)

                #get similar user specific features for the event
                (yesCount, maybeCount, invitedCount, noCount) = \
                    getEventAtnCount(set(simUsersDic[userId]),\
                                         eventAttendeesDic[eventId])
                features.extend([yesCount, maybeCount, invitedCount, noCount])

                if not isTest:
                    inter = int(row[TRAIN_CONSTS.INTERESTED_COL])
                    notInter = -1 * int(row[TRAIN_CONSTS.NOT_INTERESTED_COL])
                    #get the label +1/-1/0
                    target = inter + notInter
                    features.append(target)

                features = map(str, features)

                #write features
                featureWriter.writerow(features)

    
#get similar users from the file
#{user : [(simUser, prank)]}
def getSimUsersDic(simUserFileName):
    simUsersDic = {}
    with open(simUserFileName, 'r') as simUserFile:
        simUserReader = csv.reader(simUserFile, delimiter = '\t')
        for row in simUserReader:
            userId = int(row[0])
            friendPRanks = []
            for friendPRank in row[1:]:
                (friend, pRank) = friendPRank.split(':')
                friendPRanks.append((int(friend), float(pRank)))
            simUsersDic[userId] = friendPRanks
    return simUsersDic


#create adjacency list of users
def createAdjList(userFriendsFileName, testUsers, trainUsers):
    
    #contain mapping for user to friends
    userAdjList = {}

    #create adjacency list for user friends 
    with open(userFriendsFileName, 'r') as userFriendsFile:
        adjReader = csv.reader(userFriendsFile)
        #skip header
        header = adjReader.next()
        for row in adjReader:
            user = int(row[0])
            userFriends = map(int, row[1].split())
            for friend in userFriends:
                if friend not in userAdjList:
                    userAdjList[friend] = array.array('L', [])
            userAdjList[user] = array.array('L', userFriends)

    #add test user data to adj, for cases when they dont have friends
    for user in testUsers:
        if user not in userAdjList:
            userAdjList[user] = array.array('L', [])
                
    #add train user data to adj, for cases when they dont have friends
    for user in trainUsers:
        if user not in userAdjList:
            userAdjList[user] = array.array('L', [])
                
    return userAdjList


def main():
    if len(sys.argv) > 9:
        trainFileName = sys.argv[1]
        testFileName = sys.argv[2]
        eventAttFileName = sys.argv[3]
        eventsFileName = sys.argv[4]
        usersFileName = sys.argv[5]
        simUserFileName = sys.argv[6]
        userFriendsFileName  = sys.argv[7]
        trainFeatureOutFileName = sys.argv[8]
        testFeatureOutFileName = sys.argv[9]
        
        trainUsersSet = getFirstColSet(trainFileName)
        testUsersSet = getFirstColSet(testFileName)
        #eventsSet = getFirstColSet(eventAttFileName)
        #writeModdedFiles(eventsSet, eventsFileName)
        eventAttendeesDic = getEventAttendees(eventAttFileName)
        
        simUsersDic = getSimUsersDic(simUserFileName)
        print 'num sim users: ', len(simUsersDic)
        
        adjList = createAdjList(userFriendsFileName, testUsersSet, trainUsersSet)

        modEventFileName = getModdedName(eventsFileName)

        prepDataFeature(trainFileName, eventAttendeesDic, simUsersDic,\
                      usersFileName, adjList, modEventFileName,\
                            trainFeatureOutFileName, isTest = False)
        
        
        prepDataFeature(testFileName, eventAttendeesDic, simUsersDic,\
                            usersFileName, adjList, modEventFileName,\
                            testFeatureOutFileName, isTest = True)
        
    else:
        print 'err: insuff arguments'

                

if __name__=='__main__':
    main()
