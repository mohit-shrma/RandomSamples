/*
 * find longest increasing sequence between two sequences
 */
class LCS {

    enum BackFlags {
        UP, LEFT, DIAG;
    }

    private int[][] editDist;
    private int[][] cost;
    private BackFlags[][] backPointer;
    private String str1;
    private String str2;
    
    

    public LCS(String str1, String str2) {
        this.str1 = str1;
        this.str2 = str2;
        cost = new int[str1.length()+1] [str2.length()+1];
        backPointer = new BackFlags[str1.length()] [str2.length()];
        editDist = new int[str1.length()+1] [str2.length()+1];
    }

    private void printLCS(int i, int j) {
        
        if ( i == -1 || j == -1) {
            return;
        }

        if (backPointer[i][j] == BackFlags.DIAG) {
            printLCS(i-1, j-1);
            System.out.print(str1.charAt(i));
        } else if (backPointer[i][j] == BackFlags.UP) {
            printLCS(i-1, j);
        } else {
            printLCS(i, j-1);
        }
        
    }

    public void dispLCS() {
        printLCS(str1.length()-1, str2.length()-1);
    }

    private int max(int a, int b, int c) {
        if ( a > b ) {
            if ( a > c ) {
                return a;
            } else {
                return c;
            }
        } else {
            if ( b > c) {
                return b;
            } else {
                return c;
            }
        }
    }
    
    public void doLCS() {

        int i, j;

        for (i = 0; i < str1.length()+1; i++) {
            cost[i][0] = 0;
        }
        
        for (i = 0; i < str2.length()+1; i++) {
            cost[0][i] = 0;
        }

        int tempCostinEq = -1;
        
        for (i = 1; i <= str1.length(); i++) {
            for (j = 1; j <= str2.length(); j++) {

                if (str1.charAt(i-1) == str2.charAt(j-1)) {
                    tempCostinEq = cost[i-1][j-1] + 1;
                } else {
                    tempCostinEq = -1;
                }

                cost[i][j] = max(cost[i-1][j], cost[i][j-1], tempCostinEq);
                
                if (cost[i][j] == cost[i-1][j]) {
                    backPointer[i-1][j-1] = BackFlags.UP;
                } else if (cost[i][j] == cost[i][j-1]) {
                    backPointer[i-1][j-1] = BackFlags.LEFT;
                } else {
                    backPointer[i-1][j-1] = BackFlags.DIAG;
                }
                
            }
        }
    }
    
    private int min(int a, int b, int c) {
        if ( a < b) {
            if ( a < c) {
                return a;
            } else {
                return c;
            }
        }else {
            if ( c < b ) {
                return c;
            } else {
                return b;
            }
        }
    }

    public void computeEditDistance() {
        int i, j;

        for (i = 0; i < str1.length()+1; i++) {
            editDist[i][0] = i;
        }

        for (i = 0; i < str2.length()+1; i++) {
            editDist[0][i] = i;
        }

        int tempMin = 99;
        
        for (i = 1; i < str1.length()+1; i++) {
            for (j = 1; j < str2.length()+1; j++) {

                if (str1.charAt(i-1) == str2.charAt(j-1)) {
                    tempMin = editDist[i-1][j-1];
                } else {
                    tempMin = 99;
                }
                
                editDist[i][j] = min(editDist[i-1][j]+1,
                                     editDist[i][j-1]+1,
                                     tempMin);
            }
        }
        
    }

    public int getEditDistance() {
        computeEditDistance();
        return editDist[str1.length()][str2.length()];
    }
    
    public static void main(String[] args) {

        String str1 = "TGCATA";
        String str2 = "TTAGCA";
        LCS myLCS = new LCS(str1, str2);
        
        //find the LCS
        myLCS.doLCS();
        
        //display the longest common subsequence
        myLCS.dispLCS();
        
        //print the length of common subsequence
        System.out.println();
        System.out.println(myLCS.getEditDistance());
    }
    
}