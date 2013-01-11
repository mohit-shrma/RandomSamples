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