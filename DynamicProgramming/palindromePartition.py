""" given a string determine fewest cuts in string such that 
all resulting substrings are palindrome
if string already palindrome -> 0 cuts
if all diff char in string -> len(String) - 1 cuts
 """

def getFewestCutCount(string):

    if isPalind(string):
        #string already palindrome no cut needed
        return 0

    if len(string) == 1:
        #string is of one character length, palind in itself
        #no cut needed
        return 0

    #initialize minimum cut count for passed string
    minCutCount = len(string)

    for i in range(len(string)-1):
        #i E [0, n-1] where n -> len(string)

        #left partition count from string[0:i+1] or (0...i)
        leftPartCutCount = getFewestCutCount(string[0:i+1])

        #right partition count from string[i+1:len(string)] or (i+1...n-1)
        rightPartCutCount = getFewestCutCount(string[i+1:len(string)])

        #get total cut count for current partition
        partCutCount = leftPartCutCount + 1 + rightPartCutCount

        if partCutCount < minCutCount:
            #if current partition required fewest cuts till now
            minCutCount = partCutCount

    return minCutCount


""" determine whether passed string is palindrome or not """
def isPalind(string):
    lenStr = len(string)
    start = 0
    end = lenStr - 1
    while (start < end):
        if string[start] != string[end]:
            #found a point where char dont match symmetrically
            return False
        start += 1
        end -= 1
    return True

def main():
    string = 'ababbbabbababa' #this should be done in 3 cuts
    print "usin DP top down sol  redundant computation "
    print getFewestCutCount(string)
    #TODO: optimize above by building table using bottom up approach in O(n^2)
    
if __name__ == '__main__':
    main()

