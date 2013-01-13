import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Vector;



class OptLongIncSeq {
    
    
    /*
     * binary search for index i such that element passed is smaller than element
     * at that place i.e. elem <= arr[endISElem[i]]
     */
    public int binSearch(int elem, int lo, int hi, int[] arr, int[] endISElem) {
        
       int mid = -1;
        
        while (hi > lo + 1) {
            //while we have more than two elements
            mid = lo + (hi - lo)/2;
            
            if (arr[endISElem[mid]] >= elem) {
                hi = mid;
            } else {
                lo = mid;
            }
        }
        
        return hi;
    }
    
    
    
    /*
     * find the longest increasing subsequence in passed integer array
     * O(nlgn) complexity
     */
    public void findLongestIncSubSeq(int[] arr) {
        
        //array to store the end elements indexes of 
        //longest increasing subsequences of various sizes
        //we will maintain that end element of smaller list is smaller than 
        //end element of larger list
        int endISElem[] = new int[arr.length];
        //initialize end elements
        for (int i = 0; i < endISElem.length; i++) {
            endISElem[i] = 0;
        }
        
        //array to store previous pointers of subsequences
        int prev[] = new int[arr.length];
        for (int i = 0; i < prev.length; i++) {
            prev[i] = -1;
        }
        
        //number of increasing sequence found till now, 
        //endISElem[len] will always be emty
        //length of longest subsequence found,
        int len = 1;
        
        //temporary variable to use
        int pos = -1;
        
        //traverse the array and update the length of longest increasing
        //subsequences found so far
        for (int i = 1; i < arr.length; i++) {
          
            if (arr[i] < arr[endISElem[0]]) {
                //if current element is the smallest found till now
                //replace the end index of smallest subseq
                endISElem[0] = i;
            } else if (arr[i] > arr[endISElem[len-1]]) {
                //if current element is largest of all found till now
                //duplicate the largest seq and append curr element to it
                //current element extends previous largest subseq ending at 
                //arr[endISElem[len -1]]
                
                //store the previous of current element as index of 
                //previous end element in largest subseq
                prev[i] = endISElem[len -1];
                
                //add new element to end elements of subseq list
                endISElem[len++] = i;
            } else {
                //search for an end element in increasing sequences found till now
                //greater than current element, current element will extend
                //an existing increasing subsequence
                
                //get position in enISElem
                pos = binSearch(arr[i], 0, len-1, arr, endISElem);
                
                //previous of current element will be the one at pos - 1
                //which was extended to give old sequence which will be updated
                //now
                prev[i] = endISElem[pos - 1];

                endISElem[pos] = i;
            }
            
        }
        
        //print longest increasing subsequence
        System.out.println("LIS is as follow: ");
        Vector<Integer> lisVec = new Vector<Integer>();
        for(int i = endISElem[len-1]; i >= 0; i = prev[i]) {
            lisVec.add(0, arr[i]);
        }
        for (int num: lisVec) {
            System.out.print(num + " ");
        }
        
    }
    
    
    
    public static void main(String[] args) {
        
        OptLongIncSeq lis = new OptLongIncSeq();
        
        //open up standard input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        try  {
            //get array values from user
            System.out.println("Enter Size of array: ");
            String line = br.readLine();
            int size = Integer.parseInt(line);
            
            //declare the array to be input from user
            int[] numArr = new int[size];
            
            System.out.println("Enter array elements line by line: ");
            for (int i = 0; i < size; i++) {
                numArr[i] = Integer.parseInt(br.readLine());
            }
            
            System.out.println("Array values are as follow: ");
            for (int i = 0; i < size; i++) {
                System.out.print(numArr[i] + " ");
            }
            System.out.println();
            
            lis.findLongestIncSubSeq(numArr);
            
        } catch (IOException e) {
            System.out.println("IO error: " + e.getMessage());
        }
        
    }
    
}