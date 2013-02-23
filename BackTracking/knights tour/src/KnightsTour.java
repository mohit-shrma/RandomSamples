import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;



class KnightsTour {
    
    //dimension of the board
    private int dim;
    
    //board[i][j] indicate the hope no. of cell [i][j] in path
    private int board[][];
    
    //stor the valid moves, knight take move in 'L' shape where it move one step in one dir
    //then move two steps perpendicular to previous move, xMove and yMove will store
    //8 such possible moves, xMove[i] & yMove[i] where i E [0,7]
    private final int[] xMove = {2, 1,  2,   1, -2, -1, -2, -1};
    private final int[] yMove = {1, 2, -1,  -2,  1,  2, -1, -2};
    
    //start (x,y) position on board
    private int startX;
    private int startY;
    
    public KnightsTour(int dim, int startX, int startY) {
        //get the dimension of chess board NxN
        this.dim = dim;
        //get the coordinates of start positions
        this.startX = startX;
        this.startY = startY;
        //initialize the board
        this.board = new int[this.dim][this.dim];
        for (int i = 0; i < this.dim; i++) {
            for (int j = 0; j < this.dim; j++) {
                board[i][j] = -1; //flag to indicate not visited
            }
        }
    }
    
    public void printBoard() {
        for (int i = 0; i < dim; i++) {
            for (int j = 0; j < dim; j++) {
                System.out.print(board[i][j] + " ");
            }
            System.out.println();
        }
    }
    
    //check if move to (x, y) on board is safe
    private boolean isMoveSafe(int x, int y) {
        if (x >= 0 && x < dim && y >= 0 && y < dim && board[x][y] == -1) {
            return true;
        } else {
            return false;
        }
    }
    
    /*
     * Check if knight tour is solved at current state (x,y) also given is the
     * move number taken to reach the state. If not solved then move recursively
     * to solve and back track if solution not possible
     */
    private boolean isKnightTourSolved(int x, int y, int numMove) {
        //store next move from current state if not solved
        int nextX, nextY;
        
        if (numMove == dim*dim) {
            //total no. of moves is equal to size of board, hence visited each
            //cell once till now and knight tour is completed
            return true;
        }
        
        //try all possible moves from current state
        for (int i = 0; i < xMove.length; i++) {
            nextX = x + xMove[i];
            nextY = y + yMove[i];
            if (isMoveSafe(nextX, nextY)) {
                //mark the cell with the move number
                board[nextX][nextY] = numMove; 
                if (isKnightTourSolved(nextX, nextY, numMove + 1)) {
                    //knight tour is solved with the move
                    return true;
                } else {
                    //backtrack and unmark the move taken
                    board[nextX][nextY] = -1;
                }
            }
        }
        
        return false;
    }
    
    public boolean solveKnightsTour() {
      
        //try to solve the knoght tour with passed starting position
        board[startX][startY] = 0;
        return isKnightTourSolved(startX, startY, 1);
    }
    
    public static void main(String[] args) {
        
        //parse commandline to get input arrays
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        try {
            int dim = -1;
            int startX, startY;
            String line = null;
            //get the dimension of chess board
            System.out.println("Enter dimension of chess board: ");
            line = br.readLine();
            dim = Integer.parseInt(line);
            
            //get the start x pos on board
            System.out.println("Enter start x pos on board: ");
            line = br.readLine();
            startX = Integer.parseInt(line);
            
            //get the start y pos on board
            System.out.println("Enter start y pos on board: ");
            line = br.readLine();
            startY = Integer.parseInt(line);
            
            KnightsTour knightsTour = new KnightsTour(dim, startX, startY);
            if (knightsTour.solveKnightsTour()) {
                System.out.println("knight tour found");
                knightsTour.printBoard();
            } else {
                System.out.println("knight tour was not found on the board");
            }
            
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
        
    }
}