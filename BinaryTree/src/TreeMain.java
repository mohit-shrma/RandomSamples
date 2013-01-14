import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.Random;
import java.util.Vector;


class TreeMain {
    
    
    public void binarySearchTreeMethods(Vector<Integer> keys) {
        BinarySearchTree bst = new BinarySearchTree(null);
        for (int key: keys) {
            bst.insertKey(key);
        }
        
        Node root = bst.getRoot();
        
        System.out.println("inorder traversal");
        bst.traverse();
        
        bst.assignNodeHeight(root);
        bst.setTreeHeight();
        
        //bst.assignNodeDepth(root);

        System.out.println("inorder traversal: ");
        bst.traverse();
        
        System.out.println("preorder traversal: ");
        bst.preorderTraversal(root);
        
        System.out.println("level order traversal: ");
        bst.levelOrderTraversal();
        System.out.println();
        
        System.out.println("pretty print tree: ");
        bst.prettyPrint();
        System.out.println();
        
        //generate two random keys for lowest common ancestor from tree
        Random randomGenerator = new Random();
        int randIdx = randomGenerator.nextInt(keys.size());
        int key1 = keys.elementAt(randIdx);
        randIdx = randomGenerator.nextInt(keys.size());
        int key2 = keys.elementAt(randIdx);
        
        System.out.println("LCA key1: "+ key1 + " LCA key2: " + key2);
        System.out.println("LCA bst: " 
                            + bst.bstLCA(key1, key2).getKey());
        System.out.println("LCA bottom up: " 
                + bst.bottomUpLCA(root, key1, key2).getKey());
        System.out.println("LCA parent: " + bst.lcaUseParentBST(key1, key2).getKey());
        
        
        //populate inorder successor
        bst.populateNext(root, null);
        
        
        //do inorder traversal
        System.out.println("Inorder traversal using next: ");
        bst.inorderByNext(root);
        
        //populate next right at each level
        bst.populateNextRight(root);
        
        //do level order traverse using next right
        System.out.println("Level order traversal using next rt: ");
        bst.levelOrderTraverseUsingNextRt(root);
        
        //do iterative preorder traversal
        System.out.println("iterative preorder traversal: ");
        bst.iterativePreorder(root);
        
        //do iterative inorder traversal
        System.out.println("\niterative inorder traversal: ");
        bst.iterativeInorder(root);
        
        //do iterative postorder traversdal
        System.out.println("\niterative postorder traversal: ");
        bst.iterativePostorder(root);
        
        
        //maximum width
        System.out.println("max width of tree: " + bst.findMaxWidth(root));
        
        //diameter
        System.out.println("diameter of tree: " + bst.diameter(root));
        
        //check if bst
        System.out.println("is bst: " + bst.isBinarySearchTree(root, -100, 100));
        //validateBST();
        
        //convert tree to doubly link list and traverse
        Node head = bst.convertToDoublyLinkList(root);
        bst.traverseDoublyLL(head);
        
        //TODO: write a code to reconstruct tree from above DLL by looking at
        //pre/post order traversal stored previously
        
    } 
    
    
    public void mergeTwoBSTs(Vector<Integer> keys1, Vector<Integer> keys2) {
        
        BinarySearchTree bst1 = new BinarySearchTree(null);
        for (int key: keys1) {
            bst1.insertKey(key);
        }
        bst1.assignNodeHeight(bst1.getRoot());
        bst1.setTreeHeight();
        System.out.println("pretty print tree1: ");
        bst1.prettyPrint();
        System.out.println();
        
        BinarySearchTree bst2 = new BinarySearchTree(null);
        for (int key: keys2) {
            bst2.insertKey(key);
        }
        
        bst2.assignNodeHeight(bst2.getRoot());
        bst2.setTreeHeight();
        System.out.println("pretty print tree2: ");
        bst2.prettyPrint();
        System.out.println();
        
        System.out.println("merged binary trees: ");
        bst1.printMergeBSTs(bst1.getRoot(), bst2.getRoot());
        
        
    }
    
    
    
    /*
     * to construct binary tree from given preorder and post order
     */
    public void prePostTree() {
        int[] pre = {10, 6, 11, 15, 4, 17, 8, 9, 6};
        int[] post = {11, 15, 6, 17, 9, 6, 8, 4, 10};
        
        Node root = constrTreeFromPrePost(pre, post);
        BinarySearchTree bst = new BinarySearchTree(root);
        System.out.println("preorder traversal: ");
        bst.preorderTraversal(root);
        System.out.println();
        //populate next right at each level
        bst.populateNextRight(root);
        
        //do level order traverse using next right
        System.out.println("Level order traversal using next rt: ");
        bst.levelOrderTraverseUsingNextRt(root);
    }
    
    
    /*
     * construct tree from given inorder traversal or postorder traversal
     */
    public Node constrTreeFromPrePost(int[] pre, int[] post) {
        
        //identify top node or root node
        Node root = new Node(pre[0]);
        
        //identify left subtree elements
        int leftPreStartInd = -1;
        int leftPreEndInd = -1;
        int leftPostStartInd = -1;
        int leftPostEndInd = -1;
        int i = -1;
        int numPostElem = -1;
        
        //identify right subtree elements
        int rightPreStartInd = -1;
        int rightPreEndInd = -1;
        
        int rightPostStartInd = -1;
        int rightPostEndInd = -1;
        
        int preOrdrSuc  = -1;
        
        if (pre.length > 1) {
            
            //get preorder successor
            preOrdrSuc = pre[1];
            
           
         
            //search for preOrdrSuc in postOrdr
            for (i = 0; i < post.length; i++) {
                if (post[i] == preOrdrSuc) 
                    break;
            }
            
            //set start and end ind for left subtree post order
            leftPostEndInd = i;
            leftPostStartInd = 0;
            
            
            //num of elements in left subtree
            numPostElem = leftPostEndInd - leftPostStartInd + 1;
            
            //set start and end ind for left subtree pre order
            leftPreStartInd = 1;
            leftPreEndInd = leftPreStartInd + numPostElem - 1;
            
            if (leftPreEndInd < pre.length - 1) {
                
                //set indices for right subtree
                rightPreStartInd = leftPreEndInd + 1;
                rightPreEndInd = pre.length - 1;
                
                rightPostStartInd = leftPostEndInd + 1;
                rightPostEndInd = pre.length - 2;
            }
            
            //add left child to current node
            if (leftPreStartInd >= 0) {
                root.setLeftChild(constrTreeFromPrePost(
                    Arrays.copyOfRange(pre, leftPreStartInd, leftPreEndInd + 1),
                    Arrays.copyOfRange(post, leftPostStartInd, leftPostEndInd + 1)));
            } else {
                root.setLeftChild(null);
            }
            
            //add right child to current node
            if (rightPreStartInd >= 0) {
                root.setRightChild(constrTreeFromPrePost(
                    Arrays.copyOfRange(pre, rightPreStartInd, rightPreEndInd + 1),
                    Arrays.copyOfRange(post, rightPostStartInd, rightPostEndInd + 1)));
            } else {
                root.setRightChild(null);
            }
        }
        
        return root;
        
    }
    
    /*
     * validate if tree is a BST or not
     */
    public void validateBST() {
        Node root = new Node(10);
        root.setLeftChild(new Node(5));
        root.setRightChild(new Node(12));
        root.getLeftChild().setRightChild(new Node(9));
        root.getRightChild().setLeftChild(new Node(10));
        
        BinarySearchTree bst = new BinarySearchTree(root);
        System.out.println("is BST: " + bst.isBinarySearchTree(root, -100, 100));
        
    }
    
    
    public static void main(String[] args) {
        
        TreeMain bTree = new TreeMain();
        
        Vector<Integer> keys1 = new Vector<Integer>();
        Vector<Integer> keys2 = new Vector<Integer>();
        
        //parse commandline line by line to get keys
        //open up standard input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        System.out.println("Enter input keys for binary tree1 : ");
        
        try {
            String line = "";
            while((line = br.readLine()) != null) {
                /*if (Integer.parseInt(line) == 997) {
                    break;
                }*/
                keys1.add(Integer.parseInt(line));
            }
        } catch (IOException ioe) {
             System.out.println("IO error: " + ioe.getMessage());
        }
       
        
        
        bTree.binarySearchTreeMethods(keys1);
        
        //get input for second binary tree
        /*System.out.println("Enter input keys for binary tree1 : ");
        
        try {
            String line = "";
            while((line = br.readLine()) != null) {
                if (Integer.parseInt(line) == 997) {
                    break;
                }
                keys2.add(Integer.parseInt(line));
            }
        } catch (IOException ioe) {
             System.out.println("IO error: " + ioe.getMessage());
        }
        
        bTree.mergeTwoBSTs(keys1, keys2);*/
        
    }
    
}