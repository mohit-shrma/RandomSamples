""" given input of matrix dimensions chain [p0,p1,p2,...,pn-1, pn]
where A1 = p0Xp1, A2 = p1Xp2, ... An = pn-1Xpn, 
find the optimal parenthesization S.T. multiplication of these matrices
incur minimal cost
reference: cormen
 """

import sys

""" count the number of parenthesizaton possible for multiplying n matrices"""
def countParenthesization(n):
    count = 0
    if n == 1:
        #if only one matrix is there, only one way
        count = 1
    else:
        for k in range(1, n):
            count += countParenthesization(k) * countParenthesization(n-k)
    return count


""" compute the minimal cost of multiplying the sequence of matrices of passed
dimensions [p0,p1,p2,...,pn-1, pn] """
def matrixChainOrder(p):
    #get the number of matrices
    numMatrices = len(p)-1

    #initialize the cost table m,
    #where m[i,j] = min. no. of computations needed to produce Ai...j
    #m[i,j] = min{m[i,k] + m[k+1,j] + pi-1*pk*pj if i<j}
    #       = 0 if i = j
    #we are adding +1 below for m[0,] and m[,0]
    #we will be considering m[1...n, 1...n] only
    #similarly s[i,j] will store the value of k
    m = [None]*(numMatrices + 1)
    s = [None]*(numMatrices + 1)
    for i in range(numMatrices+1):
        m[i] = [None]*(numMatrices + 1)
        s[i] = [None]*(numMatrices + 1)

    #set m[i,i] = 0
    for i in range(numMatrices+1):
        m[i][i] = 0

    #fill the cost in order of increasing chain length
    for chainLen in range(2, numMatrices + 1):
        for i in range(1, numMatrices - chainLen + 2):
            j = i + chainLen - 1
            #initialize m[i][j] to some max cost say infinity
            m[i][j] = 1000000
            for k in range(i, j):
                tempCost = m[i][k] + m[k+1][j] + p[i-1]*p[k]*p[j]
                if tempCost < m[i][j]:
                    m[i][j] = tempCost
                    s[i][j] = k
                    
    #return the cost and split locations
    return (m, s)


""" print the learned optimal parenthesis expression after minimizing cost """
def printOptimalParenthesis(s, i, j):
    if i == j:
        print i
    else:
        print "("
        printOptimalParenthesis(s, i, s[i][j])
        printOptimalParenthesis(s, s[i][j] + 1, j)
        print ")"


""" returns the dimension of matrix from passed chain
i.e [(rows,cols), (rows, cols), ...]"""        
def getMatricesDim(p):
    dim = []
    for i in range(len(p)-1):
        dim.append((p[i], p[i+1]))
    return dim
    
        
        
def main():
    #matrices dimension sequence
    p = [30, 35, 15, 5, 10, 20, 25]
    numMatrices = len(p) - 1
    print "no. of matrices: ", numMatrices
    print "dimensions of matrices: ", getMatricesDim(p)
    print "possible number of parenthesis: ", countParenthesization(numMatrices)
    #get the min cost of matrix multiplications
    (m,s) = matrixChainOrder(p)
    #print optimal cost
    print 'minimal cost: ', m [1] [numMatrices]
    #print the optimal parenthesis
    print 'after optimal parenthesizations: '
    printOptimalParenthesis(s, 1, numMatrices)
    
    
        
if __name__ == '__main__':
    main()

    
        
