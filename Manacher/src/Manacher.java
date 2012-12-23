/*
 * Apply manacher algorithm to find longest substring palindrome in linear time,
 * reference http://www.leetcode.com/2011/11/longest-palindromic-substring-part-ii.html
 */


class Manacher {
	
	
	//add '#' before and after each character in string
	public String preProcess(String str) {
		
		int lenStr = str.length();
		String processedStr = "";
		for (int i = 0; i < lenStr; i++) {
			processedStr += "#" + str.charAt(i);
		}
		processedStr += "#";
		return processedStr;
	}
	
	
	//delete '#' before and after each character in string
		public String postProcess(String str) {
			
			int lenStr = str.length();
			String processedStr = "";
			for (int i = 0; i < lenStr; i++) {
				if (str.charAt(i) != '#') { 
					processedStr += str.charAt(i);
				}
			}
			return processedStr;
		}
	
	
	public String findLongestPalindrome(String ipStr) {
		
		int i = 0;
		
		//pre-process ip string 
		String processedStr = preProcess(ipStr);
		
		//pre-process ip string length
		int processedStrLen = processedStr.length();
		
		//store length of each palindrome substr at each index in string
		int[] palLen = new int[processedStrLen];
		
		//palindrome can't be present at first and last ind of string
		palLen[0] = palLen[processedStrLen - 1] = 0;
		
		//current center index for palindrome
		int center = 0;
		
		//right edge of current palindrome, centered at 'center'
		int right = 0;
		
		//mirrored index (i') by symmetry on the left of center C
		int iMirror = -1;
		
		//get palindrome length of each substring at each index
		for (i = 0; i < processedStrLen; i++) {
			
			//get the mirrored index (i') by symmetry on the left of center C,
			//this i' corresponds to i on the right of center
			iMirror = center - (i - center);
			
			if (right > i) {
				//right edge lies beyond curr index
				if (right - i < palLen[iMirror]) {
					/*remaining str smaller than palindrome length at mirrored 
					 *index, it's atleast equal to remaining str but need to 
					 *expand beyond right for correct len
					 */
					palLen[i] = right - i;
				} else {
					/*remaining str greater than palind length at mirrored indx
					 *palind length is exactly equal to length at mirrored index
					 */
					palLen[i] = palLen[iMirror];
				}
				
			} else {
				//right is not on right of current index, like at initial pos
				//palindrome length at current index is 0
				palLen[i] = 0;
			}
			
			
			//try to expand palindrome centered at i
			//TODO: check if expansion helps in case of nested else above
			int leftExt = -1;
			int rightExt = -1;
			while ( (leftExt = i + palLen[i] + 1) >= 0 && leftExt < processedStrLen 
					&& (rightExt = (i - palLen[i] - 1)) >= 0 && rightExt < processedStrLen
					&& processedStr.charAt(leftExt) == processedStr.charAt(rightExt)) {
				palLen[i]++;
			}
			
			
			//update center if palindrome centered at i extend beyond 'right' 
			//edge, then update center to current i and right to palindrome edge 
			//on the right to current palindrome
			if (i + palLen[i] > right) {
				center = i;
				right = i + palLen[i];
			}
			
		}
		
		//find the maximum length palindrome sub-string 
		int maxInd = 0;
		for (i = 0; i < processedStrLen; i++) {
			if (palLen[i] > palLen[maxInd]) {
				maxInd = i;
			}
		}
		
		//print the palindrome substring
		int maxPalLen = palLen[maxInd];
		
		//get the palindrome substring
		String longPalindStr = processedStr.substring(maxInd - maxPalLen,
														maxInd + maxPalLen);
		//post-process palindrome string, removing '#'
		longPalindStr = postProcess(longPalindStr);
		
		return longPalindStr;
		
		
	}
	
	
	public static void main(String[] args) {
	
		//input string
		String ipString = args[0];
		
		Manacher manacher = new Manacher();
		
		//apply manacher algo to find longest palindrome substring
		String longPalinStr = manacher.findLongestPalindrome(ipString);
		
		System.out.println(ipString);
		System.out.println(longPalinStr);
		
	}
	
	
}