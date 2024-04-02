#include <iostream>
#include <cstdlib>
#include <ctime>

/**
 * @brief Generates a random bit sequence of length 128.
 * 
 * This function generates a random bit sequence of length 128 
 * and prints it to the standard output.
 */
void generator() {
    std::srand(static_cast<unsigned>(std::time(0)));
    for (int i = 0; i < 128; ++i) {
        int random_bit = std::rand() % 2;
        std::cout << random_bit;
    }
}

/**
 * @brief Entry point of the program.
 * 
 * Calls the generator function to generate random bits.
 * 
 * @return 0 on success.
 */
int main() {
    generator();
    return 0;
}