package main

import (
	"fmt"
	"os"
	"bufio"
	"strings"
	"strconv"
	"io"
)


func filterNWriteTerms( w io.Writer, r io.Reader, counts [21019937]int, thresh int) {
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
		
		//read words from line
		currWords = strings.Split(currLine, " ")
		var currWordInd int64
		for i:=0; i < len(currWords); i+=2 {
			currWordInd, _ = strconv.ParseInt(currWords[i], 10, 64) 
			if counts[currWordInd-1] >= thresh {
				w.Write([]byte(currWords[i]))
				w.Write([]byte(" "))
				w.Write([]byte(currWords[i+1]))
			}
		}
	}
}


func getTermCount( r io.Reader, counts [21019937]int) {
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
		
		//read words from line
		currWords = strings.Split(currLine, " ")
		var currWordInd int64
		var currWordCount int64
		for i:=0; i < len(currWords); i+=2 {
			currWordInd, _ = strconv.ParseInt(currWords[i], 10, 64)
			currWordCount, _ = strconv.ParseInt(currWords[i+1], 10, 0) 
			counts[currWordInd-1] += int(currWordCount)
		}
	}
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

	//close fi on exit and check its returned error
	defer func() {
		if err := fo.Close(); err != nil {
			fmt.Println("can't close op file")
		}
	}()

	//make write buffer
	iw := bufio.NewWriter(fo)
	
	//make read buffer
	ir = bufio.NewReader(fi)

	var counts [21019937]int
	
	getTermCount( ir, counts)
	
	filterNWriteTerms( iw, ir, counts, 100)
}