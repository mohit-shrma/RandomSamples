import sys 
import csv
import time
from dateutil.parser import parse
from prepareClassifyData import *
from time import gmtime, strftime


def getTimeDeltas(eventStart, userJoined, userShown):
    deltaStartJoin = eventStart - userJoined
    deltaStartShown = eventStart - userShown
    deltaShownJoin = userShown - userJoined
    return (deltaStartJoin, deltaStartShown, deltaShownJoin)



def getEvents(eventFileName):
    events = {}
    with open(eventFileName, 'r') as eventFile:
        eventReader = csv.reader(eventFile)
        #skip header
        eventReader.next()
        for row in eventReader:
            events[int(row[0])] = row
    return events


def getEventCount(fileName):
    #contains event count
    #{user: count}
    eventCount = {}
    with open(fileName, 'r') as file:
        fReader = csv.reader(file)
        #skip header
        fReader.next()
        for row in fReader:
            user = int(row[TRAIN_CONSTS.USER_COL])
            if user not in eventCount:
                eventCount[user] = 0
            eventCount[user] += 1
    return eventCount


def getEventPopularity(eventId, eventAttendeesDic):
    yesCount = len( (eventAttendeesDic[eventId])[EVENT_ATTN.YES_COL - 1] )
    noCount = len((eventAttendeesDic[eventId])[EVENT_ATTN.NO_COL - 1])
    maybeCount = len((eventAttendeesDic[eventId])[EVENT_ATTN.MAYBE_COL - 1])
    invCount = len((eventAttendeesDic[eventId])[EVENT_ATTN.INVITED_COL - 1])
    return (yesCount, noCount, maybeCount, invCount)



def getEventDetailsFromDic(eventsDic, eventId):
    row = eventsDic[eventId]
    eventCreator = int(row[EVENTS_CONSTS.USER_COL])
    eventLoc = row[EVENTS_CONSTS.CITY_COL] + ' '\
        + row[EVENTS_CONSTS.STATE_COL] + ' '\
        + row[EVENTS_CONSTS.COU_COL]
    eventLat = row[EVENTS_CONSTS.LAT_COL]
    eventLong = row[EVENTS_CONSTS.LONG_COL]
    eventStartTime = time.mktime(parse(row[EVENTS_CONSTS.START_TIME]).timetuple())
    return (eventCreator, eventLoc, eventLat, eventLong, eventStartTime)




def getExtraFeatures(fileName, eventAttendeesDic, \
                         usersFileName, featureOpFileName, eventsDic):
    
    print 'getting events count...', strftime("%Y-%m-%d %H:%M:%S", gmtime())
    eventCount = getEventCount(fileName)

    with open(fileName, 'rb') as trainFile,\
            open(featureOpFileName, 'w') as featureOpFile:
        trainReader = csv.reader(trainFile)
        featureWriter = csv.writer(featureOpFile)
        #skip header
        trainReader.next()
        prevUserId = ''
        (birthYear, gender, joinedAt, location, timezone, locale) = \
            ('','','','','', '')
        eventFeatureDic = {}

        #write header for feature output file
        headersTitle = ['user', 'event', 'deltaStartJoin', 'deltaStartShown',\
                            'deltaShownJoin', 'eventCount', 'popYes', 'popNo',\
                            'popMaybe', 'popInv']
        
        #write headers
        featureWriter.writerow(headersTitle)
        
        print 'reading train file', strftime("%Y-%m-%d %H:%M:%S", gmtime())

        count = 0

        for row in trainReader:
            features = []
            userId = int(row[TRAIN_CONSTS.USER_COL].strip())
            features.append(userId)
            eventId = int(row[TRAIN_CONSTS.EVENT_COL].strip())
            features.append(eventId)
            userShownTime = time.mktime(parse(\
                               row[TRAIN_CONSTS.TIMESTAMP_COL]).timetuple())

            #get user features
            #(birthYear, gender, joinedAt, location, timezone) 
            if userId != prevUserId:
                (birthYear, gender, joinedAt, location, timezone, locale) = \
                    getUserCharacteristics(userId, usersFileName)
                prevUserId = userId

            (eventCreator, eventLoc, eventLat, eventLong, eventStartTime) = \
                getEventDetailsFromDic(eventsDic, eventId)

            #get event deltas
            (deltaStartJoin, deltaStartShown, deltaShownJoin) = getTimeDeltas(\
                                              eventStartTime, joinedAt,\
                                                  userShownTime)
            features.extend([deltaStartJoin, deltaStartShown, deltaShownJoin])
            
            #get number of events by user in current file
            userEvCount = eventCount[userId]
            features.append(userEvCount)
            
            #get event popularity
            (yesCount, noCount, maybeCount, invCount) = \
                getEventPopularity(eventId, eventAttendeesDic)
            features.extend([yesCount, noCount, maybeCount, invCount])
            
            features = map(str, features)
            
            #write features
            featureWriter.writerow(features)

            if (count%100 == 0):
                print '100 done...', strftime("%Y-%m-%d %H:%M:%S", gmtime())


def extraFeatureWorker((fileName, featureOutFileName, usersFileName, eventAttendeesDic, eventsDic)):
    getExtraFeatures(fileName, eventAttendeesDic, \
                         usersFileName, featureOutFileName, eventsDic)



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
        
        #trainUsersSet = getFirstColSet(trainFileName)
        #testUsersSet = getFirstColSet(testFileName)
        #eventsSet = getFirstColSet(eventAttFileName)
        #writeModdedFiles(eventsSet, eventsFileName)
        
        print 'get event attendees dic...', strftime("%Y-%m-%d %H:%M:%S", gmtime())
        eventAttendeesDic = getEventAttendees(eventAttFileName)

        #simUsersDic = getSimUsersDic(simUserFileName)
        #adjList = createAdjList(userFriendsFileName, testUsersSet, trainUsersSet)

        modEventFileName = getModdedName(eventsFileName)
        
        print 'reading events file...', strftime("%Y-%m-%d %H:%M:%S", gmtime())
        eventsDic = getEvents(modEventFileName)

        
        extraFeatureWorker((trainFileName, trainFeatureOutFileName,\
                                usersFileName, eventAttendeesDic,\
                                eventsDic)) 

        extraFeatureWorker((testFileName, \
                                testFeatureOutFileName,\
                                usersFileName,\
                                eventAttendeesDic,\
                                eventsDic))
        
    else:
        print 'err: insuff arguments'

                

if __name__=='__main__':
    main()

