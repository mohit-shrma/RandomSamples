import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;



class MedianSortedArr {
    
    /*
     * returns the median of a sorted array
     */
    public float getMedian(int[] a) {
        int len = a.length;
        if (len%2 == 0) {
            return (a[len/2] + a [len/2 - 1])/2;
        } else {
            return a[len/2];
        }
        
    }
    
    
    /*
     * returns median of two sorted array of equal length
     */
    public float getMedianEqLenSortedArrs(int[] arrA, int[] arrB) {
        
       //check for invalid input 
       if (arrA.length != arrB.length || arrA.length <= 0) {
           return -1;
       }
        
       if (arrA.length == 1) {
           //both array have only one element, 
           //then median is average of two elem
           return (arrA[0] + arrB[0]) / 2;
       }
       
       if (arrA.length == 2 && arrB.length == 2) {
           //both arrays have two elem, in total four elem
           //out of the four median will be given by middle two elements of 
           //combined array
           float mid1 = Math.max(arrA[0], arrB[0]);
           float mid2 = Math.min(arrA[1], arrB[1]);
           return (mid1 + mid2) / 2;
       }
       
       //get median of first array A
       float med1 = getMedian(arrA);
       

       //get median of first array B
       float med2 = getMedian(arrB);

       int[] arrASub = {};
       int[] arrBSub = {};
       if (med1 < med2) {
           //median of first array is lesser than median of second array
           //discard first array's first half as it is definitely less than 
           //half of total combined elements
           //discard second array's second half as it is definitely greater than 
           //half of total combined elements
           //recursively determine median in left over array
           if (arrA.length %2 == 0) {
               //arrays are of even size
               arrASub = Arrays.copyOfRange(arrA, arrA.length/2 - 1, 
                                                        arrA.length);
               arrBSub = Arrays.copyOfRange(arrB, 0, 
                                                        arrB.length/2 + 1);
           } else {
               //arrays are of odd size
               arrASub = Arrays.copyOfRange(arrA, arrA.length/2, 
                                                        arrA.length);
               arrBSub = Arrays.copyOfRange(arrB, 0, 
                                                        arrB.length/2 + 1);
           }
           
           return getMedianEqLenSortedArrs(arrASub, arrBSub);
       } else {
           //median of first array is greater than median of second array
           //discard first array's second half as it is definitely greater than 
           //half of total combined elements
           //discard second array's first half as it is definitely lesser than 
           //half of total combined elements
           //recursively determine median in left over array
           if (arrA.length %2 == 0) {
               //arrays are of even size
               arrBSub = Arrays.copyOfRange(arrB, arrB.length/2 - 1, 
                                                        arrB.length);
               arrASub = Arrays.copyOfRange(arrA, 0, 
                                                        arrA.length/2 + 1);
           } else {
               //arrays are of odd size
               arrBSub = Arrays.copyOfRange(arrB, arrB.length/2, 
                                                        arrB.length);
               arrASub = Arrays.copyOfRange(arrA, 0, 
                                                        arrA.length/2 + 1);
           }
           
           return getMedianEqLenSortedArrs(arrASub, arrBSub);
       }
       
    }
    
    
    
    /*
     * get median of two sorted array works on unequal length 
     * O(lgn) complexity
     */
    public float getMedianSortedArrs(int arrA[], int arrB[], int left, int right) {
        
      
        //combined size of arrays
        int n = arrA.length + arrB.length;
        
        if (left > right) {
            //crossed boundary of one array, look into other array
            //return getMedian(arrB, arrA, 0, arrB.length-1);
            //optimal call with max/min
            return getMedianSortedArrs(arrB, arrA, Math.max(0, n/2 - arrA.length -1), 
                                         Math.min(arrB.length-1, n/2 - 1));
        }
        
        //index to search as median from arrA
        int i = (left + right)/2;
        
        //if A[i] is median then its exactly gr8r than j elements of B 
        //given as follow
        int j = n/2 - i - 1;
        
        if (j >= 0 && arrA[i] < arrB[j]) {
            //A[i] is not exactly greater than j elements, we need to look in
            //right half of A i.e. A[i+1...right]
            return getMedianSortedArrs(arrA, arrB, i+1, right);
        } else if (j < arrB.length-1 && arrA[i] > arrB[j+1]) {
            //A[i] is greater than j+1 elements not exactly greater than j elem
            //need to look in left half of A
            return getMedianSortedArrs(arrA, arrB, left, i-1);
        } else {
            //A[i] is exactly greater than j elements i.e.
            // B[j] < A[i] <= B[j+1]
            
            if (n%2 == 0) {
                //length of combined array is even
                //median is given by average of A[i] and 
                //element that comes before A[i]
                if (i > 0) {
                    if (arrA[i-1] > arrB[j]) {
                        //A[i-1] comes before A[i] in sorted array
                        return ((float)(arrA[i-1] + arrA[i]))/2;
                    } else {
                        //B[j] comes before A[i] in sorted array
                        return ((float)(arrA[i] + arrB[j]))/2;
                    }
                } else {
                    //B[j] comes before A[i] in sorted array
                    return ((float)(arrA[i] + arrB[j]))/2;
                }
                
            } else {
                //length of combined array is odd
                //median is exactly given by A[i]
                return arrA[i];
            }
        }
        
    }
    
    
    
    
    public static void main(String[] args) {
        
        MedianSortedArr medSort = new MedianSortedArr();
        
        //open up standard input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        try {
            //get array values from user
            System.out.println("Enter size of first sorted array:");
            String line = br.readLine();
            int size = Integer.parseInt(line);
            
            //declare the array to be input from user
            int[] arrA = new int[size];
            
            System.out.println("Enter array elements line by line: ");
            for (int i = 0; i < size; i++) {
                arrA[i] = Integer.parseInt(br.readLine());
            }
            
            //get array values from user
            System.out.println("Enter size of second sorted array:");
            line = br.readLine();
            size = Integer.parseInt(line);
            
            //declare the array to be input from user
            int[] arrB = new int[size];
            
            System.out.println("Enter array elements line by line: ");
            for (int i = 0; i < size; i++) {
                arrB[i] = Integer.parseInt(br.readLine());
            }
            
            System.out.println("First array values are as follow: ");
            for (int val: arrA) {
                System.out.print(val + " ");
            }
            
            System.out.println();
            
            System.out.println("Second array values are as follow: ");
            for (int val: arrB) {
                System.out.print(val + " ");
            }
            
            
            System.out.println();
            
            if (arrA.length < arrB.length) {
            
                System.out.println("Median is given as: " 
                        + medSort.getMedianSortedArrs(arrA, arrB, 0, arrA.length-1));
            } else {
                System.out.println("Median is given as: " 
                        + medSort.getMedianSortedArrs(arrA, arrB, 0, arrA.length-1));
                System.out.println("Median is given as for eq len arr: " 
                        + medSort.getMedianEqLenSortedArrs(arrA, arrB));
            }
            
            
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
       
        
    }
}