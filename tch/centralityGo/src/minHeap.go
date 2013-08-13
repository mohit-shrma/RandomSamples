package main


type HeapNode struct {
	nodeId int
	dist int
}

type Heap struct {
	heapNodes[] HeapNode
	heapSize int
	//map from nodeid to index in heap
	nodeIdInd map[int]int
}


func parent(i int) int {
	return i/2
}


func left(i int) int {
	return 2*i
}


func right(i int) int {
	return 2*i + 1
}

//TODO: change for node id
func minHeapify( A Heap, i int) {

	l := left(i)
	r := right(i)
	 
	if  l <= A.heapSize && A.heapNodes[l].dist < A.heapNodes[i].dist {
		smallest := l
	} else {
		smallest := i
	}

	if r <= A.heapSize && A.heapNodes[r].dist < A.heapNodes[smallest].dist {
		smallest = r
	}

	if smallest != i {
		//swap A[i] with smallest
		temp := A.heapNodes[i].dist
		A.heapNodes[i].dist = smallest
		smallest = temp
		minHeapify(A, smallest)
	}
	
}


func buildMinHeap(A Heap) {
	A.heapSize = len(A.heapNodes)
	for i := len(A.heapNodes)/2; i >= 1; i-- {
		minHeapify(A, i)
	}
}


func getMinFrmHeap(A Heap) {
	return A.heapNodes[0]
}


func heapExtractMin(A Heap) {
	if A.heapSize < 1 {
		fmt.Println("heap underflow")
	}
	min = A.heapNodes[0]
	A.heapNodes[0] = A[A.heapSize - 1]
	minHeapify(A, 0)
	return min
}


//TODO: index i identifies whose key we want to decrease
func heapDecKey(A Heap, i int, key HeapNode) {
	if key.dist > A.heapNodes[i].dist {
		fmt.Println("Err: new key larger than current key")
	}

	A.heapNodes[i] = key
	var temp HeapNode
	for ; i > 0 && A[parent[i]].dist > A[i].dist; {
		//exchange A[i] with A[Parent(i)]
		temp.nodeId = A.heapNodes[i].nodeId
		temp.dist = A.heapNodes[i].dist

		A.heapNodes[i].nodeId = A[parent(i)].nodeId
		A.heapNodes[i].dist = A[parent(i)].dist

		A[parent(i)].nodeId = temp.nodeId
		A[parent(i)].dist = temp.dist

		i = parent(i)
	}

}



func minHeapInsert(A Heap, key HeapNode) {
	A.heapSize += 1
	//TODO: max +ve int
	A.heapNodes[A.heapSize] = 9999999
	heapDecKey(A, A.heapSize, key)
}


func clearHeap(A Heap) {
	A.heapSize = 0
}

