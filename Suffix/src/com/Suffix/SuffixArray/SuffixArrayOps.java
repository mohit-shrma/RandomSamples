package com.Suffix.SuffixArray;

public class SuffixArrayOps {
	
	private String text;
	private int[] suffixArray;
	
	
	public SuffixArrayOps(String text, int[] suffixArray) {
		this.text = text;
		this.suffixArray = suffixArray;
	}
	
	
	//return suffix beginning at passed index
	public String getSuffix(int begInd) {
		return text.substring(begInd);
	}
	
	
	//return index if query is found in text, else -1
	public int search(String query) {
		
		int lo = 0;
		int hi = suffixArray.length-1;
		int mid = -1;
		int midCompared = -1;
		String midSuffix = "";
		
		while ( lo <= hi) {
			mid = (lo + hi) / 2;
			midSuffix = getSuffix(suffixArray[mid]);
			midCompared = query.compareTo(midSuffix); 
			if (midCompared > 0)  {
				lo = mid + 1;
			} else if (midCompared < 0) {
				hi = mid - 1;
			} else {
				return suffixArray[mid];
			}
		}
		
		return -1;
	}
	
	
	
}