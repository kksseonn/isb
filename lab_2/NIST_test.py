import json
import logging
from math import sqrt
from scipy.special import erfc, gammainc

logging.basicConfig(level=logging.INFO)

PI = {"v1": 0.2148, "v2": 0.3672, "v3": 0.2305, "v4": 0.1875}


def frequency_bit_test(sequence: str) -> float:
    """
    Perform frequency bit test on the given binary sequence.

    Args:
        sequence (str): The binary sequence.

    Returns:
        float: The p-value of the test.
    """
    try:
        n_zeros = sequence.count('0')
        n_ones = sequence.count('1')
        total_length = len(sequence)
        value = (n_ones - n_zeros) / sqrt(total_length)
        p_value = erfc(abs(value) / sqrt(2))
        return p_value
    except Exception as e:
        logging.error(f"An error occurred in frequency_bit_test: {e}")

def consecutive_bits_test(sequence: str) -> float:
    """
    Perform consecutive bits test on the given binary sequence.

    Args:
        sequence (str): The binary sequence.

    Returns:
        float: The p-value of the test.
    """
    try:
        sequence = [int(bit) for bit in sequence]
        ones_count = sum(sequence)
        n = len(sequence)
        dzeta = ones_count / n
        if abs(dzeta - 0.5) < (2 / sqrt(n)):
            v = 0
            for i in range(len(sequence) - 1):
                if sequence[i] != sequence[i + 1]:
                    v += 1
            numerator = abs(v - 2 * n * dzeta * (1 - dzeta))
            denominator = 2 * sqrt(2 * n) * dzeta * (1 - dzeta)
            p_value = erfc(numerator / denominator)
        else:
            p_value = 0
        return p_value
    except Exception as e:
        logging.error(f"An error occurred in consecutive_bits_test: {e}")


def longest_sequence_test(sequence: str) -> float:
    """
    Perform longest sequence test on the given binary sequence.

    Args:
        sequence (str): The binary sequence.

    Returns:
        float: The p-value of the test.
    """
    try:
        block_size = 8
        blocks = [sequence[i:i + block_size] for i in range(0, len(sequence), block_size)]
        statistics = {"v1": 0, "v2": 0, "v3": 0, "v4": 0}
        
        for block in blocks:
            max_length = 0
            current_length = 0
            for bit in block:
                if bit == '1':
                    current_length += 1
                    max_length = max(max_length, current_length)
                else:
                    current_length = 0
                    
            match max_length:
                case 0 | 1:
                    statistics["v1"] += 1
                case 2:
                    statistics["v2"] += 1
                case 3:
                    statistics["v3"] += 1
                case _:
                    statistics["v4"] += 1
        
        chi_sqrt = sum(pow(v - 16 * PI[k], 2) / (16 * PI[k]) for k, v in statistics.items())
        p_value = gammainc(3 / 2, chi_sqrt / 2)
        return p_value
    except Exception as e:
        logging.error(f"An error occurred in longest_sequence_test: {e}")


def write_to_file(file_path: str, data: str) -> None:
    """
    Write data to the specified file.

    Args:
        file_path (str): The path to the file.
        data (str): The data to be written.
    """
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(data + '\n')
        logging.info(f"Data written to '{file_path}' successfully.")
    except Exception as e:
        logging.error(
            f"An error occurred while writing to the file '{file_path}': {e}")


if __name__ == "__main__":
    try:
        with open("lab_2/options.json", "r") as options_file:
            options = json.load(options_file)

        c_plus_plus_bit_test = frequency_bit_test(options['c++_sequence'])
        if c_plus_plus_bit_test is not None:
            write_to_file(options['file_name'], f"C++ frequency_bit_test: {c_plus_plus_bit_test:.16f}")

        java_bit_test = frequency_bit_test(options['java_sequence'])
        if java_bit_test is not None:
            write_to_file(options['file_name'], f"Java frequency_bit_test: {java_bit_test:.16f}")

        c_plus_plus_consecutive_test = consecutive_bits_test(options['c++_sequence'])
        if c_plus_plus_consecutive_test is not None:
            write_to_file(options['file_name'], f"C++ consecutive bits test: {c_plus_plus_consecutive_test:.16f}")

        java_consecutive_test = consecutive_bits_test(options['java_sequence'])
        if java_consecutive_test is not None:
            write_to_file(options['file_name'], f"Java consecutive bits test: {java_consecutive_test:.16f}")

        c_plus_plus_longest_sequence_test = longest_sequence_test(options['c++_sequence'])
        if c_plus_plus_longest_sequence_test is not None:
            write_to_file(options['file_name'], f"C++ longest sequence test: {c_plus_plus_longest_sequence_test:.16f}")

        java_longest_sequence_test = longest_sequence_test(options['java_sequence'])
        if java_longest_sequence_test is not None:
            write_to_file(options['file_name'], f"Java longest sequence test: {java_longest_sequence_test:.16f}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")