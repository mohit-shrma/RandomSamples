import sys


""" naive recursive implementation using dynamic programming, top-down approach
    L[i] - length of LIS till i S.T. seq[i] is also part of this LIS and is last element
    L[i] = 1 + max(L[j]) S.T. j < i and seq[j] < seq[i]
         = 1 if no such j found
"""

""" return length of LIS in this seq 
    prev stores the back pointer to previous index in LIS
    subLisLen stores the LIS length ending at say index i
"""
def getNaiveRecursiveLenLIS(seq, subLISLen, prev):
    
    lenSeq = len(seq)
    
    if lenSeq == 1:
        #sequence is of unit length, then it is in itself a LIS of len 1
        return 1

    #length of LIS ending at current sequence last element
    lenLISEndCurrLast = 1

    #initialize the value of default previous pointer
    prev[lenSeq -1] = lenSeq -1

    #recursively get all LIS length from seq[0] to seq[lenSeq - 2]
    #if last element is greater than element before it and
    #if LIS length at element before + 1 is greater than LIS length of last element (lenLISEndCurrLast)
    #then update lenLISEndCurrLast =  element's LIS length + 1
    for i in range(lenSeq-1):
        #compute length of LIS of seq[0:i+1]
        lenSubLIS = getNaiveRecursiveLenLIS(seq[0:i+1], subLISLen, prev)
        if seq[lenSeq -1] > seq[i] and (1 + lenSubLIS) > lenLISEndCurrLast:

            #update length of LIS ending at last element of current sequence
            lenLISEndCurrLast = 1 + lenSubLIS

            #update the value of previous pointer
            prev[lenSeq - 1] = i

    #store the length of LIS found ending at last elem of current index
    subLISLen[lenSeq - 1] =  lenLISEndCurrLast
            
    return lenLISEndCurrLast


def naiveDPLIS(seq):
    #get length of sequence
    lenSeq = len(seq)

    #initialize previous pointer list
    prev = [-1 for i in range(lenSeq)]

    #subLisLen stores the LIS length ending at say index i
    subLISLen = [1 for i in range(lenSeq)]

    #get the length of LIS ending at sequence's last element and
    #update previous pointer list and subLisLen
    getNaiveRecursiveLenLIS(seq, subLISLen, prev)
    
    #get the index with max subseq length
    maxLen = 1
    maxInd = 0
    for i in range(lenSeq):
        if maxLen < subLISLen[i]:
            maxLen = subLISLen[i]
            maxInd = i

    #store the longest increasing subsequence using previous pointers
    lisRev = []
    ind = maxInd
    while(ind >= 0):
        lisRev.append(seq[ind])
        prevInd = prev[ind]
        if prevInd == ind:
            lisRev.append(seq[prevInd])
            break
        else:
            ind = prevInd
    
    lis = [lisRev[i]  for i in range(len(lisRev)-1, -1, -1)] 
            
    return lis



""" Bottom up implementation
    In previous implementation: in recursive iteration same subLISLen is
    computed multiple number of times
    we can avoid this if we go bottom up and store the computation
"""
def bottomUpLenLIS(seq, subLisLen, prev):
    
    #get LIS values in bottom up manner
    for i in range(len(seq)):
        #current sequence element
        for j in range(i):
            #for all element before i or curr seq element
            if seq[i] > seq[j] and subLisLen[i] < subLisLen[j] + 1:
                #current seq element is greater than previous element and 
                #current LIS ending at current elem is shorter
                #than 1 + LIS ending at prev Element
                
                #update current LIS ending at current elem
                subLisLen[i] = subLisLen[j] + 1

                #update previous pointer of current elem
                prev[i] = j


def naiveDPBottomUpLIS(seq):
    #get length of sequence
    lenSeq = len(seq)

    #initialize previous pointer list
    prev = [-1 for i in range(lenSeq)]

    #subLisLen stores the LIS length ending at say index i
    subLISLen = [1 for i in range(lenSeq)]

    #get the length of LIS ending at sequence's last element and
    #update previous pointer list and subLisLen
    bottomUpLenLIS(seq, subLISLen, prev)
    
    #get the index with max subseq length
    maxLen = 1
    maxInd = 0
    for i in range(lenSeq):
        if maxLen < subLISLen[i]:
            maxLen = subLISLen[i]
            maxInd = i

    #store the longest increasing subsequence using previous pointers
    lisRev = []
    ind = maxInd
    while(ind >= 0):
        lisRev.append(seq[ind])
        prevInd = prev[ind]
        if prevInd == ind:
            lisRev.append(seq[prevInd])
            break
        else:
            ind = prevInd
    
    lis = [lisRev[i]  for i in range(len(lisRev)-1, -1, -1)] 
            
    return lis

                
    

""" https://en.wikipedia.org/wiki/Longest_increasing_subsequence O(nlg(n)) implementation"""
#return the index of largest possible element and element itself after
#searching for element < passed value    
def binSearch(sortedSeq, value):

    lo = 0
    hi = len(sortedSeq) - 1
    
    while (lo <= hi):
        #index of middle element in sequence
        mid = (lo + hi)/2

        if sortedSeq[mid] < value:
            lo = mid + 1
        elif sortedSeq[mid] >  value:
            hi = mid - 1
        else:
            #equality
            return mid, sortedSeq[mid]
        
    if (lo - 1) >= 0:
        #found the largest value <= passed value
        return lo - 1, sortedSeq[lo - 1]
    else:
        return -1, -1


        
def getSeq(sequence, predecessorStor, lastElemIndice):
    seq = []
    if lastElemIndice != -1:
        tempLis = getSeq(sequence, predecessorStor, predecessorStor[lastElemIndice])
        for i in tempLis:
            seq.append(i)
        seq.append(sequence[lastElemIndice])
    return seq

def findLIS(sequence):

    #positionByLenStor[j]
    #stores the position k of the smallest value X[k]
    #such that there is an increasing subsequence of length j ending at sequence[k]
    #on the range k < i(index into passed sequence)  
    #stores position of indices 
    positionByLenStor = [-1 for i in range(len(sequence))]
    
    #stores the position of the predecessor of sequence[k] in the
    #longest increasing subsequence ending at sequence[k]
    predecessorStor = []

    #length of LIS
    lenLIS = -1
    
    for i in range(len(sequence)):
        #find largest +ve j<=lenLIS
        #S.T. sequence[positionByLenStor[j]] < sequence[i]
        endPosSeq = [ sequence[positionByLenStor[j]] for j in range(lenLIS+1) ] 
        j, elem = binSearch(endPosSeq, sequence[i])
        predecessorStor.append(positionByLenStor[j])
        if j == lenLIS or sequence[i] < sequence[positionByLenStor[j+1]]:
            positionByLenStor[j+1] = i
            lenLIS = max(lenLIS, j+1)
    
    return getSeq(sequence, predecessorStor, positionByLenStor[lenLIS])


def main():
    someSeq = [1,8,2,4,3,4,5,10,10]
    #someSeq = [4, 2, 7, 9]
    print "using optimal O(nlgn) approach using binary search"
    print findLIS(someSeq)
    print "usin DP top down sol O(n^2) redundant computation "
    print naiveDPLIS(someSeq)
    print "using DP bottom up sol O(n^2)"
    print naiveDPBottomUpLIS(someSeq)
    
    
if __name__ == '__main__':
    main()
