package com.interval;

import com.redblack.RedBlackNode;

public class IntervalNode extends RedBlackNode {
	
	
	private int low;
	private int high;
	private int maxHi;
	private String scaffName;
	
	public IntervalNode(int low, int high) {
		super(low);
		this.low = low;
		this.high = high;
		this.maxHi = high;
		this.scaffName = null;
	}
	
	public IntervalNode(int low, int high, String scaffName) {
		super(low);
		this.low = low;
		this.high = high;
		this.maxHi = high;
		this.scaffName = scaffName;
	}
	
	public IntervalNode() {
		super();
		this.low = -1;
		this.high = -1;
		this.maxHi = -1;
		this.scaffName = null;
	}
	
	public int getLow() {
		return low;
	}
	
	public int getHigh() {
		return high;
	}
	
	public void setMaxHi(int hi) {
		this.maxHi = hi;
	}
	
	public int getMaxHi() {
		return maxHi;
	}	
	
	public String getScaffName() {
		return scaffName;
	}
	
}
