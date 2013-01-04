import sys


""" naive recursive implementation using dynamic programming, top-down approach
    maxSum[i] - sum of max sum IS till i S.T. seq[i] is also part of this max sum IS and is last element
    maxSum[i] = seq[i] + max(maxSum[j]) S.T. j < i and seq[j] < seq[i]
         = seq[i] if no such j found
"""

""" return sum of max sum IS in this seq and the index max sum Inc sequence ends
    prev stores the back pointer to previous index in max sum IS
    subLisSum stores the sum of max sum IS ending at say index i
"""
def getNaiveRecursiveMaxSumIS(seq, subLisSum, prev):
    
    lenSeq = len(seq)
    
    if lenSeq == 1:
        #sequence is of unit length, then it is in itself a max sum IS
        return seq[0]

    #max sum of IS ending at current sequence's last element
    maxSumISEndCurrLast = seq[lenSeq-1]

    #initialize the value of default previous pointer
    prev[lenSeq -1] = lenSeq -1

    #recursively get all sum of max sum IS from seq[0] to seq[lenSeq - 2]
    #if last element is greater than element before it and
    #if sum of max sum IS at element before + last elem  is greater than sum of max sum IS of last element (maxSumISEndCurrLast)
    #then update maxSumISEndCurrLast =  element before's sum of max sum IS + last elem
    for i in range(lenSeq-1):
        #compute sum  of max sum IS of seq[0:i+1]
        maxSumSubLIS = getNaiveRecursiveMaxSumIS(seq[0:i+1], subLisSum, prev)
        if seq[lenSeq -1] > seq[i] and\
                (seq[lenSeq -1] + maxSumSubLIS) > maxSumISEndCurrLast:

            #update length of LIS ending at last element of current sequence
            maxSumISEndCurrLast = seq[lenSeq -1]  + maxSumSubLIS

            #update the value of previous pointer
            prev[lenSeq - 1] = i

    #store the length of LIS found ending at last elem of current index
    subLisSum[lenSeq - 1] =  maxSumISEndCurrLast
            
    return maxSumISEndCurrLast

def naiveDPMaxSumIS(seq):
    #get length of sequence
    lenSeq = len(seq)

    #initialize previous pointer list
    prev = [-1 for i in range(lenSeq)]

    #subLisSum stores the LIS length ending at say index i
    subLISSum = [1 for i in range(lenSeq)]

    #get the sum of max sum IS ending at sequence's last element and
    #update previous pointer list and subLisSum
    getNaiveRecursiveMaxSumIS(seq, subLISSum, prev)
    
    #get the index with max subseq sum
    maxLen = 1
    maxInd = 0
    for i in range(lenSeq):
        if maxLen < subLISSum[i]:
            maxLen = subLISSum[i]
            maxInd = i
    maxSum = subLISSum[maxInd]
    
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
            
    return lis, maxSum



def main():
    someSeq = [1, 101, 2, 3, 100, 4, 5]
    #someSeq = [3, 4, 5, 10]
    print "usin DP top down sol O(n^2) redundant computation "
    print naiveDPMaxSumIS(someSeq)
    
if __name__ == '__main__':
    main()

