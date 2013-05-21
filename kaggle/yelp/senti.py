from pattern.en.wordnet import sentiment
import math
import numpy as np

#load sentiword net
sentiment.load()


def getReviewsBusinessDates(reviewIds, dbReviews, reviewDateFileName):
    with open(reviewDateFileName, 'w') as f:
        for reviewId in reviewIds:
            dt = dbReviews.find_one({'review_id':reviewId})['date']
            dtTuple = dt.timetuple()
            year = dtTuple.tm_year
            month = dtTuple.tm_mon
            dayOfWk = dtTuple.tm_wday
            dayOfYr = dtTuple.tm_yday
            dList = [year, month, dayOfWk, dayOfYr]
            f.write(','.join(map(str, dList)) + '\n')


def getReviewsBusinessTopCateg(topCateg, dbBusiness, reviews,\
                                     topBizCategFileName):
    topCategDic = {}
    for i in range(len(topCateg)):
        topCategDic[topCateg[i]] = i

    with open(topBizCategFileName, 'w') as f:
        #write header
        f.write('business_id,' + ','.join(topCateg) + '\n')
        for bizId in reviews['businessId']:
            isCategPresent = [0]*len(topCateg)
            bizCat = dbBusiness.find_one({'business_id':bizId},\
                                              {'categories':1})['categories']
            for uCateg in bizCat:
                categ = uCateg.encode('utf8')
                if categ in topCategDic:
                    isCategPresent[topCategDic[categ]] = 1
            f.write(bizId+','+','.join(map(str, isCategPresent))+'\n')
            

def getBusinessZipCode(dbBusiness):
    businessZip = {}
    zipPattern = re.compile('(\d{5})$')
    for biz in dbBusiness.find():
        if 'full_address' in biz:
            fAddr = biz['full_address']
            zipSearch = zipPattern.search(fAddr)
            if zipSearch is not None:
                zipCode = zipSearch.groups()[0]
                businessZip[biz['business_id']] = int(zipCode)
    return businessZip


def getBusinessUsefulRatio():
    bIdUsefulRatio = {}
    with open('trainBusinessUsefulRatio.txt','r') as f:
        line = f.readline()    
        for line in f:
            cols = line.strip().split(',')
            bIdUsefulRatio[cols[0]] = cols[2]
    return bIdUsefulRatio



def writeNewFeatures(oldFeatureFileName, newFeatureFileName, bIdUsefulRatio):
    with open(oldFeatureFileName, 'r') as f:
        with open(newFeatureFileName, 'w') as g:
            line = f.readline().strip()
            g.write(','.join(line.split(',')[0:-1]) \
                        +',userUsefulRatio,businessUsefulRatio,' \
                        + line.split(',')[-1] + '\n')
            for line in f:
                cols = line.strip().split(',')
                userUsefulRatio = float(cols[9])/float(cols[8])
                businessUsefulRatio = '0'
                if cols[1] in bIdUsefulRatio:
                    businessUsefulRatio = bIdUsefulRatio[cols[1]]
                g.write( ','.join(cols[0:-1]) + ',' + str(userUsefulRatio) \
                             + ',' + businessUsefulRatio + ',' + cols[-1]  \
                             + '\n')


def getPcUsefulCountByReviews(businessId, py_reviews):
    reviews = py_reviews.find({'business_id':businessId})
    reviewCount = 0.0
    usefulCount = 0.0
    ratio = 0.0
    for review in reviews:
        reviewCount += 1
        usefulCount += review['votes']['useful']
        ratio = usefulCount/reviewCount
    return reviewCount, ratio



def getUsefulnessRatio(businesses, py_reviews, ratioOpFileName):
    with open(ratioOpFileName, 'w') as f:
        for businessId in businesses:
            (reviewCount, usefulRatio) = \
                getPcUsefulCountByReviews(businessId, py_reviews)
            f.write(','.join([businessId, str(reviewCount), str(usefulRatio)]) + '\n')


            
def fetchReviewNText(py_reviews, reviewIdsFileName, reviewsTextFileName):
    with open(reviewIdsFileName, 'w') as revIds, \
            open(reviewsTextFileName, 'w') as revText:
        for review in py_reviews.find():
            revIds.write(review['review_id'] + '\n')
            reviewText = review['text'].encode('utf-8').strip()
            reviewText = ' '.join(reviewText.split('\n'))
            revText.write(reviewText + '\n')



def normalizedRowNSumTFIDF(numTerms, termIDFFile):
    normTermSum = np.zeros((numTerms,), dtype=np.float)
    with open(termIDFFile, 'r') as f:
        for line in f:
            tokens = map(float, line.strip().split())
            numTokens = len(tokens)
            inds = range(1, numTokens, 2)
            norm = np.sqrt(np.sum((np.asarray(tokens)[inds])**2))
            for i in range(0, numTokens, 2):
                normTermSum[tokens[i]-1] += tokens[i+1]/norm
    return normTermSum




def getInvDocFreq(numTerms, termFreqFile):
    freqArr = np.zeros((numTerms,), dtype=np.float)
    numDocs = 0
    with open(termFreqFile, 'r') as f:
        #read header
        f.readline()
        for line in f:
            numDocs += 1
            tokens = map(int, line.strip().split())
            numTokens = len(tokens)
            for i in range(0, numTokens, 2):
                freqArr[tokens[i]-1] += 1
    invDocFreq = np.log((freqArr**-1)*numDocs)
    return (invDocFreq, freqArr)

    
                
def getTFIDF(numTerms, termFreqFile, termIDFFile, invDocFreq):
    with open(termFreqFile, 'r') as f, open(termIDFFile, 'w') as g:
        #read header
        f.readline()
        for line in f:
            tokens = map(int, line.strip().split())
            numTokens = len(tokens)
            for i in range(0, numTokens, 2):
                termInd = int(tokens[i]-1)
                #tfIdf = float(tokens[i+1])*invDocFreq[termInd]
                tfIdf = (1 + np.log(float(tokens[i+1])))*invDocFreq[termInd]
                g.write(str(termInd+1) + " " + str(tfIdf) + " ")
            g.write('\n')



            
def fetchTopKTerms(numTerms, K, termFreqFile):
    freqArr = np.zeros((numTerms,), dtype=np.uint32)

    with open(termFreqFile, 'r') as f:
        #read header
        f.readline()
        for line in f:
            tokens = map(int, line.strip().split())
            numTokens = len(tokens)
            for i in range(0, numTokens, 2):
                freqArr[tokens[i]-1] += tokens[i+1]
    sortInd = np.argsort(freqArr)
    revTopK = sortInd[-1*K:]
    topK = revTopK[::-1]
    return topK


def extractTopKFreqFeature(k, topKInd, termFreqFile, \
                               topTermsFeatureFileName):
    topKSet = set(topKInd[:k])

    #create a reverse lookup dictionary
    indMap = {}
    for i in range(k):
        indMap[topKInd[i]] = i

    with open(termFreqFile, 'r') as f, \
            open(topTermsFeatureFileName, 'w') as g:
        #skip header
        f.readline()
        for line in f:
            freqArr = np.zeros((k,), dtype=np.uint32)
            tokens = map(float, line.strip().split())
            numTokens = len(tokens)
            for i in range(0, numTokens, 2):
                if (tokens[i]-1) in topKSet:
                    freqArr[indMap[(tokens[i]-1)]] += tokens[i+1]
            g.write(','.join(map(str, freqArr)) + '\n')
            

def sentiword_sentiment_score(s, negationWordSet):
    v = 0
    prevWord = None
    for w in s.split(" "):
        w = w.strip(",.!?)(#:;\"\'").lower()
        if w in sentiment:
            score = sentiment[w][0] - sentiment[w][1]
            if prevWord and prevWord in negationWordSet:
                v += -1*score
            else:
                v+= score
        prevWord = w
    return v


def liu_senti_score(text, posWordSet, negWordSet, negationWordSet):
    score = 0
    tokens = text.split(" ")
    prevWord = None
    for i in range(len(tokens)):
        w = tokens[i].strip(",.!?)(#:;\"\'").lower()
        orientation = 0
        if w in posWordSet:
            orientation = 1
        elif w in negWordSet:
            orientation = -1
        if prevWord and prevWord in negationWordSet:
            orientation *= -1
        score += orientation
        prevWord = w
    return score

