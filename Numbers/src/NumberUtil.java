//TODO: import math
import java.lang.Math;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

class NumberUtil {

    public static int sizeInBits(int num) {
        int count = 0;
        while (num != 0) {
            count++;
            num = num >> 1;
        }
        return count;
    }
    
    public static boolean isPalindrome(int num) {
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
    
    
    public static String toBinary(int num) {
        String binStr = "";
        while (num != 0) {
            binStr = (num % 2) + binStr;
            num = num / 2;
        }
        return binStr;
    }
    
    
    // swap ith bit with jth bit of num
    public static int bitSwap(int i, int j, int num) {
        //xor ith and jth bit to check if different
        int iBit = (num >> i) & 1;
        int jBit = (num >> j) & 1;
        if ((iBit ^ jBit) == 1) {
            //need to swap bits, xor ith & jth bit with one to toggle them
            num = num ^ ((1<<i) | (1<<j));
        }
        return num;
    }
    
    
    //reverse bit of numbers
    //swap the bits from LSB half with MSB half
    public static int reverse(int num) {
        int size = sizeInBits(num);
        for (int i = 0; i < size/2; i++) {
            num = bitSwap(i, (size - i) - 1, num);
        }
        return num;
    }
    
    
    /*
     * reverse by using divide and conquer approach for bits
     * swap first all odd and even bits
     * then swap two bits bit neighbor, then four ...
     * O(lgn) complexity. Following work for number till 32 bits of 
     * representation
     */
    public static int reverseByDivNCon(int num) {
        if (sizeInBits(num) <= 32) {
            
            //System.out.println(Integer.toBinaryString(num));
            //swap odd & even bits
            num = ((num & 0x55555555) << 1) | ((num & 0xAAAAAAAA) >> 1);
            //System.out.println(Integer.toBinaryString(num));
            
            //swap two bits with the other two 
            num = ((num & 0x33333333) << 2) | ((num & 0xCCCCCCCC) >> 2);
            //System.out.println(Integer.toBinaryString(num));
            
            //swap 4 bits with other 4
            num = ((num & 0x0F0F0F0F) << 4) | ((num & 0xF0F0F0F0) >> 4);
            //System.out.println(Integer.toBinaryString(num));
            
            //swap 8 bits with other 8
            num = ((num & 0x00FF00FF) << 8) | ((num & 0xFF00FF00) >> 8);
            //System.out.println(Integer.toBinaryString(num));
            
            //swap one half with the other
            num = ((num & 0x0000FFFF) << 16) | ((num & 0xFFFF0000) >> 16);
            //System.out.println(Integer.toBinaryString(num));
            return num;
        } else {
            System.out.println("reverse using divide and con supported till" 
                                + " 32 bits only");
            return -1;
        }
    }

    
}