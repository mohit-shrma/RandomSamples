import java.util.Random;

/*
 * contains an array class containing an array and some methods to work on the 
 * array
 */


class ArraySim {
    
    //an integer array
    private int[] arr;
    
    
    public ArraySim(int[] a) {
        arr = a;
    }
    
    
    public void setArray(int[] a) {
        arr = a;
    }
    
    /*
     * swap a[i] and a[j]
     */
    public void swap(int[] a, int i, int j) {
        int temp = a[i];
        a[i] = a[j];
        a[j] = temp;
    }
    
    /*
     * partition the array such that pivot is at its correct pos
     * return the new pivot position
     */
    public int partition(int[] a, int pivotInd, int start, int end) {
        
        //get the pivot element
        int pivotElem = a[pivotInd];
        
        //swap the pivot element with start
        swap(a, start, pivotInd);
        pivotInd = start;
        
        //index of element where partition happens 
        //s.t. a[i < partIndx] <= pivotElem,
        //a[i >= partIndx] > pivotElem
        //in following loop partIndx points to first element gr8r than pivot
        int partIndx = start + 1;
        
        for (int i = start + 1; i <= end; i++) {
            if (a[i] <= pivotElem) {
                //swap this element with a[partIndx]
                swap(a, partIndx, i);
                partIndx++;
            }
        }
        
        if (partIndx > start + 1) {
            //swap pivot element with element at partition index
            a[pivotInd] = a[partIndx - 1];
            a[partIndx - 1] = pivotElem;
        }
        
        return partIndx - 1;
    }
    
    //quick sort the array
    public int[] quickSort(int[] a, int start, int end) {
        
        
        //choose the pivot, say first index
        int pivotInd = start;
        
        //partition the array such that pivot is at its correct pos
        int partIndx = partition(a, pivotInd, start, end); 
        
        //recursively sort the subarray left of partIndx
        int leftStart = start;
        int leftEnd = partIndx - 1;
        if (leftEnd - leftStart > 0) {
            //left subarray size is > 1
            quickSort(a, leftStart, leftEnd);
        }
        
        //recursively sort the subarray right of partIndx
        int rightStart = partIndx + 1;
        int rightEnd = end;
        if (rightEnd - rightStart > 0) {
            //left subarray size is > 1
            quickSort(a, rightStart, rightEnd);
        }
        
        return a;
    }
    
    /*
     * merge sort the passed array
     */
    public int[] mergeSort(int[] a, int start, int end) {
        
        if (start == end) {
            //array of size one
            return a;
        }
        
        int mid = (start + end) / 2;
        
        //boundary of left subarray
        int leftStart = start;
        int leftEnd =  mid;
        
        //boundary of right subarray
        int rightStart = mid + 1;
        int rightEnd = end;
        
        //merge sort left subarray
        mergeSort(a, leftStart, leftEnd);
        
        //merge sort right subarray
        mergeSort(a, rightStart, rightEnd);
        
        //linear merging of left and right subarray
        
        //temporary space to store the sorted array
        int[] temp = new int[end - start + 1];
        //pointer to temp unfilled space
        int tempPointer = 0;
        //pointer to smallest elemnt in left subarray
        int leftPointer = leftStart;
        //pointer to smallest element in right subarray
        int rightPointer = rightStart;
        
        while (leftPointer <= leftEnd && rightPointer <= rightEnd) {
            if (a[leftPointer] < a[rightPointer]) {
                temp[tempPointer++] = a[leftPointer++];
            } else {
                temp[tempPointer++] = a[rightPointer++];
            }
        }
        
        while(leftPointer <= leftEnd) {
            //right array exhausted, left array remains
            temp[tempPointer++] = a[leftPointer++];
        }
        
        while(rightPointer <= rightEnd) {
            //left array exhausted right array remains
            temp[tempPointer++] = a[rightPointer++];
        }
        
        //write the merged sorted values back into array
        tempPointer = start;
        for (int elem: temp) {
            a[start++] = elem;
        }
        
        return a;
    }
    
    //sort the array
    public void sort() {
        //sort the array using quicksort
        int[] sortedArr = quickSort(arr, 0, arr.length - 1);
        
        //sort the array using merge sort
        //int[] sortedArr = mergeSort(arr, 0, arr.length - 1);
    }
    
    
    //display the elements of array
    public void displayArr() {
        for(int elem: arr) {
            System.out.print(elem + " ");
        }
        System.out.println();
    }
    
    
    /*
     * perform binary search to find the max element ind <= curr key
     * this return index
     */
    public int binSearchMaxElem(int[] a, int key, int low, int high) {
        
        if (high < low)  {
            //not found
            return -1;
        }
        
        int mid = (low + high) /2;       
        if (a[mid] == key) {
            return mid;
        } else if (a[mid] > key) {
            if (mid == 0) {
                return a[mid];
            }
            
            if (key > a[mid-1]) {
                return mid - 1;
            }
            return binSearchMaxElem(a, key, low, mid - 1);
        } else {
            if (mid == arr.length -1) {
                return mid;
            }
            if (key < a[mid+1]) {
                return mid;
            }
            return binSearchMaxElem(a, key, mid + 1, high);
        }
    }
    
    
    public int binSearchMaxElem(int key) {
        return binSearchMaxElem(arr, key, 0, arr.length-1);
    }
    
    
    /*
     * perform binary search for passed key on the passed array
     */
    public int binarySearch(int[] a, int key, int low, int high) {
        
        if (high < low)
            //not found 
            return -1;
        
        int mid = (low + high) /2;       
        if (a[mid] == key) {
            return mid;
        } else if (a[mid] > key) {
            return binarySearch(a, key, low, mid - 1);
        } else {
            return binarySearch(a, key, mid + 1, high);
        }
        
    }
    
    public int binarySearch(int key) {
        return binarySearch(arr, key, 0, arr.length-1);
    }
    
    /*
     * find no. of all possible triangles in unsorted arr 
     * S.T. a + b > c, b + c > a, a + c > b
     */
    public int findAllTriangles() {
        
        //sort the array 
        sort();
        int numTriag = 0;
        int sum = 0;
        int searchInd = -1;
        for (int i = 0; i < arr.length; i++) {
            for (int j = i+1; j < arr.length; j++) {
                sum = arr[i] + arr[j];
                searchInd = binSearchMaxElem(sum);
                if (searchInd == -1) {
                    System.out.println("Error cant found the num < " 
                                        + arr[searchInd]);
                } else if (searchInd > j) {
                    //found ind such that arr[i] + arr[j] < arr[searchInd + 1] 
                    //arr[i] + arr[j] > arr[j+1 ... searchInd]
                    //num of triangs
                    numTriag += searchInd - j;
                }
            }
        }
        
        return numTriag;
    }
    
    /*
     * shuffles the array 
     */
    public void shuffle() {
        Random generator = new Random();
        int randInd = -1;
        for (int i = arr.length -1; i > 0; i--) {
            //swap i with any random ind before
            randInd = generator.nextInt(i);
            swap(arr, i, randInd);
        }
    }
    
    
    //find max of two int
    int max(int a, int b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
    
    
    //find min of two numbers
    int min(int a, int b) {
        if (a < b) {
            return a;
        } else {
            return b;
        }
    }
    
    
    //find median of two num
    float median(int a, int b) {
        return ((float)(a+b))/2;
    }
    
    
    
    //find median of three num
    int median(int a, int b, int c) {
        int maxNum = max(a, max(b, c));
        int minNum = min(a, min(b, c));
        return (a + b + c -minNum - maxNum);
    }
    
    
    
    //find median of four num
    float median(int a, int b, int c, int d) {
        int maxNum = max(a, max(b, max(c, d)));
        int minNum = min(a, min(b, max(c, d)));
        return ((float)(a + b + c + d - minNum - maxNum))/2;
    }
    
    
    
    //get median of two sorted arrays
    //first one is the smaller array of the two
    float getMedianSortedArr(int[] a, int aStart, int aEnd,
                             int[] b, int bStart, int bEnd) {
        int aLen = aEnd - aStart + 1;
        int bLen = bEnd - bStart + 1;
        
        if (aLen == 1) {
            //smaller array is of unit length
            
            if (bLen == 1) {
                //larger array of unit length
                return median(a[aStart], b[bStart]);
            }
            
            if (bLen % 2 != 0) {
                //larger array has odd elements
                //median will be given by three elem in mid of larger array 
                //and element in smaller array
                return median(b[bLen/2], median(a[aStart], b[bLen/2 - 1], b[bLen/2 + 1]));
            } else {
                //larger array has even elements
                //median is given by two mid elem of larger array
                //and element in smaller array
                return median(a[aStart], b[bLen/2 - 1], b[bLen/2]);
            }
        } else if (aLen == 2) {
            //smaller array is having two elements
            
            if (bLen == 2) {
                //larger array has two elements
                return median(a[aStart], a[aStart+1],
                              b[bStart], b[bStart+1]);
            }
            
            if (bLen %2 != 0) {
                //larger array has odd elements
                //median will be given by median of three elements
                //B[M/2], max(A[0], B[M/2 - 1]), min(A[1], B[M/2 + 1])
                return median(b[bLen/2], max(a[aStart], b[bLen/2 - 1]),
                              min(a[aStart+1], b[bLen/2 + 1]));
                
            } else {
                //larger array has even elements
                //median will be given by median of four elements
                // B[M/2], B[M/2 - 1], max( A[0], B[M/2 - 2] ), min( A[1], B[M/2 + 1] )
                return median(b[bLen/2], b[bLen/2 - 1], max(a[aStart], 
                              b[bLen/2 - 2]), min(a[aStart+1], b[bLen/2 + 1]));
            }
            
        }
        
        int midA = aStart + (aLen - 1) / 2;
        int midB = bStart + (bLen - 1) / 2;
        
        if (a[midA] <= b[midB]) {
            //median lies in a[midA,...] and b[...midB]
            return getMedianSortedArr(a, midA, aEnd, b, bStart, midB);
        } else {
            //median lies in a[...,midA] and b[midB,...]
            return getMedianSortedArr(a, aStart, midA, b, midB, bEnd);
        }
        
    }
    
    
    
    
    /*
     * median of two array
     */
    public float getMedian(int[] a, int[] b) {
        
        //sort the two arrays
        a = quickSort(a, 0, a.length - 1);
        b = quickSort(b, 0, b.length - 1);
        
        //task is to find the median of these two sorted arrays
        float median = getMedianSortedArr(a, 0, a.length - 1, 
                                          b, 0, b.length - 1);
        return median;
    }
    
    
    
    /*
     * find max sum subarray
     * kadane's algo
     */
    public int maxSumSubArr() {
        int maxSumTillHere = 0;
        int maxSumTillNow = 0;
        for (int elem: arr) {
            maxSumTillNow += elem;
            if (maxSumTillHere < 0) {
                maxSumTillHere = 0; 
            }
            if (maxSumTillHere > maxSumTillNow) {
                maxSumTillNow = maxSumTillHere; 
            }
        }
        return maxSumTillNow;
    }
    
    
    
    /*
     * find max product subarray
     */
    public int maxProdSubArr() {
        
        int maxProdTillHere = 1;
        int minProdTillHere = 1;
        int maxTillNow = 1;
        int maxProdTillHereNew = 1;
        int minProdTillHereNew = 1;
        for (int elem: arr) {
            maxProdTillHereNew = max(max(elem*maxProdTillHere, 
                                    max(elem*minProdTillHere, elem)), 1);
            minProdTillHereNew = min(elem*maxProdTillHere, min(elem*minProdTillHere, elem));
            maxProdTillHere = maxProdTillHereNew;
            minProdTillHere = minProdTillHereNew;
            if (elem == 0) {
                minProdTillHere = 1;
            }
            if (maxTillNow < maxProdTillHere) {
                maxTillNow = maxProdTillHere;
            }
        }
        
        return maxTillNow;
    }
    
    
    /*
     * check if given array can be partitioned into two subsets of equal sum
     */
    public boolean isEqualSubsetPossible() {
        
        int sum = 0;
        
        for (int elem: arr) {
            sum += elem;
        }
        
        if (sum % 2 != 0) {
            //odd sum can't be divided into two equal parts
            return false;
        } else {
            //even check if can be divided into two equal subset sum
            return isSubsetSum(arr, arr.length, sum/2);
        }
        
    }
    
    
    /*
     *check if a[0...last] can have subset with sum as 'sum'
     */
    public boolean isSubsetSum(int[] a, int size, int sum) {
        
        if (sum == 0) {
            return true;
        } 
        
        if (size == 0 && sum != 0) {
            return false;
        }
        
        //if last element greater than sum then just check recursively with 
        //other elements before last
        if (a[size-1] > sum) {
            return isSubsetSum(a, size - 1, sum);
        }
        
        /*sum can be obtained in following ways
         * 1) by including last element
         * 2) by excluding last element
         */
        return isSubsetSum(a, size-1, sum - a[size-1]) 
                || isSubsetSum(a, size-1, sum);
        
    }
    
    /*
     * find subarray with given sum, array not necessarily sorted
     */
    public boolean isSubarraySum(int sum) {
        
        int start = 0;
        int currSubarrSum = 0;
        int i = 0;
        while (i < arr.length) {
            currSubarrSum += arr[i];
            if (currSubarrSum == sum) {
                //we have got the desired sum from start to ith ndex
                System.out.println("desired subarray sum: " + sum + " start: " 
                                    + start + " end: " + i);
                return true;
            } else if (currSubarrSum > sum) {
                while (currSubarrSum > sum) {
                    currSubarrSum -= arr[start++];
                }
            }
            
            i++;
        }
        
        return false;
    }
    
    
    /*
     * find minimum jumps to reach end of array where you can jump as many steps
     * as value at current index
     */
    public int minJumps() {
        
        //jumps contain minimum jump required from corresponding index to 
        //reach end
        int[] jumps = new int[arr.length];
        //initialize jumps to 786, indicates no jump possible
        for (int i = 0; i < jumps.length; i++) {
           jumps[i] = 786;
        }
        //jump require from last position is 0
        jumps[jumps.length - 1] = 0;
        
        //temperary var to store minimum jump require in third case
        int min = 786;
        
        for (int i = arr.length-2; i >= 0; i--) {
            
            if (arr[i] == 0) {
              //arr[i] == 0 then cant jump to end anyway
                continue;
            } else if (arr[i] >= arr.length - i -1) {
                //can jump to last elem directly from here
                jumps[i] = 1;
            } else {
                //cant jump to end directly from here, search for best index 
                //afterwards that is reachable from here to jump to end
                min = 786;
                for (int j = i+1; j <= i + arr[i] && j < arr.length; j++) {
                    if (min > jumps[j]) {
                        min = jumps[j];
                    }
                }
                
                if (min < 786) {
                    jumps[i] = min + 1;
                }
                
            }
        }
        
        System.out.println("jumps: ");
        for (int jump: jumps) {
            System.out.print(jump + " ");
        }
        
        //return jump required from first index to reach end
        return jumps[0];
    }
    
}