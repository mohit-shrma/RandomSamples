import java.util.Vector;



class BinarySearchTree {
	
	private Node root;
	private int height;
	
	public BinarySearchTree(Node root) {
		this.root = root;
	}
	
	public Node getRoot() {
		return root;
	}
		
	public int setTreeHeight() {
		this.height = root.getDepth();
		return this.height;
	}
	
	/*
	 * add key to the tree
	 */
	public void addKey(int key) {
		if (root == null) {
			root = new Node(null, null, key);
		} else {
			Node parent = getInorderInsertNode(root, key);
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
	 * performs inorder traversal of tree
	 */
	public void traverse() {
		inorderTraversal(root);
	}
	
	public void inorderTraversal(Node root) {
		
		if (root.getLeftChild() != null) {
			inorderTraversal(root.getLeftChild());
		} 
		
		System.out.println("key: " + root.getKey() + " ht: " + root.getDepth());
		
		if (root.getRightChild() != null) {
			inorderTraversal(root.getRightChild());
		} 
		
	}
	
	public void preorderTraversal(Node root) {
		
		System.out.println("key: " + root.getKey() + " ht: " + root.getDepth());
		
		if (root.getLeftChild() != null) {
			preorderTraversal(root.getLeftChild());
		} 
		
		
		if (root.getRightChild() != null) {
			preorderTraversal(root.getRightChild());
		} 
		
	}
	
	
	public void levelOrderTraversal() {
		
		Vector<Node> queue = new Vector<Node>();
		queue.add(root);
		
		assignNodeDepth(root);
		
		int prevHt = -1;
		
		while(queue.size() > 0) {
			Node poppedNode = queue.remove(queue.size()-1);
			//insert it's child at start
			Node leftChild = poppedNode.getLeftChild();
			Node rightChild = poppedNode.getRightChild();
			
			if (leftChild != null) {
				queue.add(0, leftChild);
			}
			
			if (rightChild != null) {
				queue.add(0, rightChild);
			}
			
			int currHt = poppedNode.getDepth();
			if (currHt != prevHt) {
				System.out.println();
				prevHt = currHt;
			}
			
			//print key
			System.out.print(poppedNode.getKey() + " ");
		}
		
	}
	
	/*
	 * find lca by finding intersection or merge point of path to top from
	 * two key nodes, same as merge point detection of two link lists
	 */
	public Node lcaUseParent(int key1, int key2) {
		
		//assign depth to node, starting from top as "0"
		assignNodeDepth(root);
		
		Node key1Node = inorderSearch(root, key1);
		Node key2Node = inorderSearch(root, key2);
		
		//get the node with greater depth and by how much
		Node deeperNode = null;
		Node otherNode = null;
		
		if (key1Node.getDepth() > key2Node.getDepth()) {
			deeperNode = key1Node;
			otherNode = key2Node;
		} else {
			deeperNode = key2Node;
			otherNode = key1Node;
		}
		
		int heightDiff = deeperNode.getDepth() - otherNode.getDepth();
		
		//traverse up of deeper node so that both nodes at same depth
		while (heightDiff > 0) {
			deeperNode = deeperNode.getParent();
			heightDiff--;
		}
		
		//at same depth, navigate up until both node has same parent
		while (deeperNode.getParent() != otherNode.getParent()) {
			deeperNode = deeperNode.getParent();
			otherNode = otherNode.getParent();
		}
		
		//if both nodes are same then return either
		if (deeperNode == otherNode) {
			return deeperNode;
		}
		
		//return the parent of either node, as same depth then parent is same
		return deeperNode.getParent();
	}
	
	
	/*
	 * find LCA of two nodes, using bottom up approach on a general binary tree
	 */
	public Node bottomUpLCA(Node node, int key1, int key2) {
		
		if (node!= null) {
			int nodeKey = node.getKey();
			if (nodeKey == key1 || nodeKey == key2) {
				//found key1 or key2
				return node;
			} else {
				//search for key1 and key2 in left and right child
				Node leftSearch = bottomUpLCA(node.getLeftChild(), key1, key2);
				Node rightSearch = bottomUpLCA(node.getRightChild(), key1, key2);
				if (leftSearch != null && rightSearch != null) {
					//found in both subtrees then current node is lca, pass this up
					return node;
				} else if (leftSearch != null) {
					//either of them could be in left subtree, pass this upwards
					return leftSearch;
				} else {
					//either of them could be in right subtree, pass this up
					//null in case none in subtrees
					return rightSearch;
				}
			}
		} else {
			return null;
		}
		
	}
	
	
	/*
	 * find LCA, exploiting bst property
	 */
	public Node bstLCA(int key1, int key2) {
		
		Node top = root;
		int topKey = root.getKey();
				
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
	
	
	/*
	 * display tree hierarchically with evenly spaced nodes
	 */
	public void prettyPrint() {
	
		int treeHt = this.height;
		int numLeaves = (int) Math.pow(2, treeHt);
		int perNodeSpace = 3;
		int leavesWidth = numLeaves * perNodeSpace + (numLeaves - 1);
		
		//assign depth to each node i.e from top to down
		assignNodeDepth(root);
		
		//create dummy node to add in case of empty node at a level
		//TODO: consts 786
		Node dummyNode = new Node(null, null, 786);
		
		Vector<Node> currQueue = new Vector<Node>();
		Vector<Node> childQueue = new Vector<Node>();
		int currHt = root.getDepth();
		
		currQueue.add(root);
		
		int numNodes = 0;
		
		while (currHt <= treeHt) {
			
			//print new line for next level
			System.out.println();
			
			//get node count at current ht
			numNodes = (int) Math.pow(2, currHt);
			
			//check for current queue size
			if (currQueue.size() != numNodes) {
				System.out.println("queue not of exact size: "+ currQueue.size()
						+ " as current ht: " + currHt);
				System.exit(-2);
			}
			
			//print L/(2**(depth+1)) spaces b4 first node
			int numGaps = (int) (leavesWidth/(Math.pow(2, currHt + 1)));
			for (int i = 0; i < numGaps - (1*perNodeSpace/2); i++) {
				System.out.print(" ");
			}
			
			//get all nodes at current ht from queue and add their child for 
			//next level to queue
			childQueue.clear();
			while (currQueue.size() > 0) {
				
				//pop a node from currQueue
				Node poppedNode = currQueue.remove(currQueue.size()-1);
				
				//display popped node key
				if (poppedNode != dummyNode) {
					System.out.format("%"+perNodeSpace+"s", poppedNode.getKey());
				} else {
					System.out.format("%"+perNodeSpace+"s", "N");
				}
				
				//display gaps after key, 2L/(2**(depth+1)) spaces b4 first node
				for (int i = 0; i < 2*numGaps - (1*perNodeSpace/2); i++) {
					System.out.print(" ");
				}
				
				//add poppedNode's child to childQueue
				Node leftChild = poppedNode.getLeftChild();
				if (leftChild == null) {
					leftChild = dummyNode;
				}
				
				Node rightChild = poppedNode.getRightChild();
				if (rightChild == null) {
					rightChild = dummyNode;
				}
				
				childQueue.add(0, leftChild);
				childQueue.add(0, rightChild);
			}
			
			currQueue.clear();
			currQueue.addAll(childQueue);
			
			currHt++;
			
		}
		
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
	
	
	/*
	 * assign depth to each node in tree
	 */
	public void assignNodeDepth(Node node) {
		
		if (node == root) {
			node.setDepth(0);
		} else {
			node.setDepth(node.getParent().getDepth() + 1);
		}
		
		if (node.getLeftChild() != null) {
			assignNodeDepth(node.getLeftChild());
		}
		
		if (node.getRightChild() != null) {
			assignNodeDepth(node.getRightChild());
		}
	}
	
	
	/*
	 * assign height to each node in tree
	 */
	public void assignNodeHeight(Node node) {
		
		int leftHt = -1;
		int rightHt = -1;
		int ht = -1;
		
		if (node.getLeftChild() != null) {
			assignNodeHeight(node.getLeftChild());
			leftHt = node.getLeftChild().getDepth() + 1;
		} else {
			leftHt = 0;
		}
		
		
		if (node.getRightChild() != null) {
			assignNodeHeight(node.getRightChild());
			rightHt = node.getRightChild().getDepth() + 1;
		} else {
			rightHt = 0;
		}
		
		ht = leftHt > rightHt ? leftHt : rightHt;
		
		node.setDepth(ht);
		
	}
	
}