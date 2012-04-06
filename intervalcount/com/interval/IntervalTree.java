package com.interval;

import java.util.Vector;

import com.redblack.RedBlackNode;
import com.redblack.RedBlackTree;

public class IntervalTree extends RedBlackTree {

	
	
	//will be passing interval node as arg, WARNING: need to reusse
	public void LeftRotate(RedBlackNode nodeX) {
		
		super.LeftRotate(nodeX);
		
		//update maxhi for nodeX
		updateMaxHi((IntervalNode) nodeX);
		
		//update maxhi for nodeY
		updateMaxHi((IntervalNode) nodeX.getParent());
	}
	
	public void RightRotate(RedBlackNode nodeY) {
		
		super.RightRotate(nodeY);
		
		//update maxhi for nodeX
		updateMaxHi((IntervalNode) nodeY);
		
		//update maxhi for nodeY
		updateMaxHi((IntervalNode) nodeY.getParent());
		
		
	}
	
	public void insert(RedBlackNode nodeZ) {
		RedBlackNode nodeY = getLeaf();
		RedBlackNode nodeX = getRoot();
		
		while (nodeX != getLeaf()) {
			nodeY = nodeX;
			
			//update maxHi for nodeY, as nodeZ will got its left or right
			if (((IntervalNode) nodeY).getMaxHi() < 
					((IntervalNode) nodeZ).getHigh()) {
				((IntervalNode) nodeY).setMaxHi(
										((IntervalNode) nodeZ).getHigh());
			}
			
			if (nodeZ.getKey() < nodeX.getKey()) {
				nodeX = nodeX.getLeft();
			} else {
				nodeX = nodeX.getRight();
			}
		}
		
		nodeZ.setParent(nodeY);
		if (nodeY == getLeaf()) {
			setRoot(nodeZ);
		} else if (nodeZ.getKey() < nodeY.getKey()) {
			nodeY.setLeft(nodeZ);
		} else {
			nodeY.setRight(nodeZ);
		}
		
		nodeZ.setLeft(getLeaf());
		nodeZ.setRight(getLeaf());
		nodeZ.setColor(RedBlackNode.Color.RED);
		insertFixUp(nodeZ);
	}
	
	private void updateMaxHi(IntervalNode nodeX) {
		
		int maxHi = nodeX.getHigh();
		
		if (nodeX.getLeft() != getLeaf()) {
			if (maxHi < ((IntervalNode)nodeX.getLeft()).getMaxHi()) {
				maxHi = ((IntervalNode)nodeX.getLeft()).getMaxHi();
			}
		}
		
		if (nodeX.getRight() != getLeaf()) {
			if (maxHi < ((IntervalNode)nodeX.getRight()).getMaxHi()) {
				maxHi = ((IntervalNode)nodeX.getRight()).getMaxHi();
			}
		}
		
		nodeX.setMaxHi(maxHi);
	}
	
	//bfs traversal
	public void levelOrderWalk(RedBlackNode node) {
		
		Vector<RedBlackNode> queue = new Vector<RedBlackNode>();
		if (node != getLeaf()) {
			queue.insertElementAt(node, 0);
			while (queue.size() > 0) {
				RedBlackNode lastElem = queue.remove(queue.size()-1);
				System.out.println(lastElem.getKey() + "\t" 
									+ ((IntervalNode)lastElem).getHigh() + "\t"
									+ ((IntervalNode)lastElem).getMaxHi() + "\t"
									+ lastElem.getColor() + '\t' 
									+ getBlackHeight(lastElem));
				
				if (lastElem.getLeft() != getLeaf()) {
					queue.insertElementAt(lastElem.getLeft(), 0);
				}
				
				if (lastElem.getRight() != getLeaf()) {
					queue.insertElementAt(lastElem.getRight(), 0);
				}
				
			}
		}
	}
	
	
	public void inorderTreeWalk(RedBlackNode node) {
		if (node != getLeaf()) {
			inorderTreeWalk(node.getLeft());
			System.out.println(node.getKey() + "\t"
								+ ((IntervalNode)node).getHigh() + "\t"
								+ ((IntervalNode)node).getMaxHi() + "\t"
								+ node.getColor() + '\t'
								+ getBlackHeight(node));
			inorderTreeWalk(node.getRight());
		}
	}
	private boolean isOverlap(IntervalNode node1, IntervalNode node2) {
		if (node1.getLow() > node2.getHigh() 
				|| node1.getHigh() <  node2.getLow()) {
			return false;
		} else {
			return true;
		}
	}
	
	public IntervalNode intervalSearch(IntervalNode query) {
		RedBlackNode x = getRoot();
		while (x != getLeaf() && !isOverlap(query, (IntervalNode)x) ) {
			if (x.getLeft() != getLeaf() && 
					((IntervalNode)x.getLeft()).getMaxHi() >= query.getLow()) {
				x = x.getLeft();
			} else {
				x = x.getRight();
			}
		}
		return (IntervalNode) x;
	}
	
	private IntervalNode getMergedInterval(IntervalNode node1,
											IntervalNode node2) {

		int low = -1, high = -1;
		
		//if node2 low is in between node 1
		if (node2.getLow() <= node1.getHigh() 
				&& node2.getHigh() >= node1.getHigh()) {
			low = node1.getLow() < node2.getLow() ? node1.getLow():node2.getLow();
			high = node2.getHigh();
		}
		
		//if node2 high is in b/w
		if (node2.getHigh() >= node1.getLow() 
				&& node2.getHigh() <= node1.getHigh()) {
			low = node1.getLow() < node2.getLow() ? node1.getLow():node2.getLow();
			high = node1.getHigh();
		}
		
		
		return new IntervalNode(low, high);
	}
	
	//parse tree in inorder and push nodes in stack and return it
	public Vector<IntervalNode> inOrderWalk(RedBlackNode node,
												Vector<IntervalNode> walkedNode) {
		if (node != getLeaf()) {
			inOrderWalk(node.getLeft(), walkedNode);
			walkedNode.addElement((IntervalNode) node);
			inOrderWalk(node.getRight(), walkedNode);
		}
		
		return walkedNode;
	}
	
	
	public Vector<IntervalNode> inOrderMergedWalk(RedBlackNode node, 
									Vector<IntervalNode> mergedWalkNodeStack ) {
		
		
		if (node != getLeaf()) {
			
			inOrderMergedWalk(node.getLeft(), mergedWalkNodeStack);
			
			if (mergedWalkNodeStack.size() > 0) {
				//pop the last one and merge if overlap
				IntervalNode popped = mergedWalkNodeStack.elementAt(
													mergedWalkNodeStack.size()-1);
				mergedWalkNodeStack.removeElementAt(mergedWalkNodeStack.size()-1);
				
				if (isOverlap((IntervalNode) node, popped)) {
					//merge and push
					mergedWalkNodeStack.addElement(getMergedInterval(popped, (IntervalNode) node));
				} else {
					//push 'popped' then 'node'
					mergedWalkNodeStack.addElement(popped);
					mergedWalkNodeStack.addElement((IntervalNode) node);
				}
			} else {
				mergedWalkNodeStack.addElement((IntervalNode) node);
			}
			
			inOrderMergedWalk(node.getRight(), mergedWalkNodeStack);
		}
		
		return mergedWalkNodeStack;
	}
	
	public int countGaps(int start, int end) {
		Vector<IntervalNode> mergedWalkNodeStack = new Vector<IntervalNode>();
		inOrderMergedWalk(getRoot(), mergedWalkNodeStack);
		int gapCount = 0;
		IntervalNode lastIntervalNode = null;
		for (IntervalNode  intervalNode : mergedWalkNodeStack) {
			
			if (lastIntervalNode == null) {
				gapCount += intervalNode.getLow() - start;
			} else {
				gapCount += intervalNode.getLow() 
								- lastIntervalNode.getHigh() - 1;
			}
			lastIntervalNode = intervalNode;
		}
		if (lastIntervalNode != null) {
			gapCount += end - lastIntervalNode.getHigh();
		}
		return gapCount;
	}
	
	
	
}