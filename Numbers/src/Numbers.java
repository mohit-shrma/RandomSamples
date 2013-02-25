import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;


class Numbers {
    
    private int num;
    
    public Numbers(int num) {
        this.num = num;
    }
    
    public void numberMethods() {
        int size = NumberUtil.sizeInBits(num);
        System.out.println("number size in bits: " + size);
        System.out.println("is number palindrome: " + 
                                NumberUtil.isPalindrome(num));
        
        System.out.println("To binary: " + NumberUtil.toBinary(num));
        System.out.println("Reverse to bin: " + 
                            NumberUtil.toBinary(NumberUtil.reverse(num)));
        System.out.println("Reverse to bin div N Con: " + 
                    Integer.toBinaryString(NumberUtil.reverseByDivNCon(num)));
    }
    
    
    
    public static void main(String[] args) {

        //parse commandline line by line to get keys
        //open up standard input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        try {
            System.out.println("Enter number: ");
            String line = br.readLine();
            int number = Integer.parseInt(line);
            Numbers numbers = new Numbers(number);
            numbers.numberMethods();
        }catch (IOException e) {
            System.out.println("IO error: " + e.getMessage());
        }
        
    }
}