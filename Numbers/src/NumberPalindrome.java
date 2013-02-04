//TODO: import math
import java.lang.Math;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

class NumberPalindrome {

    private int num;

    public NumberPalindrome(int num) {
        this.num = num;
    }

    public boolean isPalindrome() {
    	int numDigits = 0;
    	int temp = num;
    	while (temp > 0) {
    	    numDigits++;
    	    temp = temp/10;
    	}
    	temp = num;
    	int count = numDigits - 1;
    	while (count > 0 && temp > 0) {
    	    
    	    int startDigit = temp / (int)Math.pow(10, count);
    	    int remDigit = temp % (int)Math.pow(10, count);
    	    int lastDigit = temp % 10;
    	    if (lastDigit != startDigit) {
    	        return false;
    	    }
    	    temp = remDigit/10;
    	    count -= 2;
    	}
    
    	return true;
    }

    public static void main(String[] args) {

	//parse commandline line by line to get keys
        //open up standard input
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        
        try {
            System.out.println("Enter number to check for palindrome: ");
            String line = br.readLine();
            int number = Integer.parseInt(line);
	    
	    NumberPalindrome numPalind = new NumberPalindrome(number);
	    
            System.out.println("is palindrome: " + numPalind.isPalindrome());
                    
        }catch (IOException e) {
            System.out.println("IO error: " + e.getMessage());
        }

	
    }
}