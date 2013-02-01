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