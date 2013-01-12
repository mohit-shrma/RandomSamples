import java.util.Vector;



class BinarySearchTree extends BinaryTree {
	
	
	public BinarySearchTree(Node root) {
        super(root);
    }




    /*
	 * add key to the tree
	 */
	public void insertKey(int key) {
		if (getRoot() == null) {
			setRoot(new Node(null, null, key));
		} else {
			Node parent = getInorderInsertNode(getRoot(), key);
			if (parent.getKey() >= key) {
				if (parent.getLeftChild() != null) {
					System.out.println("Err: addKey");
				} else {
					Node leftChild = new Node(null, null, key, parent);
					parent.setLeftChild(leftChild);
				}
			} else {
				if (parent.getRightChild() != null) {
					System.out.println("Err: addKey");
				} else {
					Node rightChild = new Node(null, null, key, parent);
					parent.setRightChild(rightChild);
				}
			}
		}
		
	}
	
	
	
	/*
	 * find lca by finding intersection or merge point of path to top from
	 * two key nodes, same as merge point detection of two link lists
	 */
	public Node lcaUseParentBST(int key1, int key2) {
	    Node key1Node = inorderSearch(getRoot(), key1);
	    Node key2Node = inorderSearch(getRoot(), key2);
	    
	    return lcaUseParent(key1Node, key2Node);
	    
	}
	
	/*
	 * merge two binary search trees, use two stacks to print in sorted order
	 * complexity: O(ht of I tree + ht of II tree)
	 */
	public void printMergeBSTs(Node node1, Node node2) {
	    
	    //stack to store nodes from first tree
	    Vector<Node> nodeStack1 = new Vector<Node>();
	    
	    //stack to store nodes from second tree
	    Vector<Node> nodeStack2 = new Vector<Node>();
	    
	    //push all nodes towards left leaf in tree1
	    while (node1 != null) {
	        nodeStack1.add(0, node1);
	        node1 = node1.getLeftChild();
	    }
	    
	    //push all nodes towards left leaf in tree2
	    while (node2 != null) {
	        nodeStack2.add(0, node2);
	        node2 = node2.getLeftChild();
	    }
	    
	    //top node of first
	    Node topNode1 = null;
	    
	    //top node of second stack
	    Node topNode2 = null;
	    
	    Node temp = null;
	    
	    while (nodeStack1.size() > 0 && nodeStack2.size() > 0) {
	        
	        //get top node from first stack
	        topNode1 = nodeStack1.elementAt(0);
	        
	        //get top node from second stack
	        topNode2 = nodeStack2.elementAt(0);
	        
	        if (topNode1.getKey() < topNode2.getKey()) {
	            //top node of stack 1 is lesser
	            //pop and display the node
	            nodeStack1.remove(0);
	            System.out.println(topNode1.getKey());
	            //push if any right child is there
	            if (topNode1.getRightChild() != null) {
	                temp = topNode1.getRightChild();
	                while (temp != null) {
	                    nodeStack1.add(0, temp);
	                    temp = temp.getLeftChild();
	                }
	            }
	        } else {
	            //top node of stack 2 is lesser
                //pop and display the node
                nodeStack2.remove(0);
                System.out.println(topNode2.getKey());
                //push if any right child is there
                if (topNode2.getRightChild() != null) {
                    temp = topNode2.getRightChild();
                    while (temp != null) {
                        nodeStack2.add(0, temp);
                        temp = temp.getLeftChild();
                    }
                }
	            
	        }
	        
	        
	    }
	    
	    //either both stacks are empty or one of them is empty
	    //so print themone by one
	    
	    if (nodeStack1.size() > 0 ) {
	        while(nodeStack1.size() > 0) {
	            topNode1 = nodeStack1.remove(0);
	            System.out.println(topNode1.getKey());
	        }
	    }
	    
	    if (nodeStack2.size() > 0) {
	        while(nodeStack2.size() > 0) {
                topNode2 = nodeStack2.remove(0);
                System.out.println(topNode2.getKey());
            }
	    }
	    
	    
	    
	}
	
	
	
	
	/*
	 * find LCA, exploiting bst property
	 */
	public Node bstLCA(int key1, int key2) {
		
		Node top = getRoot();
		int topKey = getRoot().getKey();
				
		while((topKey >= key1 && topKey >= key2) ||  
				(topKey < key1 && topKey < key2)) {
			//if either key is current node return it as lca
			if (topKey == key1 || topKey == key2) {
				return top;
			}
			
			//either both keys are to the left or on the right side
			if (topKey > key1 && topKey > key2) {
				//both keys are to the left
				if (top.getLeftChild() != null) {
					top = top.getLeftChild();
					topKey = top.getKey();
				} else {
					return top;
				}
				
			} else {
				//both keys are to the right
				if (top.getRightChild() != null) {
					top = top.getRightChild();
					topKey = top.getKey();
				} else {
					return top;
				}				
			}
		}
		
		return top;
	}
	
	
	
	
	
	private Node getInorderInsertNode(Node node, int key) {
		if (node != null) {
			
			Node searchNode = null;
			
			if  (node.getKey() >= key) {
				//search left
				searchNode = node.getLeftChild();
			} else if (node.getKey() < key) {
				//search right
				searchNode = node.getRightChild();
			} 
			
			if (searchNode != null) {
				return getInorderInsertNode(searchNode, key);
			} else {
				return node;
			}
		} else {
			//passed  null node shudn't come here
			System.out.println("inorderSearch: passed null node");
			return null;
		}
	}
	
	
	/*
	 * do inorder search on node and return the node if found or the node 
	 * reached last
	 */
	public Node inorderSearch(Node node, int key) {
		if (node != null) {
			Node searchNode = null;
			if  (node.getKey() > key) {
				//search left
				searchNode = node.getLeftChild();
			} else if (node.getKey() < key) {
				//search right
				searchNode = node.getRightChild();
			} else {
				return node;
			}
			
			if (searchNode != null) {
				return inorderSearch(searchNode, key);
			} else {
				return node;
			}
		} else {
			//passed  null node shudn't come here
			System.out.println("inorderSearch: passed null node");
			return null;
		}
		
	}
	
	
	
	
	
	
	
}