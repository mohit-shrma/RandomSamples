package com.redblack;


public class RedBlackNode {
	
	public enum Color {RED, BLACK};
	
	private RedBlackNode left;
	private RedBlackNode right;
	private RedBlackNode parent;
	private int key;
	private Color color;
	
	
	public RedBlackNode() {
		this(null, null, null, -1);
	}
	
	public RedBlackNode(int key) {
		//TODO: check if need to set parent or leaves to nil
		this(null, null, null, key);
	}

	public RedBlackNode(RedBlackNode left, RedBlackNode right, 
						RedBlackNode parent, int key) {
		this.left = left;
		this.right = right;
		this.parent = parent;
		this.key = key;
	}
	
	public Color getColor() {
		return color;
	}
	
	public RedBlackNode getRight() {
		return right;
	}
	
	public RedBlackNode getLeft() {
		return left;
	}
	
	public RedBlackNode getParent() {
		return parent;
	}
	
	public int getKey() {
		return key;
	}
	
	public void setColor(Color color) {
		this.color = color;
	}
	
	public void setRight(RedBlackNode right) {
		this.right = right;
	}
	
	public void setLeft(RedBlackNode left) {
		this.left = left;
	}
	
	public void setParent(RedBlackNode parent) {
		this.parent = parent;
	}
	
	public void setKey(int key) {
		this.key = key;
	}
	
}
