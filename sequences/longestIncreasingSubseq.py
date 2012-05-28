""" https://en.wikipedia.org/wiki/Longest_increasing_subsequence """

import sys

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
    print findLIS(someSeq)
    
if __name__ == '__main__':
    main()
