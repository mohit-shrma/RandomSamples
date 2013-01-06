import sys


""" given tuples or pairs like { (a,b), (c,d) } (c,d) can follow (a,b) only if b < c
of the given pairs or tuples find the longest chain which can be formed from the given
tuples/pairs

(I) sort the given tuple/pairs by first element to give list of tuple[]
(II) apply LIS considering second element 
    naive recursive implementation using dynamic programming, top-down approach
    L[i] - length of LIS till i S.T. tuple[i] is also part of this LIS and is last tuple
    L[i] = 1 + max(L[j]) S.T. j < i and tuple[i] follows tuple[j]
         = 1 if no such j found
"""

""" return length of longest chain in the sorted tuple seq
    prev stores the back pointer to previous tuple index in LIS
    subLisLen stores the LIS length ending at say tuple index i
"""
def getNaiveRecursiveLenLIS(tupleList, subLISLen, prev):

    lenTupleList = len(tupleList)

    if lenTupleList == 1:
        #sequence is of unit length, then it is in itself a LIS of len 1
        return 1

    #length of LIS ending at current sequence last element
    lenLISEndCurrLast = 1

    #initialize the value of default previous pointer
    prev[lenTupleList -1] = lenTupleList -1

    #recursively get all LIS length from tupleList[0] to tupleList[lenTupleList - 2]
    #if last tuple can follow tuple before it and
    #if LIS length at tuple before + 1 is greater than LIS length of last element (lenLISEndCurrLast)
    #then update lenLISEndCurrLast =  element's LIS length + 1
    for i in range(lenTupleList-1):
        #compute length of LIS of tupleList[0:i+1]
        lenSubLIS = getNaiveRecursiveLenLIS(tupleList[0:i+1], subLISLen, prev)
        if tupleList[lenTupleList -1][0] > tupleList[i][1]\
                and (1 + lenSubLIS) > lenLISEndCurrLast:
            #last tuple element can follow previous tuple
            #and including it our length increases
            #update length of LIS ending at last element of current sequence
            lenLISEndCurrLast = 1 + lenSubLIS

            #update the value of previous pointer
            prev[lenTupleList - 1] = i

    #store the length of LIS found ending at last elem of current index
    subLISLen[lenTupleList - 1] =  lenLISEndCurrLast
            
    return lenLISEndCurrLast


""" apply dynamic programming solution of longest increasing subsequence on the
sorted tuple list
"""
def naiveDPLIS(tupleList):
    
    lenTupleList = len(tupleList)

    #initialize previous pointer list
    prev = [-1 for i in range(lenTupleList)]

    #subLisLen stores the LIS length ending at say index i
    subLISLen = [1 for i in range(lenTupleList)]

    #get the length of LIS ending at sequence's last element and
    #update previous pointer list and subLisLen
    getNaiveRecursiveLenLIS(tupleList, subLISLen, prev)
    
    #get the index with max subseq length
    maxLen = 1
    maxInd = 0
    for i in range(lenTupleList):
        if maxLen < subLISLen[i]:
            maxLen = subLISLen[i]
            maxInd = i

    #store the longest increasing subsequence using previous pointers
    lisRev = []
    ind = maxInd
    while(ind >= 0):
        lisRev.append(tupleList[ind])
        prevInd = prev[ind]
        if prevInd == ind:
            lisRev.append(tupleList[prevInd])
            break
        else:
            ind = prevInd
    
    lis = [lisRev[i]  for i in range(len(lisRev)-1, -1, -1)] 
            
    return lis


""" sort the given tuples by first element of tuple """
def sortByFirstElem(tupleList):
    sortedTupleList = sorted(tupleList, key = lambda tupleElement: tupleElement[0])
    return sortedTupleList



def main():
    #input tuples
    tupleList=[(5,24),(39,60),(15,28),(27,40),(50,90)]
    print 'tuple list: ', tupleList
    sortedTupleList = sortByFirstElem(tupleList)
    print 'sorted tuple list: ', sortedTupleList
    print naiveDPLIS(sortedTupleList)

    
if __name__ == '__main__':
    main()
