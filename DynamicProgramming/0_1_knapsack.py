""" given n items with integer sizes size[] and values value[] also given is
the capacity of knapsack say C
Fill the knapsack with items of maximum possible value not exceeding its
capacity
"""
import sys



""" get the max possible value by filling knapsack over all possible subsets
of items
M[i,j] = optimal value for filling EXACTLY a capacity j knapsack with same
         subsets of items 1..i
M[i,j] = max{ M[i-1,j] i.e. ith item NOT used, 
              M[i-1,j-size[i]] + value[i] i.e. ith item used
            }
optimal objective value is given by: max <j> {M[n,j]}
O(nc) subproblems, O(nc) space if solution required, O(c) if only value is req
"""
def getMaxPossibleValue(capacity, value, size):

    #number of items
    numItems = len(value) 
    
    if (capacity == 0) or (len(value) == 0):
        #if capacity to be filled is 0
        #or if all items have been used
        return 0

    #get the max possible value if last item not used
    maxValIfLastNotUsed = getMaxPossibleValue(capacity, value[0:numItems-1],\
                                                  size[0:numItems-1])
     
    #max possible value if last item is used
    maxValIfLastUsed = 0
    if capacity >= size[numItems-1]:
        #if capacity is greater than last item, then we can use the last item
        maxValIfLastUsed = getMaxPossibleValue(capacity - size[numItems-1],\
                                                    value[0:numItems-1],\
                                                    size[0:numItems-1])\
                                                    + value[numItems-1]
    
    #print 'numItems: ', numItems, ' capacity: ', capacity
    #print 'maxValIfLastNotUsed: ', maxValIfLastNotUsed,\
    #    ' maxValIfLastUsed: ', maxValIfLastUsed

    #maximum of above two value will give the optimal value
    return max(maxValIfLastNotUsed, maxValIfLastUsed)
        

def main():
    #input values of items
    value = [60, 100, 120]

    #input sizes of items in knapsack
    size = [10, 20, 30]

    #capcity of knapsack
    capacity = 50

    print 'values: ', value
    print 'sizes: ', size
    print 'capacity: ', capacity
    print 'optimal value in knapsack: ', getMaxPossibleValue(capacity, value,\
                                                                 size)

    
    
if __name__ == '__main__':
    main()
