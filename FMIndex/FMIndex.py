import sys

""" implement FMIndex using bwt, 
reference: http://en.wikipedia.org/wiki/FM-index
           http://www.alexbowe.com/fm-indexes-and-backwards-search-32172 """


#returns burrow wheeler transform of text
def findBWT(text):
    modText = text + '$'
    #produce circular rotations of modText
    rotText = []
    for i in range(len(modText)):
        rotText.append(modText[i:]+modText[0:i])
    rotText.sort()

    #get all chars in last columns
    bwt = ''.join([ rot[-1]  for rot in rotText  ])

    #get all chars in first column
    fCol = ''.join([ rot[0]  for rot in rotText  ])
    
    return fCol, bwt, rotText


#compute C[c] table, or each character c in the alphabet,
#contains the number of occurrences of lexically smaller characters in the text.
def computeCTable(text):
    #find the alphabets in text
    alpha = list(set(text))
    alpha.sort()
    charCount = {}
    for ch in text:
        if ch not in charCount:
            charCount[ch] = 1
        else:
            charCount[ch] += 1
    cTable = {}
    prevCount = 0
    for ch in alpha:
        cTable[ch] = prevCount
        prevCount += charCount[ch]
    return cTable



#function Occ(c, k) is the number of occurrences of character c 
#in the prefix L[1..k] or bwt[1:k]
#this can be done in const time by storing values in table
def Occ(c, k, bwt):
    count = 0
    for i in range(k):
        if bwt[i] == c:
            count += 1
    return count



#return the position of char in fCol for given position in lastCol/bwt string 
#here assuming one based index
#position returned is also one based index
def getLastColToFirstColMapping(lColInd, bwt, cTable):
    return cTable[bwt[lColInd-1]] + Occ(bwt[lColInd-1], lColInd, bwt)



#return the range in first col and count of occurence
def searchPattern(pattern, fCol, cTable, bwt):
    #initialize start, end
    #note one based indexing
    start = 1
    end = len(fCol)
    #start from last character of pattern
    for ch in pattern[::-1]:
        start = cTable[ch] + Occ( ch, start-1, bwt) + 1
        end = cTable[ch] + Occ(ch, end, bwt)
    return (start, end, end - start + 1)
    
    
    

def main():
    text = 'abracadabra'
    fCol, bwt, rotText = findBWT(text)
    cTable =  computeCTable(text+'$')
    print 'fCol: ', fCol
    print 'bwt: ',  bwt
    for rot in rotText:
        print rot
    #print Occ('a', 9, bwt)
    #print getLastColToFirstColMapping(9, bwt, cTable)
    start, end, count = searchPattern('bra', fCol, cTable, bwt)
    print 'start: ', start, 'end: ', end, 'count: ', count


    
if __name__ == '__main__':
    main()
