import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Vector;


/*
 * pretty print a text by applying dynamic programming to minimize slack/cost
 * reference: http://web.media.mit.edu/~dlanman/courses/cs157/HW5.pdf
 */

class PrettyPrint {
	
	private final int INF = 1000000;
	
	/*
	 * get the vector of words from the passed text file
	 */
	private Vector<String> getWords(String textFileName) {
		Vector<String> words = new Vector<String>(10);
		try {
			FileInputStream fstream  = new FileInputStream(textFileName);
			DataInputStream in = new DataInputStream(fstream);
			BufferedReader br = new BufferedReader(new InputStreamReader(in));
			String line = "";
			String[] temp = null;
			while ((line = br.readLine()) != null) {
				//assuming words are separated by single space " ", 
				//split around it
				temp = line.split(" ");
				
				for (String word: temp) {
					//add words to word vector
					words.add(word);
				}
			}
			
		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
		
		return words;
	}
	
	
	/*
	 * get the  words len from the passed words
	 */
	private int[] getWordsLen(Vector<String> words) {
		//no. of words
		int numWords = words.size();
		
		//initialize the words length array
		int[] wordsLen = new int[numWords];
		
		//get the words length into array
		int i = 0;
		for (String word: words) {
			wordsLen[i++] = word.length();
		}
		
		return wordsLen;
	}
	
	/*
	 * construct a slack table 
	 * L - length/no. of chars in a line
	 * 
	 * total no. of printed chars in a line
	 * N[i,k] = sum< i<=j<=k > { wordsLen[j] + (k - i) }
	 * 
	 * also, we have
	 * N[i,k] = N[1,k] - N[1,i-1] - 1 for i > 1 
	 * 
	 * slack is defined as below
	 * S[i,k]^2 = if (L - N(i,K) >= 0 then (L - N(i,k))^2; else inf
	 * 
	 */
	private int[][] constructSlackTable(int[] wordsLen, int lineLength) {
		
		//number of words
		int numWords = wordsLen.length;
		
		//initialize slack table -> S in comments above
		int[][] slackTable = new int [numWords][numWords];
		for (int i = 0; i < numWords; i++) {
			for (int j = 0; j < numWords; j++) {
				slackTable[i][j] = -1; //inf
			}
		}
		slackTable[0][0] = wordsLen[0];
		
		//initialize "last allowed word on a line" storage
		int[] lastWord = new int[numWords];
		lastWord[0] = numWords -1;
		
		//fill first row of slack table
		for (int i = 1; i < numWords; i++) {
			slackTable[0][i] = slackTable[0][i - 1] + wordsLen[i];
		}
		
		//fill remaining rows of slack table
		for (int i = 1; i < numWords; i++) {
			int k = i;
			slackTable[i][k] = slackTable[1][k] - slackTable[1][i-1];
			//while you can add more words to a line
			while (k <= numWords - 2 && 
					(lineLength - slackTable[i][k] - (k - i)) > 0) {
				k++;
				slackTable[i][k] = slackTable[0][k] - slackTable[0][i-1];
			}
			lastWord[i] = k;
		}
		
		//evaluate sum of squares for valid entries
		for (int i = 0; i < numWords; i++) {
			for (int k = i; k <= lastWord[i]; k++) {
				slackTable[i][k] = lineLength - slackTable[i][k] - (k - i);
				if (slackTable[i][k] < 0) {
					slackTable[i][k] = INF; //inf
				} else {
					slackTable[i][k] = slackTable[i][k] * slackTable[i][k]; 
				}
			}
		}
		
		//make 'INF' those which are still < 0 or aren't touched by above
		//as they are invalid entries
		for (int i = 0; i < numWords; i++) {
			for (int j = 0; j < numWords; j++) {
				if (slackTable[i][j] < 0) {
					slackTable[i][j] = INF;//inf
				}
			}
		}
		
		return slackTable;
	}
	
	
	/*
	 * returns list of indices of first word on each line
	 * fact used: once a minimum cost partition of words to a set of lines has 
	 * been discovered, the inclusion of additional words can only 
	 * alter configuration of last line.
	 * recurrence relation on minimum cost C[i] of arranging first i words in text
	 * C[i] = { 0                                if i = 0; 
	 *          min< 1<=k<=i > C[k - 1] + S[k,i] if i>= 1 }
	 *          where S[k,i] is last line cost
	 * we compute C[i] in "bottom-up" manner
	 */
	private Vector<Integer> printNeatly(int[] wordsLen, int lineLength) {
		
		//number of words
		int numWords = wordsLen.length;
				
		//construct slack table for given words and line length
		int[][] slackTable = constructSlackTable(wordsLen, lineLength);
		
		//initialize costs of arranging first i words in text
		int[] cost = new int[numWords + 1];
		
		//initialize the array to store breaking word: corresponding to first 
		//word on last line for best arrangement of first i"" words
		int breakingWords[] = new int[numWords]; 
		
		//determine the least cost arrangement in text
		//cost of arranging first word (1-1)
		//cost of arranging first word in text is 0, 
		//as there is only word to arrange with no cost
		cost[0] = 0;
		for (int i = 0; i < numWords; i++) {
			cost[i+1] = INF; //inf
			int k = i;
			
			/*
			 * cost of arranging k words in the text + 
			 * slack of words from kth word to ith word on a single line
			 */
			int T = cost[k] + slackTable[k][i];
			
			if (T < cost[i+1]) {
				//if cost of arranging k words in the text + 
				//slack of words from kth word to ith word on a single line 
				//smaller than previous costs
				
				cost[i+1] = T;
				breakingWords[i] = k;
			}
			while (k >= 1 && T < INF) {
				//find min k such that cost of arranging k words + 
				//slack from kth word to ith word decreases 
				k--;
				T = cost[k] + slackTable[k][i];
				if (T < cost[i+1]) {
					cost[i+1] = T;
					breakingWords[i] = k;
				}
			}
		}
		
		//determine the first word on each line
		
		//initilize list of indices of first word on each line
		Vector<Integer> firstWordInd = new Vector<Integer>();
		//add first word index of last line if all words used
		firstWordInd.add(0, breakingWords[numWords- 1]);
		int i = breakingWords[numWords- 1] - 1;
		while (i >= 0) {
			//backtrack to find first word on lines
			firstWordInd.add(0, breakingWords[i]);
			i = breakingWords[i] - 1;
		}
		
		return firstWordInd;
	}
	
	
	public void applyPrettyPrint(String ipFileName, int lineLength) {
		
		//get the string of words from input file
		Vector<String> words = getWords(ipFileName);
				
		//get the length of words in the array
		int[] wordsLen = getWordsLen(words);
				
		//list of indices of first word on each line
		Vector<Integer> firstWordInd = printNeatly(wordsLen, lineLength);
		
		int prevInd = 0;
		//int firstInd = -1;
		for (int firstInd : firstWordInd) {
			//firstInd = firstWordInd.elementAt(i);
			//print words from prevInd to firstind -1 in a single line
			for (int j = prevInd; j < firstInd; j++) {
				System.out.print(words.elementAt(j));
				System.out.print(' ');
			}
			System.out.println();
			prevInd = firstInd;
		}
		
		for (int i = prevInd; i < words.size(); i++) {
			System.out.print(words.elementAt(i));
			System.out.print(' ');
		}
	}
	
	
	public static void main(String[] args) {
		
		//get ipfile name containing words
		String ipFileName = args[0];
		
		//length of line allowed to pretty print
		int lineLength = Integer.parseInt(args[1]);
		
		PrettyPrint prettyPrint = new PrettyPrint();
		
		prettyPrint.applyPrettyPrint(ipFileName, lineLength);
		
		
	}
	
	
}