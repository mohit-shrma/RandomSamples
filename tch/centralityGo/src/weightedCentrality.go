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


	

}