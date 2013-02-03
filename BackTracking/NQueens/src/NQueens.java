import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;



class NQueens {
    
    
    private int numQueens;
    private int[][] board;
    
    
    public NQueens(int numQueens) {
        this.numQueens = numQueens;
        //initialize board where '0' indicates unassigned
        //1 indicates queen is assigned
        this.board = new int[numQueens][numQueens];
        for (int i = 0; i < numQueens; i++) {
            for (int j = 0; j < numQueens; j++) {
                this.board[i][j] = 0;
            }
        }
    }
    
    
    //return true if its safe to keep queen on board[row][col]
    //as we are starting from left side and col - 1 already has queens
    //so we need to check left side col  only
    private boolean isSafe(int row, int col) {
        
        //check if there is any queen on left of col
        for (int j = 0; j < col; j++) {
            if (board[row][j] == 1) {
                return false;
            }
        }
        
        //check if queen along upper diag '\' on left 
        for (int i = row - 1, j= col - 1; j >= 0 && i >= 0; j--, i--) {
            if (board[i][j] == 1) {
                return false;
            }
        }
        
        //check if queen along lower diag '/' on left 
        for (int i = row + 1, j= col - 1; i < numQueens && j >= 0; i++, j--) {
            if (board[i][j] == 1) {
                return false;
            }
        }
        
        return true;
    }
    
    
    //solve the given n-queens problem, starting from specified  col
    //assuming a queen is placed in previous 0...col-1 coumns
    private boolean solve(int col) {
            
        if (col >= numQueens) {
            //all the queens have been place safely
            return true;
        }
        
        for (int i = 0; i < numQueens; i++) {
            //try each row to place queen
            if (isSafe(i, col)) {
                // i, j is safe to place queen
                board[i][col] = 1;
                //now move to next column
                if (solve(col+1)) {
                    //placing queen in this row solved the problem
                    return true;
                } else {
                    //back track prev sol dont work out try other row
                    board[i][col] = 0;
                }
            }
        }
        
        //backtrack, no row safe in this col
        return false;
    }
    
    
    
    /*
     *solve the current nqueen problem 
     */
    public boolean solve() {
        //solve n queens problem starting from first column
        return solve(0);
    }
    
    
    
    /*
     * display the board
     */
    public void displayBoard() {
        for (int i = 0; i < numQueens; i++) {
            for (int j = 0; j < numQueens; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }
    
    

    public static void main(String[] args) {
        
        //parse commandline to get 'N'
        //open up standard input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        try {
            System.out.println("Enter no. of queens (N): ");
            String line = br.readLine();
            int numQueens = Integer.parseInt(line);
            NQueens nQueens = new NQueens(numQueens);
            if (nQueens.solve()) {
                System.out.println("Hurrah! problem is solved");
                nQueens.displayBoard();
            } else {
                System.out.println("problem can not be solved");
            }
        }catch (IOException e) {
            System.out.println("IO error: " + e.getMessage());
        }
        
    }
    
}