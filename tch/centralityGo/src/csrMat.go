package main

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
