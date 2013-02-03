import sys
#try to permute in place
""" e.g. 'abc' combine 'a' with al perms of 'bc' , then swap(2,1) combine 'b' with all perms of 'ac' 
then swap(3,1) 'c' with all perms of 'ab', follow this recursively
"""

#permutes list containing char  
#permute part starting from i index till n-1 index (including)
def permutations(strList, i, n):
    if i == n-1:
        #if reached the nth char
        #print the list or string
        print ''.join(strList)
    else:
        #from ith indice to n-th indice, swap char with first indice(i)
        for j in range(i, n):
            #swap 'j' with 'i'
            strList[j], strList[i] = strList[i], strList[j]
            #now permute from i+1 to n part
            permutations(strList, i+1,n )
            #swap back to get original string
            strList[j], strList[i] = strList[i], strList[j]


def main():
    if len(sys.argv) >= 2:
        word = sys.argv[1]
    else:
        word = 'cat'
    permutations(list(word), 0 , len(word))

if __name__ == '__main__':
    main()
