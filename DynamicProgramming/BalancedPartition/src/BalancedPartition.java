import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.Math;

class BalancedPartition {
    
    private int[] arr;
    
    /*
     * subsetSum[i,j] = 1 if sum of arr[0...i-1] = j
     *                = 0 otherwise
     */
    private int[][] subsetSum;
    private int sum;
    
    public BalancedPartition(int[] arr) {
        this.arr = arr;
        this.sum = 0;
        //assuming array is having +ve integers
        for ( int elem: arr) {
            this.sum += elem;
        }
        subsetSum = new int[arr.length][this.sum + 1];
        //initialize with flag to indicate not computed
        for (int i = 0; i < arr.length; i++) {
            for (int j = 0; j < this.sum + 1; j++ ) {
                subsetSum[i][j] = -99;
            }
        }
    }
    
    
    /*fill the table subset sum, where 
    subsetSum[i,j] = 1 if sum of arr[0...i-1] = j
                   = 0 otherwise
    */
    private void computeSubsetSum() {
        //ofcourse this is 1, recursively calling to fill other elements
        //of table
        for (int j = 0; j < this.sum + 1; j++) {
            subsetSum[arr.length - 1][j] = isSubsetSum(arr.length -1, 
                                                       this.sum);
        }
    }
    
    
    /*
     * 
     */
    private int max(int a, int b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
    
    
    /*
     * return 1 if subsetSum[i,j] = 1
     * which happens if subsetSum[i-1, j] = 1 i.e w/o using arr[i]
     * or if subsetSum[i-1, j - arr[i]] = 1 i.e. with using arr[i]
     * if element range from 1...k, then j vary from 0...nk & i from 0...n-1
     * complexity to fill this table is o(n*n*k)
     */
    private int isSubsetSum(int i, int j) {
        
        if (subsetSum[i][j] != -99) {
            return subsetSum[i][j];
        }
        
        if (j == 0 && i > 0) {
            //we have some elemnts left but previous elements exactly made the 
            //sum, no need to recurse with i
            subsetSum[i][j] = 1;
            return 1;
        }
        
        if (i == 0) {
            //we have only the first element
            if (arr[i] == j) {
                subsetSum[i][j] = 1;
                return 1;
            } else {
                subsetSum[i][j] = 0;
                return 0;
            }
        }
        
        //is subset sum 'j' present including arr[i]
        int isSubsetSumIncl = isSubsetSum(i-1, j-arr[i]);
        
        //is subset sum 'j' present excluding arr[i]
        int isSubSetSumExcl  = isSubsetSum(i-1, j);
        
        subsetSum[i][j] = max(isSubsetSumIncl, isSubSetSumExcl);
        
        return subsetSum[i][j];
    }
    
    
    
    /*
     * we want to partition array into two subset S1, S2 
     * s.t. we reach min|sum(S1) - sum(S2)|, ideal sol is reach when sum(s1) = sum(s2)
     * also we know that sum(s1) + sum(s2) = sum(arr[0...n-1]) for above ideal sol
     * sum(s1) = sum(s2) = sum(arr[0...n-1])/2, we want either sum to reach this
     * value to meet min|sum(s1) - sum(s2)| 
     * search for j s.t. subsetSum[n-1][j] is 1 and 
     * j is closest to sum(arr[0...n-1])/2
     * in that case partition can happen s.t. sum(s1) = j and 
     * sum(s2) = sum(arr[0...n-1]) - j  
     */
    private int[] getSubSetSums() {
        int[] subsetSums = new int[2];
        int halfSum = sum/2;
        int numElem = arr.length - 1;
        
        //store the minimum diff and index giving the min diff
        int minDiff = sum + 1;
        int minIdx = -1; //sum(s1)
        int diff = 0;
        for (int j = sum; j >= 0; j--) {
            if (subsetSum[arr.length - 1][j] == 1) {
                diff = j - halfSum;
                if (Math.abs(diff) < minDiff) {
                    minIdx = j;
                    minDiff = Math.abs(diff); 
                }
            }
        }
        subsetSums[0] = minIdx;
        subsetSums[1] = sum - subsetSums[0]; //sum(s2)
        return subsetSums;
    }
    
    
    public void doBalancedPartition() {
        computeSubsetSum();
        int[] subsetSums = getSubSetSums();
        System.out.println("first set sum: " + subsetSums[0]);
        System.out.println("second set sum: " + subsetSums[1]);
    }
    
    
    public static void main(String[] args) {
        
        //parse commandline to get input arrays
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int[] arr; 
        try {
            int numElem = -1;
            String line = null;
            
            //input elements in array 1
            System.out.println("Enter no. of elements in array: ");
            line = br.readLine();
            numElem = Integer.parseInt(line);
            arr = new int[numElem];
            System.out.println("Enter " + numElem +" elements line by line: ");
            for (int i = 0; i < numElem; i++) {
                arr[i] = Integer.parseInt(br.readLine());
            }
            
            BalancedPartition balPart = new BalancedPartition(arr);
            balPart.doBalancedPartition();
            
            
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
    }
}