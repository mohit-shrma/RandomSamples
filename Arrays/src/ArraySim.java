

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
    
    
}