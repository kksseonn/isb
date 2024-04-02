package lab_2;

import java.util.Random;

/**
 * A class to generate random binary numbers.
 */
public class generator {
    
    /** The size of the generated binary number. */
    private static final int SIZE = 128;

    /**
     * Main method to generate and print a random binary number.
     * 
     * @param args The command-line arguments (not used).
     */
    public static void main(String[] args) {
        Random random = new Random();

        for (int i = 0; i < SIZE; i++) {
            int bit = random.nextInt(2);
            System.out.print(bit);
        }
    }
}