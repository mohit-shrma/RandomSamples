""" given a string of 0 & 1, find the max len substring wit equal 0 & 1 """


""" replace 0 with -1 and for each i , compute sum from 0 to ith index,
sum[i] = a[0] + a[1] + ..... + a[i]
sum[j] - sum[i-1] = a[i] + a[i+1] + .... + a[j]
above is 0 if a[i]...a[j] have equal 1 and 0, we need to find farthest apart
i and  j such that sum[j] and sum[i-1] is 0. i < j, i >= 0, sum[-1] = 0 
return the substring having maximum length and equal num of 0 and 1 """
def getMaxSubEq0N1(seq):
    newSeq = []
    for elem in seq:
        if elem == 0:
            newSeq.append(-1)
        else:
            newSeq.append(1)
    #sumSeq to store sum from 0 to i
    sumSeq = []
    tempSum = 0
    #dictinory to sore sum:[indces]
    sumIndDict = {0:[-1]}
    for i in range(len(newSeq)):
        tempSum += newSeq[i]
        if tempSum in sumIndDict:
            sumIndDict[tempSum].append(i)
        else:
            sumIndDict[tempSum] = [i]
        sumSeq.append(tempSum)
    
    #for each sum find the difference between left and right indices 
    #and print the substring corresponding to max diff
    mini = []
    maxj = []
    maxDiff = -1
    eqSum = -1
    for tempSum, indices in sumIndDict.iteritems():
        diff = indices[-1] - indices[0]
        if diff > maxDiff:
            mini = []
            maxj = []
            mini.append(indices[0])
            maxj.append(indices[-1])
            eqSum = tempSum
            maxDiff = diff
        elif diff == maxDiff:
            mini.append(indices[0])
            maxj.append(indices[-1])
            
    
    
    #sequence will be from mini +1 to maxj,
    #to include maxj in python need to give maxj+1 as last indices
    result = []
    for i in range(len(mini)):
        result.append(seq[mini[i] + 1: maxj[i] + 1])

    return result


 


def main():
    someSeq = [1, 0, 1, 1, 1, 0, 1, 1,  1, 0]
    print getMaxSubEq0N1(someSeq)
    
if __name__ == '__main__':
    main()
