/*
 * contains all methods applicable on an link list
 */ 

class LinkList {
    
    //starting node of link list
    private Node head;
    
    //last node of linklist
    private Node end;
    
    public LinkList(Node head) {
        this.head = head;
    }
    
    public LinkList(int key) {
        this.head = new Node(key);
    }
    
    public LinkList() {
        this.head = null;
    }
    
    /*
     * create link list using passed keys and return head
     */
    public Node createLinkList(int[] keys) {
        
        Node temp = head;
        
        for (int key: keys) {
            if (head == null) {
                head = new Node(key);
                temp = head;
            } else {
                temp.setNext(new Node(key));
                temp = temp.getNext();
            }
        }
        
        return head;
    }
    
    
    /*
     * display contents of linklist from start
     */
    public void displayFromStart() {
        
        Node temp = head;
        while(temp != null) {
            System.out.print(temp + " ");
            temp = temp.getNext();
        }
    }

    /*
     * display contents from end of the link list
     */
    public void displayFromEnd(Node node) {
        
        if (node == null) {
            //reach the end don't do anything here
            return;
        }
        
        displayFromEnd(node.getNext());
        System.out.print(node.getKey() + " ");
    }
    
    
    /*
     * recursively reverse a link list
     */
    public Node revLinkListRecur(Node node, Node prev) {
        
        if (node.getNext() == null) {
            //reached last node, make this node new head
            head = node;
            return node;
        }
        
        //reverse all nodes next to current and get the new previous node
        Node newPrev = revLinkListRecur(node.getNext(), node);
        //assign the node next to new previous node
        newPrev.setNext(node);
        //reset the current node next pointer
        node.setNext(null);
        
        return node;
    }
    
   
    
}