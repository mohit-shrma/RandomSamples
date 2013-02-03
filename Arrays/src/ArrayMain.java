import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


class ArrayMain {
    
    public void arrayMethods(int[] keys) {
        ArraySim arrSim = new ArraySim(keys);
        System.out.println("display array: ");
        arrSim.displayArr();
        System.out.println("sort array: ");
        arrSim.sort();
        arrSim.displayArr();
        System.out.println("binary search: " + 10);
        System.out.println(arrSim.binarySearch(10));
        System.out.println("binary search max elem: " + 8);
        int searchInd  = arrSim.binSearchMaxElem(8);
        if (searchInd != -1) {
            System.out.println(keys[searchInd]);
        } else {
            System.out.println("Not found");
        }
        System.out.println("num of triangles: " + arrSim.findAllTriangles());
        arrSim.shuffle();
        arrSim.displayArr();
       
        int[] a = {900};
        int[] b = {1, 3, 5, 8, 9, 2, 6, 7, 6, 8, 9};
        System.out.println("median of two arrays: " + arrSim.getMedian(a, b));
        System.out.println("max sum. of subarray: " + arrSim.maxSumSubArr());    
        System.out.println("max prod. of subarray: " + arrSim.maxProdSubArr());
        System.out.println("is equal subset sum possible: " + arrSim.isEqualSubsetPossible());
        System.out.println("is sub array sum equals 10: " + arrSim.isSubarraySum(10));
        int[] c = {1, 3, 5, 8, 9, 2, 6, 7, 6, 8, 9};
        arrSim.setArray(c);
        arrSim.displayArr();
        System.out.println("minimum jumps require to reach end from start: " + arrSim.minJumps());
    }
    
    
    public static void main(String[] args) {
        ArrayMain arrayMain = new ArrayMain();
        //parse commandline line by line to get keys
        //open up standard input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        try {
            System.out.println("Enter no. of keys for array: ");
            String line = br.readLine();
            int size = Integer.parseInt(line);
            
            //keys array to store key
            int[] keys = new int[size];
            System.out.println("Enter keys line by line: ");
            for (int i = 0; i < size; i++) {
                keys[i] = Integer.parseInt(br.readLine());
            }
            
            arrayMain.arrayMethods(keys);
            
        }catch (IOException e) {
            System.out.println("IO error: " + e.getMessage());
        }
        
    }
}