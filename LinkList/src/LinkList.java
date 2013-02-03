import java.util.Vector;

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
     * will make the link list cyclic
     */
    public void makeListCyclic() {
        Node endNode = head;
        while (endNode.getNext() != null) {
            endNode = endNode.getNext();
        }
        //point last node to head to make it cyclic
        endNode.setNext(head);
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
    
    
    /*
     * check whether link list has cycle, returns a node in the loop
     */
    public Node isCyclePresent() {
        //initialize slow and fast pointer
        Node slowPtr = head;
        Node fastPtr = head;
        
        while (slowPtr != null && fastPtr != null) {
            slowPtr = slowPtr.getNext();
            fastPtr = fastPtr.getNext();
            if (fastPtr != null) {
                //can move ahead
                fastPtr = fastPtr.getNext();
            } else {
                //reached end
                return null;
            }
            if (slowPtr == fastPtr) {
                //fast pointer overtakes slow pointer
                return slowPtr;
            }
        }
        
        return null;
        
    }
    
    
    /*
     * get the point where the cycle starts in the link list
     */
    private Node getLoopStartNode(Node loopNode) {
        
        //get the loop length of node
        int loopLength = 0;
        Node startNode = loopNode.getNext();
        while(startNode != loopNode) {
            startNode = startNode.getNext();
            loopLength++;
        }
        loopLength += 1; //for last node
        
        //pointer to head
        startNode = head;
        
        //forward node which is ahead of head by loop length
        Node forwardNode = head;
        int forwardSteps = 0;
        while (forwardSteps < loopLength) {
            forwardNode = forwardNode.getNext();
            forwardSteps++;
        }
        
        //advance both start and forward 1 by 1 they should meet at start of loop
        while (startNode != forwardNode) {
            startNode = startNode.getNext();
            forwardNode = forwardNode.getNext();
        }
        
        //Node loopStart = startNode;
        
        return startNode;
        
    }
    
    
    /*
     * remove the cycle from the link list
     */
    public void removeCycle() {
        //first verify if cycle present in link list
        Node loopNode = isCyclePresent();
        if (loopNode != null) {
            //cycle is present in the link list
            Node startNode = getLoopStartNode(loopNode);
            
            //find last loop node
            Node endNode = startNode.getNext();
            while (endNode.getNext() != startNode) {
                endNode = endNode.getNext();
            }
            
            //set the next of this end node to null remove the loop
            endNode.setNext(null);
            
        }
    }
    
    /*
     * TODO: search in sorted rotated linklist
     */
    
    /*
     *Split the nodes of the given list into front and back halves,
     *and return the two lists using the reference parameters.
     *If the length is odd, the extra node should go in the front list.
     */
     private Vector<Node> frontBackSplit(Node head) {
         
         Node frontHead = null;
         Node backHead = null;
         //Node[] frontBackHalves = {frontHead, backHead};
         Vector<Node> frontBackHalves = new Vector<Node>();
         if (head == null || head.getNext() == null) {
             //length of list is < 2
             frontHead = head;
             backHead = null;
         } else {
             Node slowPtr = head;
             Node fastPtr = head.getNext();
             //make fast move twice as fast as the slow
             while (fastPtr != null) {
                 fastPtr = fastPtr.getNext();
                 if (fastPtr != null) {
                     fastPtr = fastPtr.getNext();
                     slowPtr = slowPtr.getNext();
                 }
             }
             //slow ptr will be before the middle of the list
             //we should split at that point
             frontHead = head;
             backHead = slowPtr.getNext();
             //detach slow ptr or detach first list
             slowPtr.setNext(null);
         }
         frontBackHalves.add(frontHead);
         frontBackHalves.add(backHead);
         return frontBackHalves;
     }

     
     /*
      * linearly merge the passed sorted list
      */
     private Node sortedMerge(Node front, Node back) {
         
         Node merged = null;
         
         if (front == null) {
             return back;
         } else if (back == null) {
             return front;
         }
         
         if (front.getKey() < back.getKey()) {
             //front head is lesser so should be added to merged
             merged = front;
             merged.setNext(sortedMerge(front.getNext(), back));
         } else {
             //back head is smaller so should be added to merged
             merged = back;
             merged.setNext(sortedMerge(front, back.getNext()));
         }
         
         return merged;
     }
     
    
    /*
     * merge sort the link list, return head of the new sorted list
     */
    public Node mergeSortList(Node head) {
        
        if (head == null || head.getNext() == null) {
            return head;
        }
        
        //divide the list in two half
        Vector<Node> frontBackHalves = frontBackSplit(head);
        Node front = frontBackHalves.elementAt(0);
        Node back = frontBackHalves.elementAt(1);
        front = mergeSortList(front);
        back = mergeSortList(back);
        
        //linearly merge the sorted list, and return head to merged list
        return sortedMerge(front, back);
    }
   
    
    /*
     * merge sort the link list
     */
    public void mergeSort() {
        head = mergeSortList(head);
    }
}