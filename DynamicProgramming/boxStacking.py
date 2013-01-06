"""given n rectangular boxes, using theze boxes create stack as tall as possible
base area of lower box in stack is larger than base area of box above
can use multiple instances of same box and can rotate box
follows similar approach as longest common increasing sequence
"""
import sys

class BoxConsts:

    HEIGHT_IND = 0
    WIDTH_IND = 1
    DEPTH_IND = 2


""" generate all possible rotations of passed box """
def getBoxRotations((h, w, d)):
    return [(h, w, d), (w, h, d), (d, h, w)]


""" sort boxes in increasing order of base area and return the sorted list  """
def sortBoxesByBaseArea(boxes):
    #sort boxes [(height, width, depth)],
    #base area = width*depth = box[BoxConsts.WIDTH_IND]*box[BoxConsts.DEPTH_IND]
    sortedBoxes = sorted(boxes,\
                             key = lambda box:\
                             box[BoxConsts.WIDTH_IND]*box[BoxConsts.DEPTH_IND])
    return sortedBoxes


""" return height of tallest stack formed by passed boxes
    H(j) : tallest stack of boxes with box j on top
    H(j) = {max ( i < j ) { H(i) }}  + height of jth box
         = height of jth box if no such i found
    subStackHeights - ith location in array store height of tallest stack
                      with box i on top
    prev - stores the backpointer to previous box in tallest stack
"""
def getNaiveRecursiveHeightStack(boxes, subStackHeights, prev):
    #get number of boxes
    numBoxes = len(boxes)

    if numBoxes == 1:
        #an individual box is tall in itself, return its height
        #i.e. box[Boxconsts.HEIGHT_IND]
        return boxes[0][BoxConsts.HEIGHT_IND]

    #last box of boxes
    lastBox = boxes[numBoxes - 1]
    
    #height of tallest stack with last box on top from current boxes
    heightStackLastOnTop = lastBox[BoxConsts.HEIGHT_IND]

    #initialize the value of default previous pointer
    prev[numBoxes - 1] = numBoxes - 1
    
    #recursively get all tallest stack heights
    #from boxes[0] to boxes[numBoxes - 2] : i
    #if boxes[i] has strictly lower dimension than last box and
    #if tallest stack height at boxes[i] + last Box's height >
    #tallest stack height found till now(heightStackLastOnTop) then update
    #heightStackLastOnTop
    for i in range(numBoxes-1):
        #compute tallest stack in boxes[0:i+1]
        heightTallestSubStack = getNaiveRecursiveHeightStack(boxes[0:i+1],\
                                                              subStackHeights,\
                                                              prev)
        if (lastBox[BoxConsts.WIDTH_IND] > boxes[i][BoxConsts.WIDTH_IND]) and\
                (lastBox[BoxConsts.DEPTH_IND] > boxes[i][BoxConsts.DEPTH_IND])\
                and (heightTallestSubStack + lastBox[BoxConsts.HEIGHT_IND] >\
                         heightStackLastOnTop) :
            #update tallest stack height for given boxes
            heightStackLastOnTop = heightTallestSubStack \
                + lastBox[BoxConsts.HEIGHT_IND]

            #update previous pointer
            prev[numBoxes - 1] = i

    #store the tallest height found with last box on top
    subStackHeights[numBoxes - 1] = heightStackLastOnTop

    return heightStackLastOnTop
    

""" apply dynamic programming to compute the height of tallest stack that
can be formed by boxes"""
def naiveDPTallestStack(boxes):
        
    numBoxes = len(boxes)

    #initialize previous pointer list
    prev = [-1 for i in range(numBoxes)]

    #subStackHeights stores the LIS length ending at say index i
    subStackHeights = [1 for i in range(numBoxes)]

    #get the length of LIS ending at sequence's last element and
    #update previous pointer list and subStackHeights
    tallestStackHt = getNaiveRecursiveHeightStack(boxes, subStackHeights, prev)
    
    #get the index with max subseq length
    maxLen = 1
    maxInd = 0
    for i in range(numBoxes):
        if maxLen < subStackHeights[i]:
            maxLen = subStackHeights[i]
            maxInd = i

    #store the longest increasing subsequence using previous pointers
    lisRev = []
    ind = maxInd
    while(ind >= 0):
        lisRev.append(boxes[ind])
        prevInd = prev[ind]
        if prevInd == ind:
            lisRev.append(boxes[prevInd])
            break
        else:
            ind = prevInd
    
    lis = [lisRev[i]  for i in range(len(lisRev)-1, -1, -1)] 
            
    return (lis, tallestStackHt)


    

def main():

    #input dimensions of various boxes [(h, w, d)]
    #height, width, depth of boxes, base is width*depth
    boxes = [(4, 6, 7), (1, 2, 3), (4, 5, 6), (10, 12, 32)]

    #generate all 3 rotations of each box from given boxes
    rotatedBoxes = []
    for box in boxes:
        rotatedBoxes += getBoxRotations(box)

    #sort boxes in increasing order of base area
    sortedBoxes = sortBoxesByBaseArea(rotatedBoxes)
    
    #get the tallest stack of boxes
    (tallestStack, tallestStackHt) = naiveDPTallestStack(sortedBoxes)

    print 'boxes: ', boxes
    print 'rotated and sorted boxes: ', sortedBoxes
    print 'tallest stack: ', tallestStack
    print 'tallest Stack Ht: ', tallestStackHt


    
if __name__ == '__main__':
    main()

