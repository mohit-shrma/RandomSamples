""" find the largest sum possible of contiguous subarray within the array
we can use kadane's algorithm to solve it in linear time
"""
import sys

""" returns the maximum sum possible of contiguous subarray in the given
sequence """
def getMaxSumContigSubArr(seq):

    #store the maximum sum of subarray possible in current sequence
    maxSum  = 0

    #store the maximum sum till current ind
    maxTillCurrInd = 0

    for num in seq:
        maxTillCurrInd += num

        if maxTillCurrInd < 0:
            #using current index elem makes sum < 0
            maxTillCurrInd = 0

        if maxSum < maxTillCurrInd:
            #save the maximum contiguous sum found till now
            maxSum = maxTillCurrInd

    return maxSum


def main():
    #input sequence
    seq = [-2, -3, 4, -1, -2, 1, 5, -3]

    print 'seq: ', seq
    print 'max sum contiguous subarr: ', getMaxSumContigSubArr(seq)
    
    
if __name__ == '__main__':
    main()


