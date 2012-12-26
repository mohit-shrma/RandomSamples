/*
 * Node class
 */
class Node {
	
	private Node left;
	private Node right;
	private Node parent;
	private int key;
	private int depth;
	
	public Node(Node left, Node right, int key) {
		this(left, right, key, null);
	}
	
	public Node(Node left, Node right, int key, Node parent) {
		this.left = left;
		this.right = right;
		this.parent = parent;
		this.key = key;
	}
	 
	
	public void setLeftChild(Node left) {
		this.left = left;
	}
	
	public void setRightChild(Node right) {
		this.right = right;
	}
	
	public void setKey(int key) {
		this.key = key;
	}
	
	public void setParent(Node parent) {
		this.parent = parent;
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
	
	public void setDepth(int depth) {
		this.depth = depth;
	}
	
	public int getDepth() {
		return depth;
	}
	
}