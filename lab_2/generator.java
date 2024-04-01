package lab_2;

import java.util.Random;

public class generator{
    private static final int SIZE=128;
    public static void main(String[] args) {
        Random random = new Random();

        for (int i = 0; i < 128; i++) {
            int bit = random.nextInt(2);
            System.out.print(bit);
        }
    }
}