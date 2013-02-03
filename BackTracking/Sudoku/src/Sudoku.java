/*
 * will solve the given sudoku by back tracking
 * here each row, col and subgrid of 3x3 must have all digits from 1 - 9
 */


class Sudoku {
    
    private int[][] grid;
    private int numRows;
    private int numCols;
    
    public Sudoku(int[][] grid) {
        this.grid = grid;
        this.numRows = grid.length;
        this.numCols = grid[0].length;
    }
    
    /*
     * returns the index of any unassigned cell
     */
    private int[] getUnassignedCell() {
        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j < numCols; j++) {
                if (grid[i][j] == 0) {
                    int[] rowColUnassigned = {i, j};
                    return rowColUnassigned;
                } 
            }
        }
        
        return null;
    }
    
    
    /*
     * returns true if it is safe to assign num to passed row col 
     */
    private boolean isSafe(int row, int col, int num) {
        
        //check if num is used in same row
        for (int j = 0; j < numCols; j++) {
            if (grid[row][j] == num && j != col) {
                return false;
            }
        }
        
        //check if num is used in same col
        for (int i = 0; i < numRows; i++) {
            if (grid[i][col] == num && i != row) {
                return false;
            }
        }
        
        //check if num is used in the sub grid surrounding (row, col)
        int subGridStartRow = row - (row % 3);
        int subGridStartCol = col - (col % 3);
        int subGridEndRow = subGridStartRow + (3-1);
        int subGridEndCol = subGridStartCol + (3-1);
        for (int i = subGridStartRow; i <= subGridEndRow; i++) {
            for (int j = subGridStartCol; j <= subGridEndCol; j++) {
                if (grid[i][j] == num) {
                    return false;
                }
            }
        }
        
        
        return true;
    }
    
    
    public boolean solveSudoku() {
        
        int[] unAssignedRowCol = getUnassignedCell();
        
        if (unAssignedRowCol == null) {
            //no unassigned grid left, sudoku is solved
            return true;
        }
        
        int unAssignedRow = unAssignedRowCol[0];
        int unAssignedCol = unAssignedRowCol[1];
        
        for (int num = 1; num <= 9; num++) {
            if (isSafe(unAssignedRow, unAssignedCol, num)) {
                //try the num as solution for the unassigned cell
                grid[unAssignedRow][unAssignedCol] = num;
                
                if (solveSudoku()) {
                    //try to solve sudoku with new assignment
                    return true;
                } else {
                    //backtrack
                    //make the coordinate unassigned, try it with the next num
                    //in next iteration
                    grid[unAssignedRow][unAssignedCol] = 0;
                }
            }
        }
        
        //backtrack
        return false;
    }
    
    public void printGrid() {
        //display the grid
        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j < numCols; j++) {
                System.out.print(grid[i][j] + " ");
            }
            System.out.println();
        }
    }
    
    public static void main(String[] args) {
     
        //sudoku grid input, 9 x 9, 0 indicates unassigned cell
        int[][] grid = {{3, 0, 6, 5, 0, 8, 4, 0, 0},
                        {5, 2, 0, 0, 0, 0, 0, 0, 0},
                        {0, 8, 7, 0, 0, 0, 0, 3, 1},
                        {0, 0, 3, 0, 1, 0, 0, 8, 0},
                        {9, 0, 0, 8, 6, 3, 0, 0, 5},//{8, 0, 0, 7, 6, 3, 0, 0, 9}, 
                        {0, 5, 0, 0, 9, 0, 6, 0, 0},
                        {1, 3, 0, 0, 0, 0, 2, 5, 0},
                        {0, 0, 0, 0, 0, 0, 0, 7, 4},
                        {0, 0, 5, 2, 0, 6, 3, 0, 0}};
        
        Sudoku sudoku = new Sudoku(grid);
        
        //display the grid
        sudoku.printGrid();
        
        //solve the sudoku grid
        boolean sudokuSolved = sudoku.solveSudoku();
        if (sudokuSolved) {
            System.out.println("Hurrah! solution exists!!");
            sudoku.printGrid();
        } else {
            System.out.println("Passed sudoku grid can't be solved");
        }
        
    }
    
}