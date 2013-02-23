import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;



/*
 * given a row of n coins i.e. coins[0...n-1], two players tkae alternating turn
 * to select either first or last coin from the row. Determine the max amount 
 * that can be won if you move first 
 */

class OptGameStrategy {
    
    //store the value of coins in row
    private int[] coins;
    
    //value[i][j] stores the max value we can definitely win if it's our turn
    //& only coins[i ... j] remains 
    private int[][] value;
    
    public OptGameStrategy(int[] coins) {
        //initialize coins
        this.coins = coins;
        
        //initialize value to be won if coins i to j remains
        value = new int[coins.length][coins.length];
        for (int i = 0; i < coins.length; i++) {
            for (int j =0; j < coins.length; j++) {
                value[i][j] = -1; //flag to indicate value not set yet
            }
        }
    }
    
    
    //get the value to be won if coin[i ... j] remains
    private int getValue(int i, int j) {
        
        if (value[i][j] != -1) {
            return value[i][j];
        }
        
        if (i == j) {
            //only one coin remains, we pick the only remaining coin
            value[i][j] = coins[i];
            return value[i][j];
        }

        if (j == i+1) {
            //only two coins remains, we pick the coin with maximum value
            value[i][j] = max(coins[i], coins[j]);
            return value[i][j];
        }
        
        //min value we can guarantee, if we pick coin[i]
        //opponent will have option to pick either i+1 or jth coin, we can guarantee
        //atleast minimum of two scenarios in our next turn
        int minValIfPicki = coins[i] 
                            + min(getValue(i+1, j-1), //if opponent in next turn pick coin[j]
                                  getValue(i+2,j)); //if opponent in next turn pick coin[i+1]
        

        //min value we can guarantee, if we pick coin[j]
        //opponent will have option to pick either i or j-1th coin, we can guarantee
        //atleast minimum of two scenarios in our next turn
        int minValIfPickj = coins[j] 
                + min(getValue(i+1, j-1), //if opponent in next turn pick coin[i]
                      getValue(i, j-2)); //if opponent in next turn pick coin[j-1]
        
        //of the above moves we will prefer the one which gives max value
        value[i][j] = max(minValIfPicki, minValIfPickj);

        return value[i][j];
    }
    

    //get the max of two values
    private int min(int a, int b) {
        if (a < b) {
            return a;
        } else {
            return b;
        }
    }

    
    //get the max of two values
    private int max(int a, int b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
    
    
    //return the max value that can be won all the given coins lying in a row
    public int getMaxValuePossible() {
        return getValue(0, coins.length-1);
    }
    
    
    public static void main(String[] args) {
    
      //parse commandline to get input arrays
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int[] arr; 
        try {
            int numElem = -1;
            String line = null;
            
            //input elements in array 1
            System.out.println("Enter no. of coins in row (even): ");
            line = br.readLine();
            numElem = Integer.parseInt(line);
            arr = new int[numElem];
            System.out.println("Enter " + numElem +" coin values line by line: ");
            for (int i = 0; i < numElem; i++) {
                arr[i] = Integer.parseInt(br.readLine());
            }
            
            OptGameStrategy optGameStrategy = new OptGameStrategy(arr);
            int maxValuePossible = optGameStrategy.getMaxValuePossible();
            System.out.println("max value possible to be won if taking first move: " 
                                + maxValuePossible);
            
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
    
}