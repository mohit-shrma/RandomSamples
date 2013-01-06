""" find length of the longest palindromic subsequence in given sequence,
e.g. "BBABCBCAB" has "BABCBAB" "BBBBB" "BBCBB"
as palindromic subsequences first one being longest """

import sys

""" return length of longest palindromic subsequence  of given sequence
    seq[0..n-1] -> i/p sequence L(0,n-1) denotes LPS of X
    if seq[0]==seq[n-1] then L(0,n-1) = 2 + L(1,n-2)
    else L(0, n-1) = max(L(1, n-1), L(0,n-2))
"""
def lengthOfLPS(seq):
    if len(seq) == 1:
        #single character palindrome
        return 1

    if seq[0] != seq[len(seq)-1]:
        #first and last char are diff
        lengthRightLPS = lengthOfLPS(seq[1:])
        lengthLeftLPS = lengthOfLPS(seq[:len(seq)-1])
        return max(lengthRightLPS, lengthLeftLPS)
    elif len(seq) == 2 and seq[0] == seq[1]:
        #sequence is of just 2 char in length and both same
        return 2
    else:
        #sequence is of more than 2 char, with first and last char matching
        return 2 + lengthOfLPS(seq[1:len(seq)-1])

def main():
    #strSeq = "BBABCBCAB" #BABCBAB is longest
    #strSeq = "GEEKSFORGEEKS" # 7
    strSeq = "DABANGG"
    print 'strSeq: ', strSeq
    print 'length of longest palindromic subsequence: ', lengthOfLPS(strSeq)
    
    
if __name__ == '__main__':
    main()
