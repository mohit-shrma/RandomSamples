import sys


def permutations(str):
    allPerms = []
    if len(str) == 1:
        return str
    allPrevPerms = permutations(str[0:-1])
    for prevPerm in allPrevPerms:
        for i in range(len(prevPerm)):
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
