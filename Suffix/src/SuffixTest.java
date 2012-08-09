import com.Suffix.SuffixArray.SuffixArrayConstructor;
import com.Suffix.SuffixArray.SuffixArrayOps;

class SuffixTest {
	
	
	private String text;
	
	
	public SuffixTest(String text) {
		this.text = text;
	}
	
	public int[] getSuffixArray() {
		SuffixArrayConstructor suffConst = new SuffixArrayConstructor(text);
		suffConst.generateSuffixArray();
		return suffConst.getSuffixArray();
	}
	
	public int search(String query, int[] suffixArray) {
		SuffixArrayOps suffArrOps = new SuffixArrayOps(text, suffixArray);
		return suffArrOps.search(query);
	}
	
	public static void main(String[] args) {
		String text = args[0];
		System.out.println(text);
		SuffixTest obj = new SuffixTest(text);	
		int[] suffixArr = obj.getSuffixArray();
		System.out.println("Printing suffix array ...");
		for (int i = 0; i < suffixArr.length; i++) {
			System.out.print(suffixArr[i] + ", ");
		}
		System.out.println("");
		String query = "cadabra";
		int searchRes = obj.search(query, suffixArr);
		System.out.println("Search result for " + query + ": " + searchRes);
	}
	
}