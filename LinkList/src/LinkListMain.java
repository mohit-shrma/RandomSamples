import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Vector;



class LinkListMain {
    
    
    public void linkListMethods(int[] keys) {
        
        //create empty link list
        LinkList linkList =  new LinkList();
        
        //construct link list with keys
        Node head = linkList.createLinkList(keys);
        
        System.out.println("link list from start: ");
        linkList.displayFromStart();
        System.out.println();
        
        System.out.println("link list from end: ");
        linkList.displayFromEnd(head);
        System.out.println();
        
        System.out.println("link list after reversal: ");
        linkList.revLinkListRecur(head, null);
        linkList.displayFromStart();
        System.out.println();
    }
    
    
    public static void main(String[] args) {
        
        LinkListMain linkListMain = new LinkListMain();
        
        //parse commandline line by line to get keys
        //open up standard input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        try {
            System.out.println("Enter no. of keys for link list: ");
            String line = br.readLine();
            int size = Integer.parseInt(line);
            
            //keys array to store key
            int[] keys = new int[size];
            System.out.println("Enter keys line by line: ");
            for (int i = 0; i < size; i++) {
                keys[i] = Integer.parseInt(br.readLine());
            }
            
            linkListMain.linkListMethods(keys);
            
        }catch (IOException e) {
            System.out.println("IO error: " + e.getMessage());
        }
        
    }
    
}