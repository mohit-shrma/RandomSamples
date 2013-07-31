package main

import (
	"fmt"
	"os"
	"strings"
	"strconv"
)

type CSRMat struct {
	rows []int
	cols []int
	values []float
	nnz int
	numRows int
	numCols int
}


//read csr matrix from file in csr format
func readCSRMat(csrFileName string) CSRMat {
	
	//open input file
	fi, err := os.Open(csrFileName)
	if err != nil {
		fmt.Println("term file don't exists")
		return
	}

	//close fi on exit and check its returned error
	defer func() {
		if err := fi.Close(); err != nil {
			fmt.Println("can't close term file")
		}
	}()


	csrMat := new(CSRMat)
	
	//make read buffer
	ir := bufio.NewReader(fi)
	scanner := bufio.NewScanner(ir)

	//read header to get number of rows, number of cols, nnz
	header := scanner.Text()
	toks := strings.Split(header, " ")
	//TODO: parse int
	csrMat.numRows,_ := strconv.Atoi(toks[0])
	csrMat.numCols := strconv.Atoi(toks[1])
	csrMat.nnz := strconv.Atoi(toks[2])
	
	//TODO:initialize the arrays in csrMAt


	var currLine string
	var currToks []string
	var col int
	var val int
	//read rest of lines in file to get elements of mat
	currRowInd := 0
	for scanner.Scan() {
		//read current line
		currLine = scanner.Text()
		currLine = strings.Trim(currLine, " ")
		//TODO
		currLine = strings.Trim(currLine, "\n")
		//read columns and values from the line
		currToks = strings.Split(currLine, " ")
		for i:=0; i < len(currToks); i+=2 {
			col = strconv.Atoi(currToks[i])
			val = strconv.Atoi(currToks[i+1])
			//TODO: save the col val into CSR matrix
			
		}
	}
	


}


func main() {

	
}