import sys
import math

""" find maximum subarray of passed contiguous array using divide & conquer,
 nlog(n) complexity, reference cormen"""


""" find maximum subarray of passed subarray arr,
 and of range in between lo & hi indices"""
def findMaxSubArr(arr, lo, hi):
    if lo == hi:
        #only one element (base case)
        return (lo, hi, arr[lo])
    else:
        mid = int(math.floor((lo + hi) / 2))

        #find max sub array in left of mid element
        (leftLow, leftHigh, leftSum) = findMaxSubArr(arr, lo, mid)
        
        #find max sub array in right of mid element
        (rightLow, rightHigh, rightSum) = findMaxSubArr(arr, mid + 1, hi)

        #find max subarray which crosses mid element
        (crossLow, crossHigh, crossSum) = findMaxCrossSubArr(arr, lo, mid, hi)

        #return the largest of above computed three subarrays sums
        if leftSum >= rightSum and leftSum >= crossSum:
            return (leftLow, leftHigh, leftSum)
        elif rightSum >= leftSum and rightSum >= crossSum:
            return (rightLow, rightHigh, rightSum)
        else:
            return (crossLow, crossHigh, crossSum)
        
        

""" find maximum subarray which crosses mid element of the array,
 lo mid hi are indices"""

def findMaxCrossSubArr(arr, lo, mid, hi):

    #initialize it to -ve infinity or minimum int value possible
    leftSum = -sys.maxint - 1
    rightSum = -sys.maxint - 1
    maxLeft = -1
    maxRight = -1

    tempSum = 0

    for i in range(mid, lo-1, -1):
        tempSum += arr[i]
        if leftSum < tempSum:
            leftSum = tempSum
            maxLeft = i

    tempSum = 0

    for i in range(mid+1, hi+1):
        tempSum += arr[i]
        if rightSum < tempSum:
            rightSum = tempSum
            maxRight = i

    return (maxLeft, maxRight, leftSum+rightSum)


""" linear time algorithm to compute maximmum contiguous subarray sum """
def kadanesMaxSubArr(arr):
    maxSoFar = maxEndingHere = 0
    for num in arr:
        maxEndingHere = max(0, maxEndingHere + num)
        maxSoFar = max(maxEndingHere, maxSoFar)
    return maxSoFar


""" return the maximum subarray sum in case of circular array"""
def maxSubCircularSubArr(arr):

    #get max subarray sum in non wrapping case
    nonWrapMaxSum = kadanesMaxSubArr(arr)

    #get max subarray sum in case of circular arrays
    #get the sum of array and inver the sign of number in array
    sum = 0
    for i in range(len(arr)):
        sum += arr[i]
        arr[i] = -arr[i]

    #get max sum subarray in inverted array
    nonWrapInvMaxSum = kadanesMaxSubArr(arr)

    #subtract with total sum to get sum of max subarray in wrapped
    #case of original array
    wrapMaxSum = sum + nonWrapInvMaxSum

    #return the maximum of two cases
    return max(nonWrapMaxSum, wrapMaxSum)
    

def main():
    #arr = [-10, 2, 4, -9, 6, 7 , -2, -8]
    #arr = [10, -12, 11, 10, -12, 11]
    arr = [10, -12, 11]
    lo = 0
    hi = len(arr) - 1
    subArrLo, subArrHi, subArrSum = findMaxSubArr(arr, lo, hi)
    print 'array: ', arr
    print 'low, high, arrSum: ', subArrLo, subArrHi, subArrSum
    print 'subArr: ', arr[subArrLo:subArrHi+1]
    print 'kadanes sum of subarr: ', kadanesMaxSubArr(arr)
    print 'max subarray sum in circular arr', maxSubCircularSubArr(arr)
 
if __name__ == '__main__':
    main()
