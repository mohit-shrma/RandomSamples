package com.outputreader;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

import au.com.bytecode.opencsv.CSVReader;

class OutputReader {
	
	
	private String filePath;
	private CSVReader reader;
	
	public OutputReader(int columnStart, int columnEnd, String filePath,
							char separator) {
		this.filePath = filePath;
	}
	
	public String[] readNext() {
		
		if (reader == null) {
			try {
				reader = new CSVReader(new FileReader(this.filePath), '\t');
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} 
		
		try {
			return reader.readNext();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
		return null;
	
	}
	
	
}

