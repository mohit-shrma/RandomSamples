#generate nCk values
#elegant solution same logic as in hi school maths
#fix one place, then vary other places,
#reference http://cs.utsa.edu/~dj/ut/utsa/cs3343/lecture25.html

import sys

def combinations(bigList, start, n, k, kMax):
    #k counter of which element is goin 2 be selected, selected till now k-1
    #print selections if k > kMax i.e required num of elem selected kMax == k-1
    if k > kMax:
        print bigList[1:kMax+1]
        return
    #fix this kth element from start to n
    #and vary other following elements from start + 1 to n
    for i in range(start, n+1):
        #fix kth element
        bigList[k] = i
        #vary other following elements from i+1 to n
        combinations(bigList, i+1, n, k+1, kMax)

def main():
    if len(sys.argv) >= 3:
        n = int(sys.argv[1])
        k = int(sys.argv[2])
    else:
        n = 2
        k = 1
    bigList = [ 0 for i in range(100)]
    combinations(bigList, 1, n, 1, k)

if __name__ == '__main__':
    main()
