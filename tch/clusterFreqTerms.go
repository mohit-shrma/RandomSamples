package main

import (
	"fmt"
	"os"
	"strings"
	"strconv"
	"bufio"
	"math"
	"runtime"
	"flag"
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

type DenseFMat [][]float64

type Pair struct {
	term1Ind int
	term2Ind int
}

const NCPU = 4


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
func klDiv(vecA, vecB []float64) float64 {
	d := 0.0
	for i := range vecA {
		if (vecA[i] != 0) && (vecB[i] != 0) {
			d += math.Log( (float64(vecA[i])) / vecB[i]) * vecA[i]
		}
	}
	return d
}


func normalizeVector(vec []float64) []float64 {
	//normalize vectors
	sum := 0.0
	for _, elem := range vec {
		sum += elem
	}

	for i := range vec {
		vec[i] = vec[i] / sum
	}

	return vec
}


//get mutual-info based on occurence count
//TODO: Assuming termInd starts from 0, maxOccCount is maximum possible number of
//occurences 
func mutualInfo(csrMat CSRMat, term1Ind, term2Ind int, maxOccCount float64) float64 {
	
	//get co-occurence count
	jointCount := 0.0
	for j:=csrMat.rows[term1Ind]; j < csrMat.rows[term1Ind+1]; j++ {
		if csrMat.cols[j] == term2Ind {
			jointCount = float64(csrMat.values[j])
		}
	}
	if jointCount == 0 {
		return 0.0
	}

	//get term1 occurence count
	term1Count := 0.0
	for j:=csrMat.rows[term1Ind]; j < csrMat.rows[term1Ind+1]; j++ {
		term1Count += float64(csrMat.values[j])
	}
	if term1Count == 0 {
		return 0.0
	}

	//get term2 occurence count
	term2Count := 0.0
	for j:=csrMat.rows[term2Ind]; j < csrMat.rows[term2Ind+1]; j++ {
		term2Count += float64(csrMat.values[j])
	}
	if term2Count == 0 {
		return 0.0
	}


	jointProb := (jointCount/maxOccCount)
	term1Prob := (term1Count/(maxOccCount*float64(csrMat.numRows)))
	term2Prob := (term2Count/(maxOccCount*float64(csrMat.numRows)))

	//fmt.Println(jointProb, term1Prob, term2Prob)

	return jointProb * math.Log( jointProb / (term1Prob*term2Prob) )
}



//get Jensen-Shannon divergence b/w two vectors
func jensenShannonDiv(csrMat CSRMat, vecAInd , vecBInd int) float64 {

	//create vectors
	vecA := make([]float64, csrMat.numRows)
	vecB := make([]float64, csrMat.numRows)
	vecM := make([]float64, csrMat.numRows)

	for j:=csrMat.rows[vecAInd]; j < csrMat.rows[vecAInd+1]; j++ {
		vecA[csrMat.cols[j]] = float64(csrMat.values[j])
	}

	for j:=csrMat.rows[vecBInd]; j < csrMat.rows[vecBInd+1]; j++ {
		vecB[csrMat.cols[j]] = float64(csrMat.values[j])
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



func (denseFMat DenseFMat) getJensenSim(termPairs []Pair, csrMat CSRMat, c chan int) {

	//compute similarities for allotted chunk
	jsd := 0.0
	for _, termPair := range termPairs {
		jsd = jensenShannonDiv(csrMat, termPair.term1Ind, termPair.term2Ind)
		denseFMat[termPair.term1Ind][termPair.term2Ind] = jsd
		denseFMat[termPair.term2Ind][termPair.term1Ind] = jsd
	}
	
	//signal that this work part is done
	c <- 1 
}


//create similarity matrix
func getJensenSimMatrix(csrMat CSRMat) [][]float64 {

	//initialize dense sim matrix
	denseSimCSRMat := make([]([]float64), csrMat.numRows)
	for i := range denseSimCSRMat {
		denseSimCSRMat[i] = make([]float64, csrMat.numRows)
	}

	denseFMat := DenseFMat(denseSimCSRMat)

	//create channel for synchronization
	c := make(chan int, NCPU)

	//number of possible pairs numRows<C>2 nC2 = n!/ (n-2!) 2! = n * (n-1)/2
	numPairs := (csrMat.numRows * (csrMat.numRows-1)) / 2
	//generate all pairs
	allPairs := make([]Pair, 0, numPairs)
	for i:=0; i < csrMat.numRows; i++ {
		for j:=i+1; j < csrMat.numRows; j++ {
			allPairs = append(allPairs, Pair{i, j})
		}
	}

	/*
	for _, pair := range allPairs {
		fmt.Println(pair.term1Ind, pair.term2Ind)
	}*/


	fmt.Printf("\nest number of pairs: %d actual number of pairs: %d\n",
		numPairs, len(allPairs))

	//compute all pair similarity and divide among cpus
	for i:=0; i < NCPU; i++ {
		//do for pairs [i*numPairs/NCPU -> (i+1)*numPairs/NCPU]
		go denseFMat.getJensenSim(
			allPairs[(i*numPairs*1.0)/NCPU:((i+1)*numPairs*1.0)/NCPU],
			csrMat, c)
	}

	//drain the channel
	for i:=0; i < NCPU; i++ {
		<-c //wait for task to complete
	}

	//show learned sim matrix
	/*for _, row := range denseFMat {
		fmt.Println(row)
	}*/

	return denseFMat

}


func (denseFMat DenseFMat) getMutInfoSim(termPairs []Pair, csrMat CSRMat, maxOccCount int, c chan int) {

	//compute similarities for allotted chunk
	mutInfo := 0.0
	for _, termPair := range termPairs {
		mutInfo = mutualInfo(csrMat, termPair.term1Ind, termPair.term2Ind, float64(maxOccCount))
		denseFMat[termPair.term1Ind][termPair.term2Ind] = mutInfo
		denseFMat[termPair.term2Ind][termPair.term1Ind] = mutInfo
	}
	
	//signal that this work part is done
	c <- 1 
}


//create mutual Info similarity matrix
func getMutInfoSimMatrix(csrMat CSRMat, maxOccCount int) [][]float64 {

	//initialize dense sim matrix
	denseSimCSRMat := make([]([]float64), csrMat.numRows)
	for i := range denseSimCSRMat {
		denseSimCSRMat[i] = make([]float64, csrMat.numRows)
	}

	denseFMat := DenseFMat(denseSimCSRMat)

	//create channel for synchronization
	c := make(chan int, NCPU)

	//number of possible pairs numRows<C>2 nC2 = n!/ (n-2!) 2! = n * (n-1)/2
	numPairs := (csrMat.numRows * (csrMat.numRows-1)) / 2
	//generate all pairs
	allPairs := make([]Pair, 0, numPairs)
	for i:=0; i < csrMat.numRows; i++ {
		for j:=i+1; j < csrMat.numRows; j++ {
			allPairs = append(allPairs, Pair{i, j})
		}
	}

	/*
	for _, pair := range allPairs {
		fmt.Println(pair.term1Ind, pair.term2Ind)
	}*/


	fmt.Printf("\nest number of pairs: %d actual number of pairs: %d\n",
		numPairs, len(allPairs))

	//compute all pair similarity and divide among cpus
	for i:=0; i < NCPU; i++ {
		//do for pairs [i*numPairs/NCPU -> (i+1)*numPairs/NCPU]
		go denseFMat.getMutInfoSim(
			allPairs[(i*numPairs*1.0)/NCPU:((i+1)*numPairs*1.0)/NCPU],
			csrMat, maxOccCount, c)
	}

	//drain the channel
	for i:=0; i < NCPU; i++ {
		<-c //wait for task to complete
	}

	//show learned sim matrix
	/*for _, row := range denseFMat {
		fmt.Println(row)
	}*/

	return denseFMat
}



//write dense sim  matrix to file in csr format
func writeDenseMat(csrFileName string, denseFMat DenseFMat) {
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


	nnzCount := 0

	//write out the elements in cluto csr format
	for _, row := range denseFMat {
		for colInd, val := range row {
			if val != 0 {
				iw.WriteString(strconv.Itoa(colInd+1) + " " + strconv.FormatFloat(val, 'f', 6, 64) + " ")
				nnzCount++
			}
		}
		iw.WriteString("\n")
	}

	fmt.Println("NNZCount: ", nnzCount)

	iw.Flush()
}



func saveMergeSeq(merges []Pair, opFileName string) {
	//open output file 
	fo, err := os.Create(opFileName)
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
	
	for _, pair := range merges {
		iw.WriteString(strconv.Itoa(pair.term1Ind) + " " + strconv.Itoa(pair.term2Ind) + "\n")
	}

	iw.Flush()

}



func simpleHAC(denseFMat DenseFMat, numTerms int) []Pair {

	//keep track of active clusters
	inActCluster := make([]bool, numTerms)

	//store sequence of merges
	merges := make([]Pair, 0, 2400)
	maxPair := Pair{}
	maxVal := 0.0
	for k:=0; k < numTerms-1; k++ {
		fmt.Println("Merge Iter: " + strconv.Itoa(k))
		//get the pair(i,m) with max similarity S.T.
		// i != m, inActCluster[i] == false, inActCluster[m] == false
		maxPair = Pair{}
		maxVal = 0

		for i:=0; i < numTerms; i++ {
			for m:=i+1; m < numTerms; m++ {
				if !inActCluster[i] && !inActCluster[m] {
					if denseFMat[i][m] > maxVal {
						maxVal = denseFMat[i][m]
						maxPair = Pair{i, m}
					}
				}
			}
		}

		if maxVal > 0 {
			merges = append(merges, maxPair)
		} else {
			//can't proceed ahead
			break
		}
		
		i := maxPair.term1Ind
		m := maxPair.term2Ind
		
		//update similarity of all terms with i
		for j:=0; j < numTerms; j++ {
			if i != j {
				denseFMat[i][j] = min(denseFMat[j][i],denseFMat[j][m])
				denseFMat[j][i] = denseFMat[i][j]
 			}
		}

		//deactivate clusters
		inActCluster[m] = true
	}

	return merges
}



func min(a, b float64) float64 {
	if a < b {
		return a
	} else {
		return b
	}
}


func main() {

	var fileName = flag.String("file","csr1.mat","matrix file name to read")
	flag.Parse()
	fmt.Println("\nfileName is: ", *fileName)
	fmt.Println("numCpu: ", runtime.NumCPU())

	csrFileName := *fileName
	csrMat := readCSRMat(csrFileName)
	//fmt.Println(strconv.Itoa(csrMat.numRows))
	if csrMat.numRows > 0 {
		//writeCSRMat(csrFileName+"_dup", csrMat)
	}

	denseJSDMat := getJensenSimMatrix(csrMat)
	writeDenseMat(csrFileName+"_dense_sim", denseJSDMat)

	merges := simpleHAC(denseJSDMat, csrMat.numRows)
	saveMergeSeq(merges, csrFileName+"_merges")

	//maxOccCount := 90000 //max occurences possible equal number of movies
	//denseMutInfMat := getMutInfoSimMatrix(csrMat, maxOccCount)
	//writeDenseMat(csrFileName+"_dense_MutInf", denseMutInfMat)
}

