package main

import (
	"fmt"
	"os"
	"bufio"
	"strings"
	"strconv"
	"io"
)


func filterNWriteTerms( w bufio.Writer, r io.Reader,
	counts []int, thresh int) []int {

	nnzCount := 0
	scanner := bufio.NewScanner(r)
	//read lines from the file
	var currLine string
	var currWords []string

	isHeaderRead := false
	fmt.Println("start writing")
	for scanner.Scan() {
		if !isHeaderRead {
			isHeaderRead = true
			fmt.Println("writing header")
			w.WriteString(scanner.Text())
			w.WriteString("\n")
			continue
		}

		//read current line
		currLine = scanner.Text()
		currLine = strings.Trim(currLine, " ")
		if len(currLine) == 0 {
		    w.Write([]byte("\n"))
		    continue
		  }
		//read words from line
		currWords = strings.Split(currLine, " ")
		var currWordInd int64
		//fmt.Println(currWords)
		for i:=0; i < len(currWords); i+=2 {
			currWordInd, _ = strconv.ParseInt(currWords[i], 10, 64)			
			if counts[currWordInd-1] >= thresh {
			    //fmt.Println(currWordInd, counts[currWordInd-1], currWords[i], currWords[i+1])  
				w.WriteString(currWords[i])
				w.WriteString(" ")
				w.WriteString(currWords[i+1])
			        w.WriteString(" ")
				nnzCount++
			}
		}
	   w.WriteString("\n")
	}
	
	fmt.Println("new nnz count: ", nnzCount)
	
	//get all new nnz ind
	nnzs := make([]int, nnzCount)
	j := 0
	for i, count := range counts {
		if count >= thresh {
			nnzs[j] = i + 1
			j++
		}
	}
	
	w.Flush()
	return nnzs
}


func getTermCount( r io.Reader, counts []int) {
	scanner := bufio.NewScanner(r)
	//read lines from the file
	var currLine string
	var currWords []string
	isHeaderRead := false
	for scanner.Scan() {
		if !isHeaderRead {
			isHeaderRead = true
			continue
		}

		//read current line
		currLine = scanner.Text()
		currLine = strings.Trim(currLine, " ")
		if len(currLine) == 0 {
		    continue
		}
		//read words from line
		currWords = strings.Split(currLine, " ")
		var currWordInd int64
		var currWordCount int64

		//fmt.Printf("%q\n", currWords)
		//fmt.Println(len(currWords), currWords[len(currWords)-1], currWords[len(currWords)-2])
		for i:=0; i < len(currWords); i+=2 {
		  //fmt.Println(i)
			currWordInd, _ = strconv.ParseInt(currWords[i], 10, 64)
			currWordCount, _ = strconv.ParseInt(currWords[i+1], 10, 0) 
			counts[currWordInd-1] += int(currWordCount)
		}
	}
}


func createValidTermMap( fileName string, valIndMap map[int]bool) (valTermMap map[string]bool) {

	valTermMap = make(map[string]bool)

	//open input file
	fi, err := os.Open(fileName)
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

	//make read buffer
	ir := bufio.NewReader(fi)

	scanner := bufio.NewScanner(ir)

	//read lines from file
	i := 1
	currLine := ""
	for scanner.Scan() {
		currLine = scanner.Text()
		currLine = strings.Trim(currLine, " ")
		_, ok := valIndMap[i]
		if ok {
			valTermMap[currLine] = true
		}
		i++
	}

	return 
}


func main() {
	//open input file
	fi, err := os.Open("trainMat")
	if err != nil {
		fmt.Println("ip file don't exists")
		return
	}

	//close fi on exit and check its returned error
	defer func() {
		if err := fi.Close(); err != nil {
			fmt.Println("can't close ip file")
		}
	}()


	//make read buffer
	ir := bufio.NewReader(fi)


	//open output file
	fo, err := os.Create("trainMat_trim")
	if err != nil {
		fmt.Println("op File can't be created")
		return
	}

	//close fo on exit and check its returned error
	defer func() {
		if err := fo.Close(); err != nil {
			fmt.Println("can't close op file")
		}
	}()


	counts:= make([]int, 21019937)
	
	getTermCount( ir, counts)
	
	fmt.Println("done with term counts: ", counts[:10])

	//make read buffer
	fi.Close()
	fi, err = os.Open("trainMat")
	if err != nil {
		fmt.Println("ip file don't exists")
		return
	}
	ir = bufio.NewReader(fi)

	//make write buffer
	iw := bufio.NewWriter(fo)

	//write the trimmed mat, get the valid nnzs ind
	valNNZS := filterNWriteTerms( *iw, ir, counts, 100)

	fo.Close()
	
	//use these nnzs ind, to create valid term map
	valIndMap := make(map[int]bool)
	for _, valInd := range valNNZS {
		valIndMap[valInd] = true
	}

	//use valIndMap to create valid term map
	valTermMap := createValidTermMap( "", valIndMap)

	//save these valid terms in a file
	fo, err = os.Create("valTrainTerm")
	if err != nil {
		fmt.Println("op File can't be created")
		return
	}

	//close fo on exit and check its returned error
	defer func() {
		if err := fo.Close(); err != nil {
			fmt.Println("can't close op file")
		}
	}()

	//make write buffer
	iw = bufio.NewWriter(fo)

	for valTerm, _ := range valTermMap {
		//write out the valterm
		iw.WriteString(valTerm + "\n")
	}
	
	
	
}
