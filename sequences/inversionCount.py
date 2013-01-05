import sys
import math

""" count the number of inversions in a given sequence of number
e.g. [2,4,1,3,5] , 3 inversions (2,1) (4,1) and (4,3)
"""



""" merge and count inversions in the combine list, assuming left and right
part are sorted while using linear merging procedures count the inversions
where an element in right part is less than left part
return inversion count and sorted list
"""
def mergeNCountInv(leftSeq, rightSeq):

    #initialize a left and right ptr on the start of both list
    leftPtr = 0
    rightPtr = 0

    #initialize inversion count
    invCount = 0

    #init merged sorted list
    mergedList = []

    #linearly merge the list and count inversions
    while (leftPtr < len(leftSeq)) and (rightPtr < len(rightSeq)):
        if leftSeq[leftPtr] <= rightSeq[rightPtr]:
            #element at left is smaller than element on right
            #append left to merged list and no inversion
            mergedList.append(leftSeq[leftPtr])

            #increment the leftPtr
            leftPtr += 1
        else:
            #element at right is smaller than element on left
            #append right element to merged list
            mergedList.append(rightSeq[rightPtr])

            #increment the inversion count to no. of elments
            #in left after and incl leftPtr index
            invCount += len(leftSeq) - leftPtr

            print 'inversions: right - ', rightSeq[rightPtr], ' left - ',\
                leftSeq[leftPtr:len(leftSeq)]
            
            #increment the rightPtr
            rightPtr += 1

    if leftPtr < len(leftSeq):
        #left list remains, right one empty
        while (leftPtr < len(leftSeq)):
            mergedList.append(leftSeq[leftPtr])
            leftPtr += 1


    if rightPtr < len(rightSeq):
        #right list remains, right one empty
        while (rightPtr < len(rightSeq)):
            mergedList.append(rightSeq[rightPtr])
            rightPtr += 1

    return (invCount, mergedList)

""" recursively partition the lsit and count the inversions"""            
def sortListAndCountInv(seq):
    #inversion count of current list
    invCount = 0

    if len(seq) == 1:
        #no inversion in one char and list is sorted in itself
        return (invCount, seq)
    else:
        #divide the current list into two parts and recursively
        #sort and count inversions in it

        #left part of the list i.e. ceil(n/2) elements
        leftLastInd = int(math.ceil( float(len(seq))/2 -1))
        leftSeq = seq[0:leftLastInd+1]

        #right part of the list i.e. remaining elements
        rightSeq = seq[leftLastInd+1:len(seq)]

        #get inversion count and sorted left sequence
        (leftInvCount, sortedLeft) = sortListAndCountInv(leftSeq)
        
        #get inversion count and sorted right sequence
        (rightInvCount, sortedRight) = sortListAndCountInv(rightSeq)

        #get merged inv count and combined sorted sequence
        (mergedInvCount, mergedSortedSeq) = mergeNCountInv(sortedLeft,\
                                                               sortedRight)

        #get net inversion count
        totalInvCount = leftInvCount + rightInvCount + mergedInvCount

        return (totalInvCount, mergedSortedSeq)


def main():
    seq = [2, 4, 1, 3, 5]
    print 'seq: ', seq
    (inversionCount, sortedSeq) = sortListAndCountInv(seq)
    print "sorted seq: ", sortedSeq
    print 'inversion count: ', inversionCount 

 
if __name__ == '__main__':
    main()
