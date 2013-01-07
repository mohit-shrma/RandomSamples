""" given n eggs k floors, including a critical floor if eggs are dropped from
higher floors then eggs will break
find that critical floor in minimum number of drops for worst case scenario
http://www.datagenetics.com/blog/july22012/index.html
"""
""" recursively try dropping egg from every floor 1->k & calulate min no of
droppings in worst case to get floor which gives minimum number of droppings.
for each floor there are two cases:
    I. egg break -> check lower floors       | find drops in this scenario
    II. egg dont break -> check upper floors | find drops in this scenario
    worst case for this floor will be given by the case giving the max/greater
    number of drops
choose the floor which gives min. of worst case drops
"""

""" returns the minimum number of worst case egg drops for the given
number of floors and number of eggs"""
def eggDropCount(numFloors, numEggs):

    if (numFloors == 1) or (numFloors == 0):
        #in case of 1 floor drop requiresd will be 1
        #when no floors then no drop required
        return numFloors

    if (numEggs == 1):
        #if only one egg remains then you have to go linearly from bottom
        #to top floors
        return numFloors

    #store the minimum worst case droppings found for these number of floors
    minFloorDropping = 1000 #some large num
    
    #for every floor drop the egg and choose the one which gives the minimum
    #worst case droppings
    for i in range(1,numFloors+1):

        #num of Drops if egg break from current floor i
        numDropIfBreak = eggDropCount(i-1, numEggs - 1)

        #num of Drops if egg don't break from current floor i
        numDropIfDontBreak = eggDropCount(numFloors - i, numEggs)

        #find the worst case dropping count for current floor
        worstDropCount = max(numDropIfBreak, numDropIfDontBreak)

        if worstDropCount < minFloorDropping:
            #worst case dropping count for current floor is smaller than
            #minimum worst case dropping found till now
            minFloorDropping = worstDropCount
            
    #add 1 to min Floor dropping fir current floor dropping
    minFloorDropping = 1 + minFloorDropping

    
    #print 'numFloors: ', numFloors, ' minFloorDropping: ', minFloorDropping
    
    return  minFloorDropping




def main():
    numFloors = 11
    numEggs = 3

    print 'numFloors: ', numFloors
    print 'numEggs: ', numEggs
    print 'min drops required: ', eggDropCount(numFloors, numEggs)

    #TODO: quite slow use bottom approach to build table and
    #remove solving same subproblem again n again otherwise its too slow
    
if __name__ == '__main__':
    main()
