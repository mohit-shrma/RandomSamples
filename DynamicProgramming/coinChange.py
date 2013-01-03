""" find number of all possible denominations of given amount of 
given coins"""

import sys

"""
denomination of given coins and amount can be decomposed into
denomination using all but last coin + denomination using atleast one last coin
count(coins, amount) = count(coins - last Coin, amount)
                           + count(coins, amount - last Coin) """
def countDenominationsTopDown(coins, amount):

    if amount == 0:
        #if there is no amount then nothing is also a way
        #to make denominations
        return 1

    if amount < 0:
        #if amount is -ve no solution
        return 0

    if len(coins) <= 0 and amount > 0:
        #no coins, no solution
        return 0

    #denomination using all but last coin
    denomAllButLast = countDenominationsTopDown(coins[0:len(coins)-1], amount)

    #denomination using atleast one last coin
    denomAtleastOneLast = countDenominationsTopDown(coins, amount - coins[-1])
    
    return denomAllButLast + denomAtleastOneLast



""" above involves lot of redundant subproplems solution this can be further
optimized by storing subproblem's solutions in a table """
def countDenominationsBottomUp(coins, amount):
    #denomination table of coins,
    #denomTable[i, j] = denomTable[i - coin[j], j] + denomTable[i][j-1]
    # = count of denominations including coin[j] and value i 
    #    + count of denominations excluding coin[j] and value i
    denomTable = []
    #initialize table: [0 -> amount] * coins
    denomTable = [[0] * len(coins) for i in  range(amount+1) ]

    #initialize row for value 0
    for i in range(len(coins)):
        denomTable[0][i] = 1

    #complete table in bottom up order
    for i in range(1, len(denomTable)):
        #for each value from 1 to amount
        for j in range(len(coins)):
            #for each possible coin

            #number of solution including coin j
            inclCurrCoin = 0
            if (i - coins[j]) >= 0:
                inclCurrCoin = denomTable[i - coins[j]][j]
            
            #number of solution excluding coin j
            exclCurrCoin = 0
            if j > 0:
                exclCurrCoin = denomTable[i][j - 1]

            denomTable[i][j] = inclCurrCoin + exclCurrCoin
    
    #return possible denominations using all coins and given amount
    return denomTable[amount][len(coins) - 1]
            


def main():
    amount = 5
    coins = [1,2,3,4,5, 6]

    #amount = 10
    #coins = [2, 5, 3, 6]

    print 'amount: ', amount
    print 'coins: ', coins
    print 'top down recursive denomination count: ',\
        countDenominationsTopDown(coins, amount)
    print 'bottom up denomination count: ',\
        countDenominationsBottomUp(coins, amount)

    
if __name__ == '__main__':
    main()
