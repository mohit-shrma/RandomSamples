import sys 
import csv
import time
from dateutil.parser import parse
from prepareClassifyData import *
from time import gmtime, strftime
from multiprocessing import Process, Manager, Pool


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
    with open(fileName, 'r') as eventFile:
        fReader = csv.reader(eventFile)
        #skip header
        fReader.next()
        for row in fReader:
            user = int(row[TRAIN_CONSTS.USER_COL])
            if user not in eventCount:
                eventCount[user] = 0
            eventCount[user] += 1
    return eventCount



""" compute weighted PRank for similar users '{user:[(simUser, pRank)]}'responses """
def getWeightedResponseWt(eventAttendeesDic, simUsersDic, userId, eventId):
    #get event attendees
    yesAtn = set((eventAttendeesDic[eventId])[EVENT_ATTN.YES_COL - 1])
    noAtn = set((eventAttendeesDic[eventId])[EVENT_ATTN.NO_COL - 1])
    mayBeAtn = set((eventAttendeesDic[eventId])[EVENT_ATTN.MAYBE_COL - 1])
    invAtn = set((eventAttendeesDic[eventId])[EVENT_ATTN.INVITED_COL - 1])
    
    #get wt of respnses for similar users
    weightDic = {'yes':0, 'no':0, 'maybe':0, 'inv':0}
    
    for (simUser, pRank) in simUsersDic[userId]:
        if simUser in yesAtn:
            weightDic['yes'] += pRank
        elif simUser in noAtn:
            weightDic['no'] += pRank
        elif simUser in mayBeAtn:
            weightDic['maybe'] += pRank
        elif simUser in invAtn:
            weightDic['inv'] += pRank

    return weightDic
    


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




def getExtraFeatures(fileName, eventAttendeesDic, simUsersDic, \
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
        """headersTitle = ['user', 'event', 'deltaStartJoin', 'deltaStartShown',\
                            'deltaShownJoin', 'eventCount', 'simYes', 'simNo',\
                            'simMaybe', 'simInv', 'popYes', 'popNo',\
                            'popMaybe', 'popInv']"""
        headersTitle = ['user', 'event',  'simYes', 'simNo', 'simMaybe',\
                            'simInv', 'simYCount', 'simNCount', 'simMCount',\
                            'simICount']
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

            """
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
            """

            #get response based on similarity
            weightDic = getWeightedResponseWt(eventAttendeesDic, simUsersDic,\
                                                  userId, eventId)
            features.extend([weightDic['yes'], weightDic['no'], \
                                  weightDic['maybe'], weightDic['inv']])

            #get attendees count from similar users
            simUsersSet = set([value[1] for value in simUsersDic.values()])
            (yesSimCount, maybeSimCount, invitedSimCount, noSimCount) = \
                getEventAtnCount(simUsersSet, eventAttendeesDic[eventId])
            features.extend([yesSimCount, noSimCount, maybeSimCount,\
                                 invitedSimCount])
            
            """
            #get event popularity
            (yesCount, noCount, maybeCount, invCount) = \
                getEventPopularity(eventId, eventAttendeesDic)
            features.extend([yesCount, noCount, maybeCount, invCount])
            """

            features = map(str, features)
        
            #write features
            featureWriter.writerow(features)

            if (count%100 == 0):
                print '100 done...', strftime("%Y-%m-%d %H:%M:%S", gmtime())


def extraFeatureWorker((fileName, featureOutFileName, usersFileName,\
                            eventAttendeesDic, simUsersDic,  eventsDic)):
    getExtraFeatures(fileName, eventAttendeesDic, simUsersDic,\
                         usersFileName, featureOutFileName, eventsDic)



""" get the list of events attended by each user i.e. indicated 'yes' """
def getUserEventsDic(eventAttendeesDic):
    userEventsDic = {}
    for event, attendees in eventAttendeesDic.iteritems():
        for user in attendees[EVENT_ATTN.YES_COL - 1]:
            if user not in userEventsDic:
                userEventsDic[user] = set([])
            userEventsDic[user].add(event)
    return userEventsDic



def writeUserEventsDic(userEventsDic, userEventsFileName):
    with open(userEventsFileName, 'w') as userEventsFile:
        for user, events in userEventsDic.iteritems():
            eventsStr = ' '.join(map(str, events))
            userEventsFile.write(str(user) + ',' + eventsStr +'\n')
            

def getJacSimUser((userIdx, sharedUserEventsAtn)):
    simDic = {}
    if userIdx < len(sharedUserEventsAtn):
        for j in range(userIdx+1, len(sharedUserEventsAtn)):
            #find the intersecting events b/w user i and user j
            unionEvCount = len(sharedUserEventsAtn[i][1] | sharedUserEventsAtn[j][1])
            interEvCount = len(sharedUserEventsAtn[i][1] & sharedUserEventsAtn[j][1])
            if interEvCount > 0:
                simDic[sharedUserEventsAtn[j][0]] = float(interEvCount)/unionEvCount
    return simDic



#will write user, user, 'event co-attendance jaccard sim'
def writeUserEventsJacc(userEventsDic, userEventsJacFileName, chunkSize=16):
    userEventsAtn = []
    for user, events in userEventsDic.iteritems():
        userEventsAtn.append((user, set(events)))
    
    manager = Manager()
    sharedUserEventsAtn = manager.list(userEventsAtn)
    sharedUserEventsAtn.extend(userEventsAtn)

    with open(userEventsJacFileName, 'w') as userEvJacFile:
        for i in range(0, len(userEventsAtn), chunkSize):
            pool = Pool(processes=chunkSize)
            workIdx = range(i, i+chunkSize)
            workerArgs = map(lambda x : (x, sharedUserEventsAtn), workIdx)
            simDics = pool.map(getJacSimUser, workerArgs)
            pool.close()
            pool.join()
            for idx in range(i, i+chunkSize):
                #write similar user for userEventsAtn[idx]
                
                if len(simDics[idx-i]) > 0:
                    userEvJacFile.write(str(userEventsAtn[idx][0])
                    for simUser, jacSim in (simDics[idx-i]).iteritems():
                        userEvJacFile.write(' ' + str(simUser) + ' '\
                                                + str(jacSim))    
                userEvJacFile.write('\n')

            """
            for j in range(i+1, len(userEventsAtn)):
                #find the intersecting events b/w user i and user j
                unionEvCount = len(userEventsAtn[i][1] | userEventsAtn[j][1])
                interEvCount = len(userEventsAtn[i][1] & userEventsAtn[j][1])
                if interEvCount > 0:
                    userEvJacFile.write(str(userEventsAtn[i][0]) + ','\
                                            + str(userEventsAtn[j][0])\
                                            + ','\
                                            + str(float(interEvCount)/unionEvCount)\
                                            + '\n')"""



def main():
    if len(sys.argv) > 9:
        trainFileName = sys.argv[1]
        testFileName = sys.argv[2]
        eventAttFileName = sys.argv[3]
        eventsFileName = sys.argv[4]
        usersFileName = sys.argv[5]
        simUserFileName = sys.argv[6]
        userFriendsFileName  = sys.argv[7]
        userEventsFileName = sys.argv[8]
        trainFeatureOutFileName = sys.argv[9]
        testFeatureOutFileName = sys.argv[10]
        
        #trainUsersSet = getFirstColSet(trainFileName)
        #testUsersSet = getFirstColSet(testFileName)
        #eventsSet = getFirstColSet(eventAttFileName)
        #writeModdedFiles(eventsSet, eventsFileName)
        
        print 'get event attendees dic...', strftime("%Y-%m-%d %H:%M:%S", gmtime())
        eventAttendeesDic = getEventAttendees(eventAttFileName)

        print 'building user events dic...', strftime("%Y-%m-%d %H:%M:%S", gmtime())
        userEventsDic = getUserEventsDic(eventAttendeesDic)
        writeUserEventsJacc(userEventsDic, userEventsFileName)
        #writeUserEventsDic(userEventsDic, userEventsFileName)

        #simUsersDic = getSimUsersDic(simUserFileName)
        #adjList = createAdjList(userFriendsFileName, testUsersSet, trainUsersSet)
        """
        modEventFileName = getModdedName(eventsFileName)
        
        print 'reading events file...', strftime("%Y-%m-%d %H:%M:%S", gmtime())
        eventsDic = getEvents(modEventFileName)

        simUsersDic = getSimUsersDic(simUserFileName)
        
        extraFeatureWorker((trainFileName, trainFeatureOutFileName,\
                                usersFileName, eventAttendeesDic,\
                                simUsersDic, eventsDic)) 

        extraFeatureWorker((testFileName, \
                                testFeatureOutFileName,\
                                usersFileName,\
                                eventAttendeesDic,\
                                simUsersDic, eventsDic))
        """
    else:
        print 'err: insuff arguments'

                

if __name__=='__main__':
    main()

