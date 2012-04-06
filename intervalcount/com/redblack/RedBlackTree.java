package com.redblack;

import java.util.Vector;

public class RedBlackTree {
	
	private RedBlackNode nodeRoot;	//root
	private RedBlackNode nodeNil;	//leaves
	
	public RedBlackTree() {
		nodeNil = new RedBlackNode();
		nodeRoot = nodeNil;
	}
	
	
	public RedBlackNode getLeaf() {
		return nodeNil;
	}
	
	public void setRoot(RedBlackNode nodeX) {
		nodeRoot = nodeX;
	}
	
	//cormen fig 13.2 R-B tree
	public void LeftRotate(RedBlackNode nodeX) {
		
		//set y
		RedBlackNode nodeY = nodeX.getRight();
		
		//turn y's left into x's right
		nodeX.setRight(nodeY.getLeft());
		if (nodeY.getLeft() != nodeNil) {
			nodeY.getLeft().setParent(nodeX);
		}
		
		//link x's parent to y
		nodeY.setParent(nodeX.getParent());
		if (nodeX.getParent() == nodeNil) {
			nodeRoot = nodeY;
		} else if (nodeX == nodeX.getParent().getLeft()) {
			nodeX.getParent().setLeft(nodeY);
		} else {
			nodeX.getParent().setRight(nodeY);
		}
		
		nodeY.setLeft(nodeX);
		nodeX.setParent(nodeY);
	}
	
	public void RightRotate(RedBlackNode nodeY) {
		
		//set x
		RedBlackNode nodeX = nodeY.getLeft();
		
		//turn x's right into y's left
		nodeY.setLeft(nodeX.getRight());
		if (nodeX.getRight() != nodeNil) {
			nodeX.getRight().setParent(nodeY);
		}
		
		//link y's parent to x
		nodeX.setParent(nodeY.getParent());
		if (nodeY.getParent() == nodeNil) {
			nodeRoot = nodeX;
		} else if (nodeY == nodeY.getParent().getLeft()) {
			nodeY.getParent().setLeft(nodeX);
		} else {
			nodeY.getParent().setRight(nodeX);
		}
		
		nodeX.setRight(nodeY);
		nodeY.setParent(nodeX);
	}
	
	//insert a nodeZ with key already filled in
	public void insert(RedBlackNode nodeZ) {
		RedBlackNode nodeY = nodeNil;
		RedBlackNode nodeX = nodeRoot;
		
		while (nodeX != nodeNil) {
			nodeY = nodeX;
			if (nodeZ.getKey() < nodeX.getKey()) {
				nodeX = nodeX.getLeft();
			} else {
				nodeX = nodeX.getRight();
			}
		}
		
		nodeZ.setParent(nodeY);
		if (nodeY == nodeNil) {
			nodeRoot = nodeZ;
		} else if (nodeZ.getKey() < nodeY.getKey()) {
			nodeY.setLeft(nodeZ);
		} else {
			nodeY.setRight(nodeZ);
		}
		
		nodeZ.setLeft(nodeNil);
		nodeZ.setRight(nodeNil);
		nodeZ.setColor(RedBlackNode.Color.RED);
		insertFixUp(nodeZ);
	}
	
	public void insertFixUp(RedBlackNode nodeZ) {
		while (nodeZ.getParent() != nodeNil && 
				nodeZ.getParent().getColor() == RedBlackNode.Color.RED) {
			if (nodeZ.getParent() == nodeZ.getParent()
										.getParent().getLeft()) {
				
				//nodeY is uncle of nodeZ
				RedBlackNode nodeY = nodeZ.getParent()
										.getParent().getRight();
				
				if (nodeY.getColor() == RedBlackNode.Color.RED) {
					//Case 1 : see cormen : recoloring
					//recolor parent and uncle as black
					nodeZ.getParent().setColor(RedBlackNode.Color.BLACK);
					nodeY.setColor(RedBlackNode.Color.BLACK);
					
					//recolor grandparent as red
					nodeZ.getParent().getParent().setColor(
													RedBlackNode.Color.RED);
					
					//change nodeZ to grandparent and recurse
					nodeZ = nodeZ.getParent().getParent();
				} else { 
					if(nodeZ == nodeZ.getParent().getRight()) {
						//case 2 : see cormen
						//if nodeZ is right child
						nodeZ = nodeZ.getParent();
						LeftRotate(nodeZ);
					}
					//case 3
					nodeZ.getParent().setColor(RedBlackNode.Color.BLACK);
					nodeZ.getParent().getParent().setColor(
													RedBlackNode.Color.RED);
					RightRotate(nodeZ.getParent().getParent());
				}
			} else {
				// same as then clause with "left" and "right" interchange
				RedBlackNode nodeY = nodeZ.getParent()
											.getParent().getLeft();
				if (nodeY.getColor() == RedBlackNode.Color.RED) {
					//Case 1 : see cormen
					nodeZ.getParent().setColor(RedBlackNode.Color.BLACK);
					nodeY.setColor(RedBlackNode.Color.BLACK);
					nodeZ.getParent().getParent().setColor(
													RedBlackNode.Color.RED);
					nodeZ = nodeZ.getParent().getParent();
				} else { 
					if(nodeZ == nodeZ.getParent().getLeft()) {
						//case 2 : see cormen
						nodeZ = nodeZ.getParent();
						RightRotate(nodeZ);
					}
					//case 3
					nodeZ.getParent().setColor(RedBlackNode.Color.BLACK);
					nodeZ.getParent().getParent().setColor(
													RedBlackNode.Color.RED);
					LeftRotate(nodeZ.getParent().getParent());
				}
			}
		}
		
		nodeRoot.setColor(RedBlackNode.Color.BLACK);
	}
	
	
	public void transplant(RedBlackNode nodeU, RedBlackNode nodeV) {
		
		if (nodeU.getParent() == nodeNil) {
			nodeRoot = nodeV;
		} else if (nodeU == nodeU.getParent().getLeft()) {
			nodeU.getParent().setLeft(nodeV);
		} else {
			nodeU.getParent().setRight(nodeV);
		}
		
		nodeV.setParent(nodeU.getParent());
	}
	
	public RedBlackNode minimum(RedBlackNode nodeX) {
		while(nodeX.getLeft() != nodeNil) {
			nodeX = nodeX.getLeft();
		}
		return nodeX;
	}
	
	public void delete(RedBlackNode nodeZ) {
		
		RedBlackNode nodeY = nodeZ;
		RedBlackNode.Color nodeYOrigColor = nodeY.getColor();
		RedBlackNode nodeX = null;
		
		if (nodeZ.getLeft() == nodeNil) {
			nodeX = nodeZ.getRight();
			transplant(nodeZ, nodeZ.getRight());
		} else if (nodeZ.getRight() == nodeNil) {
			nodeX = nodeZ.getLeft();
			transplant(nodeZ, nodeZ.getLeft());
		} else {
			nodeY = minimum(nodeZ.getRight());
			nodeYOrigColor = nodeY.getColor();
			nodeX = nodeY.getRight();
			if (nodeY.getParent() == nodeZ) {
				nodeX.setParent(nodeY);
			} else {
				transplant(nodeY, nodeY.getRight());
				nodeY.setRight(nodeZ.getRight());
				nodeY.getRight().setParent(nodeY);
			}
			transplant(nodeZ, nodeY);
			nodeY.setLeft(nodeZ.getLeft());
			nodeY.getLeft().setParent(nodeY);
			nodeY.setColor(nodeZ.getColor());
		}
		
		if (nodeYOrigColor == RedBlackNode.Color.BLACK) {
			deleteFixUp(nodeX);
		}
		
	}
	
	public void deleteFixUp(RedBlackNode nodeX) {
		while (nodeX != nodeRoot && nodeX.getColor() == 
													RedBlackNode.Color.BLACK) {
			if (nodeX == nodeX.getParent().getLeft()) {
				RedBlackNode nodeW = nodeX.getParent().getRight();
				if (nodeW.getColor() == RedBlackNode.Color.RED) {
					//case 1
					nodeW.setColor(RedBlackNode.Color.BLACK);
					nodeX.getParent().setColor(RedBlackNode.Color.RED);
					LeftRotate(nodeX.getParent());
					nodeW = nodeX.getParent().getRight();
				}
				if (nodeW.getLeft().getColor() == RedBlackNode.Color.BLACK
						&& nodeW.getRight().getColor() == RedBlackNode.Color.BLACK) {
					//case 2
					nodeW.setColor(RedBlackNode.Color.RED);
					nodeX = nodeX.getParent();
				} else {
					if (nodeW.getRight().getColor() == RedBlackNode.Color.BLACK) {
						//case 3
						nodeW.getLeft().setColor(RedBlackNode.Color.BLACK);
						nodeW.setColor(RedBlackNode.Color.RED);
						RightRotate(nodeW);
						nodeW = nodeX.getParent().getRight();
					}
					//case 4
					nodeW.setColor(nodeX.getParent().getColor());
					nodeX.getParent().setColor(RedBlackNode.Color.BLACK);
					nodeW.getRight().setColor(RedBlackNode.Color.BLACK);
					LeftRotate(nodeX.getParent());
					nodeX = nodeRoot;
				}
			} else {
				//same as then clause exchange "left" <-> "right"
				RedBlackNode nodeW = nodeX.getParent().getLeft();
				if (nodeW.getColor() == RedBlackNode.Color.RED) {
					//case 1
					nodeW.setColor(RedBlackNode.Color.BLACK);
					nodeX.getParent().setColor(RedBlackNode.Color.RED);
					RightRotate(nodeX.getParent());
					nodeW = nodeX.getParent().getLeft();
				}
				if (nodeW.getRight().getColor() == RedBlackNode.Color.BLACK
						&& nodeW.getLeft().getColor() == RedBlackNode.Color.BLACK) {
					//case 2
					nodeW.setColor(RedBlackNode.Color.RED);
					nodeX = nodeX.getParent();
				} else {
					if (nodeW.getLeft().getColor() == RedBlackNode.Color.BLACK) {
						//case 3
						nodeW.getRight().setColor(RedBlackNode.Color.BLACK);
						nodeW.setColor(RedBlackNode.Color.RED);
						LeftRotate(nodeW);
						nodeW = nodeX.getParent().getLeft();
					}
					//case 4
					nodeW.setColor(nodeX.getParent().getColor());
					nodeX.getParent().setColor(RedBlackNode.Color.BLACK);
					nodeW.getLeft().setColor(RedBlackNode.Color.BLACK);
					RightRotate(nodeX.getParent());
					nodeX = nodeRoot;
				}
			}
			
		}
		
		nodeX.setColor(RedBlackNode.Color.BLACK);
	}
	
	//bfs traversal
	public void levelOrderWalk(RedBlackNode node) {
		
		Vector<RedBlackNode> queue = new Vector<RedBlackNode>();
		if (node != nodeNil) {
			queue.insertElementAt(node, 0);
			while (queue.size() > 0) {
				RedBlackNode lastElem = queue.remove(queue.size()-1);
				System.out.println(lastElem.getKey() + "\t" 
									+ lastElem.getColor() + '\t' 
									+ getBlackHeight(lastElem));
				
				if (lastElem.getLeft() != nodeNil) {
					queue.insertElementAt(lastElem.getLeft(), 0);
				}
				
				if (lastElem.getRight() != nodeNil) {
					queue.insertElementAt(lastElem.getRight(), 0);
				}
				
			}
		}
		
		
	}
	
	//TODO: inorder treewalk returning array list of all nodes in tree
	public void inorderTreeWalk(RedBlackNode node) {
		if (node != nodeNil) {
			inorderTreeWalk(node.getLeft());
			System.out.println(node.getKey()+"\t" + node.getColor() + '\t'
									+ getBlackHeight(node));
			inorderTreeWalk(node.getRight());
		}
	}
	
	public RedBlackNode getRoot() {
		return nodeRoot;
	}
	
	public int getBlackHeight(RedBlackNode node) {
		//count the number of black nodes in path to leaves
		int height = 1; //counting nodeNil as 1 for sure in leaves
		while (node.getLeft() != nodeNil) {
			node = node.getLeft();
			if (node.getColor() == RedBlackNode.Color.BLACK) {
				height++;
			}
		}
		return height;
	}
	
}
