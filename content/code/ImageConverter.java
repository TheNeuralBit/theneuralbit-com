import java.awt.Color;
import java.awt.Graphics;
import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;

import javax.swing.ImageIcon;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.filechooser.FileFilter;
import javax.swing.filechooser.FileNameExtensionFilter;
/**
 * This class creates a text version of a user-selected image.
 *
 * @author Brian Hulette
 *         Created Jan 22, 2008.
 */
public class ImageConverter {
	
	private static BufferedImage bImage;
	private static File text;
	//Number of columns in the output file, in characters. 
	//Will be user selcted in the future.
	private static int numCols;
	//The characters that will make up the final product, in order from lightest to darkest.
	//You can modify this if you want to use different characters, just be sure theyre in order from light to dark.
	private static char[] shadings = {' ', '.', '-', '+', '!', ';', '(', '[', '{', '5', '&', '9', '$', '8', '@', '#'};
	/**
	 * Begins process of conversion. Prompts user for image file and text file.
	 *
	 * @param args
	 */
	public static void main(String[] args) {
	    JFileChooser imageChooser = new JFileChooser();
	    imageChooser.setName("Choose image to be converted...");
	    FileFilter filter = new FileNameExtensionFilter("JPEG & GIF images", "jpg", "jpeg", "gif");
	    imageChooser.setFileFilter(filter);
	    int returnVal = imageChooser.showOpenDialog(null);
	    if(returnVal == JFileChooser.APPROVE_OPTION) {
	    	String imFile = imageChooser.getSelectedFile().getPath();
	    	bImage = loadImage(imFile);
	    		    	
	    	String[] sp = imFile.split("[.]");
	    	String textName = "";
	    	for(int i = 0; i < sp.length-1; i++){
	    		 textName += sp[i];
	    	}
	    	textName += ".txt";
	    	
	    	numCols = Integer.parseInt(JOptionPane.showInputDialog("Please choose the approximate number of columns (will be adjusted)"));
	    	text = new File(textName);
	    	fillText();
	    }
	    else{ return; }    
	}
	
	/*
	 * Goes through the rather convoluted process of loading an image into a 
	 * BufferedImage.  It doesn't make much sense to me either so I won't explain it.
	 */
	private static BufferedImage loadImage(String filename){
		ImageIcon icon = new ImageIcon(filename);
		Image image = icon.getImage();
		
		BufferedImage rtrn = new BufferedImage(image.getWidth(null),
											   image.getHeight(null), 
											   BufferedImage.TYPE_INT_ARGB);
		Graphics g = rtrn.getGraphics();
	    g.drawImage(image, 0, 0, null);
	    
	    return rtrn;
	}
	
	/* Finds the appropriate characters to replace each rectangle in the image
	 * and writes it to the file.
	 */
	private static void fillText(){
		// Width and height (in pixels) a character covers.
		// Width gets rounded to closest integer value then numCols is adjusted to account for this change.
		int charWidth = (int)Math.round((double)(bImage.getWidth())/numCols);
		int charHeight = (int)Math.round(charWidth * 2.0);
		
		numCols = bImage.getWidth()/charWidth;		
		int numRows = bImage.getHeight()/charHeight;
		
		PrintWriter writer = null;
		try{
			writer = new PrintWriter(text);
			for(int row = 0; row < numRows ; row++){
				for(int col = 0; col < numCols; col++){
					writer.write(pickChar(col*charWidth, row*charHeight, charWidth, charHeight));
				}
			writer.write('\n');
			}
		}
		catch(IOException e){e.printStackTrace();}
		finally{writer.close();}
	}
	
	/*Picks the character with the appropriate darkness to replace the pixels
	 *in the rectangle from x to x+w and y to y+h.
	 */
	private static char pickChar(int x, int y, int w, int h){
		//Average the grayscale Values
		int colSum = 0;
		int rowSum = 0;
		for(int col = x; col < x + w; col++){
			rowSum = 0;
			for(int row = y; row < y + h; row++){
				rowSum += getGray(col, row);
			}
			colSum += rowSum/h;
		}
		int avgGray = colSum/w;
		//Pick the appropriate character, a value of 255 picks the lightest
		//character, and 0 picks the darkest.
		return shadings[(int)((shadings.length-1)*(1.0 - avgGray/255.0))];
	}
	
	/*
	 * Returns the average of the R,G and B values at pixel (x,y)
	 */
	private static int getGray(int x, int y){
		Color tempColor = new Color(bImage.getRGB(x,y));
		return (tempColor.getBlue() + 
				tempColor.getGreen() + 
				tempColor.getRed()) / 3;
	}
	
}