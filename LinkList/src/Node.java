/*
 * defines the structure of a node in a link list
 */

class Node {
    
    //value in a node
    int key;
    
    //pointer to next node in link list
    Node next;
    
    //pointer to previous node in link list
    Node prev;
    
    public Node(int key, Node next, Node prev) {
        this.key = key;
        this.next = next;
        this.prev = prev;
    }
    
    public Node(int key) {
        this(key, null, null);
    }

    public Node(int key, Node next) {
        this(key, next, null);
    }
    
    public void setNext(Node node) {
        this.next = node;
    }
    
    public Node getNext() {
        return next;
    }
    
    public int getKey(){
        return key;
    }
    
    public String toString() {
        return "" + key;
    }
}
