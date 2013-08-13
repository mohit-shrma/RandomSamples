package main


//find shortest paths from passed vertex to every vertex using dijkstra
//return a min binary heap containg the nodes and keyed on distance
func getShortDistFrmVertex(adjMat CSRMat, srcId int) {
	//TODO: assign +ve inf dist to all vertices
	distNodes := make([]int, adjMat.numRows)
	for i:=0; i < adjMat.numRows; i++ {
		distNodes[i] = 9999999
	}

	//label of nodes
	// 1 - indicates 'exact' distance calculated exactly
	// 0 - indicaes 'estimated', distance estimate can be wrong
	labelNodes := make([]int, adjMat.numRows) 
	for i:=0; i < adjMat.numRows; i++ {
		labelNodes[i] = 0
	}
	
	//mark the dist from src vertex to be 0
	distNodes[srcId] = 0

	//create the min heap
	vertHeap := Heap{}
	vertHeap.heapNodes = make([]HeapNode, 7000)
	vertHeap.heapSize = 0

	minHeapInsert(vertHeap, HeapNode{srcId, 0})

	//count of vertices assigned exact dist
	exactVertCount = 0

	for ;exactVertCount < adjMat.numRows; exactVertCount++ {
		//extract the vertex with min dist from the min heap
		minHeapNode := heapExtractMin(vertHeap)

		//mark this as exact dist
		labelNodes[minHeapNode.nodeId] = 1
		distNodes[minHeapNode.nodeId] = minHeapNode.dist


		//clear the heap
		//TODO: pass struct by pointer or make method on heap
		//clearHeap(vertHeap)

		//estimate dist to adj nodes of extracted node
		for i:=adjMat.rows[minHeapNode.nodeId]; 
         i < adjMat.rows[minHeapNode.nodeId+1]; i++ {
					 //insert only if need to relax
					 minHeapInsert(vertHeap, HeapNode{adjMat.cols[i],
						 minHeapNode.dist + adjMat.values[i]})
		}

		
	}

}
