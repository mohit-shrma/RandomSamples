#get consecutive elements from unsorted array in o(n)
def getMaxConsecSeq(arr):
    #create a set of all elem
    elemSet = set(arr)

    maxLen = 0
    max = -1
    min = -1
    for num in arr:

        #look for elem > temp  in set and remove
        temp = num
        while temp in elemSet:
            elemSet.remove(temp)
            temp += 1
        tempMax = temp - 1
        
        #look for elem < temp in set and remove
        temp = num - 1
        while temp in elemSet:
            elemSet.remove(temp)
            temp -= 1
        tempMin = temp + 1
        
        if maxLen < tempMax - tempMin + 1:
            maxLen = tempMax - tempMin + 1
            max = tempMax
            min = tempMin
    return (maxLen, range(min, max+1))


def main():
    #arr = [100, 4, 200, 1, 3, 2]
    arr = [100, 4, 200, 1, 201, 3, 199, 202, 2, 198]
    print getMaxConsecSeq(arr)

if __name__ == '__main__':
    main()
