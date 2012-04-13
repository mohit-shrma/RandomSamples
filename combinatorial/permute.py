import sys


def permutations(str):
    allPerms = []
    #return single character if passed
    if len(str) == 1:
        return str
    #get all possible perms of string one char less
    allPrevPerms = permutations(str[0:-1])
    #append last char in all possible loc in previous permutations 
    for prevPerm in allPrevPerms:
        for i in range(len(prevPerm)):
            #append to the list the possible permutation generated
            allPerms.append(prevPerm[0:i] + str[-1] + prevPerm[i:])
        allPerms.append(prevPerm + str[-1])
    return allPerms

def main():
    if len(sys.argv) >= 2:
        word = sys.argv[1]
    else:
        word = 'cat'
    print permutations(word)

if __name__ == '__main__':
    main()
