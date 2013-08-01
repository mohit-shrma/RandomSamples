package main

import (
	"fmt"
	"os"
	"strings"
	"strconv"
	"bufio"
	"math"
)


type CSRMat struct {
	rows []int
	cols []int
	//TODO: figure out float to string
	values []int
	nnz int
	numRows int
	numCols int
}


//write csr matrix to file in csr format
func writeCSRMat(csrFileName string, csrMat CSRMat) {
	//open output file 
	fo, err := os.Create(csrFileName)
	if err != nil {
		fmt.Println("op File can't be created")
		return
	}

	//close fo on exit and check its returned error
	defer func() {
		if err := fo.Close(); err != nil {
			fmt.Println("can't close op file", err)
		}
	}()

	//make write buffer
	iw := bufio.NewWriter(fo)	

	//write out the header
	header := strconv.Itoa(csrMat.numRows) + " " +
		strconv.Itoa(csrMat.numCols) + " " + strconv.Itoa(csrMat.nnz)
	fmt.Println(header)
	iw.WriteString(header + "\n")

	//write out the elements in cluto csr format
	for i:=0; i < csrMat.numRows; i++ {
		for j:=csrMat.rows[i]; j < csrMat.rows[i+1]; j++ {
			iw.WriteString(strconv.Itoa(csrMat.cols[j]+1) + " " + strconv.Itoa(csrMat.values[j]) + " ")
		}
		iw.WriteString("\n")
	}
	iw.Flush()
}


//read csr matrix from file in csr format
func readCSRMat(csrFileName string) CSRMat {
	
	csrMat := CSRMat{}

	//open input file
	fi, err := os.Open(csrFileName)
	if err != nil {
		fmt.Println("i/p CSR file don't exists")
		return csrMat
	}

	//close fi on exit and check its returned error
	defer func() {
		if err := fi.Close(); err != nil {
			fmt.Println("can't close term file")
		}
	}()
	
	//make read buffer
	ir := bufio.NewReader(fi)
	scanner := bufio.NewScanner(ir)

	//read header to get number of rows, number of cols, nnz
	scanner.Scan()
	header := scanner.Text()
	fmt.Println(header)
	toks := strings.Split(header, " ")
	fmt.Println(toks)
	//TODO: parse int
	csrMat.numRows,_ = strconv.Atoi(toks[0])
	csrMat.numCols,_ = strconv.Atoi(toks[1])
	csrMat.nnz,_ = strconv.Atoi(toks[2])
	
	//TODO:initialize the arrays in csrMAt
	csrMat.rows = make([]int, csrMat.numRows+1)
	csrMat.cols = make([]int, csrMat.nnz)
	csrMat.values = make([]int, csrMat.nnz)

	var currLine string
	var currToks []string
	var col int
	var val int
	//read rest of lines in file to get elements of mat
	currRowInd := 0
	valInd := 0 //store the indices of value written
	
	//set the start row element
	csrMat.rows[currRowInd] = 0 
	
	for scanner.Scan() {
		//read current line
		currLine = scanner.Text()
		currLine = strings.Trim(currLine, " ")
		//TODO:verify
		currLine = strings.Trim(currLine, "\n")
		//read columns and values from the line
		currToks = strings.Split(currLine, " ")
		
		for i:=0; i < len(currToks); i+=2 {
			col,_ = strconv.Atoi(currToks[i])
			val,_ = strconv.Atoi(currToks[i+1])
			//fmt.Println(currToks[i] + " " + currToks[i+1])
			//save the col val into CSR matrix
			csrMat.values[valInd] = val
			csrMat.cols[valInd] = col-1
			valInd++
		}

		currRowInd++

		//set the start col of next row
    csrMat.rows[currRowInd] = valInd 
	}
	
	return csrMat
}

//get KL divergence between two vectors
func klDiv(vecA, vecB []int) float64 {
	d := 0.0
	for i := range vecA {
		if (vecA[i] != 0) && (vecB[i] != 0) {
			d += math.Log((vecA[i]*1.0)/vecB[i]) * vecA[i]
		}
	}
	return d
}


func normalizeVector(vec []float64) []float64 {
	//normalize vectors
	sum := 0
	for _, elem := range vec {
		sum += elem
	}

	for i := range vecA {
		vec[i] = vec[i] / sum
	}

	return vec
}


//get Jensen-Shannon divergence b/w two vectors
func jensenShannonDiv(csrMat CSRMat, vecAInd int, vecBInd int) float64 {

	//create vectors
	vecA := make([]float, csrMat.numRows)
	vecB := make([]float, csrMat.numRows)
	vecM := make([]float, csrMat.numRows)

	for j:=csrMat.rows[vecAInd]; j < csrMat.rows[vecAInd+1]; j++ {
		vecA[csrMat.cols[j]] = csrMat.values[j]
	}

	for j:=csrMat.rows[vecBInd]; j < csrMat.rows[vecBInd+1]; j++ {
		vecB[csrMat.cols[j]] = csrMat.values[j]
	}

	//normalize vectors
	vecA = normalizeVector(vecA)
	vecB = normalizeVector(vecB)

	//average the vectors
	for i := range vecA {
		vecM[i] = (vecA[i] + vecB[i]) / 2
	}

	//calculate jensen shannon divergence
	jsd := 0.5*(klDiv(vecA, vecM) + klDiv(vecB, vecM))

	return jsd
}


type DenseFMat [][]float64
type BlockMat struct {
	startRow, endRow int
	startCol, endCol int
}
const NCPU = 4

func (denseFMat DenseFMat) getJensenSim(blockMat BlockMat, csrMat CSRMat, c chan int) {

	//compute similarities for allotted block 
	//startRow -> endRow-1 , startCol -> endCol-1 
	for i:=blockMat.startRow; i < blockMat.endRow; i++ {
		for j:=blockMat.startCol; j < blockMat.endCol; j++ {
			denseFMat[i][j] = jensenShannonDiv(csrMat, i, j)
		}
	}
	
	//signal that this work part is done
	c <- 1 
}




//create similarity matrix
func getJensenSimMatrix(CSRMat csrMat) [][]float64 {

	//initialize dense sim matrix
	denseSimCSRMat := [csrMat.numRows][csrMat.numRows]float64{}

	//create channel for synchronization
	c := make(chan int, NCPU)

	var cpuBlockMap map[int]BlockMat
	cpuBlockMap = make(map[int]BlockMat)

	cpuInd := 0
	blockSize := (csrMat.numRows * 1.0) / math.Sqrt(NCPU)
	for i:=0; i < csrMat.numRows; i += blockSize {
			for j:=0; j < csrMat.numRows; j += blockSize {
				cpuBlockMap[cpuInd] = BlockMat{i, i+blockSize, j, j+blockSize}
				cpuInd++
			}
	}

	for i:=0; i < NCPU; i++ {
		go denseSimCSRMat.getJensenSim(cpuBlockMap[i], csrMat, c)
	}

	//drain the channel
	for i:=0; i < NCPU; i++ {
		<-c //wait for task to complete
	}

}


func main() {

	csrFileName := "csr1.mat"
	csrMat := readCSRMat(csrFileName)
	//fmt.Println(strconv.Itoa(csrMat.numRows))
	if csrMat.numRows > 0 {
		writeCSRMat(csrFileName+"_dup", csrMat)
	}

}