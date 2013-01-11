/*
 * Node class
 */
class Node {
	
    //left child
	private Node left;
	
	//right child
	private Node right;
	
	//parent of child
	private Node parent;
	
	//inorder successor of current node
	private Node next;
	
	//key value of node
	private int key;
	
	//depth/height of node
	private int depth;
	
	//next right node at same level
	private Node nextRight;
	
	
	public Node(Node left, Node right, int key) {
		this(left, right, key, null);
	}
	
	public Node(Node left, Node right, int key, Node parent) {
		this.left = left;
		this.right = right;
		this.parent = parent;
		this.key = key;
	}
	
	public Node(Node node) {
	    this.left = node.left;
	    this.right = node.right;
	    this.parent = node.parent;
	    this.next = node.next;
	    this.key = node.key;
	    this.depth = node.depth;
	}
	 
	
	public void setLeftChild(Node left) {
		this.left = left;
	}
	
	public void setRightChild(Node right) {
		this.right = right;
	}
	
	public void setNext(Node next) {
	    this.next = next;
	}
	
	public void setKey(int key) {
		this.key = key;
	}
	
	public void setParent(Node parent) {
		this.parent = parent;
	}
	
	public void setNextRight(Node nextRight) {
	    this.nextRight = nextRight;
	}
	
	public Node getParent() {
		return parent;
	}
	
	public int getKey() {
		return key;
	}
	
	public Node getLeftChild() {
		return left;
	}
	
	public Node getRightChild() {
		return right;
	}
	
	public Node getNext() {
	    return next;
	}
	
	public Node getNextRight() {
	    return nextRight;
	}
	
	public void setDepth(int depth) {
		this.depth = depth;
	}
	
	public int getDepth() {
		return depth;
	}
	
}