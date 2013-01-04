""" find the best price obtained after trying all the combination of splitting
 a rod/rope, given the price of each length of rod"""

import sys

""" bestPrice(currLen) =
      max <0<i<currLen> (bestPrice(i) + bestPrice(currLen - i))
      maximum over all i E (0, currLen)
      it contains overlapping subproblems and solve them again n again
"""
def getBestPriceTopDown(lengthRod, pricesPerLen):

    if (lengthRod == 0):
        #if passed length is 0
        return 0

    #market price for curr len
    mktPrice = pricesPerLen[lengthRod-1]

    #get best price after trying all combination of splitting
    bestPriceAfterSplit = -1

    #solve for all possible spit and select the max one
    for i in range(1, lengthRod):
        bestPrice4Leni = getBestPriceTopDown(i, pricesPerLen)
        bestPrice4RemLen = getBestPriceTopDown(lengthRod - i, pricesPerLen)
        bestPrice4CurrSplit = bestPrice4Leni + bestPrice4RemLen
        if (bestPrice4CurrSplit > bestPriceAfterSplit):
            bestPriceAfterSplit = bestPrice4CurrSplit

    #compare with the mkt price of curr len rod
    if mktPrice > bestPriceAfterSplit:
        bestPriceAfterSplit = mktPrice

    return bestPriceAfterSplit
    

#TODO: optimized above by storing subproblems solution in a table. O(n^2)

def main():
    lengthRod = 8

    #array of prices for length of rod, starting with length 1
    pricesPerLen = [3, 5, 8, 9, 10, 17, 17, 20]

    print 'length: ', lengthRod
    print 'bestPrice: ', getBestPriceTopDown(lengthRod, pricesPerLen)
    
if __name__ == '__main__':
    main()
