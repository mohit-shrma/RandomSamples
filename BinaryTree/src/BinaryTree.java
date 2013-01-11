import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Random;
import java.util.Vector;


class BinaryTree {
	
    private Node root;
    private int height;
    
    public BinaryTree(Node root) {
        this.root = root;
    }
    
    public Node getRoot() {
        return root;
    }
        
    public void setRoot(Node node) {
        this.root = node;
    }
    
    public int setTreeHeight() {
        this.height = root.getDepth();
        return this.height;
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
     * find lca by finding intersection or merge point of path to top from
     * two key nodes, same as merge point detection of two link lists
     */
    public Node lcaUseParent(Node key1Node, Node key2Node) {
        
        //assign depth to node, starting from top as "0"
        assignNodeDepth(root);
        
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

    
    /*
     * populate inorder successor of all nodes
     * i.e node.next = inorder successor
     * do this by reverse inorder traversal right, node, left
     * 
     */
    public Node populateNext(Node node, Node next) {
        
        if (node != null) {
            
            next = populateNext(node.getRightChild(), next);
            
            node.setNext(next);
           
            next = node;
            
            next = populateNext(node.getLeftChild(), next);
        }
        
        return next;
        
    }
    
    
    
    /*
     * inorder traversal by following next
     */
    public void inorderByNext(Node node) {
        
        //get the left most leaf
        while (node.getLeftChild() != null) {
            node = node.getLeftChild();
        }
        
        //print left most key
        System.out.println(node.getKey() + " ");
        
        //follow next or inorder succesor pointer
        while (node.getNext() != null) {
            node = node.getNext();
            System.out.println(node.getKey() + " ");
        }
    }
    
    
    /*
     * populate nextRight of each node in tree
     * nextRight at a node point to node to the right at same level
     * use a traversal similar to preorder
     * next right of current level is set before the next level
     */
    public void populateNextRight(Node node) {
        
        if (node == null) {
            return;
        }
        
        if (node.getNextRight() != null) {
            //set next right of child of other nodes at same level
            populateNextRight(node.getNextRight());
        }
        
        if (node.getLeftChild() != null) {
            //left child of node exists
            Node leftChild = node.getLeftChild();
           
            if (node.getRightChild() != null) {
                //right child of node exists
                //set the next right of left child to the node's right child 
                leftChild.setNextRight(node.getRightChild());
                //set the next right of right child of current node
                node.getRightChild().setNextRight(nextRightChild(node));
            } else {
                //no right child, set the next right of left child
                leftChild.setNextRight(nextRightChild(node));
            }
            
            //call for next level nodes
            //calling only left child, this call will call for right child
            populateNextRight(leftChild);
        } else if (node.getRightChild() != null) {
            //left child dont exists, set the next right child of right
            node.getRightChild().setNextRight(nextRightChild(node));
            //recursively call for next level nodes
            populateNextRight(node.getRightChild());
        } else {
            //both left and right child dont exists
            //call to connect non-null childs at the next level
            populateNextRight(nextRightChild(node));
        }
        
    }
    
    
    /*
     * get the next non-null child of nodes in right at current level
     */
    private Node nextRightChild(Node node) {
        //get the node to the right at same level
        node = node.getNextRight();
        
        while (node != null) {
            if (node.getLeftChild() != null) {
                //return the non null child
                return node.getLeftChild();
            }
            
            if (node.getRightChild() != null) {
                //return the non null child
                return node.getRightChild();
            }
            
            //no child found, look at other nodes on right
            node = node.getNextRight();
        }
        
        return null;
    }
    
    /*
     * level order traversal using next right node
     */
    public void levelOrderTraverseUsingNextRt(Node node) {
        
        if (node == null)
            return;
        
        System.out.print(node.getKey() + " ");
        
        Node nodeNextRt = null;
        nodeNextRt = node; 
        
        //display keys of all nodes to the right
        while( (nodeNextRt = nodeNextRt.getNextRight()) != null) {
            System.out.print(nodeNextRt.getKey() + " ");
        }
        
        System.out.println("");
        
        //traverse next level, by finding first non-null child of next level
        if (node.getLeftChild() != null) {
            levelOrderTraverseUsingNextRt(node.getLeftChild());
        } else if (node.getRightChild() != null) {
            levelOrderTraverseUsingNextRt(node.getRightChild());
        } else {
            levelOrderTraverseUsingNextRt(nextRightChild(node));
        }
        
    }
     
}