package com.Suffix.SuffixArray;

import java.lang.Math;

public class SuffixArrayConstructor {
	
	private String text;
	private int[] sortedSuffixIndices;
	
	
	public SuffixArrayConstructor(String text) {
		this.text = text;
		//initialize sortedSuffixIndices
		sortedSuffixIndices = new int[this.text.length()];
		for (int i = 0; i < this.text.length(); i++) {
			sortedSuffixIndices[i] = i;
		}
	}

	
	//return the suffix starting at particular index
	private String getSuffix(int beginInd) {
		return text.substring(beginInd);
	}
	
	
	/* 
	 * sort the sortedSuffixIndices list based on suffix in text
	 * lo and hi are indices 
	 */
	private void randQSort(int lo, int hi) {
		
		if (lo < hi) {
			int partLoc = randomizedPartition(lo, hi);
			randQSort(lo, partLoc - 1);
			randQSort(partLoc + 1, hi);
		}
	}
	
	
	/*
	 * partition the array around a pivot element choosen at random
	 * lo and hi are indices in sortedSuffixindices
	 */
	private int partition(int lo, int hi) {
		
		//generate random indice in array as pivot
		//int pivotIndice = lo + (int)(Math.random() * ((hi - lo) + 1));
		int pivot = sortedSuffixIndices[hi];
		String pivotSuffix = getSuffix(pivot);
		
		int partLoc = lo - 1;
		int swapTemp = -1;
		for (int j = lo; j < hi; j++) {
			if (getSuffix(sortedSuffixIndices[j]).compareTo(pivotSuffix) <= 0) {
				
				//suffix is lexicographically less than or equal to pivot suffix
				partLoc += 1;
			
				//exchange sortedSuffixIndices[j] with sortedSuffixIndices[partLoc]
				swapTemp = sortedSuffixIndices[j];
				sortedSuffixIndices[j] = sortedSuffixIndices[partLoc];
				sortedSuffixIndices[partLoc] = swapTemp;
			}
		}
		
		//exchange sortedSuffixIndices[partLoc+1] with pivot / sortedSuffixIndices[hi] 
		swapTemp = sortedSuffixIndices[hi];
		sortedSuffixIndices[hi] = sortedSuffixIndices[partLoc+1];
		sortedSuffixIndices[partLoc+1] = swapTemp;
		
		return partLoc+1;
	}
	
	
	private int randomizedPartition(int lo, int hi) {
		int randIndex = lo + (int)(Math.random() * ((hi - lo) + 1));
		//exchange sortedSuffixIndices[randIndex] with sortedSuffixIndices[hi] 
		int swapTemp = sortedSuffixIndices[hi];
		sortedSuffixIndices[hi] = sortedSuffixIndices[randIndex];
		sortedSuffixIndices[randIndex] = swapTemp;
		return partition(lo, hi);
	}
	
	
	public int[] getSuffixArray() {
		return sortedSuffixIndices;
	}
	
	
	public void generateSuffixArray() {
		randQSort(0, sortedSuffixIndices.length-1);
	}
	
}


