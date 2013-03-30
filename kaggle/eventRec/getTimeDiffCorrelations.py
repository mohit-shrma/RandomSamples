import csv
import sys
from dateutil.parser import parse
import time

import matplotlib
#initialize pyplot for non interactive backend
matplotlib.use('Agg')
from pylab import *
import matplotlib.pyplot as plt
import os
    
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


def getUsers(fileName):
    userSet = set([])
    with open(fileName, 'r') as f:
        fReader = csv.reader(f)
        #skip header
        fReader.next()
        for row in fReader:
            userSet.add(int(row[USERS_CONSTS.USER_COL]))
    return userSet


def getEvents(fileName):
    eventsSet = set([])
    with open(fileName, 'r') as f:
        fReader = csv.reader(f)
        #skip header
        fReader.next()
        for row in fReader:
            eventsSet.add(int(row[EVENTS_CONSTS.EVENT_COL]))
    return eventsSet

    
def getUsersJoinTime(usersFileName, userSet):
    userJoinTimeDic = {}
    with open(usersFileName, 'r') as usersFile:
        usersReader = csv.reader(usersFile)
        #skip header
        usersReader.next()
        for row in usersReader:
            user = int(row[USERS_CONSTS.USER_COL])
            if user in userSet:
                strJoinTime = row[USERS_CONSTS.JOINED_AT_COL]
                if len(strJoinTime) > 0 and strJoinTime != 'None':
                    userJoinedTime = time.mktime(parse(strJoinTime).timetuple())
                    userJoinTimeDic[user] = userJoinedTime
    return userJoinTimeDic



def getEventStartTime(eventsFileName, eventsSet):
    eventStartTimedic = {}
    with open(eventsFileName, 'r') as eventsFile:
        eventsReader = csv.reader(eventsFile)
        #skip header
        eventsReader.next()
        for row in eventsReader:
            event = int(row[EVENTS_CONSTS.EVENT_COL])
            if event in eventsSet:
                strEventTime = row[EVENTS_CONSTS.START_TIME]
                if len(strEventTime) > 0 and strEventTime != 'None':
                    eventStartTimedic[event] = \
                        time.mktime(parse(strEventTime).timetuple())
    return eventStartTimedic



def parseIntermedTogetTimeDiff(interMedFileName):

    trainLabels = []
    eventStartShownDiffs = []
    eventShownJoinDiffs = []
    eventStartJoinDiffs = []

    with open(interMedFileName, 'r') as interMedFile:
        interMedReader = csv.reader(interMedFile, delimiter='\t')
        for row in interMedReader:
            trainLabels.append(int(row[0]))
            eventStartShownDiffs.append(float(row[1]))
            eventShownJoinDiffs.append(float(row[2]))
            eventStartJoinDiffs.append(float(row[3]))

    createScatterPlots(trainLabels, eventStartShownDiffs, eventShownJoinDiffs,\
                           eventStartJoinDiffs)

    createBinPlots(trainLabels, eventStartShownDiffs, eventShownJoinDiffs,\
                       eventStartJoinDiffs)



def createBinPlots(trainLabels, eventStartShownDiffs, eventShownJoinDiffs,\
                           eventStartJoinDiffs):

    tempEventStartShownDiffs1 = []
    tempEventShownJoinDiffs1 = []
    tempEventStartJoinDiffs1 = []

    
    tempEventStartShownDiffs2 = []
    tempEventShownJoinDiffs2 = []
    tempEventStartJoinDiffs2 = []

    
    #create hist for intereseted labels
    for i in range(len(trainLabels)):
        if trainLabels[i] == 1:
            tempEventStartShownDiffs1.append(float(eventStartShownDiffs[i])/(24*60*60))
            tempEventShownJoinDiffs1.append(float(eventShownJoinDiffs[i])/(24*60*60))
            tempEventStartJoinDiffs1.append(float(eventStartJoinDiffs[i])/(24*60*60))
        elif trainLabels[i] == -1:
            tempEventStartShownDiffs2.append(float(eventStartShownDiffs[i])/(24*60*60))
            tempEventShownJoinDiffs2.append(float(eventShownJoinDiffs[i])/(24*60*60))
            tempEventStartJoinDiffs2.append(float(eventStartJoinDiffs[i])/(24*60*60))

    #create plot for event start shown diff and interestedness
    
    #indicate to pyplot that we have new figure
    figure()

    #histogram
    n, bins, patches = hist(\
        [tempEventStartShownDiffs1, tempEventStartShownDiffs2],\
            100, normed=False, histtype='bar',\
            color=['crimson', 'burlywood'],\
            label=['Yes', 'No'])
    legend()
    xmin, xmax = xlim()
    xlim(-10, 200)
    xlabel('event start - event shown (days)')
    ylabel('interestedness')
    title('event start N event shown delta')
    #save figure
    savefig("eventStartShownDelta_hist.png")

    #indicate to pyplot that we have new figure
    figure()

    #histogram
    n, bins, patches = hist(\
        [tempEventShownJoinDiffs1,tempEventShownJoinDiffs2],\
            100, normed=False, histtype='bar',\
            color=['crimson', 'burlywood'],\
            label=['Yes', 'No'])
    legend()
    xmin, xmax = xlim()
    xlim(-10, 100)
    xlabel('event shown - user join (days)')
    ylabel('interestedness')
    title('event shown N event join delta')
    #save figure
    savefig("eventShownJoinDelta_hist.png")

    #indicate to pyplot that we have new figure
    figure()

    #histogram
    n, bins, patches = hist(\
        [tempEventStartJoinDiffs1, tempEventStartJoinDiffs2],\
            100, normed=False, histtype='bar',\
            color=['crimson', 'burlywood'],\
            label=['Yes', 'No'])
    legend()
    xmin, xmax = xlim()
    xlim(-10, 200)
    xlabel('event start - user join (days)')
    ylabel('interestedness')
    title('event start N user join delta')
    #save figure
    savefig("eventStartUJoinDelta_hist.png")


            

def createScatterPlots(trainLabels, eventStartShownDiffs, eventShownJoinDiffs,\
                           eventStartJoinDiffs):
    #create plot for event start shown diff and interestedness
    
    #indicate to pyplot that we have new figure
    figure()

    #convert time diff to days
    x = [ float(diff)/(24*60*60) for diff in eventStartShownDiffs]
    
    #scatter plot
    scatter(x, trainLabels, s=5, color = 'tomato')
    ylim(-1.5, 1.5)
    xlim(-10, 200)
    xlabel('event start - event shown (days)')
    ylabel('interestedness')
    title('event start N event shown delta')
    #save figure
    savefig("eventStartShownDelta.png")
    
    #indicate to pyplot that we have new figure
    figure()

    #convert time diff to days
    x = [ float(diff)/(24*60*60) for diff in eventShownJoinDiffs]
    
    #scatter plot
    scatter(x, trainLabels, s=5, color = 'tomato')
    ylim(-1.5, 1.5)
    xlim(-10, 200)
    xlabel('event shown - event join (days)')
    ylabel('interestedness')
    title('event shown N event join delta')
    #save figure
    savefig("eventShownJoinDelta.png")

    #indicate to pyplot that we have new figure
    figure()

    #convert time diff to days
    x = [ float(diff)/(24*60*60) for diff in eventStartJoinDiffs]
    
    #scatter plot
    scatter(x, trainLabels, s=5, color = 'tomato')
    ylim(-1.5, 1.5)
    xlim(-10, 200)
    xlabel('event start - user join (days)')
    ylabel('interestedness')
    title('event start N user join delta')
    #save figure
    savefig("eventStartUJoinDelta.png")


            

def parseTrainToGetTimeDiff(trainFileName, eventStartTimeDic, userJoinTimeDic):

    trainLabels = []
    eventStartShownDiffs = []
    eventShownJoinDiffs = []
    eventStartJoinDiffs = []
    
    with open(trainFileName, 'r') as trainFile:
        trainReader = csv.reader(trainFile)
        #skip header
        trainReader.next()
        f = open("saveDiff.txt", 'w')
        for row in trainReader:
            user = int(row[TRAIN_CONSTS.USER_COL])
            event = int(row[TRAIN_CONSTS.EVENT_COL])
            eventShownTime = time.mktime(\
                parse(row[TRAIN_CONSTS.TIMESTAMP_COL]).timetuple())
            isInterested = int(row[TRAIN_CONSTS.INTERESTED_COL])
            isNotInterested = -1*int(row[TRAIN_CONSTS.NOT_INTERESTED_COL])
            
            if event in eventStartTimeDic:
                eventStartShownDiff = eventStartTimeDic[event] - eventShownTime
            else:
                eventStartShownDiff = 0
                
            if user in userJoinTimeDic:
                eventShownJoinDiff = eventShownTime - userJoinTimeDic[user]
            else:
                eventShownJoinDiff = 0

            if event in eventStartTimeDic and user in userJoinTimeDic:
                eventStartJoinDiff = eventStartTimeDic[event] - userJoinTimeDic[user]
            else:
                eventStartJoinDiff = 0
                
            trainLabels.append(isInterested + isNotInterested)

            eventStartShownDiffs.append(eventStartShownDiff)
            eventShownJoinDiffs.append(eventShownJoinDiff)
            eventStartJoinDiffs.append(eventStartJoinDiff)
            f.write('\t'.join([str(isInterested + isNotInterested),\
                                   str(eventStartShownDiff),\
                                   str(eventShownJoinDiff),\
                                   str(eventStartJoinDiff)]) + '\n')
        f.close()
        createScatterPlots(trainLabels, eventStartShownDiffs, eventShownJoinDiffs,\
                               eventStartJoinDiffs)
    

def main():
    if len(sys.argv) > 4:
        usersFileName = sys.argv[1]
        eventsFileName = sys.argv[2]
        trainFileName = sys.argv[3]
        interMedFileName = sys.argv[4]
        
        if os.path.isfile(interMedFileName):
            parseIntermedTogetTimeDiff(interMedFileName)
        else:
            users = getUsers(usersFileName)
            events = getEvents(eventsFileName)

            userJoinTimeDic = getUsersJoinTime(usersFileName, users)
            eventStartTimeDic = getEventStartTime(eventsFileName, events)

            parseTrainToGetTimeDiff(trainFileName, eventStartTimeDic,\
                                        userJoinTimeDic)
            
            createBinPlots(trainLabels, eventStartShownDiffs, eventShownJoinDiffs,\
                               eventStartJoinDiffs)

    else:
        print 'err: invalid args'

if __name__=='__main__':
    main()
    
